from django.db import models
from django.contrib.auth.models import User

'''
Product would generally assume its own django app, just putting it here for simplicity of this project
'''
class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    cost = models.FloatField(default=0, blank=False)

    class Meta:
        verbose_name_plural = "Products"
        verbose_name = "Product"

    def __str__(self):
       return self.name

class Cart(models.Model):
    customer = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    items = models.ManyToManyField("CartItem")
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Carts"
        verbose_name = "Cart"

    def search_item(self, product):
        for item in self.items.all():
            if item.product.id == int(product):
                return item
        return None

    def add_item(self, product=None, quantity=None):
        if product is not None and quantity is not None:

            product = Product.objects.get(id=int(product))

            # Create Cart Item
            item = CartItem.objects.create(
                product=product,
                quantity=quantity,
            )

            self.items.add(item)
            return item
        return None

    def get_total(self):
        return sum(item.product.cost*item.quantity for item in self.items.all()) or 0

    def __str__(self):
        return str(self.customer)


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()


    @classmethod
    def create_cartitem(cls, data):
        for item in data:
            cart_item = CartItem.objects.create(
                product=item['product'],
                quantity=item['quantity']
            )

    def update_quantity(self, quantity):
        if int(quantity) == 0:
            self.delete()
            return None
        else:
            self.quantity = int(quantity)
            return self.save()

    def __str__(self):
        return "Cart Item: " + str(self.product)