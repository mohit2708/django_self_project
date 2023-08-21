from django.contrib import admin
from crud_function_based.models import Customer

# Register your models here.
 
admin.site.register(Customer) 		# instead of @admin.register(Product)