import redis
from django.db import models
from django_redis import get_redis_connection
from django_redis import get_redis_connection


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()


    def __str__(self):
        return self.name

    def get_cached_product_name(self):
        cache_key = f"product_details_{self.id}"
        redis_client = redis.Redis(
			host="localhost", port=6379, db=0
		)
        product_name = redis_client.get(cache_key)

        # if product_name is None:
        #     product_name = self.name
        #     redis_client.set(cache_key, product_name, ex=60) 
        # return product_name
        if product_name is None:
        	product_name = self.name
        	redis_client.set(cache_key, product_name, ex=60) 
        	return product_name
        return product_name

