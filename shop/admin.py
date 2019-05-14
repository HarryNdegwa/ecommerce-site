from django.contrib import admin

from .models import Item,Order,Category,Cart,Notification

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Notification)
