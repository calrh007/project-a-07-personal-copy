from django import template

from measurement.measures import Distance, Weight

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()

@register.simple_tag
def round_if_measurement(poss_measurement):
    if type(poss_measurement) == type(Distance()):
        return str(round(poss_measurement.mi, 3)) + ' mi'
    if type(poss_measurement) == type(Weight()):
        return str(round(poss_measurement.lb, 3)) + ' lb'
    return poss_measurement