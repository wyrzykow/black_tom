ERROR_LOG_SLACK_CHANNEL = 'UP414JK1D' #my slack id, instead of name

#wyrzykowski_bright_microlensing_v4

from scipy.stats import skew
import numpy as np
from scipy.optimize import leastsq


def ulens_fixedbl(t, t0, te, u0, I0):
    fs=1.
    tau=(t-t0)/te
    x=tau
    y=u0
    
    u=np.sqrt(x**2+y**2)
    ampl= (u**2 + 2)/(u*np.sqrt(u**2+4))
    F = ampl*fs + (1-fs)
    I = I0 - 2.5*np.log10(F)
    return I

def fit_ulensfixedbl(epoch, avmag, err):

    #catching short light curves:
    if (len(epoch)<10): 
        return [999,999,999,999], 1999999.

    t0=epoch[np.argmin(avmag)]
    te=50.
    u0=0.1
    I0=np.amax(avmag)
    x=epoch
    y=avmag
    
    ulensparam=[t0, te, u0, I0]
    fp = lambda v, x: ulens_fixedbl(x, v[0],v[1],v[2],v[3])
    e = lambda v, x, y, err: ((fp(v,x)-y)/err)
    v, success = leastsq(e, ulensparam, args=(x,y,err), maxfev=1000000)
    #no solution:
    if (success == 0) : return ulensparam, 999999.
    chi2 = sum(e(v,x,y,err)**2)
    chi2dof=sum(e(v,x,y,err)**2)/(len(x)-len(v))
    out = []
    for t in v:
        out.append(t)
    out.append(chi2)
    out.append(chi2dof)
    return out, chi2dof

def bright_microlensing(ld):
    skewThreshold = 0
    etaThreshold = 0.3
    chi2Threshold = 1000.
    u0Threshold = 0.3
    teThreshold = 1000.

    p = ld.get_properties()
    fid = p['ztf_fid']

    _, mjd = ld.get_time_series(filters={'ztf_fid': fid})
    if len(mjd) < 10:
        return

    mags, errs, times, is_var_star, corrected = ld.get_varstar_corrected_mags(fid=fid)
    if is_var_star and corrected:
        stream_name = 'bright_microlensing_variable_star'
    else:
        stream_name = 'bright_microlensing'

    #computing stats
    nrtrid=len(mjd)
    eta=1./(nrtrid-1.)/np.var(mags)*np.sum((mags[1:]-mags[:-1])*(mags[1:]-mags[:-1]))
    #skewness
    skewness=skew(mags)    
    rmax=np.amax(mags)

    if (rmax<17.0 and skewness<skewThreshold and eta<etaThreshold) :
        fitparams, chi2dof = fit_ulensfixedbl(times, mags, errs)
#        t0=fitparams[0]
        te=np.abs(fitparams[1])
        u0=np.abs(fitparams[2])
        if (np.abs(u0)<u0Threshold and chi2dof<chi2Threshold and te<teThreshold) : 
            ld.send_to_stream(stream_name)