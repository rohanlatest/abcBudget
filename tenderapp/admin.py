from django.contrib import admin
from .models import Property, Purchase, Sale, Management, Finance, User, Vendor_Model
from .models import Particulars,Purchase_Order_Model,Invoice_Model,Invoice,Request_model,Payment_Model, Budget_model
admin.site.register(Particulars)
admin.site.register(Purchase_Order_Model)
admin.site.register(Invoice_Model)
admin.site.register(Invoice)
admin.site.register(Request_model)
admin.site.register(Payment_Model)
admin.site.register(Property)
admin.site.register(Purchase)
admin.site.register(Sale)
admin.site.register(Management)
admin.site.register(Finance)
admin.site.register(User)
admin.site.register(Vendor_Model)
admin.site.register(Budget_model)
