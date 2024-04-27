from django.urls import path
from tasks.views import home_view, categories_listing, add_category, category_listing, post_detail, category_edit,category_delete

urlpatterns = [
    path('', home_view, name='home'),
    path('categories/', categories_listing, name='categories'),
    path('category/', category_listing, name='category'),
    path('add_category/<str:foo>/',add_category, name='add_category' ),

    path('<slug:slug>/', post_detail, name='post_detail'),
    path('categories/edit_category/<int:category_id>',
         category_edit, name='category_edit'),

    path('categories/delete_category/<int:category_id>',
         category_delete, name='category_delete'),

    #path('categories/category_detail/<int:category_id>',
    #     category_detail, name='category_detail'),
]