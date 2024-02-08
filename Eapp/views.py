import datetime

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.checks import Tags
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Sum
from django.shortcuts import render, redirect,get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from Eapp.models import Product, Contact_us, Order, Orderitem, review
from Eapp.models import  Categories
from Eapp.models import Filter_Price
from Eapp.models import Colour
from Eapp.models import Brand
from Eapp.models import Tag
from Eapp.models import wishlist
from cart.cart import Cart
import razorpay

client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRATE))




# Create your views here.


def index(request):
    product = Product.objects.order_by('-id')[:15]
    categories=Categories.objects.all()
    featured=Product.objects.order_by('priority')[:15]
    offer=Product.objects.filter(offer='YES')[:3]
    tag=Tag.objects.all()
    # bestsell=Orderitem.objects.filter(date_added__lte=datetime.datetime.today(), date_added__gt=datetime.datetime.today()-datetime.timedelta(days=7)).annotate(quantity_sum=Sum('quantity')).order_by('quantity_sum')[:8]
    stock=Product.objects.filter(stock='IN STOCK')

    context = {
        'product': product,
        'cat':categories,
        'tag':Tag,
        'featured':featured,
        'offer':offer,
        'stock':stock
    }
    return render(request, 'index.html', context)


def product(request):
    product = Product.objects.all()
    categories=Categories.objects.all()
    price=Filter_Price.objects.all()
    color=Colour.objects.all()
    brand=Brand.objects.all()


    AT0Zid=request.GET.get('ATOZ')
    ZTOA = request.GET.get('ZTOA')
    lh = request.GET.get('lh')
    hl = request.GET.get('hl')
    new=request.GET.get('new')
    old=request.GET.get('old')


    catid=request.GET.get('categories')
    priceid=request.GET.get('filterprice')
    colorid=request.GET.get('color')
    brandid=request.GET.get('brand')
    tagid=request.GET.get('tag')

    p=Paginator(product,5)
    pageno=request.GET.get('page')

    try:
        page_obj=p.get_page(pageno)
    except PageNotAnInteger:
        page_obj=p.page(1)
    except EmptyPage:
        page_obj=p.page(p.num_pages)


    if catid:
        product=Product.objects.filter(categories=catid)
    elif priceid:
        product=Product.objects.filter(filter_price =priceid)
    elif colorid:
        product=Product.objects.filter(colour=colorid)
    elif brandid:
        product=Product.objects.filter(brand=brandid)
    elif tagid:
        product=Tag.objects.filter(name=tagid)
    elif AT0Zid:
        product = Product.objects.order_by('name')
    elif ZTOA:
        product = Product.objects.order_by('-name')
    elif lh:
        product = Product.objects.order_by('price')
    elif hl:
        product = Product.objects.order_by('-name')
    elif new:
        product = Product.objects.filter(condtion='New').order_by('-id')
    elif old:
        product = Product.objects.filter(condtion='Old').order_by('-id')

    else:
        product=Product.objects.all()

    context = {
        'product': product,
        'cat':categories,
        'fprice':price,
        'color':color,
        'brand':brand,
        'pageobj':page_obj
    }
    return render(request, 'product.html',context)


def singleproduct(request, id):
    prod = get_object_or_404(Product, id=id)
    products = Product.objects.filter(categories=prod.categories)
    reviews = review.objects.filter(item_id=id)
    related_products = Product.objects.filter(categories=prod.categories).exclude(id=prod.id)[:5]
    context = {
        'prod': prod,
        'reviews': reviews,
        'products': products,
        'related_products': related_products
    }
    return render(request, 'singleproduct.html', context)


def search(request):
        query = request.GET.get('query')
        product = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))

        context = {
            'product': product
        }
        return render(request,'search.html',context)


def contact(request):
    categories=Categories.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('sub')


        contact = Contact_us(
            name=name,
            email=email,
            subject=subject,
        )
        contact.save()
        return redirect('home')
    context = {
            'cat':categories
        }
    return render(request,'contact.html',context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first')
        last_name = request.POST.get('last')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Create the user object
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,  # Set first name
            last_name=last_name,    # Set last name
        )

        # Save the user object
        user.save()

        return redirect('home')

    return render(request, 'register.html')

def signin(request):
        categories=Categories.objects.all()
        if request.method == 'POST':
            username = request.POST[('username')]
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                sussmsg = "Login successfully"
                messages.success(request, sussmsg)
                return redirect('home')
            else:
                # Handle invalid login
                errormsg = "invalid inputs"
                messages.error(request, errormsg)
            return render(request, 'register.html')
        else:
            context ={
                'cat':categories
            }
            return render(request, 'register.html')

def signout(request):
    logout(request)
    return redirect('home')


@login_required(login_url="signup/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("home")

@login_required(login_url="signup/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="signup/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="signup/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="signup")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="signup")
def cart_detail(request):
    return render(request, 'cart.html')


def checkout(request):
    amount_str=request.POST.get('amount')
    amount_float=float(amount_str)
    amount=int(amount_float)
    payment=client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture":"1"
    })
    order_id = payment['id']
    context={
        'order_id':order_id,
        'payment':payment
    }
    return render(request,'checkout.html',context)


def placeorder(request):
    if request.method=='POST':
        uid=request.session.get('_auth_user_id')
        user=User.objects.get(id=uid)
        cart=request.session.get('cart')
        firstname=request.POST.get('first')
        lastname=request.POST.get('last')
        country=request.POST.get('country')
        address=request.POST.get('address')
        city=request.POST.get('city')
        state=request.POST.get('state')
        postcode=request.POST.get('postcode')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        amount=request.POST.get('amount')
        order_id=request.POST.get('orderid')
        payment=request.POST.get('payment')
        context={
            'orderid':order_id
        }

        order=Order(
            user=user,
            firstname=firstname,
            lastname=lastname,
            country=country,
            address=address,
            city=city,
            state=state,
            postcode=postcode,
            phone=phone,
            email=email,
            paymentid=order_id,
            amount=amount,
            paid='True'


        )
        order.save()
        for i in cart:
            a=(int(cart[i]['price']))
            b=cart[i]['quantity']

            total=a * b


            item = Orderitem(
                user=user,
                order=order,
                product=cart[i]['name'],
                image=cart[i]['image'],
                quantity=cart[i]['quantity'],
                price=cart[i]['price'],
                total=total
            )
            item.save()

        return render(request,'placeorder.html',context)

@csrf_exempt
def success(request):
    if request.method=='POST':
        a=request.POST
        orderid=""
        for key,val in a.items():
            if key=='razorpay_orderid':
                orderid=val
                break
        user=Order.objects.filter(paymentid=orderid)

    return render(request,'thankyou.html')


def yourorder(request):
    categories=Categories.objects.all()
    uid=request.session.get('_auth_user_id')
    user=User.objects.get(id=uid)
    order=Orderitem.objects.filter(user=user)
    context={
        'order':order,
        'cat':categories
    }
    return render(request,'yourorder.html',context)


def about(request):
    categories=Categories.objects.all()
    context= {
        'cat':categories
    }
    return render(request,'about.html',context)
@login_required
def review_page(request,id):
    product = Product.objects.get(id=id)
    if request.method=="GET":
        star_rating=request.GET.get('rate')
        reviews=request.GET.get('Your Review')
        user=request.user
        review(user=user,item=product,review_desp=reviews,ratings=star_rating).save()
        # reviews=review.objects.filter(item_id=product)
        # context = {
        #     'reviews':reviews
        # }
    return redirect('singleproduct')


def product_reviews(request,id):
    reviews=review.objects.filter(id=id)
    return render(request,'reviews.html',{'reviews':reviews})


def wishlist(request):
    return render(request,'wishlist.html')



def update(request):
    if request.method=='POST':
        username=request.POST.get('username')
        first_name=request.POST.get('first')
        last_name=request.POST.get('last')
        password=request.POST.get('pass')
        email=request.POST.get('email')
        id=request.user.id

        user=User.objects.get(id=id)
        user.username=username
        user.first_name=first_name
        user.last_name=last_name
        user.email=email

        if password != None and password !="":
            user.set_password(password)
        user.save()
        return redirect('home')

    return render(request,'update.html')