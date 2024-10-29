#!/usr/bin/env python
# coding: utf-8


### By Jethan d'Hotman
### Created April 2024

import copernicusmarine
from datetime import datetime, timedelta
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
#from cartopy.io import shapereader
#from cartopy.feature import NaturalEarthFeature
import cartopy.feature as cfeature
import os
import numpy as np
import sys
import time


# command line inputs
username = sys.argv[1]
password = sys.argv[2]
sender_email = sys.argv[3]
sender_password = sys.argv[4]

#copernicusmarine.login()

# Transect
Sundays = 25.89723, -33.76603
#AB_80m = 26.12382, -33.94718
#AB_60m = 25.98882, -33.88108
offshore = 26.53570, -34.37877

#-34.483524948379234, 26.28863114952022

transect_lons = [Sundays[0],offshore[0]]
transect_lats = [Sundays[1],offshore[1]]

# OSTIA SST L4
Data_ID =  'METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2'

# Region of interest
Latitude = [-45,-25]
Longitude = [15,35]
variables = ["analysed_sst"]
my_time = (datetime.now() - timedelta(7)).strftime('%Y-%m-%d')
output_fname = 'OSTIA_SST_SA_' + my_time +'.nc'
#print('Date: ', my_time)


# Error handling
# Download and plot latest OSTIA SST

MAX_RETRIES = 3
RETRY_WAIT = 10      
    
i = 0

while i < MAX_RETRIES:
    
    try: 
        print('Attempting download of OSTIA SST data. Attempt No: ',str(i))
        sst_data_file = copernicusmarine.subset(dataset_id=Data_ID,
                                            username = username,
                                            password = password,
                                            minimum_longitude = min(Longitude),
                                             maximum_longitude = max(Longitude),
                                            minimum_latitude= min(Latitude),
                                            maximum_latitude = max(Latitude),
                                             start_datetime = my_time,
                                             end_datetime = my_time,
                                             variables = variables,
                                       output_filename = output_fname,
                                            force_download=True)
        break
    except Exception as e:
        print('Failed to download SST data')
        time.sleep(RETRY_WAIT)
        i+=1
        
if os.path.exists(output_fname) == True:

    print('Generating SST plot')
    sst_data = xr.open_dataset(sst_data_file)
    sst_data = sst_data.squeeze()
        
    title = 'SST Map for: ' + my_time

    fig = plt.figure(figsize=(10, 8))

    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    plt.title(title,fontweight='bold')

    sst_plot = ax.pcolor(sst_data.longitude,sst_data.latitude,sst_data.analysed_sst-272.15,cmap='plasma')#, extend='both')

    cax = fig.add_axes([0.22, 0.83, 0.18, 0.02])
    cbar = fig.colorbar(sst_plot, cax=cax, orientation='horizontal',label='$^o$C',extend='both')
    cbar.set_label(label='$^o$C',fontweight='bold')
    # Add coastline and land
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.LAND, color='lightgray')
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    #rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor='blue', facecolor='none')
    #ax.add_feature(rivers)

    # Add transect
    ax.plot(transect_lons,transect_lats,color='black')
    #ax.plot(Sundays[0],Sundays[1],'.',color='white',markersize=10)
    #ax.plot(AB_60m[0],AB_60m[1],'.',color='white',markersize=10)
    #ax.plot(AB_80m[0],AB_80m[1],'.',color='white',markersize=10)

    ax.plot(30.81, -29.8579,'.',color='Black',markersize=10)
    ax.text(29.5,-29.5,'Durban')

    # Add gridlines
    ax.gridlines(draw_labels=True)

    plt_fname = 'SouthernAfrica_SST_' + my_time + '.png'

    fig.savefig(plt_fname,bbox_inches='tight')
    plt.show()
        
    ####### Second figure #######
        
    fig1 = plt.figure(figsize=(10, 8))

    ax = fig1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    plt.title(title,fontweight='bold')

    sst_plot = ax.pcolor(sst_data.longitude,sst_data.latitude,sst_data.analysed_sst-272.15,cmap='plasma')#, extend='both')

    cax = fig1.add_axes([0.21, 0.83, 0.18, 0.02])
    cbar = fig1.colorbar(sst_plot, cax=cax, orientation='horizontal',label='$^o$C',extend='both')
    cbar.set_label(label='$^o$C',fontweight='bold')

    # Add coastline and land
    ax.coastlines(resolution='10m')
    ax.add_feature(cfeature.LAND, color='lightgray')
    ax.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    #rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor='blue', facecolor='none')
    #ax.add_feature(rivers)

    # Set the extent to cover Algoa Bay
    ax.set_extent([25.5, 32, -35, -29])

    # Add transect
    ax.plot(transect_lons,transect_lats,color='black')
    #ax.plot(Sundays[0],Sundays[1],'.',color='white',markersize=10)
    #ax.plot(AB_60m[0],AB_60m[1],'.',color='white',markersize=10)
    #ax.plot(AB_80m[0],AB_80m[1],'.',color='white',markersize=10)

    ax.plot(31, -29.87,'.',color='Black',markersize=10)
    ax.text(30.3,-29.8,'Durban')

    # Add gridlines
    ax.gridlines(draw_labels=True)

    plt_fname_subset = 'EC_SouthernAfrica_SST_' + my_time + '.png'

    fig1.savefig(plt_fname_subset,bbox_inches='tight')
    plt.show()

    sst_data.close()
    os.remove(sst_data_file)
    
else:
    #os.unlink(sst_data_file)
    print('No sst data to plot')          
    plt.figure()
    
    t = 'No OSTIA SST data for: ' + my_time
    plt.text(0.3,0.5,t)
    
    plt_fname = 'SouthernAfrica_SST_' + my_time + '.png'
    plt_fname_subset = 'EC_SouthernAfrica_SST_' + my_time + '.png'
    
    plt.savefig(plt_fname)
    plt.savefig(plt_fname_subset)
    plt.show()


# Download and plot forcast SST data

# Global analysis forcast model
Data_ID =  'cmems_mod_glo_phy-thetao_anfc_0.083deg_PT6H-i'

variables = ["thetao"]
Start_date = (datetime.now() - timedelta(8)).strftime('%Y-%m-%d')
End_date = (datetime.now() + timedelta(10)).strftime('%Y-%m-%d')
output_fname = 'Forcast_SST_SA_' + Start_date +'.nc'
depth = 0.49402499198913574

MAX_RETRIES = 3
RETRY_WAIT = 10  

i = 0
while i < MAX_RETRIES:
    
    try:
        print('Attempting download of forcast data. Attempt No: ',str(i))
        f_sst_data_file = copernicusmarine.subset(dataset_id=Data_ID,
                                            username = username,
                                            password = password,
                                            minimum_longitude = min(Longitude),
                                             maximum_longitude = max(Longitude),
                                            minimum_latitude= min(Latitude),
                                            maximum_latitude = max(Latitude),
                                             start_datetime = Start_date,
                                             end_datetime = End_date,
                                             variables = variables,
                                              minimum_depth=depth,
                                              maximum_depth=depth,
                                              output_filename = output_fname,
                                              force_download=True)
    
        break
    except Exception as e:
        print('Failed to download forecast data')
        time.sleep(RETRY_WAIT)
        i+=1
        
if os.path.exists(output_fname) == True:        
    f_sst_data = xr.open_dataset(f_sst_data_file)
    f_sst_data = f_sst_data.squeeze()
    
    fig2,ax = plt.subplots(3,2,figsize=(15, 10),subplot_kw={'projection': ccrs.PlateCarree()})

    ax1 = ax[0,0]
    ax2 = ax[0,1]
    ax3 = ax[1,0]
    ax4 = ax[1,1]
    ax5 = ax[2,0]
    ax6 = ax[2,1]

    fig2.suptitle('Forcast SST',x=0.51,y=0.92, fontweight='bold')

    #ax = ax1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax1.set_title(str(np.datetime64(f_sst_data.time[0].values, 'D')))
    f1_sst_plot = ax1.pcolor(f_sst_data.longitude,f_sst_data.latitude,f_sst_data.thetao[0,:,:],cmap='plasma')#, extend='both')

    cax = fig2.add_axes([0.35, 0.86, 0.07, 0.01])
    cbar = fig2.colorbar(f1_sst_plot, cax=cax, orientation='horizontal',label='$^o$C',extend='both')
    cbar.set_label(label='$^o$C',fontweight='bold')

    # Add coastline and land
    ax1.coastlines(resolution='10m')
    ax1.add_feature(cfeature.LAND, color='lightgray')
    ax1.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    #rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor='blue', facecolor='none')
    #ax.add_feature(rivers)

    # Set the extent to cover Algoa Bay
    ax1.set_extent([25.5, 32, -35, -29])

    # Add transect
    ax1.plot(transect_lons,transect_lats,color='black')
    #ax.plot(Sundays[0],Sundays[1],'.',color='white',markersize=10)
    #ax.plot(AB_60m[0],AB_60m[1],'.',color='white',markersize=10)
    #ax.plot(AB_80m[0],AB_80m[1],'.',color='white',markersize=10)

    ax1.plot(31, -29.87,'.',color='Black',markersize=10)
    ax1.text(29.8,-29.8,'Durban')

    # Add gridlines
    g1 = ax1.gridlines(draw_labels=True)
    g1.top_labels = False
    g1.right_labels = False

    #############################################################################################################################

    #ax = ax1.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    ax2.set_title(str(np.datetime64(f_sst_data.time[4].values, 'D')))
    f1_sst_plot = ax2.pcolor(f_sst_data.longitude,f_sst_data.latitude,f_sst_data.thetao[5,:,:],cmap='plasma')#, extend='both')

    cax = fig2.add_axes([0.53, 0.86, 0.07, 0.01])
    cbar = fig2.colorbar(f1_sst_plot, cax=cax, orientation='horizontal',label='$^o$C',extend='both')
    cbar.set_label(label='$^o$C',fontweight='bold')

    # Add coastline and land
    ax2.coastlines(resolution='10m')
    ax2.add_feature(cfeature.LAND, color='lightgray')
    ax2.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    #rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor='blue', facecolor='none')
    #ax.add_feature(rivers)

    # Set the extent to cover Algoa Bay
    ax2.set_extent([25.5, 32, -35, -29])

    # Add transect
    ax2.plot(transect_lons,transect_lats,color='black')
    #ax.plot(Sundays[0],Sundays[1],'.',color='white',markersize=10)
    #ax.plot(AB_60m[0],AB_60m[1],'.',color='white',markersize=10)
    #ax.plot(AB_80m[0],AB_80m[1],'.',color='white',markersize=10)

    ax2.plot(31, -29.87,'.',color='Black',markersize=10)
    ax2.text(29.8,-29.8,'Durban')

    # Add gridlines
    g2 = ax2.gridlines(draw_labels=True)
    g2.top_labels = False
    g2.left_labels = False

    ############################################################################################################################

    ax3.set_title(str(np.datetime64(f_sst_data.time[8].values, 'D')))
    f1_sst_plot = ax3.pcolor(f_sst_data.longitude,f_sst_data.latitude,f_sst_data.thetao[8,:,:],cmap='plasma')#, extend='both')

    cax = fig2.add_axes([0.35, 0.59, 0.07, 0.01])
    cbar = fig2.colorbar(f1_sst_plot, cax=cax, orientation='horizontal',label='$^o$C',extend='both')
    cbar.set_label(label='$^o$C',fontweight='bold')

    # Add coastline and land
    ax3.coastlines(resolution='10m')
    ax3.add_feature(cfeature.LAND, color='lightgray')
    ax3.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    #rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor='blue', facecolor='none')
    #ax.add_feature(rivers)

    # Set the extent to cover Algoa Bay
    ax3.set_extent([25.5, 32, -35, -29])

    # Add transect
    ax3.plot(transect_lons,transect_lats,color='black')
    #ax.plot(Sundays[0],Sundays[1],'.',color='white',markersize=10)
    #ax.plot(AB_60m[0],AB_60m[1],'.',color='white',markersize=10)
    #ax.plot(AB_80m[0],AB_80m[1],'.',color='white',markersize=10)

    ax3.plot(31, -29.87,'.',color='Black',markersize=10)
    ax3.text(29.8,-29.8,'Durban')

    # Add gridlines
    g3 = ax3.gridlines(draw_labels=True)
    g3.top_labels = False
    g3.right_labels = False

    ############################################################################################################################

    ax4.set_title(str(np.datetime64(f_sst_data.time[12].values, 'D')))
    f1_sst_plot = ax4.pcolor(f_sst_data.longitude,f_sst_data.latitude,f_sst_data.thetao[12,:,:],cmap='plasma')#, extend='both')

    cax = fig2.add_axes([0.53, 0.59, 0.07, 0.01])
    cbar = fig2.colorbar(f1_sst_plot, cax=cax, orientation='horizontal',label='$^o$C',extend='both')
    cbar.set_label(label='$^o$C',fontweight='bold')

    # Add coastline and land
    ax4.coastlines(resolution='10m')
    ax4.add_feature(cfeature.LAND, color='lightgray')
    ax4.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    #rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor='blue', facecolor='none')
    #ax.add_feature(rivers)

    # Set the extent to cover Algoa Bay
    ax4.set_extent([25.5, 32, -35, -29])

    # Add transect
    ax4.plot(transect_lons,transect_lats,color='black')
    #ax.plot(Sundays[0],Sundays[1],'.',color='white',markersize=10)
    #ax.plot(AB_60m[0],AB_60m[1],'.',color='white',markersize=10)
    #ax.plot(AB_80m[0],AB_80m[1],'.',color='white',markersize=10)

    ax4.plot(31, -29.87,'.',color='Black',markersize=10)
    ax4.text(29.8,-29.8,'Durban')

    # Add gridlines
    g4 = ax4.gridlines(draw_labels=True)
    g4.top_labels = False
    g4.left_labels = False

    #########################################################################################################################

    ax5.set_title(str(np.datetime64(f_sst_data.time[16].values, 'D')))
    f1_sst_plot = ax5.pcolor(f_sst_data.longitude,f_sst_data.latitude,f_sst_data.thetao[16,:,:],cmap='plasma')#, extend='both')

    cax = fig2.add_axes([0.35, 0.315, 0.07, 0.01])
    cbar = fig2.colorbar(f1_sst_plot, cax=cax, orientation='horizontal',label='$^o$C',extend='both')
    cbar.set_label(label='$^o$C',fontweight='bold')

    # Add coastline and land
    ax5.coastlines(resolution='10m')
    ax5.add_feature(cfeature.LAND, color='lightgray')
    ax5.add_feature(cfeature.LAND, edgecolor='black', facecolor='lightgray')
    #rivers = cfeature.NaturalEarthFeature('physical', 'rivers_lake_centerlines', '10m', edgecolor='blue', facecolor='none')
    #ax.add_feature(rivers)

    # Set the extent to cover Algoa Bay
    ax5.set_extent([25.5, 32, -35, -29])

    # Add transect
    ax5.plot(transect_lons,transect_lats,color='black')
    #ax.plot(Sundays[0],Sundays[1],'.',color='white',markersize=10)
    #ax.plot(AB_60m[0],AB_60m[1],'.',color='white',markersize=10)
    #ax.plot(AB_80m[0],AB_80m[1],'.',color='white',markersize=10)

    ax5.plot(31, -29.87,'.',color='Black',markersize=10)
    ax5.text(29.8,-29.8,'Durban')

    # Add gridlines
    g5 = ax5.gridlines(draw_labels=True)
    g5.top_labels = False
    g5.right_labels = False

    ###########################################################################################################################

    ax6.axis('off')

    plt.subplots_adjust(wspace=-0.7)

    fcast_fname = 'Forecast_SST_' + Start_date + '.png'
    fig2.savefig(fcast_fname,bbox_inches='tight')
    
else:
    plt.figure()
        
    t = 'No forcast SST data for: ' + Start_date
    plt.text(0.3,0.5,t)
        
    fcast_fname = 'Forecast_SST_' + Start_date + '.png'
    plt.savefig(fcast_fname,bbox_inches='tight')


# Import modules for email notification
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_email(sender_email, sender_password, receiver_email, subject, message, files=[]):
    # Setup the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # Attach the message
    msg.attach(MIMEText(message, 'plain'))
    
    # Attach files if any
    for file in files:
        attachment = open(file, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= {file}")
        msg.attach(part)
    
    # Create SMTP session
    session = smtplib.SMTP('smtp.gmail.com', 587) #use your smtp server details here
    session.starttls() #enable security
    session.login(sender_email, sender_password) #login with mail_id and password
    
    # Send the email
    text = msg.as_string()
    session.sendmail(sender_email, receiver_email, text)
    session.quit()

# Email details
reciever_email_list = ['js.dhotman@saeon.nrf.ac.za']#,
                      # 'gfearon11@gmail.com',
                      # 't.morris@saeon.nrf.ac.za']
#
#reciever_email_list = ['js.dhotman@saeon.nrf.ac.za']
#receiver_email = reciever_email_list
subject = 'Latest SST Images'
message = 'OSTIA Level 4 SST images for Southern Africa and Forecast SST from Mercator global ocean'
files = [plt_fname, plt_fname_subset, fcast_fname]  # List of file paths to attach

for i in range(len(reciever_email_list)):
    send_email(sender_email, sender_password, reciever_email_list[i], subject, message, files)


