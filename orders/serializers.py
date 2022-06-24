from rest_framework import serializers
from .models import Order

class OrderCreationSerializer(serializers.ModelSerializer):
    order_status = serializers.HiddenField(default='PENDING')
    class Meta:
        model = Order
        fields = ['id','size','order_status','qunatity']
        
class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id','size','order_status','qunatity','created_at','updated_at']
        
class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    order_status = serializers.CharField(default='PENDING')
    class Meta:
        model = Order
        fields = ['order_status']