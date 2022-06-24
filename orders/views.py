from django.shortcuts import render,get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import OrderCreationSerializer,OrderDetailSerializer, OrderUpdateStatusSerializer
from .models import Order
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,IsAdminUser
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class HelloOrderViews(GenericAPIView):
    def get(self,request):
        return Response(data={'message':'Hello Order'},status=status.HTTP_200_OK)
    
class OrderCreateListView(GenericAPIView):
    serializer_class = OrderCreationSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self,request):
        orders = Order.objects.all()
        serializer = OrderCreationSerializer(instance=orders,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    def post(self,request):
        user = request.user
        data = request.data
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save(customer=user)
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    
# For Update, Delete and retrive one data 
class OrderDetailView(GenericAPIView):
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAdminUser]
    def get(self,request,order_id):
        order = get_object_or_404(Order,pk=order_id)
        serializer = self.serializer_class(instance=order)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    
    def put(self,request,order_id):
        data = request.data
        order = get_object_or_404(Order,pk=order_id)
        serializer = self.serializer_class(data=data,instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,order_id):
        order = get_object_or_404(Order,pk=order_id)
        order.dalete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UpdateOrderStatus(GenericAPIView):
    serializer_class = OrderUpdateStatusSerializer
    permission_classes = [IsAdminUser]
    def put(self,request,order_id):
        order = get_object_or_404(Order,pk=order_id)
        data = request.data
        serializer = self.serializer_class(data=data,instance=order)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserOrderView(GenericAPIView):
    serializer_class = OrderDetailSerializer
    def get(self,request,user_id):
        user = User.objects.get(pk=user_id)
        order = Order.objects.all().filter(customer = user)
        serializers = self.serializer_class(instance=order,many=True)
        return Response(data=serializers.data,status=status.HTTP_200_OK)
    
class UserOrderDetail(GenericAPIView):
    serializer_class = OrderDetailSerializer
    def get(self,request,user_id,order_id):
        user = User.objects.get(pk=user_id)
        order = Order.objects.all().filter(customer=user).get(pk=order_id)
        serializers = self.serializer_class(instance=order)
        return Response(data=serializers.data,status=status.HTTP_200_OK)