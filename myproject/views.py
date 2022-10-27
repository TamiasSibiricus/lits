from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render
from django.views import generic

from .models import Article

def index(request):
    # Simple response without any processing
    #return HttpResponse("You're looking at articles")
    
    # Get some articles from 
    latest_articles_list = Article.objects.select_related('reporter').prefetch_related('tags').order_by('-published_at')[:5]
    #output = ', '.join([a.title for a in latest_articles_list])
    #return HttpResponse(output)
    
    context = {
        'latest_articles_list': latest_articles_list,
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
    # or
    # return render(request, 'index.html', context)
    
def article(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Question does not exist")
    # or
    #article = get_object_or_404(Article, pk=article_id)
    return render(request, 'articles/detail.html', {'article': article})


class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'latest_articles_list'

    def get_queryset(self):
        """Return the last five published articles."""
        return Article.objects.select_related('reporter').prefetch_related('tags').order_by('-published_at')[:5]


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'articles/detail.html'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True