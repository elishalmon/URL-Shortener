import random
import string

CHARACTERS = string.ascii_letters + string.digits
LENGTH = 10


def generate_random_string():

    """
        Generates a random 10 characters string from 62 possible characters,
        (Capital letters, lowercase letters and digits)
        This allows us to store a very huge number of short urls
    """

    random_string = ''.join(random.choice(CHARACTERS) for _ in range(LENGTH))
    return random_string


def create_random_url(shortener):

    """
        After generating the short url, checking for colissions
        and if so, we generate antoher one
    """

    random_url = generate_random_string()
    shortener_class = shortener.__class__
    while shortener_class.objects.filter(short_url=random_url).exists():
        random_url = generate_random_string()

    return random_url
