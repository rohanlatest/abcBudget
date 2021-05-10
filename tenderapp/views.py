from django.contrib.auth.decorators import login_required
from django.db.models import Count

from . import models
from .form import PropertyDetails, SaleSignUpForm, FinanceSignUpForm,Budget_Form,InvoiceModelForm, PurchaseModelForm,InvoiceFormset,ParticularsFormset,ManagementSignUpForm, PurchaseSignUpForm,Vendor_Form,Update_Vendor_Form
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages, auth
from django.views.generic import CreateView
import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Vendor_Model,Payment_Model,Request_model,Budget_model,Invoice_Model
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect,get_object_or_404
from django.views import generic
from .models import Purchase_Order_Model, Particulars, Invoice


def property1(request):
    if request.method == 'POST':
        postForm = PropertyDetails(request.POST)

        if postForm.is_valid():
            post_form = postForm.save(commit=False)
            post_form.save()
            return redirect("view_p")
    else:
        postForm = PropertyDetails()
    return render(request, 'property.html', {'postForm': postForm})


def view_p(request):
    info = models.Property.objects.all()
    return render(request, 'view_p.html', {'info': info})


def home(request):
    return render(request, 'home.html')


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="tender1.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data')  # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Name', 'Type', ' Status', 'Address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)  # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = models.Property.objects.all().values_list('name', 'type', 'status', 'address')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)

    return response


@login_required(login_url='/login')
def purchase_dashboard(request):
    if request.user.is_purchase:
        return render(request, 'purchase_dashboard.html')
    else:
        return redirect('/error_page')


@login_required(login_url='/login')
def management_dashboard(request):
    if request.user.is_management:
        return render(request, 'management_dashboard.html')
    else:
        return redirect('/error_page')


@login_required(login_url='/login')
def finance_dashboard(request):
    if request.user.is_finance:
        return render(request, 'finance_dashboard.html')
    else:
        return redirect('/error_page')


@login_required(login_url='/login')
def sale_dashboard(request):
    if request.user.is_sale:
        return render(request, 'sale_dashboard.html')
    else:
        return redirect('/error_page')


class sale_register(CreateView):
    model = User
    form_class = SaleSignUpForm
    template_name = 'sale_register.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('/login')


class purchase_register(CreateView):
    model = User
    form_class = PurchaseSignUpForm
    template_name = 'purchase_register.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('/login')


class finance_register(CreateView):
    model = User
    form_class = FinanceSignUpForm
    template_name = 'finance_register.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request,user)
        return redirect('/login')


class management_register(CreateView):
    model = User
    form_class = ManagementSignUpForm
    template_name = 'management_register.html'

    def form_valid(self, form):
        user = form.save()
        auth.login(self.request, user)
        return redirect('/login')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password1']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            # request.session['user_id'] = user.id
            # request.session['username'] = user.username
            if request.user.is_sale:
                return redirect('sale_dashboard')
            elif request.user.is_purchase:
                return redirect('purchase_dashboard')
            elif request.user.is_finance:
                return redirect('finance_dashboard')
            elif request.user.is_management:
                return redirect('management_dashboard')
        else:
            messages.info(request, 'Invalid Credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')



def logout_view(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def new_tender(request):
    return render(request, 'new_tender.html')


@login_required(login_url='/login')
def view_tender(request):
    return render(request, 'view_tender.html')


@login_required(login_url='/login')
def update_tender_status(request):
    return render(request, 'update_tender_status.html')


@login_required(login_url='/login')
def request_tender_fee(request):
    return render(request, 'request_tender_fee.html')


@login_required(login_url='/login')
def sales_order(request):
    return render(request, 'sales_order.html')


@login_required(login_url='/login')
def request_BG(request):
    return render(request, 'request_BG.html')


@login_required(login_url='/login')
def prepare_budget(request):
    return render(request, 'prepare_budget.html')


@login_required(login_url='/login')
def update_budget(request):
    return render(request, 'update_budget.html')


@login_required(login_url='/login')
def view_budget(request):
    return render(request, 'view_budget.html')


@login_required(login_url='/login')
def request_quotation(request):
    return render(request, 'request_quotation.html')


@login_required(login_url='/login')
def new_vendor(request):

    if request.user.is_purchase:
        user = request.user
    if request.method == 'POST':
        postForm = Vendor_Form(request.POST)
        if postForm.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = user
            post_form.save()
            return redirect("purchase_dashboard")
    else:
        postForm = Vendor_Form()
        return render(request, 'new_vendor.html', {'form': postForm})


@login_required(login_url='/login')
def view_vendor(request):
    info = models.Vendor_Model.objects.all()
    return render(request, 'view_vendor.html', {'info': info})


@login_required(login_url='/login')
def update_vendor(request, id=0):
    form1 = Vendor_Model.objects.get(pk=id)
    form = Update_Vendor_Form()
    if request.method =="POST":
        form1 = Vendor_Model.objects.get(pk=id)
        form = Update_Vendor_Form(request.POST, instance=form1)
        if form.is_valid():
            v=Vendor_Model.objects.get(pk=id)
            v.user=request.user
            v.name=form.cleaned_data['name']
            v.mobile=form.cleaned_data['mobile']
            v.email=form.cleaned_data['email']
            v.address=form.cleaned_data['address']

            v.is_gst=form.cleaned_data['is_gst']
            v.gstin=form.cleaned_data['gstin']
            v.bank_name=form.cleaned_data['bank_name']
            v.pan =form.cleaned_data['pan']
            v.ifsc=form.cleaned_data['ifsc']
            v.is_pan=form.cleaned_data['is_pan']
            v.account_no=form.cleaned_data['account_no']
            # v.name=form.cleaned_data['name']
            # v.name=form.cleaned_data['name']
            # v.name=form.cleaned_data['name']

            v.save()
            # form.save()
            return redirect('view_vendor')
    return render(request, "update_vendor.html", {'form': form, 'form1': form1})


@login_required(login_url='/login')
def delete1(request, id):
    form1 = Vendor_Model.objects.get(pk=id)
    form1.delete()
    return redirect('view_vendor')


@login_required(login_url='/login')
def blacklist(request, id):
    form1 = Vendor_Model.objects.get(pk=id)
    if form1.black_list:
        form1.black_list = False
    else:
        form1.black_list = True
    form1.save()
    print(form1.black_list)
    return redirect('view_vendor')

@login_required(login_url='/login')
def view_quotation(request):
    return render(request, 'view_quotation.html')


def error_page(request):
    return render(request, 'error_page.html')


@login_required(login_url='/login')
def cash(request):
    return render(request, 'cash.html')


@login_required(login_url='/login')
def tender_payment(request):
    return render(request, 'tender_payment.html')


@login_required(login_url='/login')
def bg_acknowledge(request):
    return render(request, 'bg_acknowledge.html')


@login_required(login_url='/login')
def bg_issue(request):
    return render(request, 'bg_issue.html')


@login_required(login_url='/login')
def ack_app_payment(request):
    return render(request, 'ack_app_payment.html')



@login_required(login_url='/login')
def pending_payment(request):
    return render(request, 'pending_payment.html')


@login_required(login_url='/login')
def tds(request):
    return render(request, 'tds.html')


@login_required(login_url='/login')
def received_quotation(request):
    return render(request, 'received_quotation.html')




@login_required(login_url='/login')
def purchase_pending_payment(request):
    return render(request, 'purchase_pending_payment.html')


@login_required(login_url='/login')
def view_sales_order(request):
    return render(request, 'view_sales_order.html')


@login_required(login_url='/login')
def view_BG(request):
    return render(request, 'view_BG.html')


@login_required(login_url='/login')
def update_BG(request):
    return render(request, 'update_BG.html')


@login_required(login_url='/login')
def purchase_order(request):
    if request.user.is_purchase:
        user=request.user
    template_name = 'purchase_order.html'
    item = models.Budget_model.objects.all()
    # type1 = Budget_model.objects.values_list('project_no', flat=True).annotate(c=Count('project_no'))
    # type = Budget_model.objects.values_list('rml_no', flat=True).annotate(c=Count('project_no'))
    if request.method == 'GET':
        purchaseform = PurchaseModelForm(request.GET or None)
        formset = ParticularsFormset(queryset=Particulars.objects.none())
    elif request.method == 'POST':
        # selected_rml_no= get_object_or_404(Budget_model, pk=request.POST.get('rml_no'))
        # selected_project_no= get_object_or_404(Budget_model, pk=request.POST.get('project_no'))
        purchaseform = PurchaseModelForm(request.POST,request.FILES)
        formset = ParticularsFormset(request.POST,request.FILES)
        if purchaseform.is_valid() and formset.is_valid():
            purchase = purchaseform.save(commit=False)
            # purchase.project = selected_project_no
            # purchase.rml = selected_rml_no
            purchase.user = request.user
            purchase.save()
            for form in formset:
                # so that `purchase` instance can be attached.
                particular = form.save(commit=False)
                particular.purchase = purchase
                particular.save()
            return redirect('purchase_dashboard')
    return render(request, template_name, {'bookform': purchaseform,'formset': formset,'item':item})

# 'project':type1,'rml':type

@login_required(login_url='/login')
def new_invoice(request):
    info = models.Vendor_Model.objects.all()

    if request.user.is_purchase:
        user=request.user
    template_name = 'new_invoice.html'

    if request.method == 'GET':
        purchaseform = InvoiceModelForm(request.GET or None)
        formset = InvoiceFormset(queryset=Invoice.objects.none())
    elif request.method == 'POST':
        purchaseform = InvoiceModelForm(request.POST,request.FILES)
        formset = InvoiceFormset(request.POST,request.FILES)
        if purchaseform.is_valid() and formset.is_valid():
            invo = purchaseform.save(commit=False)
            invo.user = request.user
            invo.save()
            for form in formset:
                # so that `purchase` instance can be attached.
                particular = form.save(commit=False)
                particular.invoice = invo
                particular.save()
            return redirect('purchase_dashboard')
    return render(request, template_name, {'bookform': purchaseform,'formset': formset,'info':info})



@login_required(login_url='/login')
def view_purchase_order(request):
    info = models.Purchase_Order_Model.objects.all()
    return render(request, 'view_purchase_order.html', {'info': info})

@login_required(login_url='/login')
def view_single_purchase_order(request, id):
    post = get_object_or_404(Purchase_Order_Model, id=id, )
    post2 = Particulars.objects.filter(purchase=id)
    print(post, post2)
    return render(request, 'view_single_purchase_order.html',{'post': post,'post2':post2})


@login_required(login_url='/login')
def reject(request, id):
    form1 = Request_model.objects.get(pk=id)
    form1.status = 'reject'
    form1.save()
    return redirect('payment_req')

@login_required(login_url='/login')
def accept(request, id):
    form1 = Request_model.objects.get(pk=id)
    form1.status = 'Accept'
    form1.save()
    return redirect('payment_req')

@login_required(login_url='/login')
def view(request, id):
    form1 = Request_model.objects.get(pk=id)
    form1.status = 'Viewed'
    form1.save()
    return redirect('payment_pending')

@login_required(login_url='/login')
def paid_fully(request, id):
    form1 = Request_model.objects.get(pk=id)
    form1.status = 'Paid Fully'
    form1.save()
    return redirect('payment_pending')

@login_required(login_url='/login')
def paid_paritally(request, id):
    form1 = Request_model.objects.get(pk=id)
    form1.status = 'Paid Paritally'
    form1.save()
    return redirect('payment_pending')

@login_required(login_url='/login')
def payment_list(request):
    info = models.Payment_Model.objects.all()
    return render(request, 'payment_list.html', {'info': info})


@login_required(login_url='/login')
def payment_pending(request):
    info = models.Request_model.objects.all()
    return render(request, 'payment_pending.html', {'info': info})


@login_required(login_url='/login')
def view_advance_payment(request):
    info = models.Request_model.objects.all()
    return render(request, 'view_advance_payment.html', {'info': info})

@login_required(login_url='/login')
def payment_pay(request):
    if request.method == "POST":
        po_id = request.POST.get('po_id', 0)
        amt = request.POST.get('amt', 0)
        pamt = request.POST.get('pamt', 0)
        type = request.POST.get('type', '')
        mode = request.POST.get('mode', '')
        date = request.POST.get('date', '')
        tran_id = request.POST.get('tran_id', '')
        item = Payment_Model(invoice_id=po_id, amount=amt, remain_amount=pamt, transaction_type=type,
                          transaction_mode=mode, date=date, transaction_id=tran_id)
        item.save()
        return render(request, 'payment_pay.html')
    return render(request, 'payment_pay.html')

@login_required(login_url='/login')
def payment_req(request):
    info = models.Request_model.objects.all()
    return render(request, 'payment_req.html', {'info': info})

@login_required(login_url='/login')
def view_invoice(request):
    info = models.Invoice_Model.objects.all()
    return render(request, 'view_invoice.html', {'info': info})

# @login_required(login_url='/login')
# def view_invoice(request):
#     info = models.Invoice_Model.objects.all()
#     return render(request, 'view_invoice.html', {'info': info})
#
#
@login_required(login_url='/login')
def view_single_invoice(request, id):
    post = get_object_or_404(Invoice_Model, id=id, )
    post2 = Invoice.objects.filter(invoice=id)
    print(post, post2)
    return render(request, 'view_single_invoice.html',{'post': post,'post2':post2})


@login_required(login_url='/login')
def view_single_advance(request, id):
    post = get_object_or_404(Request_model, id=id, )
    return render(request, 'view_single_advance.html',{'post': post})

@login_required(login_url='/login')
def process(request, id):
    item = Request_model.objects.get(pk=id)
    if request.method == "POST":
        item.tds_type = request.POST.get('tds_type', 'None')
        tds = request.POST.get('tds', 0)
        item.tds = tds
        item.status = 'Processed'
        amt = int(str(item.amount))
        item.net_pay_amt = amt - int(tds)
        item.save()
        return render(request, 'payment_pending.html')
    return render(request, 'process.html', {'item': item})

@login_required(login_url='/login')
def pay(request, id):
    items = Request_model.objects.get(pk=id)
    po_ids = str(items.po_id)
    amount = int(str(items.net_pay_amt))
    if request.method == "POST":
        po_id = po_ids
        am = request.POST.get('amt', 0)
        amt = int(am)
        type = request.POST.get('type', '')
        mode = request.POST.get('mode', '')
        date = request.POST.get('date', '')
        tran_id = request.POST.get('tran_id', '')
        if amt < amount:
            pamt = amount - amt
            items.net_pay_amt = pamt
            items.adv_pay += amt
            items.status = 'Paid Paritially'
        if amt == amount:
            pamt = 0
            items.net_pay_amt = pamt
            items.adv_pay += amt
            items.status = 'Paid Fully'
        item = Payment_Model(invoice_id=po_id, amount=amt, remain_amount=pamt, transaction_type=type,
                             transaction_mode=mode, date=date, transaction_id=tran_id)
        item.save()
        items.save()
    return render(request, 'payment_pay.html')


@login_required(login_url='/login')
def new_advance_payment(request):
    item = models.Vendor_Model.objects.all()
    item1 = models.Purchase_Order_Model.objects.all()
    item2 = models.Invoice_Model.objects.all()
    if request.method == "POST":

        po_id = request.POST.get('po_id', 0)
        invoice_id = request.POST.get('invoice_id', 0)
        vendor = request.POST.get('vendor', '')
        amount = request.POST.get('amount', 0)
        pay_term = request.POST.get('pay_term', '')
        due_date = request.POST.get('due_date', '')
        pay_type = request.POST.get('pay_type', '')
        req_date = request.POST.get('req_date', '')
        req_by = request.POST.get('req_by', '')
        ab = Purchase_Order_Model.objects.get(pk=po_id)
        project_no = int(str(ab.project))
        print(project_no)
        item = Request_model(po_id=po_id, invoice_id=invoice_id, vendor=vendor, amount=amount, payment_terms=pay_term,
                          due_date=due_date, payment_type=pay_type, date=req_date, request_by=req_by, project_no=project_no)
        item.save()
        return render(request, 'new_advance_payment.html')
    return render(request, 'new_advance_payment.html', {'item': item,'item1':item1, 'item2': item2})

@login_required(login_url='/login')
def new_budget(request):

    #if request.user.is_management:
     #   user = request.user
    if request.method == 'POST':
        postForm = Budget_Form(request.POST,request.FILES)
        if postForm.is_valid():
            post_form = postForm.save(commit=False)
            #post_form.user = user
            post_form.save()
            return redirect("new_budget")
    else:
        postForm = Budget_Form()
        return render(request, 'new_budget.html', {'form': postForm})
