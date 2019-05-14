from django.urls import path

from . import views

urlpatterns=[
   path('',views.shop_items_view,name="shop_items_url"),
   path('item/',views.order,name="order_url"),
   path('notification/',views.view_notification,name="notification_url"),
   path('delete_notification/<int:notification_id>/',views.delete_notification,name="delete_notification_url"),
   path('view-item/<int:item_id>/',views.view_item,name="item_url"),
   path('view-cart/<int:buyer_id>/',views.view_cart,name="view_cart"),
   path('delete-item/<int:item_id>/',views.delete_from_cart,name="delete_from_cart"),
   path('payment-process/',views.process_payment,name="process_payment"),
   path('payment-done/',views.payment_done,name="payment_done"),
   path('payment-cancelled/',views.payment_cancelled,name="payment_cancelled"),
]