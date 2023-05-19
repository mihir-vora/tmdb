import time
import json
import redis
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache
from redis import Redis
from django.views.decorators.cache import cache_page
from .models import Product


TMDB_API_KEY = '0ba968234e47d96aa0c99613677bccb5'
redis_client = redis.Redis(host='localhost', port=6379, db=0)


def get_movie_details(request, movie_id):
	try:
		api_key = TMDB_API_KEY
		url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'

		cache_key = f"movie_details:{movie_id}"

		redis_client = redis.Redis(
			host="localhost", port=6379, db=0
		)
		movie_details = redis_client.get(cache_key)

		if movie_details is None:
			response = requests.get(url)
			movie_details = response.json()
			redis_client.set(cache_key, json.dumps(movie_details), ex=60)  # Set expiration time of 1 minute (60 seconds)

			return JsonResponse(movie_details)
		else:
			new_str = movie_details.decode('utf-8')
			movie_details = json.loads(new_str)  

			return JsonResponse(movie_details)
	except requests.exceptions.RequestException as e:
		return JsonResponse({'error': str(e)})


def get_movie_details_object_level_caching(request, product_id):
    """
    Retrieves movie details either from the cache or from the TMDB API.

    Args:
        movie_id (int): The unique identifier of the movie.

    Returns:
        dict: The movie details as a dictionary, or None if an error occurs.

    """
    print("object level caching")
    product = Product.objects.get(id=product_id)
    product_name = product.get_cached_product_name()

    return render(request, 'movies/product_detail.html', {'product': product, 'product_name': product_name})


@cache_page(60 * 1)  # Cache the view for 1 minutes
def get_movie_details_fragment_caching(request, movie_id):
    print("fragment caching")
    # Check if movie details are already in cache
    cache_key = f'movie_details_{movie_id}'

    redis_client = redis.Redis(
            host="localhost", port=6379, db=0
        )
    movie = redis_client.get(cache_key)

    if movie is None:
        # Fetch movie details from TMDB store
        api_key = TMDB_API_KEY
        tmdb_url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
        response = requests.get(tmdb_url)

        if response.status_code == 200:
            movie = response.json()

            # Store movie details in cache
            cache.set(cache_key, movie)
            redis_client.set(cache_key, json.dumps(movie), ex=60)  # Set expiration time of 1 minute (60 seconds)
            

    return render(request, 'movies/movie_details.html', {'movie': movie})

