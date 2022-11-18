from geopy.geocoders import Photon
# import osmnx as ox
# import networkx as nx
import folium
import json
import geocoder

import requests
def nav(loc):
    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
    )
    data = json.loads(requests.get(f"{url}/vis1.json").text)

    geolocator = Photon(user_agent="measurement")
    getLoc = geolocator.geocode(loc)
    # getLoca = geolocator.geocode("Avichi School")
    g = geocoder.ip('me')
    # print(g.latlng)
    
    # printing address
    # print(getLoc.address)
    
    # printing latitude and longitude
    # print("Latitude = ", getLoc.latitude, "\n")
    # print("Longitude = ", getLoc.longitude)
    a=[getLoc.latitude,getLoc.longitude]
    b=g.latlng
    # b=[getLoca.latitude,getLoca.longitude]
    c=tuple(a)
    d=tuple(b)
    x=(a[0]+b[0])/2
    y=(a[1]+b[1])/2
    z=[x,y]
    points=[c,d]
    m = folium.Map(location=z, zoom_start=11)
    tooltip="You need to go here"
    tooltips="You are here"
    marker = folium.Marker(
        location=a,
        radius=50,
        popup=getLoc.address,
        tooltip=tooltip)
    marker.add_to(m)
    marker1 = folium.Marker(
        location=b,
        radius=50,
        popup="<stong>You are here</stong>",
        tooltip=tooltips)
    marker1.add_to(m)
    # folium.PolyLine(points).add_to(m)
    m.save('index.html')
