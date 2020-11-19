from django import template
from datetime import timedelta

register = template.Library()


@register.filter
def duration(td):
    if not td:
        return ''
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    microseconds = str(td.microseconds)[0]
    if hours < 1:
        return '{:02d}:{:02d}.{}'.format(minutes, seconds, microseconds)
    else:
        return '{}:{:02d}:{:02d}.{}'.format(hours, minutes, seconds, microseconds)
