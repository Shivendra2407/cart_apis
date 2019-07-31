from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User

class ListProductSerializer(serializers.ModelSerializer):
    '''
    List Products serializer.
    '''

    class Meta:
        model = Product
        fields = "__all__"

class AddItemToCartSerializer(serializers.Serializer):
    '''
    Add an item to Cart Serializer.
    '''

    product = serializers.CharField()
    quantity = serializers.IntegerField(default=1)


class RemoveItemFromCartSerializer(serializers.Serializer):
    '''
    Remove an item from Cart Serializer.
    '''

    product = serializers.CharField()

class CartItemSerializer(serializers.ModelSerializer):
    '''
    Cart Item object Serializer.
    '''

    product = ListProductSerializer()

    class Meta:
        model = CartItem
        fields = "__all__"

class ListRetrieveCustomerSerializer(serializers.ModelSerializer):
    '''
    Serializes the customer object.
    '''
    class Meta:
        model = User
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    '''
    Cart object Serializer.
    '''

    customer = ListRetrieveCustomerSerializer()
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = "__all__"
