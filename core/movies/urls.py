from django.urls import path
from . import views
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('get_movie_details/<int:movie_id>/', views.get_movie_details, name='movie_details'),
    path('get_movie_details_fragment_caching/<int:movie_id>/', views.get_movie_details_fragment_caching, name='fragment_caching'),
    
    path('get_movie_details_object_level_caching/<int:product_id>/', views.get_movie_details_object_level_caching, name='level_caching'),
    # path('movie/<int:movie_id>/', views.movie_details, name='movie_details'),
    # cache the page
    # path('movie_redis/<int:movie_id>/', cache_page(60 * 15)(views.movie_details_redis), name='movie_details_redis'),
    # path('product/<int:product_id>/', views.product_detail, name='product_detail'),


]