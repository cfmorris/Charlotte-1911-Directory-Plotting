#pip install geopandas
#pip install geopy
#pip install folium

import geopandas as gpd
import geopy 
import pandas as pd
import folium

locator = geopy.geocoders.Nominatim(user_agent="cityDirectory", timeout=2)
eiffel = locator.geocode("Champ de Mars, Paris, France", language="en")

print(eiffel)
print("Latitude = {}, Longitude = {}".format(eiffel.latitude, eiffel.longitude))

dfmin = pd.read_csv("Charlotte1911final.csv")
dfmin.tail(10)

geocode = RateLimiter(locator.geocode, min_delay_seconds=1)  #rate limiter required by Nominatums API
geocode = lambda query: locator.geocode("%s, Charlotte, NC" % query) #add city, state info to avoid false positives

dfmin = dfmin.head(30)

dfmin["loc"] = dfmin["Address"].apply(geocode)
dfmin.head()

dfmin["point"] = dfmin["loc"].apply(lambda loc: tuple(loc.point) if loc else (0, 0, 0)) #else (0,0,0) avoids crashes caused when null values are returned for unlocatable addresses.
dfmin[['latitude', 'longitude', 'altitude']] = pd.DataFrame(dfmin['point'].tolist(), index=dfmin.index)
dfmin.to_csv("Charlotte1911final_example.csv")

dfmin = pd.read_csv("Charlotte1911final_georeferencedv05.csv")

dfrace = dfmin.groupby(dfmin.Race)
dfblack = dfrace.get_group("Black")
dfwhite = dfrace.get_group("White")

dfblack.count()
dfwhite.count()

# Mapping entries by race

map1 = folium.Map(
    location=[35.221,-80.8492],
    tiles='cartodbpositron',
    zoom_start=12,
)

dfblack.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]], color="green", popup=[row["Name"], row["Address"], row["Job"], row["latitude"], row["longitude"]]).add_to(map1), axis=1)
dfwhite.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]], color="blue", popup=[row["Name"], row["Address"], row["Job"], row["latitude"], row["longitude"]]).add_to(map1), axis=1)

map1

## Mapping entries by job

dfjob = dfmin.groupby(dfmin.Job)
dflab = dfjob.get_group("lab")
dfrev = dfjob.get_group("pastor")
dfpres = dfjob.get_group("pres")
dfvpres = dfjob.get_group("v-pres")

map2 = folium.Map(
    location=[35.221,-80.8492],
    position='center',
    tiles='cartodbpositron',
    zoom_start=12,
)

dflab.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]], color="black", popup=[row["Name"], row["Address"], row["Job"]]).add_to(map2), axis=1)
dfrev.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]], color="yellow", popup=[row["Name"], row["Address"], row["Job"]]).add_to(map2), axis=1)
dfpres.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]], color="blue", popup=[row["Name"], row["Address"], row["Job"]]).add_to(map2), axis=1)
dfvpres.apply(lambda row:folium.CircleMarker(location=[row["latitude"], row["longitude"]], color="blue", popup=[row["Name"], row["Address"], row["Job"]]).add_to(map2), axis=1)

map2
