from decorators import render_to
from main.models import News
from django.shortcuts import get_object_or_404

@render_to('main/index.html')
def index(request):
    return {
        'objects': News.objects.all()
    }

@render_to('main/news_details.html')
def news_details(request, id):
    obj = get_object_or_404(News, id=id)
    return {
        'obj': obj
    }