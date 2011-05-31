from decorators import render_to
from main.models import News
from django.shortcuts import get_object_or_404, redirect
from main.forms import NewsForm
from django.contrib.auth.decorators import login_required

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

@login_required
@render_to('main/create.html')    
def create(request):
    form = NewsForm(request.POST or None)
    if form.is_valid():
        return redirect('main:index')
    return {
        'form': form
    }
    
@render_to('main/flatpage.html')
def flatpage(request, val):
    return {
        'val': val
    }