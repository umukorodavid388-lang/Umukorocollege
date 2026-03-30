from django.shortcuts import render, redirect
from .models import *
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, render
from django.db.models import F
from django.core.paginator import Paginator


# Create your views here.

def news(request):
    latest_news = News.objects.order_by('-created_date')[:5]

    last_7_days = timezone.now() - timedelta(days=7)
    trending_news = News.objects.filter(
        created_date__gte=last_7_days
    ).order_by('-views')[:5]

    top_stories = News.objects.order_by('-views', '-created_date')[:5]


    news = News.objects.first()
    new = News.objects.all()

    paginator = Paginator(new, 6)  # 6 news per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'latest_news': latest_news,
        'trending_news': trending_news,
        'top_stories': top_stories,
        'news':news,
        'new':new,
        'page_obj':page_obj,
    }

    return render(request, 'news-post/news.html', context)




def post_detail(request, pk):
    post = get_object_or_404(News, pk=pk)

    News.objects.filter(pk=pk).update(views=F('views') + 1)
    post.refresh_from_db()

    return render(request, 'news-post/news-details.html', {'post': post})
