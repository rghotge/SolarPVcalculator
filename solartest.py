from solarpv import PVsystem, get_pv_power


LATITUDE = 23 #Specify the latitude in decimal degrees, between -90 and 90, north is positive (ISO 19115)
LONGITUDE = 5 #Specify the longitude in decimal degrees, between -180 and 180, east is positive (ISO 19115)
SURFACE_TILT = 15  #Tilt angle from horizontal plane
SURFACE_AZIMUTH = 180 #(north=0, east=90, south=180, west=270)
PEAK_POWER = 10 #Specify the peak installed solar power in kW, maximum permitted value of 1GW

PVsystem (
    latitude = LATITUDE,
    longitude = LONGITUDE,
    surface_tilt = SURFACE_TILT,
    surface_azimuth=SURFACE_AZIMUTH,
    peak_power= PEAK_POWER
)

pvpower, pvpower_annual_sum = get_pv_power(latitude = LATITUDE, 
                      longitude = LONGITUDE, 
                      surface_tilt = SURFACE_TILT, 
                      surface_azimuth = SURFACE_AZIMUTH, 
                      peak_power= PEAK_POWER)

print (pvpower, pvpower_annual_sum)





