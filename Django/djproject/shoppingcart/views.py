from django.shortcuts import render
from .models import Product
from .models import Cateogary
from .models import User
from .models import Address
from .models import Profile
from .models import SalesOrder
from .models import SaleOrderItem
from .session_product import SessionProduct
import datetime

from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_protect

# Create your views here.
from django.http import HttpResponse


def history(request):
    '''returns history of a user purchase'''
    users_dict = request.session["users"]     # fetch user from session who is logged in
    for id in users_dict:
        user_id = id                          #id of user
    shopping_history = []                     # contain dictionary of all items with relavant information

    saleorderlist = SaleOrderItem.objects.all()    #fetch all items purchased by a user
    # print(saleorderlist)
    # print("outside for")
    # print(user_id)
    for saleorder in saleorderlist:
        history = {}                            #contain single item
        # print("inside for")
        # print(saleorder.order_id.user_id)
        if str(saleorder.order_id.user_id) == str(user_id):
            # print("inside if")
            history.update({'product':saleorder.product_id.name,'date':saleorder.order_id.date,'quantity':saleorder.quantity,
                            'price':saleorder.price,'total':saleorder.quantity*saleorder.price})
            # print(history)
            shopping_history.append(history)
    # print(shopping_history)

    return render(request, "history.html",{'status':'logout',
                                                 'history':True,'history':shopping_history})

def userinsession(request):
    '''put user in session'''
    #print("start")
    if request.POST.get('username'):
        #print("middle")
        username = request.POST["username"]
        user = User.objects.get(user_name=username)
        user_id = user.pk
        if not request.session.has_key("users"):
            users_dict = {}
            users_dict.update({user_id: username})
            request.session["users"] = users_dict

        else:
            users_dict = request.session["users"]
            users_dict.update({user_id: username})
            request.session["users"] = users_dict

def contact_us(request):
    '''return contact page'''
    #print("incontact")
    if request.session.has_key("users"):     #if user is in session means logged in then login change to logout
        return render(request, "contact.html",{'status':'logout','history':True})
    return render(request,"contact.html",{'status':'Login'})

def new_account(request):
    '''return create account page'''
    #print("newaccount")
    return render(request,"newaccount.html")   #create new account

@csrf_protect
def index(request):
    '''returns home page'''
    if not request.session.has_key("cart_products"):           #create key in session if not created here error in cart and checkout if no cart_product key
        dict_cart_product = {}
        request.session["cart_products"] = dict_cart_product
    try:
        if request.POST.get('fname'):                  #fetch information from create new account
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            username = request.POST["username"]
            password_ = request.POST["password"]
            companyname = request.POST["company"]
            phonenumber = request.POST["phone"]
            email_ = request.POST["email"]
            try:                                    #if user already exists
                user = User.objects.get(user_name=username)
                return render(request,"newaccount.html",{'validation':'The username already exists. Please use a different username'})
            except:
                user = User(user_name=username, password=password_, first_name=fname, last_name=lname,
                            company_name=companyname, phone_number=phonenumber, email=email_, )
                user.save()
    except:
        return render(request, "newaccount.html")

    products = Product.objects.all()     #all products available to be displayed on home
    categories = Cateogary.objects.all()
    # if request.session.has_key("users"):
    #     del request.session['users']
    #     request.session.modified = True
    # request.session.clear()

    userinsession(request)
    if request.session.has_key("users"):
        return render(request, "category.html", {'products': products, 'categories': categories,'status':'logout',
                                                 'history':True})
    return render(request, "category.html",{'products':products,'categories':categories,'status':'login'})
   # return HttpResponse("Hello, world. You're at the polls index.")

def login(request):
    '''return login page'''
    message = "invalid credentials "
    #print(allusers)
    if request.session.has_key("users"):      #user is already logged in and button appear to be logout
        del request.session['users']            #logs user out
        request.session.modified = True
        return index(request)
    if request.POST.get('username'):            #log in from login page
        username = request.POST["username"]
        password_ = request.POST["password"]
        try:                                        #validations
            user = User.objects.get(user_name=username)
            user_id = user.pk
            #print(user_id,user.user_name,user.password)
            #print("enter password")
            if user.password != password_:              #password validation
                print("in password")
                return render(request, "login.html", {"message": message})

            if not request.session.has_key("users"):        #user in session
                users_dict = {}
                users_dict.update({user_id: username})
                request.session["users"] = users_dict

            else:
                users_dict = request.session["users"]
                users_dict.update({user_id: username})
                request.session["users"] = users_dict
            #print("before index")
            return index(request)

        except:
            #print("in except")
            return render(request,"login.html",{"message":message})
    return render(request,"login.html")



def product_details(request):
    '''returns product detail page of selected product'''
    if request.GET.get('id'):   #get id from home
        product_id = request.GET.get('id')
        productdetail = Product.objects.get(id=product_id)
    else:
        productdetail = Product.objects.get(id=5)   #default
    if request.session.has_key("users"):
        return render(request, "product-detail.html", {'product': productdetail,'status':'logout','history':True})
    return render(request, "product-detail.html", {'product': productdetail,'status':'login'})

@csrf_protect
def cart(request):
    if not request.session.has_key("cart_products"):
        request.session["cart_products"] = {}
    '''return shopping cart'''
    if request.POST.get('id'):          #id from product detail page
        # print("enter cart for product ")
        product_id = request.POST["id"]
        product_quantity = int(request.POST["quantity"])
        if product_quantity > 0:
            if not request.session.has_key("cart_products"):     #adds product to cart if quantity from detail page is not zero
                session_product = SessionProduct().get_session_product(product_id,product_quantity)
                dict_cart_product = {}
                dict_cart_product.update({product_id:session_product})      #put each product in session
                request.session["cart_products"] = dict_cart_product
            else:
                dict_cart_product = request.session["cart_products"]
                # print("here we go")
                # print(dict_cart_product)
                if product_id in dict_cart_product:
                    dict_cart_product[product_id].quantity += product_quantity
                    request.session["cart_products"] = dict_cart_product
                else:
                    session_product = SessionProduct().get_session_product(product_id,product_quantity)
                    dict_cart_product = request.session["cart_products"]
                    dict_cart_product.update({product_id: session_product})
                    request.session["cart_products"] = dict_cart_product
    # print(request.POST.get('id1'))
    if request.POST.get('id1'):         #hidden id for update
        lst = []                        #condition if product or products are updated
        #print("enter cart for update ")
        dict_cart_product = request.session["cart_products"]
        for cart_product in dict_cart_product.values():
            cart_product.quantity = int(request.POST['sst'+str(cart_product.id)])  #differntiate each input
            if cart_product.quantity == 0:          #if updated to zerod
                lst.append(cart_product.id)
        print(lst)
        for productid in lst:
            dict_cart_product.pop(productid)

        request.session["cart_products"] = dict_cart_product


    dict_cart_product = request.session["cart_products"]
    sub_total = 0
    flat_rate = 300
    try:
        for cart_product in dict_cart_product.values():
            sub_total += cart_product.quantity * cart_product.sales_price
    except:
        sub_total =0            #if session is empty
    if request.session.has_key("users"):
        return render(request, "cart.html",
                      {'cart_product_dict': dict_cart_product, 'sub_total': sub_total, 'flat_rate': flat_rate,'status':'logout','history':True})
    return render(request,"cart.html",
                  {'cart_product_dict':dict_cart_product,'sub_total':sub_total,'flat_rate':flat_rate,'status':'login'})

@csrf_protect
def checkout(request):
    '''returns checkout pade'''
    if not request.session.has_key("cart_products"):
        request.session["cart_products"] = {}
    dict_cart_product = request.session["cart_products"]
    sub_total = 0
    flat_rate = 300
    try:
        for cart_product in dict_cart_product.values():
            sub_total += cart_product.quantity * cart_product.sales_price

    except:
        sub_total=0

    if request.POST.get('name'):                #if user already have an account and wants to log in
        lusername = request.POST["name"]
        lpassword = request.POST["password"]

        try:
            user = User.objects.get(user_name=lusername)            #validations
            user_id = user.pk
            if user.password != lpassword:
                print("in password")
                return render(request, "checkout.html", {'cart_product_dict': dict_cart_product, 'sub_total': sub_total,
                                                         'flat_rate': flat_rate, 'status': 'login',"message": 'invalid credintials' })

            users_dict = {}
            users_dict.update({user_id: lusername})
            request.session["users"] = users_dict

        except:
            return render(request, "checkout.html", {'cart_product_dict': dict_cart_product, 'sub_total': sub_total,
                                                     'flat_rate': flat_rate, 'status': 'login',
                                                     "message": 'invalid credintials'}) #if invalid
        return render(request, "checkout.html",
                      {'cart_product_dict': dict_cart_product, 'sub_total': sub_total, 'flat_rate': flat_rate,
                       'status': 'logout', 'none': 'none','history':True })   #if valid

    if request.POST.get('add1'):                    #getting address
        country_ = request.POST["country"]
        address_line1_ = request.POST["add1"]
        address_line2_ = request.POST["add2"]
        city_ = request.POST["city"]
        district_ = request.POST["district"]
        postcode = request.POST["zip"]
        billingaddress = Address(country=country_, address_line1=address_line1_,
                                 address_line2=address_line2_, city=city_, district=district_, post_code=postcode)
        billingaddress.save()

        if request.POST.get("shipadd1"):                #if ship address is different
            ship_country_ = request.POST["shipcountry"]
            ship_address_line1_ = request.POST["shipadd1"]
            ship_address_line2_ = request.POST["shipadd2"]
            ship_city_ = request.POST["shipcity"]
            ship_district_ = request.POST["shipdistrict"]
            ship_postcode = request.POST["shipzip"]
            shippingaddress = Address(country=ship_country_, address_line1=ship_address_line1_,
                                      address_line2=ship_address_line2_, city=ship_city_, district=ship_district_,
                                      post_code=ship_postcode)
            shippingaddress.save()
        else:
            shippingaddress = billingaddress

        address_dict = {}                               #address in session so that can get at confirmation easily
        address_dict.update({'billingaddress': billingaddress})
        address_dict.update({'shippingaddress': shippingaddress})
        request.session["address"] = address_dict

        if not request.session.has_key("users"):            #if user is not log in neither has account then new account created
            fname = request.POST["fname"]
            lname = request.POST["lname"]
            username = request.POST["newusername"]
            password_ = request.POST["newpassword"]
            companyname = request.POST["company"]
            phonenumber = request.POST["number"]
            email_ = request.POST["compemailany"]
            try:
                user = User.objects.get(user_name=username)                 #if user already exists
                return render(request, "checkout.html", {'cart_product_dict': dict_cart_product, 'sub_total': sub_total,
                                                         'flat_rate': flat_rate, 'status': 'login',
                                                         'validation': 'The username already exists. Please use a different username' })

            except:
                pass
            user = User(user_name=username, password=password_, first_name=fname, last_name=lname,
                        company_name=companyname, phone_number=phonenumber, email=email_, )
            user.save()
            user_id = user.pk                   #pk is primary key that is id
            users_dict = {}
            users_dict.update({user_id: username})
            request.session["users"] = users_dict

            profile = Profile(user_id=user, billing_address=billingaddress, shipping_address=shippingaddress)
            profile.save()
            return render(request, "checkout.html",
                      {'cart_product_dict': dict_cart_product, 'sub_total': sub_total, 'flat_rate': flat_rate,
                       'status': 'logout', 'profile':profile,'bool':'True','boolifnewaccount': 'True','history':True})

        else:
            users_dict = request.session["users"]
            for user in users_dict:
                user_id = user
            user = User.objects.get(id=user_id)
            profile = Profile(user_id=user, billing_address=billingaddress, shipping_address=shippingaddress)
            profile.save()

            return render(request, "checkout.html",
                      {'cart_product_dict': dict_cart_product, 'sub_total': sub_total, 'flat_rate': flat_rate,
                       'status': 'logout','profile':profile,'bool': 'True','history':True})  #if logded in then no user info required
                                                                                    #after save

    if request.session.has_key("users"):                    #before save info
        return render(request, "checkout.html",
                      {'cart_product_dict': dict_cart_product, 'sub_total': sub_total, 'flat_rate': flat_rate,
                       'status':'logout','none':'none','history':True})
    return render(request, "checkout.html",{'cart_product_dict':dict_cart_product,'sub_total':sub_total,
                                            'flat_rate':flat_rate,'status':'login'})   #this will return from cart

@csrf_protect
def get_info(request):      #confirmation
    '''return confirmation page'''
    dict_cart_product = request.session["cart_products"]
    sub_total = 0
    flat_rate = 300
    for cart_product in dict_cart_product.values():
        sub_total += cart_product.quantity * cart_product.sales_price

    try:            #if in session as in user is logged in and address is saved
        address_dict = request.session["address"]
        users_dict = request.session['users']
        if request.session.has_key("cart_products"):

            for user in users_dict:
                session_user_id = user          #  user id
            #session_user = User.objects.get(id=id)
            #order.user_id =  session_user_id
            current_date = datetime.datetime.now()                  #date
            order = SalesOrder(user_id=session_user_id,date=current_date)       #order saved
            order.save()
            order_id = order.pk
            for products in dict_cart_product.values():         #each item in order to be saved as sale order item
                id_product = products.id
                product = Product.objects.get(id=id_product)
                neworder = SalesOrder.objects.get(id=order_id)
                quantity_product = products.quantity
                price_product = products.sales_price
                item = SaleOrderItem(product_id=product,order_id=neworder,quantity=quantity_product,price=price_product)
                item.save()

            if request.session.has_key("users"):            #user is logged in
                del request.session['cart_products']        #session products to be deleted
                request.session.modified = True
                if not request.session.has_key("cart_products"):        #new session created just to avoid error
                    # dict_cart_product = {}
                    request.session["cart_products"] = {}

                return render(request, "confirmation.html", {'cart_product_dict': dict_cart_product, 'sub_total': sub_total,
                                                             'flat_rate': flat_rate, 'billingaddress': address_dict['billingaddress'],
                                                             'shippingaddress': address_dict['shippingaddress'],'status':'logout','history':True,'order':order_id})
        return render(request, "checkout.html", {'cart_product_dict': dict_cart_product, 'sub_total': sub_total,
                                                     'flat_rate': flat_rate, 'status': 'login' })

    except:
        if not request.session.has_key("users"):
            return render(request, "checkout.html", {'cart_product_dict': dict_cart_product, 'sub_total': 0,
                                                 'flat_rate': 300, 'status': 'login' })
        else:
            return render(request, "checkout.html",
                          {'cart_product_dict': dict_cart_product, 'sub_total': sub_total, 'flat_rate': flat_rate,
                           'status': 'logout', 'none': 'none', 'history': True})
    # # return render(request, "confirmation.html",{'cart_product_dict':dict_cart_product,'sub_total':sub_total,
    #                                             'flat_rate':flat_rate,'billingaddress':address_dict['billingaddress'],
    #                                             'shippingaddress':address_dict['shippingaddress'],'status':'login'})
