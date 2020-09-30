#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 20:23:46 2020

@author: mrgr
"""

import numpy as np
import glob 
import os
import sys


path= './'
folders_bandpass=path+'??:??:0.ms'
folders=path+'??:??:00'
folders_list=sorted(glob.glob(folders))
folders_list_bandpass=sorted(glob.glob(folders_bandpass))
refant='CS011HBA1'

#print(folders_list)
###############################################################################################

#images= folders+'*.MS'
#imagelist=sorted(glob.glob(images))

############################################################################################### 
#print(path_wsclean[2:-1]+'.ms')

'''
for fol in folders_list[:]:
    #print(fol)
    images= fol+'/*.MS'
    imagelist=sorted(glob.glob(images))
    #print(imagelist)
    print('Doing folder'+fol)

    #concat(vis=imagelist, concatvis=fol[2:-1]+'.ms')


 
    

for fol in folders_list_bandpass[1:]:
	print('Doing folder'+fol)

	#bandpass(vis=fol,caltable=fol[:-3]+'.bandpass', refant=refant, gaintable='cyg-a-bandpass.cal')
	applycal(vis=fol, gaintable='cyg-a-bandpass.cal')

#applycal to apply the calibration table



for fol in folders_list_bandpass[1:]:
	print('Doing folder'+fol)
	badspw='7,9,18,20,27,28,29'
	flagdata(vis=fol, mode='manual',spw=badspw)


'''

#cell  = '1.13 arcmin'
cell='1arcmin'
size  = 256
nmax  = 10000
wpp= -1
scale = [0,1,2,4,8,16,32,64]
uv='' 

basevis='07:50:0.ms'
image_folder='images_natural_'+basevis[:-3]#+'0'

if not os.path.exists(image_folder):
  os.makedirs(image_folder)
path_images = image_folder+'/'

#things to change: nterms-> 2 or 3?


# CLEAINING WITH ROBUST 0 -- NO TAPER
def cleaning(vis, i):
    
  if i-1 == 0:
    automask = ''
  #if i-1==0:
    #automask= path_images+'mask.mask' #the name of my mask
    #automask=''
  else:
    automask = path_images+'image_'+str(i-1)+'.mask'

  if i>=5:
      stoks='IQUV'
  else: 
      stoks='I'
    
  tclean(vis=basevis, imagename=path_images+'image_'+str(i), deconvolver='mtmfs', \
	  interpolation="linear", niter=nmax, scales=scale, interactive=True, mask=automask,uvrange=uv,\
		  imsize=size, cell=cell, stokes=stoks, spw='', field='',
	  weighting='natural',robust=-1, nterms=3,\
		  gridder='wproject',wprojplanes=wpp, savemodel='modelcolumn')
      
def selfcal(vis, i, time, mode, interptab,table='cyg-a-bandpass.cal'):
  gaincal(vis=basevis,caltable=path_images+vis[:-2]+'selfcal_'+str(i), solint=time,\
        refant=refant, gaintype="G",calmode=mode,\
        gaintable=table,interp=interptab)


'''
Recall self-calibration consists of these general steps.

  1. Use clean to create a source model with current data.
  2. Perform gaincal on current data against the model from step 1.
  3. Apply the solutions from step 2.
  4. If stopping condition not met then go to step 1.
'''

'''
j = 0
'''
'''
badspw="7,9,18,20,27,28,29"
flagdata(vis=basevis,mode="manual",autocorr=False,inpfile="",reason="any",spw=badspw,field="",antenna="",   
          uvrange="",timerange="",correlation="",scan="",intent="",array="",observation="",feed="",                       
          clipminmax=[],datacolumn="DATA",clipoutside=True,channelavg=False,clipzeros=False,quackinterval=1.0,
          quackmode="beg",quackincrement=False,tolerance=0.0,addantenna="",lowerlimit=0.0,upperlimit=90.0,  
          ntime="scan",combinescans=False,timecutoff=4.0,freqcutoff=3.0,timefit="line",freqfit="poly",        
          maxnpieces=7,flagdimension="freqtime",usewindowstats="none",halfwin=1,winsize=3,timedev="",         
          freqdev="",timedevscale=5.0,freqdevscale=5.0,spectralmax=1000000.0,spectralmin=0.0,extendpols=True, 
          growtime=50.0,growfreq=50.0,growaround=False,flagneartime=False,flagnearfreq=False,minrel=0.0,      
          maxrel=1.0,minabs=0,maxabs=-1,spwchan=False,spwcorr=False,basecnt=False,action="apply",display="",
         flagbackup=False,savepars=False,cmdreason="",outfile="")    
'''
'''
print "Cleanining #" + str(j)

cleaning(basevis, j)
At
print "Self-Cal #" + str(j)
selfcal(basevis, j, '', 'p','')

'''


# PHASE ONLY
j = 1  

print "Cleanining: " + str(j)
cleaning(basevis, j)

print "Self-Cal #" + str(j)
selfcal(basevis, j, '0.75', 'p','')



#SECOND PHASE ONLY plot
j = 2

print "Cleaning :" +str(j)
cleaning(basevis, j)


print"Self-Cal #"+str(j)
selfcal (basevis, j, '0.5s','p','')


# AMP AND PHASE 
j = 3

print "Apply Self-Cal #" + str(j-1)
applycal(vis=basevis, gaintable=[path_images+basevis[:-2]+'selfcal_'+str(j-1), 'cyg-a-bandpass.cal'], interp=['linear','linear'],calwt=[False], flagbackup=True)


print "Cleanining #" + str(j)
cleaning(basevis, j)

print "Self-Cal #" + str(j)
selfcal(basevis, j, '0.5s', 'ap','linear')



# AMP AND PHASE 
j = 4

print "Apply Self-Cal #" + str(j-1) 
applycal(vis=basevis, gaintable=[path_images+basevis[:-2]+'selfcal_'+str(j-1),'cyg-a-bandpass.cal'], interp=['linear','linear'],calwt=[False], flagbackup=True)

print "Cleanining #" + str(j)
cleaning(basevis, j)

print "Self-Cal #" + str(j)
selfcal(basevis, j, '0.25s', 'ap','linear')


# Apply calibrations
j = 5

polcal(vis, caltable=path_images+'polato.pcal', poltype='Df', gaintable=['cyg-a-bandpass.cal', path_images+basevis[:-2]+'selfcal_'+str(j-1), path_images+basevis[:-2]+'selfcal_2'])
	   
print "Apply Self-Cal #" + str(j-1) 

applycal(vis=basevis, gaintable=[path_images+basevis[:-2]+'selfcal_'+str(j-1),'cyg-a-bandpass.cal', path_images+'polato.pcal'], interp=['linear','linear', 'linear'],calwt=[False], flagbackup=True)


# FINAL IMAGING
print "Cleanining #" + str(j)
cleaning(basevis, j)

#I export the fits of the final image
exportfits(imagename=+path_images+'image_'+str(j), fitsimage=basevis[:-3]+'_final_image.fits')

# polcal once with phase only selfcal AND amp+phase selfcal for D ( +QU? ) AND cyg.cal
# applycal this polato afterwards





'''
j = 6

selfcal(basevis, j-1, '0.25s', 'ap','linear')

polcal(vis=basevis, caltable=path_images+'polato.pcal', poltype='Df', gaintable=['cyg-a-bandpass.cal', path_images+basevis[:-2]+'selfcal_5', path_images+basevis[:-2]+'selfcal_2'])
	   
print "Apply Self-Cal #" + str(j-1) 

applycal(vis=basevis, gaintable=[path_images+basevis[:-2]+'selfcal_5','cyg-a-bandpass.cal', path_images+'polato.pcal'], interp=['linear','linear', 'linear'],calwt=[False], flagbackup=True)



#IMAGE IQUV
print "Cleanining #" + str(j)
cleaning(basevis, j)

#I export the fits of the final image
exportfits(imagename=path_images+'image_'+str(j)+'.image.tt0', fitsimage='IQUV'+basevis[:-3]+'_final_image.fits')
'''







