from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.urls import reverse

from .models import Article, Tag, Reporter, Comment

def homepage(request):
    # Get some articles from
    latest_articles_list = Article.objects.select_related('reporter').prefetch_related('tags').order_by('-published_at')[:5]
    return render(request, 'index.html', {'latest_articles_list': latest_articles_list})


class TagView(generic.ListView):
    paginate_by = 10
    template_name = 'tags/index.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tag'] = get_object_or_404(Tag, name=self.kwargs.get('slug'))
        return context

    def get_queryset(self):
        """Return the last five published articles."""
        slug = self.kwargs.get('slug')
        return Article.objects.select_related(
                'reporter'
            ).prefetch_related(
                'tags'
            ).filter(
                tags__name=slug
            ).order_by(
                '-published_at'
            )


class ReporterView(generic.ListView):
    paginate_by = 10
    template_name = 'reporters/index.html'

    def get_reporter_by_fullname(self, slug):
        try:
            firstname, lastname = (chunk.capitalize() for chunk in slug.split('-'))
        except Exception as e:
            raise Http404("Reporter does not exist")
        return get_object_or_404(Reporter, firstname__icontains=firstname, lastname__icontains=lastname)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['reporter'] = self.get_reporter_by_fullname(self.kwargs.get('slug'))
        return context

    def get_queryset(self):
        """Return the last five published articles."""
        slug = self.kwargs.get('slug')
        reporter = self.get_reporter_by_fullname(self.kwargs.get('slug'))
        return Article.objects.select_related(
                'reporter'
            ).prefetch_related(
                'tags'
            ).filter(
                reporter__id=reporter.id
            ).order_by(
                '-published_at'
            )


class ArticleView(generic.DetailView):
    model = Article
    template_name = 'articles/detail.html'
    slug_url_kwarg = 'slug'
    query_pk_and_slug = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['comments'] = Comment.objects.filter(article=self.get_object())[0:20]
        context['comments'] = Comment.objects.filter(article=self.get_object()).filter(aproved=True)[0:20]
        return context

def add_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if not request.POST['username'] or not request.POST['content']:
        return render(request, 'articles/detail.html', {
            'article': article,
            'comments': Comment.objects.filter(article=article).filter(aproved=True)[0:20],
            'username': request.POST['username'],
            'content': request.POST['content'],
            'error_message': "You didn't fill username or comment text.",
        })

    comment = Comment(article=article)
    comment.username = request.POST['username']
    comment.content = request.POST['content']
    comment.save()
    return HttpResponseRedirect(reverse('article', args=(article.slug,)))
