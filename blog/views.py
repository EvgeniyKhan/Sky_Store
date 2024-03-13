from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.apps import BlogConfig
from blog.models import Blogpost


class BlogpostCreateView(CreateView):
    model = Blogpost
    fields = ('title', 'content', 'publication', 'preview')
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
        return super().form_valid(form)


class BlogpostUpdateView(UpdateView):
    model = Blogpost
    fields = ('title', 'content', 'publication', 'preview')
    success_url = reverse_lazy('blog:blog_list')

    def form_valid(self, form):
        if form.is_valid():
            new_mat = form.save()
            new_mat.slug = slugify(new_mat.title)
        return super().form_valid(form)

    def get_success_url(self):
        from django.urls import reverse
        return reverse('blog:view', args=[self.kwargs.get('pk')])


class BlogpostListView(ListView):
    model = Blogpost

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(publication=True)
        return queryset


class BlogpostDetailView(DetailView):
    model = Blogpost

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return queryset


class BlogpostDeleteView(DeleteView):
    model = Blogpost
    success_url = reverse_lazy('blog:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление блога'
        return context

