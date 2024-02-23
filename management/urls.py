
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VendorViewSet, ProductViewSet, VehicleViewSet, initiate_checkout, vehicle_detail , mark_quality_check 

router = DefaultRouter()
router.register(r'vendors', VendorViewSet)
router.register(r'products', ProductViewSet)
router.register(r'vehicles', VehicleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('vehicles/<int:vehicle_id>/mark-quality-check/', mark_quality_check, name='mark_quality_check'),
    path('initiate-checkout/<int:vehicle_id>/', initiate_checkout),
    path('vehicle-detail/<int:vehicle_id>/', vehicle_detail),
]
