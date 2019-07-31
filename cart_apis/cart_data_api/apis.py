from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', RetrieveDestroyCartView.as_view(), name="retreive-destroy-cart"),
    url(r'add/$', AddItemToCartView.as_view(), name="add-cart-item"),
    url(r'delete/$', RemoveItemFromCartView.as_view(), name="remove-cart-item"),
    url(r'total/$', CartTotalAmount.as_view(), name="total-cart-cost")
]

