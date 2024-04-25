from django.urls import path
from tasks.views import home_view, categories_listing, add_category, category_listing

urlpatterns = [
    path('', home_view, name='home'),
    path('categories/', categories_listing, name='categories'),
    path('category/', category_listing, name='category'),
    path('add_category/<str:foo>/',add_category, name='post_detail' ),
]