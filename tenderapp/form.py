from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Sale, Purchase, Management, Finance
from .import models
from django import forms
from django import forms
from django.forms import (formset_factory, modelformset_factory)
from django.core.validators import EmailValidator
from .models import (Purchase_Order_Model, Particulars)

from .models import (Invoice_Model, Invoice)

from django.core.exceptions import ValidationError

def validatepass(value):
    x=str(value)
    if len(x)>=8:
        return value
    else:
        return ValidationError("incorrect password")

gst_choices = [('0', 0),('5', 5), ('6', 6), ('14', 14), ('18', 18), ('28', 28)]
invoice_choices = [('Production Purchase', 'Production Purchase'), ('Office/OH Purchase ', 'Office/OH Purchase'), ('Asset Purchase', 'Asset Purchase'), ('Other', 'Other')]

x = forms.TextInput(attrs={'class': "input--style-5"})
y = forms.NumberInput(attrs={'class': "input--style-5"})
z = forms.CheckboxInput(attrs={})
a = forms.FileInput(attrs={'class': "input--style-5"})
x1 = forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Password'})
x2 = forms.PasswordInput(attrs={'class': "form-control", 'placeholder': 'Confirm Password'})
x3 = forms.TextInput(attrs={'class': "form-control", 'placeholder': 'First Name'})
x4 = forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Last Name'})
x5 = forms.TextInput(attrs={'class': "form-control", 'placeholder': 'Username'})
x6 = forms.EmailInput(attrs={'class': "form-control", 'placeholder': 'Email'})

p = forms.TextInput(attrs={'class': "form-control round-form"})
q = forms.NumberInput(attrs={'class': "form-control round-form"})
r = forms.EmailInput(attrs={'class': "form-control round-form"})
s = forms.CheckboxInput(attrs={'class': "checkbox form-control", 'width': "20px"})
f = forms.FileInput(attrs={'class': "form-control round-form"})


class Update_Vendor_Form(forms.ModelForm):
    name = forms.CharField(required=True, widget=p)
    mobile = forms.IntegerField(required=True, widget=q)
    email = forms.EmailField(required=True, widget=r)
    address = forms.CharField(required=True, widget=p)
    is_gst = forms.BooleanField(widget=s, required=False)
    gstin = forms.CharField(required=False, widget=p)
    bank_name = forms.CharField(required=True, widget=p)
    account_no = forms.IntegerField(required=True, widget=q)
    ifsc = forms.CharField(required=True, widget=p)
    pan = forms.CharField(required=False, widget=p)
    is_pan = forms.BooleanField(widget=s, required=False)

    class Meta:
        model = models.Vendor_Model
        fields = ['name', 'mobile', 'email', 'address', 'is_gst', 'gstin', 'bank_name', 'account_no', 'ifsc', 'pan', 'is_pan', 'black_list']

class PropertyDetails(forms.ModelForm):
    name = forms.CharField(required=True, widget=x)
    type = forms.CharField(required=True, widget=x)
    address = forms.CharField(required=True, widget=x)
    status = forms.CharField(required=True, widget=x)

    class Meta:
        model = models.Property
        fields = ['status', 'type', 'name', 'address']


class SaleSignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=x5)
    password1 = forms.CharField(required=True, widget=x1,)
    password2 = forms.CharField(required=True, widget=x2)
    first_name = forms.CharField(required=True, widget=x3)
    last_name = forms.CharField(required=True, widget=x4)
    email = forms.EmailField(required=True, widget=x6)

    def clean_password1(self):
        data=self.cleaned_data.get('password1')
        if len(data)<8:
            return forms.ValidationError("pasword wrong")
        return data

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_sale = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        sale_manager = Sale.objects.create(user=user)
        sale_manager.save()
        return user


class FinanceSignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=x5)
    password1 = forms.CharField(required=True, widget=x1)
    password2 = forms.CharField(required=True, widget=x2)
    first_name = forms.CharField(required=True, widget=x3)
    last_name = forms.CharField(required=True, widget=x4)
    email = forms.EmailField(required=True, widget=x6)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_finance = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        agent = Finance.objects.create(user=user)
        agent.save()
        return user


class ManagementSignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=x5)
    password1 = forms.CharField(required=True, widget=x1)
    password2 = forms.CharField(required=True, widget=x2)
    first_name = forms.CharField(required=True, widget=x3)
    last_name = forms.CharField(required=True, widget=x4)
    email = forms.EmailField(required=True, widget=x6)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_management = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        agent = Management.objects.create(user=user)
        agent.save()
        return user


class PurchaseSignUpForm(UserCreationForm):
    username = forms.CharField(required=True, widget=x5)
    password1 = forms.CharField(required=True, widget=x1)
    password2 = forms.CharField(required=True, widget=x2)
    first_name = forms.CharField(required=True, widget=x3)
    last_name = forms.CharField(required=True, widget=x4)
    email = forms.EmailField(required=True, widget=x6)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_purchase = True
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.save()
        agent = Purchase.objects.create(user=user)
        agent.save()
        return user


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class Vendor_Form(forms.ModelForm):
    # max_value = 9999999999, min_value = 1000000000
    name = forms.CharField(required=True, widget=p)
    mobile = forms.IntegerField(required=True, widget=q),
    email = forms.EmailField(required=True, widget=r)
    address = forms.CharField(required=True, widget=p)
    is_gst = forms.BooleanField(widget=s,  required=False)
    gstin = forms.CharField(required=False, widget=p)
    bank_name = forms.CharField(required=True, widget=p)
    account_no = forms.IntegerField(required=True, widget=q)
    ifsc = forms.CharField(required=True, widget=p)
    pan = forms.CharField(required=False, widget=p)
    is_pan = forms.BooleanField(widget=s,  required=False)
    black_list = forms.BooleanField(widget=s,  required=False)

    class Meta:
        model = models.Vendor_Model
        fields = ['name', 'mobile', 'email', 'address', 'is_gst', 'gstin', 'bank_name', 'account_no', 'ifsc', 'pan', 'is_pan', 'black_list']


class Update_Vendor_Form(forms.ModelForm):
    name = forms.CharField(required=True, widget=p)
    mobile = forms.IntegerField(required=True, widget=q)
    email = forms.EmailField(required=True, widget=r)
    address = forms.CharField(required=True, widget=p)
    is_gst = forms.BooleanField(widget=s, required=False)
    gstin = forms.CharField(required=False, widget=p)
    bank_name = forms.CharField(required=True, widget=p)
    account_no = forms.IntegerField(required=True, widget=q)
    ifsc = forms.CharField(required=True, widget=p)
    pan = forms.CharField(required=False, widget=p)
    is_pan = forms.BooleanField(widget=s, required=False)

    class Meta:
        model = models.Vendor_Model
        fields = ['name', 'mobile', 'email', 'address', 'is_gst', 'gstin', 'bank_name', 'account_no', 'ifsc', 'pan', 'is_pan', 'black_list']


class PurchaseModelForm(forms.ModelForm):

    class Meta:
        model = Purchase_Order_Model
        fields = ('invoice_for','po_date','vendor','project','rml','sub_total','total_igst','amount','total_gst','total_sgst','total_cgst','attachment',)
        widgets = {
            'invoice_for': forms.Select(choices=invoice_choices,attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Invoice here',


            }),

            'vendor': forms.Select(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Choose Vendor'
            }),
            'project': forms.Select(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Choose Project No.'
            }),
            'rml': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter RML No here'
            }),
            'sub_total': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Sub Total here',
                'readonly':True
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Net Payable Amount here',
                'readonly': True
            }),
            'total_gst': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Total GST here',
                'readonly': True
            }),
            'total_sgst': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Total SGST here',
                'readonly': True
            }),
            'total_cgst': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Total CGST here',
                'readonly': True
            }),
            'attachment': forms.FileInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Choose File'
            }),
            'po_date': forms.DateInput( attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Purchase Order Date here',
                'type': 'date'

            }),

            'total_igst': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Total',
                'readonly': True
            }),
        }


ParticularsFormset = modelformset_factory(
    Particulars,
    fields=('particular','tax_value','gst','sgst','cgst','total','igst'),
    extra=1,
    widgets={'particular': forms.TextInput(attrs={
        'class': 'form-control round-form',
        'placeholder': 'Enter Particular here'
    }),
        'tax_value': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter Tax Value here',
        }),
        'gst': forms.Select(choices=gst_choices, attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter GST Rate here'
        }),
        'sgst': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter SGST Rate here'
        }),
        'cgst': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter CGST Rate here'
        }),
        'igst': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter IGST Rate here'
        }),
        'total': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Total',
            'readonly': True
        }),
    }
)




class InvoiceModelForm(forms.ModelForm):

    class Meta:
        model = Invoice_Model
        fields = ('invoice_for','total_gst','vendor','project','due_date','rml','invoice_date','po_no','total_amount','total_igst','grand_total','terms','total_sgst','total_cgst','remark',)
        widgets = {
            'invoice_for': forms.Select(choices=invoice_choices,attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Invoice here',
            }),
            'vendor': forms.Select(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Choose Vendor here'
            }),
            'project': forms.Select(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter project no. here'
            }),
            'rml': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter RML No. here'
            }),
            'po_no': forms.Select(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Choose Purchase Order Id here'
            }),

            'total_amount': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': '  Total Amount ',
                'readonly': True
            }),
            'total_igst': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': ' Total IGST ',
                'readonly': True
            }),
            'total_sgst': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': ' Total SGST ',
                'readonly': True
            }),
            'total_cgst': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': ' Total CGST ',
                'readonly': True
            }),
            'remark': forms.TextInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Your Remarks'
            }),
            'terms': forms.TextInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Terms and Condition'
            }),
            'total_gst': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter GST here',
                'readonly': True

            }),
            # 'packing': forms.NumberInput(attrs={
            #     'class': 'form-control round-form',
            #     'placeholder': 'Enter Packing Rate here',
            # }),
            # 'insurance': forms.NumberInput(attrs={
            #     'class': 'form-control round-form',
            #     'placeholder': 'Enter Insurance here',
            # }),
            'grand_total': forms.NumberInput(attrs={
                'class': 'form-control round-form',
                'placeholder': 'Grand Total',
                'readonly': True
            }),
            'due_date': forms.DateTimeInput(format= '%d-%m-%Y',attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Due Date here',
                'type':'date'

            }),
            'invoice_date': forms.DateTimeInput(format='%d-%m-%Y', attrs={
                'class': 'form-control round-form',
                'placeholder': 'Enter Invoice Date here',
                'type': 'date'

            }),

        }


InvoiceFormset = modelformset_factory(
    Invoice,
    fields=('description','amount','igst','sgst','cgst','quantity','total','gst'),
    extra=1,
    widgets={'description': forms.TextInput(attrs={
        'class': 'form-control round-form',
        'placeholder': 'Enter Description here'
    }),
        'amount': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter Amount here',
        }),
        'igst': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter IGST Rate here'
        }),
        'sgst': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter SGST Rate here'
        }),
        'cgst': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter CGST Rate here'
        }),
        'quantity': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Enter Quantity here'
        }),
        'gst': forms.Select(choices=gst_choices,attrs={
            'class': 'form-control round-form',
            'placeholder': 'Choose GST',
        }),
        'total': forms.NumberInput(attrs={
            'class': 'form-control round-form',
            'placeholder': 'Total',
            'readonly': True
        }),
    }
)


class Budget_Form(forms.ModelForm):
    rml_no = forms.IntegerField(required=True, widget=q)
    project_no = forms.IntegerField(required=True, widget=q)
    allocate = forms.IntegerField(required=True, widget=q)
    available = forms.IntegerField(required=True, widget=q)
    utilized = forms.IntegerField(required=True, widget=q)
    attachment = forms.FileField(required=True, widget=f)

    class Meta:
        model = models.Vendor_Model
        fields = ['rml_no', 'project_no', 'allocate', 'available', 'utilized', 'attachment']

