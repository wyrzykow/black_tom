import os
import requests
import logging
from astropy.time import Time, TimezoneInfo
from tom_dataproducts.models import ReducedDatum
import json
from tom_targets.templatetags.targets_extras import target_extra_field
from requests_oauthlib import OAuth1
from astropy.coordinates import SkyCoord
from astropy import units as u
import mechanize
import numpy as np

logger = logging.getLogger(__name__)

def target_post_save(target, created):
  def get(objectId):
    url = 'https://mars.lco.global/'
    request = {'queries':
      [
        {'objectId': objectId}
      ]
      }
  
    try:
      r = requests.post(url, json=request)
      results = r.json()['results'][0]['results']
      return results
    
    except Exception as e:
      return [None,'Error message : \n'+str(e)]
 
  logger.info('Target post save hook: %s created: %s', target, created)

  ### how to pass those variables from settings?
  try:
      from black_tom import local_settings as secret
  except ImportError:
      pass
  try:
      TWITTER_APIKEY = secret.TWITTER_APIKEY
      TWITTER_SECRET = secret.TWITTER_SECRET
      TWITTER_ACCESSTOKEN = secret.TWITTER_ACCESSTOKEN
      TWITTER_ACCESSSECRET = secret.TWITTER_ACCESSSECRET
      CPCS_DATA_ACCESS_HASHTAG = secret.CPCS_DATA_ACCESS_HASHTAG
  except:
      TWITTER_APIKEY = os.environ['TWITTER_APIKEY']
      TWITTER_SECRET = os.environ['TWITTER_SECRET']
      TWITTER_ACCESSTOKEN = os.environ['TWITTER_ACCESSTOKEN']
      TWITTER_ACCESSSECRET = os.environ['TWITTER_ACCESSSECRET']
      CPCS_DATA_ACCESS_HASHTAG = os.environ['CPCS_DATA_ACCESS_HASHTAG']

  ####
  if target_extra_field(target=target, name='tweet'):
    #Post to Twitter!
    twitter_url = 'https://api.twitter.com/1.1/statuses/update.json'

    api_key = TWITTER_APIKEY
    api_secret = TWITTER_SECRET
    access_token = TWITTER_ACCESSTOKEN
    access_secret = TWITTER_ACCESSSECRET
    auth = OAuth1(api_key, api_secret, access_token, access_secret)

    coords = SkyCoord(target.ra, target.dec, unit=u.deg)
    coords = coords.to_string('hmsdms', sep=':',precision=1,alwayssign=True)

    # #Explosion emoji
    # tweet = ''.join([u'\U0001F4A5 New target alert! \U0001F4A5\n',
    #     'Name: {name}\n'.format(name=target.name),
    #     'Coordinates: {coords}\n'.format(coords=coords)])
    # status = {
    #         'status': tweet
    # }

    # response = requests.post(twitter_url, params=status, auth=auth)
 
  ztf_name = next((name for name in target.names if 'ZTF' in name), None)
  if ztf_name:
    alerts = get(ztf_name)
    
    filters = {1: 'g_ZTF', 2: 'r_ZTF', 3: 'i_ZTF'}
    jdarr = []
    for alert in alerts:
        if all([key in alert['candidate'] for key in ['jd', 'magpsf', 'fid', 'sigmapsf']]):
            jd = Time(alert['candidate']['jd'], format='jd', scale='utc')
            jdarr.append(jd)
            jd.to_datetime(timezone=TimezoneInfo())
            value = {
                'magnitude': alert['candidate']['magpsf'],
                'filter': filters[alert['candidate']['fid']],
                'error': alert['candidate']['sigmapsf']
            }
            rd, created = ReducedDatum.objects.get_or_create(
                timestamp=jd.to_datetime(timezone=TimezoneInfo()),
                value=json.dumps(value),
                source_name=target.name,
                source_location=alert['lco_id'],
                data_type='photometry',
                target=target)
            rd.save()

    jdlast = np.array(jdarr).max()

    #modifying jd of last obs
    previousjd = target_extra_field(target=target, name='jdlastobs') 
    if (previousjd is not None):
      jj = float(previousjd)
      print("DEBUG-ZTF prev= ", jj, " new= ",jdlast)
      if (jj<jdlast) :
        print("DEBUG-ZTF saving new jdlast.")
        try:
          target.save(extras={'jdlastobs': jdlast})
        except:
          print("FAILED save jdlastobs (ZTF)")


  gaia_name = next((name for name in target.names if 'Gaia' in name), None)
  if gaia_name:
    base_url = 'http://gsaweb.ast.cam.ac.uk/alerts/alert'
    lightcurve_url = f'{base_url}/{gaia_name}/lightcurve.csv'

    response = requests.get(lightcurve_url)
    data = response._content.decode('utf-8').split('\n')[2:-2]

    jd = [x.split(',')[1] for x in data]
    mag = [x.split(',')[2] for x in data]

    jdlast = np.max(np.array(jd).astype(np.float))
    previousjd = target_extra_field(target=target, name='jdlastobs') 
    if (previousjd is not None):
      jj = float(previousjd)
      print("DEBUG-Gaia prev= ", jj, " new= ",jdlast)
      if (jj<jdlast) :
        print("DEBUG saving new jdlast.")
        try:
          target.save(extras={'jdlastobs': jdlast})
        except:
          print("FAILED save jdlastobs")


    for i in reversed(range(len(mag))):
        try:
            datum_mag = float(mag[i])
            datum_jd = Time(float(jd[i]), format='jd', scale='utc')
            value = {
                'magnitude': datum_mag,
                'filter': 'G_Gaia',
                'error': 0 # for now
            }
            rd, created = ReducedDatum.objects.get_or_create(
                timestamp=datum_jd.to_datetime(timezone=TimezoneInfo()),
                value=json.dumps(value),
                source_name=target.name,
                source_location=lightcurve_url,
                data_type='photometry',
                target=target)
            rd.save()
        except:
            pass

  cpcs_name = next((name for name in target.names if 'ivo://' in name), None)
  if cpcs_name:
    nam = cpcs_name[6:] #removing ivo://
    br = mechanize.Browser()
    followuppage=br.open('http://gsaweb.ast.cam.ac.uk/followup/')
    req=br.click_link(text='Login')
    br.open(req)
    br.select_form(nr=0)
    br.form['hashtag']=CPCS_DATA_ACCESS_HASHTAG
    br.submit()
    page=br.open('http://gsaweb.ast.cam.ac.uk/followup/get_alert_lc_data?alert_name=ivo:%%2F%%2F%s'%nam)
    pagetext=page.read()
    data1=json.loads(pagetext)
    if len(set(data1["filter"]) & set(['u','B','g','V','B2pg','r','R','R1pg','i','I','Ipg','z']))>0:
        fup=[data1["mjd"],data1["mag"],data1["magerr"],data1["filter"],data1["observatory"]] 
        logger.info('%s: follow-up data on CPCS found', target)
    else:
        logger.info('DEBUG: no CPCS follow-up for %s', target)
        pass


    ## ascii for single filter:
    datajson = data1

    mjd0=np.array(datajson['mjd'])
    mag0=np.array(datajson['mag'])
    magerr0=np.array(datajson['magerr'])
    filter0=np.array(datajson['filter'])
    caliberr0=np.array(datajson['caliberr'])
    obs0 = np.array(datajson['observatory'])
    w=np.where((magerr0 != -1))

    jd=mjd0[w]+2400000.5
    mag=mag0[w]
    magerr=np.sqrt(magerr0[w]*magerr0[w] + caliberr0[w]*caliberr0[w]) #adding calibration err in quad
    filter=filter0[w]
    obs=obs0[w]

    #Updating the last observation JD
    jdlast = np.max(jd)
    previousjd = target_extra_field(target=target, name='jdlastobs') 
    if (previousjd is not None):
      jj = float(previousjd)
      print("DEBUG-CPCS prev= ", jj, " new= ",jdlast)
      if (jj<jdlast) :
        print("DEBUG-CPCS saving new jdlast.")
        try:
          target.save(extras={'jdlastobs': jdlast})
        except:
          print("FAILED save jdlastobs (CPCS)")

    for i in reversed(range(len(mag))):
        try:
            datum_mag = float(mag[i])
            datum_jd = Time(float(jd[i]), format='jd', scale='utc')
            datum_f = filter[i]
            datum_err = float(magerr[i])
            value = {
                'magnitude': datum_mag,
                'filter': datum_f,
                'error': datum_err
            }
            rd, created = ReducedDatum.objects.get_or_create(
                timestamp=datum_jd.to_datetime(timezone=TimezoneInfo()),
                value=json.dumps(value),
                source_name=target.name,
                source_location=page,
                data_type='photometry',
                target=target)
            rd.save()
        except:
            pass
