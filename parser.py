from django.utils.text import slugify
import requests
import re

response = requests.get("https://www.ucas.com/explore/subjects")
found = re.findall("transition--hover-move-down\"><h3>(.+?)<", response.content.decode("utf-8"))
print(found)
for course in found:
    #response = requests.get(f"https://www.ucas.com/explore/subjects/{slugify(course)}/")
    #subcourses = re.findall("", response.content.decode("utf-8"))
    #trash = "?studyYear=2020&destination=Undergraduate&postcodeDistanceSystem=imperial&pageNumber=1&sort=ProviderAtoZ&clearingPreference=None"
    url = "https://digital.ucas.com/coursedisplay/results/courses"




