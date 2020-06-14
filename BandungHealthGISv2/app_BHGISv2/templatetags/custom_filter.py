from django import template

register = template.Library()

"""
@register.filter(is_safe=True)
def getWilayah(value, request):
	qs = Kasus.objects.filterWilayah(request)
	return qs

"""