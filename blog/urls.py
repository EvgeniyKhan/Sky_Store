from django.urls import path

from blog.apps import BlogConfig
from blog.views import BlogpostCreateView, BlogpostListView, BlogpostDetailView, BlogpostUpdateView, BlogpostDeleteView

app_name = BlogConfig.name

urlpatterns = [
    path('create/', BlogpostCreateView.as_view(), name='create'),
    path('blog_list/', BlogpostListView.as_view(), name='blog_list'),
    path('view/<int:pk>/', BlogpostDetailView.as_view(), name='view'),
    path('edit/<int:pk>/', BlogpostUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>/', BlogpostDeleteView.as_view(), name='delete'),
]
