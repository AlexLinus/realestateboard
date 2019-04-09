from django.template.context_processors import request
from pages.models import Pages
#start methods
def menus(request):
    top_menu = Pages.objects.filter(is_active=True, top_menu=True)
    footer_menu = Pages.objects.filter(is_active=True, footer_menu=True)
    context = {'top_menu': top_menu, 'footer_menu': footer_menu}
    return context