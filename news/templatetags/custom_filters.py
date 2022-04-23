from atexit import register
from django import template

register = template.Library()

@register.filter(name='censor')
def censor(value):
    str_ = str(value)
    list_str = str_.split('bad_word')
    comb_str = "!@#$%".join(list_str)
    return comb_str
            