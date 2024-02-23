from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    vehicle_number = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=50)
    dc_number = models.CharField(max_length=50)
    po_number = models.CharField(max_length=50)
    quality_check_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.vehicle_number} - {self.vehicle_type}"

class QualityCheck(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    pass_status = models.BooleanField(default=False)

    def __str__(self):
        return f"Quality Check for {self.vehicle}"

class CheckOut(models.Model):
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    initiated_by = models.ForeignKey(User, on_delete=models.CASCADE)
    initiated_at = models.DateTimeField(auto_now_add=True)