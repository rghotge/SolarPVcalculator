from pydantic import BaseModel, Field
from pvlib.iotools import get_pvgis_hourly

#Default values added here
LATITUDE = 51.0  #Specify the latitude in decimal degrees, between -90 and 90, north is positive (ISO 19115)
LONGITUDE = 5.0  #Specify the longitude in decimal degrees, between -180 and 180, east is positive (ISO 19115)
SURFACE_TILT = 0.0  #Tilt angle from horizontal plane
SURFACE_AZIMUTH = 180 #(north=0, east=90, south=180, west=270)
PEAK_POWER = 1000 #Specify the peak installed solar power in kW, maximum permitted value of 1GW


class PVsystem(BaseModel):
    latitude: float = Field (default = LATITUDE, ge = -90, le = 90)
    longitude: float = Field (default = LONGITUDE, ge = -180, le = 180)
    surface_tilt: float = Field (default = SURFACE_TILT, gt = 0, le = 90)
    surface_azimuth: float = Field (default = SURFACE_AZIMUTH, ge = 0, le = 360)
    peak_power: float = Field (default = SURFACE_AZIMUTH, ge = 0, le = 1e6)

def get_pv_power(latitude, longitude, surface_tilt, surface_azimuth, peak_power):
    """Returns the AC power from the PV system as a teim series for a whole year"""

    data, inputs, metadata = get_pvgis_hourly(latitude = latitude, longitude = longitude, 
                                start=None, end=None, raddatabase=None, 
                                components=True, surface_tilt=surface_tilt, 
                                surface_azimuth=surface_azimuth, outputformat='json', 
                                usehorizon=True, userhorizon=None, pvcalculation=True, 
                                peakpower=peak_power, pvtechchoice='crystSi', 
                                mountingplace='building', #assumption is that the PV is on the depot building
                                loss=5.4, #default loss values for system taken from SAM, based on 2% module mismatch, 0.5% diodes and connections, 2% DC wiring and 1% AC wiring
                                trackingtype=0, optimal_surface_tilt=False, 
                                optimalangles=False, url='https://re.jrc.ec.europa.eu/api/',
                                map_variables=True, timeout=30)
    
    latest_year = data.index[-1].year #data is returned as a 10 year timeseries. We select the most recent year
    
    pvpower = data.loc[data.index.year == latest_year]['P']
    pvpower.rename ("Power (kW)", inplace = True)
    pvpower_annual_sum = pvpower.sum()/1000000 #Returns value in MWh
    


    return pvpower, pvpower_annual_sum