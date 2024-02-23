from django.contrib import admin
from .models import Vehicle , Vendor , Product
# Register your models here.
admin.site.register(Vehicle)
admin.site.register(Vendor)
admin.site.register(Product)