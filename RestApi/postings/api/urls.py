from .views import (
    BlogPostRudView, 
    # BlogPostListView,
    BlogPostAPIView
)
from django.urls import path

app_name = 'postings'

urlpatterns = [
    # path('',BlogPostListView.as_view(), name='post-list'),
    path('',BlogPostAPIView.as_view(), name='post-listcreate'),
    path('<pk>/',BlogPostRudView.as_view(), name='post-rud'),
]