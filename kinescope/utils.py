"""
Helpers functions for Kinescope XBlock
"""
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def _(text):
    """
    Make '_' a no-op so we can scrape strings
    """
    return text


def is_url(text):
    """
    Check if given text is a valid url
    """
    url_validator = URLValidator()
    try:
        URLValidator()(text)
        return True
    except ValidationError as e:
        return False


def parse_valid_kinescope_url(text):
    """
    Validate that the given text is a url of the correct pattern
    """
    is_url(text)
    parsed_url = urlparse(text)
    if parsed_url.scheme == "https" and parsed_url.netloc == "kinescope.io":
        return parsed_url.path.split('/', 1)[1]
    else:
        return False