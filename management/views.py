from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

# Create your views here.

from rest_framework import viewsets
from rest_framework.decorators import api_view , permission_classes , authentication_classes
from rest_framework.response import Response
from .models import Vendor, Product, Vehicle, QualityCheck
from .serializer import VendorSerializer, ProductSerializer, VehicleSerializer, QualityCheckSerializer

class VendorViewSet(viewsets.ModelViewSet):
    queryset = Vendor.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = VendorSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = ProductSerializer

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = VehicleSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def vehicle_detail(request, vehicle_id):
    vehicle = Vehicle.objects.get(pk=vehicle_id)
    serializer = VehicleSerializer(vehicle)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def mark_quality_check(request, vehicle_id):
    try:
        quality_check = QualityCheck.objects.get(vehicle_id=vehicle_id)
        serializer = QualityCheckSerializer(quality_check, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except QualityCheck.DoesNotExist:
        return Response({"message": "Quality Check not found for the vehicle."}, status=status.HTTP_404_NOT_FOUND)

@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['POST'])
def initiate_checkout(request, vehicle_id):
    try:
        vehicle = Vehicle.objects.get(pk=vehicle_id)
        try:
            quality_check = QualityCheck.objects.get(vehicle_id=vehicle_id)
            if not quality_check.pass_status:
                return Response({"message": "Quality check not passed. Vehicle cannot be checked out."},
                                status=status.HTTP_400_BAD_REQUEST)
        except QualityCheck.DoesNotExist:
            return Response({"message": "Quality check not found for the vehicle."},
                            status=status.HTTP_404_NOT_FOUND)
        vehicle.checked_out = True
        vehicle.save()

        return Response({"message": "Check-out process initiated successfully."})
    except Vehicle.DoesNotExist:
        return Response({"message": "Vehicle not found."}, status=status.HTTP_404_NOT_FOUND)


