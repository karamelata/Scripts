#!/usr/bin/env python
# Copyright 2016 Dave Machado

from geopy.geocoders import Nominatim
geolocator = Nominatim()

x = str(raw_input("Location: "))
if len(x) < 5:
	# Python does not read leading zeros, so pad an extra '0'
	# if x < 5 (length of zip codes)
	x.zfill(5)
x += " United States"
#location = geolocator.reverse("12.345,-98.765")
location = geolocator.geocode(x)
print(location.address)
print(location.raw)
x = str(location.latitude)
y = str(location.longitude)
z = x + ", " + y
print("Coordinates: " + z)