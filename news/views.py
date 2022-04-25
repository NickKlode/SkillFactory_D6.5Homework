from datetime import datetime
from unicodedata import category
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .forms import PostForm
from .models import *
from .filters import PostFilter
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

class NewsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-dateCreation')
    paginate_by = 10
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)
    
class NewsDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'
    
    def get_object(self, *args, **kwargs):
        obj=cache.get(f"Post-{self.kwargs['pk']}", None)
        if not obj:
            obj = super().get_object(*args, **kwargs)
            cache.set(f"Post-{self.kwargs['pk']}", obj)
        return obj
    
class Search(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'search'
    queryset = Post.objects.order_by('-dateCreation')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context
    
class CreatePost(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'create.html'
    context_object_name = 'create'
    form_class = PostForm
    permission_required = 'news.add_post'
    
    
class UpdatePost(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    template_name = 'update.html'
    form_class = PostForm
    permission_required = 'news.change_post'
    
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)

class DeletePost(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    permission_required = 'news.delete_post'

class CategoryList(ListView):
    model = Category
    template_name = 'categories.html'
    context_object_name = 'categories'
    queryset = Category.objects.all()

class OneCategory(DetailView):
    model = Category
    template_name = 'category.html'
    context_object_name = 'category'
    
    def get_context_data(self,  **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('pk')
        context['catposts'] = Post.objects.filter(postCategory = id).order_by('-dateCreation')
        context['subs_list'] = Category.objects.get(pk=id).subscribers.filter(username=self.request.user).all()
        context['is_subscribed'] = Category.objects.get(pk=id).subscribers.filter(username=self.request.user).exists()
        return context
    
@login_required
def add_subscriber(request, pk):
    user = request.user
    category = Category.objects.get(pk=pk)
    if not category.subscribers.filter(username=user).exists():
        category.subscribers.add(user)
    else:
        category.subscribers.remove(user)
    
    return redirect(f'/news/categories/{pk}')

