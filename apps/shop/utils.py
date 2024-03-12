import datetime
from uuid import uuid4

from rest_framework import serializers, exceptions


def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, name=None, data=None, **kwargs):
    # Important note if you are using `drf-spectacular`
    # Please refer to the following issue:
    # https://github.com/HackSoftware/Django-Styleguide/issues/105#issuecomment-1669468898
    # Since you might need to use unique names (uuids) for each inline serializer
    if name is None:
        name = str(uuid4())
    serializer_class = create_serializer_class(name=name, fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)


def date_convertor(date: str) -> datetime.date:
    """
    corvert date format "DD.MM.YYYY" to datetime format "YYYY-MM-DD"
    :param date: str
    :return: datetime
    """
    try:
        day, month, year = map(int, date.strip().split('.'))
        correct_date = datetime.date(year, month, day)
    except (ValueError, TypeError):
        raise exceptions.APIException(detail='Invalid date format')

    return correct_date
