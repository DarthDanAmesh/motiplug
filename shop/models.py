from django.conf import settings
from django.db import models
from django.shortcuts import reverse


LABEL_CHOICES=(
 ('P','primary'),
 ('S','secondary'),
 ('D','danger')
)


#model to store the product info
class Item(models.Model):
    name=models.CharField(max_length=100)
    cost=models.FloatField()
    discount_cost=models.FloatField( blank=True ,null=True )     #not a required field
    colortag=models.CharField(choices=LABEL_CHOICES, max_length=1,blank=True ,null=True)
    tag=models.CharField(max_length=15,blank=True ,null=True)      #for giving different tags to products like bestseller, new etc.
    slug=models.SlugField()      #a unique identity for different products
    detail=models.TextField()
    photo=models.FileField(upload_to = 'images/', default = '')    #images are uploaded to media/images folder

    def __str__(self):
        return self.name    #when item is referenced its title is returned

    def get_absolute_url(self):
        return reverse("shop:product",kwargs={'slug':self.slug})     #unique url for every product due to its slug

    def get_add_item_to_cart_url(self):
        return reverse("shop:add-to-cart",kwargs={'slug':self.slug})    #url for adding an item to cart

    def get_remove_item_from_cart_url(self):
        return reverse("shop:remove-from-cart",kwargs={'slug':self.slug})    #url for adding an item to cart



#model to obtain the info of products which are ordered by a particular user
class OrderItem(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.CASCADE)    #obtaining user info from allauth
    item=models.ForeignKey(Item, on_delete=models.CASCADE)     #for obtaining product info from Item model
    number=models.IntegerField(default=1)
    ordered=models.BooleanField(default=False)   #whather the product has been added to cart or not


    def __str__(self):
        return f"{self.number} of {self.item.name}"      #when ordered item is referenced its title and quantity is returned

    def get_total_product_cost(self):
        return self.number * self.item.cost   #returns an item price according to its quantity

    def get_total_discount_product_cost(self):
        return self.number * self.item.discount_cost   #for calculating price in case of a discount

    def get_saved_cost(self):
        return self.get_total_product_cost()-self.get_total_discount_product_cost()

    def get_final_cost(self):
        if self.item.discount_cost:
            return self.get_total_discount_product_cost()
        else:
            return self.get_total_product_cost()

#model to obtain info about orders placed by particular user
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.CASCADE)    #obtaining user info from allauth
    items=models.ManyToManyField(OrderItem)      #a product can be present in more than one orders(of different users)
    order_begin_date=models.DateTimeField(auto_now_add=True)
    order_placed_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)      #whather the order has been placed or not
    address=models.ForeignKey(
            'Address',on_delete=models.SET_NULL,blank=True,null=True)   #for obtaining user address and other info to deliver the product

    def __str__(self):
        return self.user.username           #returns the username who placed the order

    def get_order_cost(self):
        order_cost=0
        for order_item in self.items.all():
            order_cost+=order_item.get_final_cost()
        return order_cost                        #returns the order total for a particular order


#model for storing data entered by user through checkout form
class Address(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.CASCADE)     #obtaining user info from allauth for storing address info
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    street_address=models.CharField(max_length=100)
    apartment_address=models.CharField(max_length=100)
    country=models.CharField(max_length=15)
    city=models.CharField(max_length=15)    #constraits are applied in form fields beacuse data is entered by user through forms
    postal_code=models.CharField(max_length=5)
    phone=models.CharField(max_length=13)

    def __str__(self):
        return '%s %s %s' %(self.street_address,self.apartment_address,self.city)
          #when user address is referenced the street and apartment address, city and country is returned
