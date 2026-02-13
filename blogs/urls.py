from django.urls import path
from . import views

app_name = "blogs"

urlpatterns = [

    # Blog Listing
    path('', views.blog_list_view, name='list'),

    # Category Filter
    path('category/<slug:slug>/', views.category_view, name='category'),

    # Add Comment (POST only)
    path('<slug:slug>/comment/', views.add_comment_view, name='add_comment'),

    # Add Reply (POST only)
    path('<slug:slug>/reply/<int:comment_id>/',
         views.add_reply_view,
         name='add_reply'),

    # Blog Detail (MUST BE LAST)
    path('<slug:slug>/', views.blog_detail_view, name='detail'),
]
