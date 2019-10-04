from tom_catalogs.harvester import AbstractHarvester

import os
import requests
import json
from collections import OrderedDict

def get(term):
  api_key = os.environ['TNSBOT_APIKEY']
  url = "https://wis-tns.weizmann.ac.il/api/get"
  try:
    get_url = url + '/object'
    
    # change term to json format
    json_list = [("objname",term)]
    json_file = OrderedDict(json_list)
    
    # construct the list of (key,value) pairs
    get_data = [('api_key',(None, api_key)),
                 ('data',(None,json.dumps(json_file)))]
   
    response = requests.post(get_url, files=get_data)
    response = json.loads(response.text)['data']['reply']
    return response
  except Exception as e:
    return [None,'Error message : \n'+str(e)]

class TNSHarvester(AbstractHarvester):
    name = 'TNS'

    def query(self, term):
        self.catalog_data = get(term)

    def to_target(self):
        target = super().to_target()
        target.type = 'SIDEREAL'
        target.identifier = (self.catalog_data['name_prefix'] +
            self.catalog_data['name'])
        target.name = target.identifier
        target.ra = self.catalog_data['radeg']
        target.dec = self.catalog_data['decdeg']
        target.epoch = 2000
        if self.catalog_data['redshift'] is not None:
            target.redshift = self.catalog_data['redshift']
        return target
