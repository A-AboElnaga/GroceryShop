from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def query_tag(context, **kwargs):
    query = context['request'].GET.copy()
    # print(kwargs)
    # print(query)
    for k, v in kwargs.items():
        query[k] = v
    # print(query)
    return query.urlencode()