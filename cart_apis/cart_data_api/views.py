from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from .models import Cart
from .serializers import AddItemToCartSerializer, CartSerializer, RemoveItemFromCartSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveDestroyAPIView, CreateAPIView, GenericAPIView


class CartTotalAmount(GenericAPIView):

    def get(self, request):
        status_code = HTTP_200_OK
        data = {}
        try:
            cart = Cart.objects.filter(customer=request.user).first()
            data['total_amount'] = cart.get_total()
        except Exception as e:
            print(str(e))
            status_code = HTTP_400_BAD_REQUEST
        finally:
            return Response(data, status=status_code)


class RetrieveDestroyCartView(RetrieveDestroyAPIView):
    '''
    Retreive or delete an cart. This API to be used to
    view a cart or empty it.
    '''

    serializer_class = CartSerializer

    def get_object(self):
        cart, created = Cart.objects.get_or_create(customer=self.request.user)
        return cart


class AddItemToCartView(CreateAPIView):
    '''
    Add an item to a cart.
    '''

    serializer_class = AddItemToCartSerializer

    def create(self, request, *args, **kwargs):
        customer = request.user

        if customer:
            cart, created = Cart.objects.get_or_create(customer=customer)
        else:
            return Response({"error": True, "message": "Not enough information to create cart."})
        # Update quantity if product is already present, otherwise add.
        item = cart.search_item(self.request.data['product'])
        cart.add_item(product=self.request.data['product'], quantity=self.request.data['quantity']) \
            if item is None else item.update_quantity(self.request.data['quantity'])
        return Response(CartSerializer(cart).data, status=HTTP_201_CREATED)


class RemoveItemFromCartView(GenericAPIView):
    '''
    Remove an item from cart
    '''

    serializer_class = RemoveItemFromCartSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        customer = request.user
        if customer:
            cart, created = Cart.objects.get_or_create(customer=customer)
        else:
            return Response({"error": True, "message": "Not enough information to create cart."})

        item = cart.search_item(self.request.data['product'])
        item.delete() if item is not None else None
        return Response(CartSerializer(cart).data, status=HTTP_200_OK)