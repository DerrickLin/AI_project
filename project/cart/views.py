from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from quiz.models import product, order, CustomUser
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
import json
import random, re
# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products = list(cart.get_prods())
    # quantities = cart.get_quants
    item_amount = request.session.get('item_amount', [])
    All_products = dict(zip(cart_products, item_amount))
    totals = cart.cart_total(item_amount)
    # print(cart_products)

    return render(request, "cart_summary.html", {"All_products": All_products, "totals":totals, "item_amount":item_amount })


def cart_add(request):
    # get the cart
    cart = Cart(request)
    product_id = 0
    item_amount = []
    
    # test for post
    if request.POST.get('action') == 'post':
        # 取得商品名稱及對應數量
        product_list = request.POST.get('product_info')
        # product_qty= request.POST.get('product_qty')
        if product_list == "None":
            # 如果獲取到的product_info為"None"，返回一個適當的響應
            return JsonResponse({'0': '0'})
        
        #這邊要對dictionary修改
        product_list1 = eval(product_list)
        # print(product_list1)
        
        for product_amount in product_list1.values():
            item_amount.append(product_amount)
        
        request.session['item_amount'] = item_amount
        
        for products in product_list1.keys():
            if products == "noodle":
                product_id = 1
            elif products == "black_tea":
                product_id = 2
            elif products == "OOha":
                product_id = 3
            elif products == "hi_chew":
                product_id = 4
            elif products == "cookie":
                product_id = 5
             
            # look up product in DB
            product_info = get_object_or_404(product, id=product_id)
            # save to session
            cart.add(product=product_info)
            
            # get cart quantity
            cart_quantity = cart.__len__()
    
            # print(cart_quantity)
            # return response
            # response_data.append({'Product Name': product_info.pName})
            response = JsonResponse({'qty': cart_quantity})
            # response_data.append({'qty': product_total_quantity})
     
        # return JsonResponse(response_data, safe=False)
        return response
    


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
		# Get stuff
        product_id = int(request.POST.get('product_id'))
		# Call delete Function in Cart
        cart.delete(product=product_id)

        response = JsonResponse({'product':product_id})
		#return redirect('cart_summary')
        # messages.success(request, ("Item Deleted From Shopping Cart..."))
        return response


def cart_update(request):
    pass


def checkout(request):
    if request.method == "POST":
        random_ID = random.randint(1000000000, 9999999999)
        current_time = timezone.now()
        order_product = request.POST["oProduct"]
        order_customer_username = request.POST["oClient"] 
        order_total = int(request.POST["oCost"])
        order_quantities = sum(eval(request.POST["order_quantity"]))
        
        pattern = r"<product: (.*?)>"
        product_names = re.findall(pattern, order_product)
        order_customer, created = CustomUser.objects.get_or_create(username=order_customer_username)
        
        unit = order.objects.create(oId=random_ID,
                                      oDate=current_time,
                                      oProduct=product_names,
                                      oClient=order_customer,
                                      oCost=order_total,
                                      order_quantity=order_quantities)
        unit.save()
        
        print(random_ID, current_time, product_names,order_customer, order_total, order_quantities)
        return redirect("/check_finished/")
      