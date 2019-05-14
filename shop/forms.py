import secrets
from django import forms

from .models import Order,Item,Category,Cart


class CheckoutForm(forms.ModelForm):

	def __init__(self,*args,**kwargs):
		super().__init__(*args,**kwargs)
		self.fields['client_id'].widget.attrs['placeholder']="Key in an id"
		# self.fields['client_id'].widget.attrs['readonly']=True
		# self.fields['client_id'].initial=secrets.token_hex(8)

	class Meta:
		model=Order
		# fields='__all__'
		fields=('client_id','email','city','address')


class SearchForm(forms.ModelForm):
	category=forms.ModelChoiceField(queryset=Category.objects.all(),empty_label='Category',label='')
	# def __init__(self,*args,**kwargs):
	# 	super().__init__(*args,**kwargs)
	# 	self.fields['category'].widget.attrs['placeholder']="Category"

	class Meta:
		model=Item
		fields=('category',)


class QuantityForm(forms.ModelForm):
	class Meta:
		model=Cart
		fields=('quantity',)