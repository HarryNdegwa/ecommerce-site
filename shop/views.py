import random
import secrets
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.urls import resolve
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,reverse,redirect
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt

from .models import Item,Order,Cart,Notification
from .forms import CheckoutForm,QuantityForm


# def login_(func):
# 	def wrapper(*args,**kwargs):
# 		if 'request' in args:
# 			req_pos=args.index('request')
# 			print(args)
# 			user=args[req_pos].user
# 			if user.is_authenticated():
# 				page=func(*args,**kwargs)
# 				return page
# 			return redirect('login')
# 	return wrapper

# @login_
def shop_items_view(request):
	items=Item.objects.all()
	return render(request,'shop/shop.html',{'items':items})

@login_required
def view_item(request,item_id):
	item=Item.objects.get(id=item_id)
	related_items=Item.objects.filter(category=item.category).exclude(id=item_id)
	if request.method=="POST":
		print(request.POST)
		form=QuantityForm(request.POST)
		if form.is_valid():
			quantity=form.cleaned_data.get('quantity',1)
			cart=Cart(buyer=request.user,item=item,quantity=quantity)
			cart.save()
			return redirect('shop_items_url')
	else:
		form=QuantityForm()
	return render(request,'shop/item.html',{'item':item,'form':form,'related_items':related_items})
@login_required
def view_cart(request,buyer_id):
	buyer_id=buyer_id
	request.session['buyer_id']=buyer_id
	buyer=User.objects.get(id=buyer_id)
	items=Cart.objects.filter(buyer=buyer)
	def total_cost():
		total_cost=0
		for item in items:
			cost=item.item.price*item.quantity
			total_cost+=cost
		request.session['total_cost']=total_cost
		print(total_cost)
		return total_cost
	return render(request,'shop/cart.html',{'items':items,'total_cost':total_cost})

@login_required
def delete_from_cart(request,item_id):
	item_to_delete=Cart.objects.get(id=item_id)
	item_to_delete.delete()
	return redirect('view_cart',buyer_id=request.session['buyer_id'])


@login_required
def order(request):
	if request.method=="POST":
		form=CheckoutForm(request.POST)
		# form=CheckoutForm(request.POST,initial={'client_id':secrets.token_hex(8)})
		if form.is_valid():
			order_id=form.cleaned_data.get('client_id')
			form.save()
			request.session['order_id']=order_id # 	caching
			cart_items=Cart.objects.filter(buyer=request.user)
			cart_items.delete()
			return redirect('process_payment')
	else:
		form=CheckoutForm()
	return render(request,'shop/checkout.html',{'form':form,'total_cost':request.session['total_cost']})

@login_required
def process_payment(request):
	order_id=request.session.get('order_id')
	order=Order.objects.get(client_id=order_id)
	host=request.get_host()

	paypal_dict={
		'business':settings.PAYPAL_RECEIVER_EMAIL,
		'amount':int(request.session['total_cost']/104),
		'invoice':str(order_id),
		'currency_code':'USD',
		'notify_url':'http://{}{}'.format(host,reverse('paypal-ipn')),
		'return_url':'http://{}{}'.format(host,reverse('payment_done')),
		'payment_cancelled':'http://{}{}'.format(host,reverse('payment_cancelled')),
	}
	form=PayPalPaymentsForm(initial=paypal_dict)
	return render(request,'shop/payment_process.html',{'order_id':order_id,'form':form})

@csrf_exempt
def payment_done(request):
	subject="Payment confirmation"
	message="You have successfully made a payment.Thanks for shopping with us!"
	sender=settings.DEFAULT_FROM_EMAIL
	recipient=Order.objects.get(client_id=request.session['order_id'])
	to=[recipient.email,]
	send_mail(subject,message,sender,to)
	Notification.objects.create(notified=request.user,notification=message)
	return render(request,'shop/payment_done.html')

@csrf_exempt
def payment_cancelled(request):
	return render(request,'shop/payment_cancelled.html')


def view_notification(request):
	notifications=User.objects.get(id=request.user.id).notification_set.order_by('-notify_date')
	return render(request,'shop/notification.html',{'notifications':notifications})


def delete_notification(request,notification_id):
	notification_to_delete=Notification.objects.get(id=notification_id)
	notification_to_delete.delete()
	return redirect('notification_url')




