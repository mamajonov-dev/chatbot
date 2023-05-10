import os
import random
import requests


def getpicture():
    # url = f'https://pixabay.com/api/?key={picturetoken}&q=yellow+flowers&image_type=photo'
    url = 'https://pixabay.com/api/?key=35656075-06406f3c7cda50868a13fd161&q=yellow+flowers&image_type=photo'
    response = requests.get(url)
    data = response.json()
    links = []
    for link in data['hits']:
        image = link['pageURL']
        links.append(image)

    return random.choice(links)
