from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.db.models import Count

from .models import Author, Article, Category, Comment
from .forms import NotAuthorizedCommentForm, AuthorizedCommentForm


class ExtraContext(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all().order_by('last_name')

        if 'author' in self.kwargs:
            context['chosen_author'] = Author.objects.get(id=self.kwargs['author'])
        elif 'category' in self.kwargs:
            context['chosen_category'] = Category.objects.get(slug=self.kwargs['category'])

        return context


class ArticlesFilterCategoryListView(ExtraContext, ListView):
    model = Article
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(category__slug=self.kwargs['category']).annotate(comments_count=Count('comments'))


class ArticlesFilterAuthorListView(ExtraContext, ListView):
    model = Article
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(author__id=self.kwargs['author']).annotate(comments_count=Count('comments'))


class ArticlesListView(ExtraContext, ListView):
    model = Article
    paginate_by = 5

    def get_queryset(self):
        return self.model.objects.select_related('author', 'category').annotate(comments_count=Count('comments'))


class ArticleDetailView(FormMixin, DetailView):
    model = Article
    form_class = NotAuthorizedCommentForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['latest_articles'] = Article.objects.order_by('-date')[:5]
        data['comments'] = Comment.objects.filter(article_id=self.kwargs['pk'], active=True)
        data['comments_count'] = Comment.objects.filter(article_id=self.kwargs['pk']).count()
        return data

    def get_success_url(self):
        return reverse('articles-detail', kwargs={'pk': self.kwargs['pk']})

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return AuthorizedCommentForm
        return super().get_form_class()

    def post(self, request, pk):
        article = Article.objects.get(pk=pk)
        if self.request.user.is_authenticated:
            form = AuthorizedCommentForm(self.request.POST)
            user = User.objects.get(username=self.request.user)
            if form.is_valid():
                Comment.objects.create(article=article, name=user.username,
                                       email=user.email, body=form.cleaned_data['body'])
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
        else:
            form = NotAuthorizedCommentForm(self.request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.save()
                return super().form_valid(form)
            else:
                return super().form_invalid(form)
