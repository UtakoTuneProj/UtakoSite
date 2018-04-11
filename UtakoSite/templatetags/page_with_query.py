from django import template

register = template.Library()

@register.simple_tag
def page_with_query(request, page_number):
    querydict = request.GET.copy()
    querydict['page'] = page_number

    return querydict.urlencode()
