import json
import traceback
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from store.models import *


def index(request):
    if request.method == "GET":
        sql = Product.objects.all().filter(section=None).order_by('-date')[:8]
        sql2 = Product.objects.all().filter(category=None).order_by('-date')[:8]
        for i in sql2:
            print(i)
        if 'cart' not in request.session.keys():
            request.session['cart'] = {}
        content = {'sql1': sql, 'wear': sql2, }
        templates = 'index.html'
        return render(request, templates, content)


def contact(request):
    if request.method == "POST":
        con = Contact()
        context = {'sucessmessage': "Thanks for contacting us hope to get back to you soon", }
        con.subject = request.POST.get('subject')
        con.Email = request.POST.get('Email')
        con.message = request.POST.get('message')
        con.save()
        subject = [con.subject, con.Email]
        message = con.message
        from_mail = settings.EMAIL_HOST_USER
        to_list = [from_mail]
        send_mail(subject=subject, message=message, from_email=con.Email, recipient_list=to_list, fail_silently=False)
        return redirect(request.META.get('HTTP_REFERER'), context)


def profile(request):
    if request.method == 'GET':
        context = locals()
        templates = 'profile.html'
        return render(request, templates, context)
        # elif request.method == 'POST':
        #     edit = Register.objects.get(id=request.session['userid'])
        #     edit.Fullname = request.POST.get('Fullname')
        #     edit.Email = request.POST.get('Email')
        #     edit.Phone = request.POST.get('Phone')
        #     edit.Username = request.POST.get('Username')
        #     edit.save()
        #     sql1 = Register.objects.get(id=request.session['userid'])
        #     context = {'prof': sql1, 'msg': "Profile updated successfully", }
        #     templates = 'profile.html'
        #     return render(request, templates, context)


def logout(request):
    if request.method == 'GET':
        request.session.clear()
        return redirect('/')


def shop(request, url_name):
    if request.method == 'GET':
        if 'cart' not in request.session.keys():
            request.session['cart'] = {}
        print(request.session['cart'])
        if url_name == "provisions":
            cat = "Provisions"
        elif url_name == "snacks":
            cat = "Snacks"
        elif url_name == "raw_food":
            cat = "Raw Food"
        elif url_name == "cooked_food":
            cat = "Cooked Food"
        elif url_name == "soup_ingredient":
            cat = "Soup ingredient"
        sql = Product.objects.filter(category=cat)
        if sql:
            context = {'sql1': sql, }
            template = url_name + '.html'
            return render(request, template, context)
        else:
            context = {'msg': "No stock available", }
            template = url_name + '.html'
            return render(request, template, context)


def wear(request, url_name):
    if request.method == 'GET':
        if 'cart' not in request.session.keys():
            request.session['cart'] = {}
        print(request.session['cart'])
        if url_name == "Men":
            cate = "Men"
        elif url_name == "Women":
            cate = "Women"
        elif url_name == "Children":
            cate = "Children"
        sql = Product.objects.filter(section=cate)
        if sql:
            context = {'sql1': sql, }
            template = url_name + '.html'
            return render(request, template, context)
        else:
            context = {'msg': "No stock available", }
            template = url_name + '.html'
            return render(request, template, context)


# def school(request, url_name):
#     if request.method == 'GET':
#         if 'cart' not in request.session.keys():
#             request.session['cart'] = {}
#         print(request.session['cart'])
#         if url_name == "Books":
#             cat = "Books"
#         elif url_name == "Bag":
#             cat = "Bag"
#         elif url_name == "Shoes":
#             cat = "Shoes"
#         sql = School.objects.filter(category=cat)
#         if sql:
#             context = {'sql1': sql, }
#             template = url_name + '.html'
#             return render(request, template, context)
#         else:
#             context = {'msg': "No stock available", }
#             template = url_name + '.html'
#             return render(request, template, context)
#
#
# def equip(request, url_name):
#     if request.method == 'GET':
#         if 'cart' not in request.session.keys():
#             request.session['cart'] = {}
#         print(request.session['cart'])
#         if url_name == "plates":
#             cat = "plates"
#         elif url_name == "plates":
#             cat = "plates"
#         sql = Equip.objects.filter(category=cat)
#         if sql:
#             context = {'sql1': sql, }
#             template = url_name + '.html'
#             return render(request, template, context)
#         else:
#             context = {'msg': "No stock available", }
#             template = url_name + '.html'
#             return render(request, template, context)


def cart(request, url_name):
    assert isinstance(request, HttpRequest)
    if request.method == "POST":
        if url_name == 'clear':
            del request.session['cart']
            # del request.session['total']
            response = {"response": "Success",
                        "details": "Cart cleared"}
            return JsonResponse(response, safe=False)
        elif url_name == 'remove':
            print('Im here')
            form = json.loads(request.body.decode(encoding='UTF-8'))
            itemid = form['id']
            cart_items = dict(request.session['cart'])
            del cart_items[itemid]
            total = 0
            for order_detail in cart_items.keys():
                total += int(cart_items[order_detail]['Total'])
            request.session['total'] = total
            request.session['cart'] = cart_items
            response = {"response": "Success",
                        "details": "Item Removed"}
            return JsonResponse(response, safe=False)
        elif url_name == 'add':
            print('hey')
            form = json.loads(request.body.decode(encoding='UTF-8'))
            if form:
                # category = form['category']
                quantity = int(form['quantity'])

                # if category == 'provisions':
                try:
                    item = Product.objects.get(id=form['id'])
                except:
                    item = None

                if item:
                    if 'cart' not in request.session.keys():
                        request.session['cart'] = {}
                    cart_items = dict(request.session['cart'])
                    data = {
                        str(item.id): {
                            'Name': item.product_name,
                            'Quantity': quantity,
                            'Total': item.price * quantity
                        }
                    }
                    cart_items.update(data)
                    total = 0
                    for order_detail in cart_items.keys():
                        total += int(cart_items[order_detail]['Total'])
                    request.session['total'] = total
                    request.session['cart'] = cart_items
                    response = {"response": "Success",
                                "details": "Added to cart"}
                    return JsonResponse(response, safe=False)
                else:
                    response = {"response": "Error",
                                "details": "Item not found"}
                    return JsonResponse(response, safe=False)
            else:
                response = {"response": "Error",
                            "details": "No Form"}
                return JsonResponse(response, safe=False)


def checkout(request):
    if request.method == "GET":
        request.session['grandtotal'] = int(request.session['total']) + 200
        template = 'checkout.html'
        return render(request, template)
    elif request.method == "POST":
        order = Order()
        order.Name = request.POST.get('Name')
        order.Email = request.POST.get('Email')
        order.Phone = request.POST.get('Phone')
        order.address = request.POST.get('address')
        order.loc = request.POST.get('loc')
        order.sumtotal = int(request.session['grandtotal'])
        order.save()
        cart_items = request.session['cart']
        for key, value in cart_items.items():
            product = Product.objects.get(id=key)
            order_detail = OrderingDetails()
            order_detail.order = order
            order_detail.item = product
            order_detail.qty = int(value['Quantity'])
            order_detail.total = int(value['Total'])
            order_detail.save()
        del request.session['cart']
        del request.session['total']
        del request.session['grandtotal']
        return redirect('/')


def adminpage(request):
    if request.method == 'GET':
        if 'username' in request.session.keys():
            prod = Product.objects.all().count()
            comm = Contact.objects.all().count()
            ord = Order.objects.all().count()
            context = {'stats': prod, 'coment': comm, 'orde': ord}
            template = 'adminpage.html'
            return render(request, template, context)
        else:
            return redirect('/Adminlog/')


def show_order(request):
    if request.method == 'GET':
        holder = []
        for order in Order.objects.all():
            details = OrderingDetails.objects.filter(order=order)
            holder.append((order, details))
        context = {'orders': holder}
        template = 'show_order.html'
        return render(request, template, context)
    elif request.method == 'POST':
        form = json.loads(request.body.decode(encoding='UTF-8'))
        if form:
            try:
                order = Order.objects.get(id=form['id'])
            except:
                order = None

            if order:
                print(form['confirm'])
                order.confirm = bool(form['confirm'])
                order.save()
                response = {"response": "Success",
                            "details": "Order Confirmed"}
                return JsonResponse(response, safe=False)
            else:
                response = {"response": "Error",
                            "details": "Order not found"}
                return JsonResponse(response, safe=False)
        else:
            response = {"response": "Error",
                        "details": "No Form"}
            return JsonResponse(response, safe=False)


def show_wear(request):
    if request.method == 'GET':
        holder = []
        for order in Order.objects.all():
            details = OrderingDetails.objects.filter(order=order)
            holder.append((order, details))
        context = {'orders': holder}
        template = 'show_wear.html'
        return render(request, template, context)


def add_product(request):
    if request.method == 'GET':
        context = locals()
        template = 'add_product.html'
        return render(request, template)
    elif request.method == 'POST' and request.FILES['image']:
        if request.POST.get('category') == "":
            product = Product()
            product.price = request.POST.get('price')
            product.product_name = request.POST.get('product_name')
            product.section = request.POST.get('section')
            product.supplier = request.POST.get('supplier')
            product.image = request.FILES['image']
            product.save()
        elif request.POST.get('category') == request.POST.get('category'):
            product = Product()
            product.price = request.POST.get('price')
            product.product_name = request.POST.get('product_name')
            product.category = request.POST.get('category')
            product.supplier = request.POST.get('supplier')
            product.image = request.FILES['image']
            product.save()
    template = 'add_product.html'
    context = {'msg': "New Product Added Successfully", }
    return render(request, template, context)


def comment(request):
    if request.method == 'GET':
        com = Contact.objects.all()
        context = {'comment': com, }
        template = 'comment.html'
        return render(request, template, context)


def Adminreg(request):
    if request.method == 'GET':
        context = locals()
        templates = "Adminreg.html"
        return render(request, templates, context)
    elif request.method == 'POST':
        admin = adminreg()
        admin.Username = request.POST.get('Username')
        admin.Password = request.POST.get('Password')
        admin.save()
        context = {'successmsg': "Registration successfull Continue to login", 'user': request.POST.get('Username'), }
        templates = 'Adminreg.html'
        return render(request, templates, context)


def Adminlog(request):
    if request.method == 'GET':
        context = locals()
        templates = 'Adminlog.html'
        return render(request, templates, context)
    elif request.method == 'POST':
        try:
            user = request.POST.get('Username')
            sql = adminreg.objects.get(Username=user)
        except:
            print(traceback.print_exc())
            sql = None
        user = request.POST.get('Username')
        if sql:
            if sql.Password == createHash(request.POST.get('Password')):
                context = {'name': sql.Username, }
                templates = 'adminpage.html'
                request.session['userid'] = sql.id
                request.session['username'] = sql.Username
                return render(request, templates, context)
        else:
            print('am here')
            # Edward
            messages.error(request, 'Sorry! invalid password')
            return redirect('/Adminlog/')


def Adminlogout(request):
    if request.method == 'GET':
        del request.session['userid']
        del request.session['username']
        return redirect('/Adminlog/')
