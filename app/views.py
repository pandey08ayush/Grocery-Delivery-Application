from django.shortcuts import render,redirect
from django.views import View
from .models import Customer,Product,Cart,orderplaced
from .forms import CustomerRegistrationForm, CustomerProfileForms
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
import csv
from .utils import write_single_csv_data
# from .utils import generate_captcha, states, set_sign_data, set_unsign_data, calc_candidate_score, calc_remaining_candidate_exam_time



class ProductView(View):
    def get(self,request):
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        flours = Product.objects.filter(category='M')
        Oil = Product.objects.filter(category='L')

        return render(request, 'app/home.html',
        {'topwear':topwear,'bottomwear':bottomwear,'flours':flours,'Oil':Oil})

class ProductDetailsView(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            print(item_already_in_cart)
        
        return render(request, 'app/productdetail.html',
        {'product':product,'item_already_in_cart':item_already_in_cart})



# def product_detail(request):
#  return render(request, 'app/productdetail.html')

def add_to_cart(request):
    user= request.user
    print(user)
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect('/cart')

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        cart= Cart.objects.filter(user=user)

        amount =0.0
        shipping_amount=70.0
        total_amount=0.0 
        cart_product=[p for p in Cart.objects.all() if p.user == request.user] #list compication python
        print(cart_product )
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.discount_price)
                amount= amount + tempamount
                total_amount = amount + shipping_amount
        return render(request,'app/addtocart.html',{'carts':cart,'total_amount': total_amount,'amount':amount})
    else:
        return render(request, 'app/emptycard.html')

def plus_cart(request):
    if request.method == 'GET':
       prod_id = request.GET['prod_id']
       c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
       c.quantity+=1
       c.save()
       amount =0.0
       shipping_amount=70.0
       total_amount=0.0 
       cart_product=[p for p in Cart.objects.all() if p.user == request.user]
       for p in cart_product:
        tempamount= (p.quantity * p.product.discount_price)
        amount= amount + tempamount
        

       data = {
        'quantity': c.quantity,
        'amount': amount,
        'total_amount':amount + shipping_amount
        }
       return JsonResponse(data)
    else:
        return render(request, 'app/emptycard.html')
    
def minus_cart(request):
    if request.method == 'GET':
       prod_id = request.GET['prod_id']
       c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
       c.quantity-=1
       c.save()
       amount =0.0
       shipping_amount=70.0
       total_amount=0.0 
       cart_product=[p for p in Cart.objects.all() if p.user == request.user]
       for p in cart_product:
        tempamount= (p.quantity * p.product.discount_price)
        amount= amount + tempamount
       

       data = {
        'quantity': c.quantity,
        'amount': amount,
        'total_amount':amount + shipping_amount
        }
       return JsonResponse(data)
    else:
        return render(request, 'app/emptycard.html')
    
def remove_cart(request):
    if request.method == 'GET':
       prod_id = request.GET['prod_id']
       c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
       c.quantity-=1
       c.delete()
       amount =0.0
       shipping_amount=70.0
       total_amount=0.0 
       cart_product=[p for p in Cart.objects.all() if p.user == request.user]
       for p in cart_product:
        tempamount= (p.quantity * p.product.discount_price)
        amount= amount + tempamount
       

       data = {
        'amount': amount,
        'total_amount':amount + shipping_amount
        }
       return JsonResponse(data)
    else:
        return render(request, 'app/emptycard.html')
    

    


def buy_now(request):
 return render(request, 'app/buynow.html')

# def profile(request):
#  return render(request, 'app/profile.html')

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForms()
        return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})

    def post(self,request):
        form = CustomerProfileForms(request.POST)
        if form.is_valid():
            usr= request.user
            name =form.cleaned_data['name']
            locality =form.cleaned_data['locality'] 
            city =form.cleaned_data['city']
            state =form.cleaned_data['state']
            zipcode =form.cleaned_data['zipcode']
            reg = Customer( user=usr,name=name, locality=locality,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request, ' Congralutaions!! Profile Updated Succesfully')
        return render(request, 'app/profile.html',{'form':form,'active':'btn-primary'})

    

# current login user mill jaye isse(first line se)

@login_required
def address(request):
    add = Customer.objects.filter(user=request.user) 

    return render(request, 'app/address.html',{'add':add})

@login_required
def orders(request):
 return render(request, 'app/orders.html')

# def change_password(request):
#  return render(request, 'app/changepassword.html')

def  flour(request,data=None):
    if data == None:
         flours = Product.objects.filter(category='M')
    elif data == 'Patanjali' or data == 'Aashirvaad':
         flours =  Product.objects.filter(category='M').filter(brand=data)
    elif data =='below':
         flours =  Product.objects.filter(category='M').filter(discount_price__lt=400)
    elif data =='above':
         flours =  Product.objects.filter(category='M').filter(discount_price__gt=400)
    return render(request, 'app/flour.html',{' flours': flours})

def  Oils(request,data=None):
    if data == None:
         Oil = Product.objects.filter(category='L')
    elif data == 'Patanjali' or data == 'Refined':
         Oil =  Product.objects.filter(category='L').filter(brand=data)
    elif data =='below':
         Oil =  Product.objects.filter(category='L').filter(discount_price__lt=300)
    elif data =='above':
         Oil =  Product.objects.filter(category='L').filter(discount_price__gt=300)
    return render(request, 'app/oils.html',{'Oil': Oil})

def topwear(request,data=None):
    if data == None:
        wears = Product.objects.filter(category='TW')
    elif data == 'Shampoo' or data == 'Soap':
        wears =  Product.objects.filter(category='TW').filter(title=data)
    elif data =='below':
        wears =  Product.objects.filter(category='TW').filter(discount_price__lt=250)
    elif data =='above':
        wears =  Product.objects.filter(category='TW').filter(discount_price__gt=250)
    return render(request, 'app/wear.html',{'wears':wears})
   

# def login(request):
#  return render(request, 'app/login.html')

# def customerregistration(request):
#  return render(request, 'app/customerregistration.html')


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request,'app/customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request,'Congratulation!! Registered    Succesfully')
            form.save()
        return render(request,'app/customerregistration.html',{'form':form})


def checkout(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        add = Customer.objects.filter(user=user) 
        cart_item = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount=70.0
        total_amount= 0.0
        cart_product=[p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount= (p.quantity * p.product.discount_price)
                amount= amount + tempamount
            total_amount = amount+shipping_amount
        return render(request, 'app/checkout.html',{'add':add,'cart_item':cart_item,'total_amount':total_amount})  
    else:
        return render(request, 'app/emptycard.html')

def export_single_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="data.csv"'

    # Define the CSV writer.
    writer = csv.writer(response)

    # Prepare data for the model
    headers = ['title', 'selling_price', 'discount_price']  # Replace with your actual headers
    queryset = Product.objects.all()  # Replace MyModel with your model name
    columns = ['title', 'selling_price', 'discount_price']  # Replace with your model fields

    
    write_single_csv_data(writer, headers, queryset, columns)

    return response

def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id=custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        orderplaced(user=user, customer=customer, product=c.Product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")

def user_logout(request):
    logout(request)
    return redirect("home")
