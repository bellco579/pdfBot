import random
import string

import requests
from core.models import Docs
from user.models import Profile

def create_random_string(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def save_photo(url):
    path = "static/photo/" + create_random_string() + ".png"
    photo = requests.get(url=url)
    file = open(path, "wb")
    file.write(photo.content)
    file.close()
    return path

