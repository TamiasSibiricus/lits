from django.conf import settings
from django import template
from myproject.models import Tag, Reporter

register = template.Library()

@register.inclusion_tag('widgets/tags_menu.html')
def tags_menu():
    tags = Tag.objects.all()
    return {'tags': tags}

@register.inclusion_tag('widgets/reporters_menu.html')
def reporters_menu():
    # TODO: find articles qty and return top 10 reporters
    reporters = Reporter.objects.all()[0:10]
    return {'reporters': reporters}

@register.inclusion_tag('widgets/user_menu.html', takes_context=True)
def user_menu(context):
    return {'user': context.get('user'), 'menu': {}}
