import random
from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal


class Category(models.Model):
	name=models.CharField(max_length=30)

	def __str__(self):
		return self.name

class Item(models.Model):
	name=models.CharField(max_length=15)
	category=models.ForeignKey(Category,on_delete=models.SET_NULL,null=True)
	item_image=models.ImageField(upload_to='items_images',null=True)
	description=models.CharField(max_length=200)
	reviews=models.IntegerField(default=0)
	sales=models.IntegerField(default=0)
	available=models.IntegerField(default=0)
	price=models.DecimalField(max_digits=6,decimal_places=2)

	class Meta:
		verbose_name_plural="Items"

	def __str__(self):
		return self.name


	@property
	def prev_price(self):
		prev_price=self.price*Decimal(1.5)
		return Decimal(prev_price).quantize(Decimal('.99'),rounding="ROUND_UP")


	def get_absolute_url(self):
		pass


class Order(models.Model):
	client_id=models.CharField(max_length=8,null=False,blank=False)
	email=models.EmailField(max_length=254,unique=True)
	city=models.CharField(max_length=30)
	address=models.IntegerField()

	def __str__(self):
		return str(self.client_id)

	# def validate_unique(self):
	# 	client_ids=Order.objects.all().client_id
	# 	if self.client_id in client_ids:
	# 		raise ValidationError("Key in another id.That one already exists.")
	# 	super().validate_unique()


	class Meta:
		unique_together=['client_id','email']
		# ordering='-client_id' it overrides the default model query order which is by id



class Cart(models.Model):
	buyer=models.ForeignKey(User,on_delete=models.CASCADE)
	item=models.ForeignKey(Item,on_delete=models.CASCADE)
	quantity=models.IntegerField(default=1)

	def __str__(self):
		return self.buyer.username

	def individual_cost(self,item_id,quantity):
		pass


	def save(self,*args,**kwargs):
		# do custom logic here eg(valudation,logging,call third party services)
		# run default save method
		super(Cart,self).save(*args,**kwargs)



class Notification(models.Model):
	notified=models.ForeignKey(User,on_delete=models.CASCADE)
	notification=models.TextField(max_length=100)
	notify_date=models.DateTimeField(auto_now_add=True)

	class meta:
		verbose_name_plural='notifications'


	def __str__(self):
		return f"Notification for {self.notified.username} stating { self.notification }"


