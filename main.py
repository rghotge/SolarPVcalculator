import streamlit as st
import leafmap.foliumap as leafmap
from solarpv import PVsystem, get_pv_power

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
This is at the experimental phase
"""

st.sidebar.title("About")
st.sidebar.info(markdown)

#st.sidebar.image(logo)

# Customize page title
st.title("Solar PV Calculator")

st.markdown(
    """
    This simple calculator takes basic specifications of a solar photovoltaic (PV) system and makes estimates of the power produced over a year and annual energy generated.
    """
)
col1, col2 = st.columns([4,5])
with col1:
    form = st.form("solar_form")
    lat = form.number_input('Site latitude', min_value=-90, max_value=+90, value = 51)
    lon = form.number_input('Site longitude', min_value=-180, max_value=+180, value = 5)
    tilt = form.number_input('Array tilt (deg. from horizontal)', min_value=0, max_value=+90, value = 15)
    az = form.number_input('Array azimuth (deg)', min_value=0, max_value=+360,  value = 180)
    ppeak = form.number_input('Peak installed capacity (kW)', min_value=1.0, max_value=1e6,  value = 10.0)
    markdown = """
    (north=0, east=90, south=180, west=270)
    """
    st.markdown(markdown)

with col2:
    #m = leafmap.Map(locate_control=True, latlon_control=True, minimap_control=True, lat = 51, lon = 5)
    #m.add_basemap("OpenTopoMap")
    #m.to_streamlit(width=350, height=350)
    
    calculate = form.form_submit_button(label="Calculate")
    if calculate:
        pvpower, pvpower_annual_sum = get_pv_power(latitude = lat, 
                      longitude = lon, 
                      surface_tilt = tilt, 
                      surface_azimuth = az, 
                      peak_power= ppeak)
        st.write("Annual Energy: ", pvpower_annual_sum, " MWh")
        #st.write(pvpower)
        st.line_chart(pvpower, y = "Power (kW)")


st.header("Assumptions")

markdown = f"""
1. The technology used is crystalline silicon.
2. Yield losses are in the range of 5\% due to module mismatch, diodes and connections, DC wiring and AC wiring Ohmic losses. These loss values are the defaults used in **SAM** (https://www.nrel.gov/docs/fy15osti/64102.pdf)
3. The PV is on the roof of the depot building, reducing ventilation and increasing the temperature of the solar modules.
4. The method used is from PVGIS, and uses the `pvlib python package` (https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.iotools.get_pvgis_hourly.html)
"""

st.markdown(markdown)