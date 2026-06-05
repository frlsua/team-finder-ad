import random
from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from uuid import uuid4

from .constants import (
    AVATAR_IMAGE_SIZE,
    AVATAR_COLORS,
    AVATAR_FONT_NAME,
    AVATAR_FONT_SIZE,
    AVATAR_TEXT_ANCHOR,
    AVATAR_TEXT_COLOR,
    AVATAR_FORMAT
)


def generate_avatar(letter, size=AVATAR_IMAGE_SIZE):
    """
    Генерация изображения с первой буквой name
    """
    background_color = random.choice(AVATAR_COLORS)
    image = Image.new('RGB', (size, size), background_color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(AVATAR_FONT_NAME, AVATAR_FONT_SIZE)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox(AVATAR_TEXT_ANCHOR, letter, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = (
        (size - text_width) // 2,
        (size - text_height) // 2
    )
    draw.text(
        position,
        letter,
        fill=AVATAR_TEXT_COLOR,
        font=font
    )

    buffer = BytesIO()
    image.save(buffer, format=AVATAR_FORMAT)
    return ContentFile(
        buffer.getvalue(),
        name=f'avatar_{uuid4().hex}.png'
    )
