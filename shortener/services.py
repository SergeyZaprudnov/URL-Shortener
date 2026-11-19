import random
import string

from django.db import IntegrityError

from .models import ShortLink


def generate_short_code(lenght=6):
    """ Генерация случайного кода из цифр и букв """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(lenght))


def create_short_link(original_url):
    """ Создание короткой ссылки """
    existing_link = ShortLink.objects.filter(original_url=original_url).first()
    if existing_link:
        return existing_link


    for _ in range(5):
        code = generate_short_code()
        try:
            return ShortLink.objects.create(original_url=original_url, short_code=code)

        except IntegrityError:
            continue

    raise Exception(" Исчерпаны 5 попыток. Не удалось сгенерировать код")