from urllib.parse import urlparse

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def validate_url(url):
    validator = URLValidator()
    try:
        validator(url)
    except ValidationError:
        raise ValidationError('Введите корректный URL')

    parsed = urlparse(url)
    if parsed.netloc not in ('github.com', 'www.github.com'):
        raise ValidationError('Ссылка должна вести на GitHub')
