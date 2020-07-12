from django import template

register = template.Library()


@register.filter
def duration(td):
    if not td:
        return ''
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    return '{:02d}:{:02d}'.format(minutes, seconds)
