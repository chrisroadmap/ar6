import sys
import os

import math
import numpy
import pandas

from scipy.interpolate import interp1d
from .constants import *

class ScmDef(object):
    """Defines the two-layer climate model.

    Attributes:
        default (dict): Default parameters for running the two-layer model. 
            Overwritten using **kwargs (see call to `__init__`)
        extforce (numpy.ndarray): Effective radiative forcing with which to
            run the model.
        exttime (numpy.ndarray): Timesteps at which to calculate the effective
            radiative forcing.
        params (dict): Parameters for running the two-layer model. Includes
            derived values.
    """
    
    default = {
        'tbeg':1850.0,
        'tend':2101.0,
        'dt':0.2,
        'outtime':None,  
        'q2x':3.74,
        'lamg':None,
        't2x':3.00,
        'cmix':8.2,
        'cdeep':109.0,
        'gamma_2l':0.67,
        'eff':1.28,
        'extforce':numpy.zeros(2),
        'exttime':numpy.zeros(2),
        'scm_in':None
        }
        
        
    def __init__(self, **kwargs):
        """Initiator for two layer model.
        
        Args:
            q2x (float): Forcing for CO2 doubling.
            t2x (float): Equilibrium warming for CO2 doubling (ECS).
            lamg (float): Global mean feedback parameter. If both t2x and 
                lamg are input, t2x takes precedence and lamg estimated from
                q2x/t2x.
            cmix (float): Heat capacity of ocean mixed layer from Geoffroy
                et al., 2013, Transient Climate Response in a Two-Layer 
                Energy-Balance Model. Part II: Representation of the 
                Efficacy of Deep-Ocean Heat Uptake and Validation for CMIP5 
                AOGCMs 
                https://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00196.1
            cdeep (float): Heat capacity of deep ocean layer [units?] from
                Geoffroy et al., 2013, Part II.
            gamma_2l (float): Heat exchange coefficient between upper and 
                deep layer [units?] from Geoffroy et al., 2013, Part II.
            eff (float): Efficacy of deep ocean from Geoffroy et al., 2013, 
                Part II. 
            extforce (numpy.ndarray): Array of radiative forcing
            exttime (numpy.ndarray): Array of times, should be equal in 
                length to extforce
            tbeg (float): Start time for simulation (year)
            tend (float): End time for simulation (year)
            dt (float): Timestep (years)
            outtime (np.ndarray or None): If set, the times (years) at which
                output response is given. If not set, output every timestep
                between tbeg and tend.
            scm_in (scmpy2l.Results): allows simple model to be re-run with
                parameters from an existing run, rather than defaults.
        """
    
        # First update params with defaults
        self.params = self.default.copy()        

        if 'scm_in' in kwargs:
            self.params.update(kwargs['scm_in'].params)

        # Second update with keyword arguments
        self.params.update(kwargs) 
 
        # Order of precedence: (keywords, defaults)
        self.exttime=self.params['exttime']
        self.extforce=self.params['extforce']
        
        # Reset feedback lamg and ecs (t2x) if needed. 
        t2x, lamg = set_feedback(
            q2x=self.params['q2x'],
            t2x=self.params['t2x'],
            lamg=self.params['lamg']
        ) 

        self.params['t2x']   = t2x
        self.params['lamg']  = lamg
        self.params['cdeep_p'] = self.params['cdeep']*self.params['eff']
        self.params['gamma_p'] = self.params['gamma_2l']*self.params['eff']

        g1      = (self.params['lamg'] + self.params['gamma_p'])/self.params['cmix'] 
        g2      = self.params['gamma_p']/self.params['cdeep_p']
        g       = g1 + g2
        gstar   = g1 - g2
        delsqrt = numpy.sqrt( g*g - 4.*g2*self.params['lamg']/self.params['cmix'] )
        afast   = (g + delsqrt)/2.
        aslow   = (g - delsqrt)/2.        
        amix_f  =  0.5*(gstar+delsqrt)/(self.params['cmix']*delsqrt)
        amix_s  = -0.5*(gstar-delsqrt)/(self.params['cmix']*delsqrt)      
        adeep_f = -self.params['gamma_p']/(self.params['cmix']*self.params['cdeep_p']*delsqrt)
        adeep_s = -adeep_f       

        self.params['afast']=afast
        self.params['aslow']=aslow
        self.params['amix_f']=amix_f
        self.params['amix_s']=amix_s
        self.params['adeep_f']=adeep_f
        self.params['adeep_s']=adeep_s
        
        
    def run(self, **kwargs):
        """Runs the two-layer model."""
        
#        self.params.update(kwargs) # is this necessary?
        tbeg      = self.params['tbeg']
        tend      = self.params['tend']
        dt        = self.params['dt']              
        q2x       = self.params['q2x']
        extforce  = self.params['extforce']
        exttime   = self.params['exttime']         
        outtime   = self.params['outtime']  
        cmix      = self.params['cmix']
        cdeep     = self.params['cdeep']
        afast     = self.params['afast']
        aslow     = self.params['aslow']
        amix_f    = self.params['amix_f']
        amix_s    = self.params['amix_s']
        adeep_f   = self.params['adeep_f']
        adeep_s   = self.params['adeep_s']

        nlev1     = 2  # TODO: make keyword
 
        time      = numpy.arange(tbeg, tend+dt, dt)
        time[-1]  = tend   # reset last to tend (possible float diff)        
        ntime     = len(time)

        # TODO: more general type and error checking
        input_type_check(extforce, 'extforce')
        #if extforce is not None and isinstance(extforce, numpy.ndarray): 
        #    if extforce[0] is None:
        #        raise AssertionError('extforce[0] is None') 
        #else:
         #   raise AssertionError('extforce not instance of numpy.ndarray') 

        tg      = numpy.zeros(ntime)
        tl      = numpy.zeros(ntime)
        to      = numpy.zeros(ntime)
        ohc     = numpy.zeros(ntime)
        hflux   = numpy.zeros(ntime)
        qtot    = numpy.zeros(ntime)       
        lam_eff = numpy.zeros(ntime)   # 'transient feedback', Eq 28 Geoffroy et al (Part 2)
        tlev    = numpy.zeros((ntime, nlev1))  
                                 
        try:
            qext = numpy.interp(time, self.exttime, self.extforce)
        except:
            raise AssertionError('Cannot interpolate numpy arrays (exttime,extforce)')

        # Initialize twolayer model
        twolayer=TwoLayer(
            lamg=self.params['lamg'],
            gamma=self.params['gamma_2l'],
            cmix=self.params['cmix'],
            cdeep=self.params['cdeep'], 
            eff=self.params['eff']
        )                                    

        temp_mix  = numpy.zeros((ntime,2))
        temp_deep = numpy.zeros((ntime,2))
 
        for i in range(1,ntime):                                        
            qtot[i] = qext[i] 
             
            # Tmix and Tdeep both have two components that need to be updated:
            #    - a fast component, first elements:  Tmix[:,0], Tdeep[:,0]
            #    - a slow component, second elements: Tmix[:,1], Tdeep[:,1]
            # Actual temperature anomaly is sum of the slow and fast components
            
            temp_mix[i,:], temp_deep[i,:], heatflux, del_ohc, lam_eff1 = (
                twolayer.update(
                    dt, temp_mix[i-1,:], temp_deep[i-1,:], qtot[i-1], qtot[i]
                )
            )
                
            # Sum fast and slow components
            tlev[i,0]  = numpy.sum(temp_mix[i,:])
            tlev[i,1]  = numpy.sum(temp_deep[i,:])
            lam_eff[i] = lam_eff1               
            ohc[i]     = ohc[i-1] + del_ohc                                         
            hflux[i]   = heatflux 

        lam_eff[0]=lam_eff[1]

        if not outtime is None:
            ohc   = interp1d(time, ohc)(outtime)
            hflux = interp1d(time, hflux)(outtime)
            qtot  = interp1d(time, qtot)(outtime)
            tlev  = interp1d(time, tlev, axis=0)(outtime)
            time  = outtime    

        results = Results(
            params=self.params,
            time=time,
            ohc=ohc,
            tlev=tlev,
            tg=tlev[:,0],
            hflux=hflux,
            qtot=qtot,
            lam_eff=lam_eff
        ) 

        return results


class Results(object):
    """Results of simple climate model."""
    
    def __init__(self, **kwargs):
    	self.__dict__.update(kwargs)
        
        
    def keys(self):
        return self.__dict__.keys()
        
        
    def __str__(self):
        return repr(self)
        
        
    def __repr__(self):
        s = str(self.__class__).split(self.__module__)[1]
        if s[0] == '.': s=s[1:]
        if s[-1] == '>': s=s[:-1]
        if s[-1] == "'": s=s[:-1] 
        attr=[a for a in dir(self) if a[0] != '_']
        ans = s + ', public attributes: ' + str(attr)
        return ans


def set_feedback(lamg=None, t2x=None, q2x=None):
    """Sets climate feedback parameter.
    
    Set lamg and/or t2x (ecs). If both are input, t2x takes precedence and
    lamg is over-written.
    
    Args:
        lamg (float): global climate feedback parameter (W m-2 K-1).
        t2x (float): equilibrium temperature for a doubling of CO2 (K).
        q2x (float): effective radiative forcing for a doubling of CO2 (W m-2).
        
    Returns:
        t2x (float)
        lamg (float)
    """
    
    if t2x is not None:
        lamg = q2x/t2x
    else:
        t2x = q2x/lamg
    return t2x, lamg


class TwoLayer(object):
    """
    Two Layer model.
    """
    
    default = {    
        'lamg'   : 1.18,
        'cmix'   : 8.2,
        'cdeep'  : 109.0,
        'gamma'  : 0.67,
        'eff'    : 1.28,               
        }    


    def __init__(self, **kwargs):
        """Initiator for TwoLayer model.
        
        Args:
            lamg (float): Global mean feedback parameter. If both t2x and 
                lamg are input, t2x takes precedence and lamg estimated from
                q2x/t2x.
            cmix (float): Heat capacity of ocean mixed layer from Geoffroy
                et al., 2013, Transient Climate Response in a Two-Layer 
                Energy-Balance Model. Part II: Representation of the 
                Efficacy of Deep-Ocean Heat Uptake and Validation for CMIP5 
                AOGCMs 
                https://journals.ametsoc.org/doi/pdf/10.1175/JCLI-D-12-00196.1
            cdeep (float): Heat capacity of deep ocean layer [units?] from
                Geoffroy et al., 2013, Part II.
            gamma_2l (float): Heat exchange coefficient between upper and 
                deep layer [units?] from Geoffroy et al., 2013, Part II.
            eff (float): Efficacy of deep ocean from Geoffroy et al., 2013, 
                Part II.
        """
        
        self.params = self.default.copy()
        self.params.update(kwargs) 

        # care with unit handling
        self.ntoa2joule = 4*math.pi*EARTHRADIUS*EARTHRADIUS*SECPERYEAR*1e-22
        #self.ntoa2joule = 1.6097567742221404    #same as above
             
        # Define derived constants                
        cdeep_p = self.params['cdeep']*self.params['eff']
        gamma_p = self.params['gamma']*self.params['eff']
        g1      = (self.params['lamg']+gamma_p)/self.params['cmix'] 
        g2      = gamma_p/cdeep_p
        g       = g1+g2
        gstar   = g1-g2
        delsqrt = numpy.sqrt(g*g - 4*g2*self.params['lamg']/self.params['cmix'])
        afast   = (g + delsqrt)/2.
        aslow   = (g - delsqrt)/2.        
        cc      = 0.5/(self.params['cmix']*delsqrt)        
        amix_f  = cc*(gstar+delsqrt)
        amix_s  = -cc*(gstar-delsqrt)        
        adeep_f = -gamma_p/(self.params['cmix']*cdeep_p*delsqrt)
        adeep_s = -adeep_f                                            
        self.params.update({
            'afast'  : afast,
            'aslow'  : aslow,
            'amix_f' : amix_f,
            'amix_s' : amix_s,
            'adeep_f': adeep_f,
            'adeep_s': adeep_s
        })
        for k in self.params.keys():
            if self.params[k] == None:
                 if k in self.default:
                    self.params[k] = self.default[k]
        self.afast   = afast
        self.aslow   = aslow
        self.amix_f  = amix_f
        self.amix_s  = amix_s
        self.adeep_f = adeep_f
        self.adeep_s = adeep_s


    def update(self, dt, temp_mix0, temp_deep0, forc0, forc1):
        """Updates two-layer model each timestep.
        
        Args:
            dt (float): Model timestep (yr).
            temp_mix0 (float): Temperature of mixed layer at last timestep (K)
            temp_deep0 (float): Temperature of deep ocean at last timestep (K)
            forc0 (float): effective radiative forcing at last timestep (W m-2)
            forc1 (float): effective radiative forcing this timestep (W m-2)
        
        Returns:
            temp_mix1 (float): Temperature of mixed layer this timestep (K)
            temp_deep1 (float): Temperature of deep ocean this timestep (K)
            heatflux (float): Ocean heat flux this timestep (units?)
            del_ohc (float): Change in ocean heat content this timestep (10*22J)
            lam_eff (float): Effective climate feedback parameter this timestep
                (W m-2 K-1)
        """
        
        adf = 1./(self.afast*dt)
        ads = 1./(self.aslow*dt)

        exp_f   = numpy.exp(-1./adf)
        exp_s   = numpy.exp(-1./ads)        
        int_f   = (forc0*adf + forc1*(1.-adf) - exp_f*(forc0*(1.+adf)-forc1*adf))/self.afast
        int_s   = (forc0*ads + forc1*(1.-ads) - exp_s*(forc0*(1.+ads)-forc1*ads))/self.aslow

        # Update [fast,slow] components of Tmix and Tdeep
        temp_mix1  = numpy.array([exp_f*temp_mix0[0] + self.amix_f*int_f, 
                                  exp_s*temp_mix0[1] + self.amix_s*int_s]) 
                                         
        temp_deep1 = numpy.array([exp_f*temp_deep0[0] + self.adeep_f*int_f, 
                                  exp_s*temp_deep0[1] + self.adeep_s*int_s])

        c_dtemp = (self.params['cmix']*(temp_mix1.sum()-temp_mix0.sum()) + 
            self.params['cdeep']*(temp_deep1.sum()-temp_deep0.sum()) )

        heatflux = c_dtemp/dt
        del_ohc  = self.ntoa2joule * c_dtemp
        
        faclameff = (self.params['eff']-1.0)*self.params['gamma']        
        if abs(numpy.sum(temp_mix1)) > 1e-6:
            ratio = ( (numpy.sum(temp_mix1) - numpy.sum(temp_deep1))
                /numpy.sum(temp_mix1) )
            lam_eff = self.params['lamg'] + faclameff*ratio
        else:
            lam_eff = self.params['lamg'] + faclameff
        
        return temp_mix1, temp_deep1, heatflux, del_ohc, lam_eff


def input_type_check(inp, name):
    if isinstance(inp, (list, pandas.core.series.Series, numpy.ndarray)):
        return
    else:
        raise ValueError(name + ' should be convertible to a 1D numpy array')
