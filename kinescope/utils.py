"""
Helpers functions for Kinescope XBlock
"""
from django.core.exceptions import ValidationError
from urllib.parse import urlparse


def _(text):
    """
    Make '_' a no-op so we can scrape strings
    """
    return text


def validate_parse_kinescope_url(text):
    """
    Check if given text is valid kinescope video url and extract
    video id from it.
    """
    parsed_url = urlparse(text)
    if parsed_url.scheme == "https" and parsed_url.netloc == "kinescope.io":
        return parsed_url.path.split('/')[-1]
    else:
        raise ValidationError(_("Provided Kinescope Video URL is invalid"))