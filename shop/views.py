from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView,DetailView,View
from .models import Item,OrderItem,Order,Address
from .forms import CheckoutForm
from django.shortcuts import redirect
from django.utils import timezone


#view connecting home page template to backend model
#list view is used because list of products is displayed
class HomeView(ListView):
    model=Item
    paginate_by=8   #after 8 items, additional items are moved to next page
    template_name="home.html"



#view connecting product detail page template to backend model
#product view is used because detail of the product is displayed
class ItemDetailView(DetailView):
    model=Item
    template_name="product.html"



#view connecting order summary page template to backend model
#login required mixin ensures that the user is logged in, if not it redirects him to login page
class OrderSummaryView(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            context={'object':order }
            return render (self.request, "order_summary.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order.")
            return redirect("/")



#view connecting checkout page template to backend model and form
#login required mixin ensures that the user is logged in, if not it redirects him to login page
class CheckoutView(LoginRequiredMixin, View):
    def get(self,*args,**kwargs):
        form=CheckoutForm()
        context={
             'form':form
        }
        return render(self.request,"checkout.html",context)

    def post(self,*args,**kwargs):
        form=CheckoutForm(self.request.POST or None)
        try:
            order=Order.objects.get(user=self.request.user, ordered=False)
            #if user enters correct data in the form then it will be saved and successful order
            if form.is_valid():
                first_name=form.cleaned_data.get('first_name')
                last_name=form.cleaned_data.get('last_name')
                street_address=form.cleaned_data.get('street_address')
                apartment_address=form.cleaned_data.get('apartment_address')
                country=form.cleaned_data.get('country')
                city=form.cleaned_data.get('city')
                postal_code=form.cleaned_data.get('postal_code')
                phone=form.cleaned_data.get('phone')
                address=Address(
                    user=self.request.user,
                    first_name=street_address,
                    last_name=last_name,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    city=city,
                    postal_code=postal_code,
                    phone=phone
                )
                #saving all the info from form into the database
                address.save()
                order.address=address
                order.ordered=True
                order.save()
                messages.info(self.request,"Your order was successful and payment will be on delivery.")
                return redirect('shop:checkout')
            #displaying error if user violates data entry constraints
            messages.warning(self.request,"Failed Checkout")
            return redirect('shop:checkout')

        #if user tries to checkout without placing an order
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order.")
            return redirect("shop:home")


#view to add an item to shopping cart
#login required decorator ensures that the user is logged in, if not it redirects him to login page
@login_required
def add_to_cart(request,slug):
    item=get_object_or_404(Item, slug=slug)
    order_item, created=OrderItem.objects.get_or_create(
    item=item,
    user=request.user,
    ordered=False
    )
    order_qs=Order.objects.filter(user=request.user,ordered=False)
    #check if user has an active order or not
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the ordered
        if order.items.filter(item__slug=item.slug).exists():
            order_item.number+=1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("shop:order-summary")
        else:
        #if item was not ordered previously
            order.items.add(order_item)
            order_item.number=1
            order_item.save()
            messages.info(request, "This item was added to your cart.")
            return redirect("shop:order-summary")
    #create a new order if user had no previous order
    else:
        order_placed_date=timezone.now()
        order=Order.objects.create(user=request.user,order_placed_date=order_placed_date)
        order.items.add(order_item)
        order_item.number=1
        order_item.save()
        messages.info(request, "This item was added to your cart.")
        return redirect("shop:order-summary")



#view to remove an item from shopping cart
#login required decorator ensures that the user is logged in, if not it redirects him to login page
@login_required
def remove_from_cart(request,slug):
    item=get_object_or_404(Item, slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    #check if user has an active order or not
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the ordered
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("shop:order-summary")
        #if item was not ordered previously
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("shop:product",slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("shop:product",slug=slug)



#view to remove an item or reduce the quantity of an item in shopping cart
#login required decorator ensures that the user is logged in, if not it redirects him to login page
@login_required
def remove_single_item_from_cart(request,slug):
    item=get_object_or_404(Item, slug=slug)
    order_qs=Order.objects.filter(
        user=request.user,
        ordered=False
    )
    #check if user has an active order or not
    if order_qs.exists():
        order=order_qs[0]
        #check if the order item is in the ordered
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order_item.number-=1
            order_item.save()
            if order_item.number==0:
                order.items.remove(order_item)
                messages.info(request, "This item was removed from your cart.")
                return redirect("shop:order-summary")
            else:
                messages.info(request, "This item quantity was updated.")
                return redirect("shop:order-summary")
        #if item was not ordered previously
        else:
            messages.info(request, "This item was not in your cart.")
            return redirect("shop:product",slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("shop:product",slug=slug)
