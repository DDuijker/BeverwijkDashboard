# MaasApp/templatetags/custom_filters.py
from django import template
from ..services.generate_color_service import GenerateColorService

register = template.Library()


@register.filter(name='get_transportation_color_code')
def get_transportation_color_code(mode):
    return GenerateColorService.get_transportation_color_code(mode)


@register.filter(name='color_code_parts')
def color_code_parts(sentence):
    return GenerateColorService.get_color_coded_parts(sentence)