from django.shortcuts import render, get_object_or_404, redirect
from .models import Component, Transaction, Beneficiary
from .forms import CheckoutForm, ComponentForm, BeneficiaryForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib import messages

def is_admin(user):
    return user.is_superuser

def dashboard(request):
    query = request.GET.get('q')
    if query:
        components = Component.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(category__name__icontains=query) |
            Q(serial_number__icontains=query) |
            Q(box_number__icontains=query)
        )
    else:
        components = Component.objects.all()
    
    context = {
        'components': components,
        'query': query,
    }
    return render(request, 'inventory/dashboard.html', context)

def component_detail(request, pk):
    component = get_object_or_404(Component, pk=pk)
    # Get active transactions (not returned yet)
    active_transactions = Transaction.objects.filter(component=component, return_time__isnull=True)
    return render(request, 'inventory/component_detail.html', {
        'component': component,
        'active_transactions': active_transactions
    })

def is_admin_or_staff(user):
    return user.is_superuser or user.is_staff

@login_required
@user_passes_test(is_admin_or_staff)
def add_component(request):
    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES)
        if form.is_valid():
            component = form.save()
            messages.success(request, f"Component '{component.name}' created successfully.")
            return redirect('component_detail', pk=component.pk)
    else:
        form = ComponentForm()
    return render(request, 'inventory/component_form.html', {'form': form, 'title': 'Add Component'})

@login_required
@user_passes_test(is_admin_or_staff)
def edit_component(request, pk):
    component = get_object_or_404(Component, pk=pk)
    if request.method == 'POST':
        form = ComponentForm(request.POST, request.FILES, instance=component)
        if form.is_valid():
            form.save()
            messages.success(request, f"Component '{component.name}' updated successfully.")
            return redirect('component_detail', pk=component.pk)
    else:
        form = ComponentForm(instance=component)
    return render(request, 'inventory/component_form.html', {'form': form, 'title': 'Edit Component', 'component': component})

@login_required
@user_passes_test(is_admin_or_staff)
def checkout_component(request, pk):
    component = get_object_or_404(Component, pk=pk)
    if request.method == 'POST':
        form = CheckoutForm(request.POST, component=component)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.component = component
            transaction.authorized_by = request.user
            transaction.save()
            
            # Decrease quantity
            component.quantity -= transaction.quantity_taken
            component.save()
            
            messages.success(request, f"Checked out {transaction.quantity_taken} of {component.name} to {transaction.borrower.name}")
            return redirect('component_detail', pk=pk)
    else:
        form = CheckoutForm(component=component)
    
    context = {
        'form': form,
        'component': component,
        'current_date': timezone.now()
    }
    return render(request, 'inventory/checkout_form.html', context)

@login_required
@user_passes_test(is_admin_or_staff)
def return_component(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)
    if transaction.return_time:
        messages.warning(request, "This item has already been returned.")
        return redirect('component_detail', pk=transaction.component.pk)
        
    if request.method == 'POST':
        transaction.return_time = timezone.now()
        transaction.save()
        
        # Increase quantity back
        component = transaction.component
        component.quantity += transaction.quantity_taken
        component.save()
        
        messages.success(request, f"Returned {transaction.quantity_taken} of {component.name} from {transaction.borrower.name}")
        return redirect('component_detail', pk=component.pk)
    
    return render(request, 'inventory/return_confirm.html', {'transaction': transaction})

@login_required
@user_passes_test(is_admin_or_staff)
def beneficiary_list(request):
    beneficiaries = Beneficiary.objects.all()
    return render(request, 'inventory/beneficiary_list.html', {'beneficiaries': beneficiaries})

@login_required
@user_passes_test(is_admin_or_staff)
def add_beneficiary(request):
    if request.method == 'POST':
        form = BeneficiaryForm(request.POST)
        if form.is_valid():
            beneficiary = form.save(commit=False)
            beneficiary.added_by = request.user
            beneficiary.save()
            messages.success(request, f"Beneficiary '{beneficiary.name}' added successfully.")
            return redirect('beneficiary_list')
    else:
        form = BeneficiaryForm()
    return render(request, 'inventory/beneficiary_form.html', {'form': form})

@login_required
@user_passes_test(is_admin_or_staff)
def beneficiary_detail(request, pk):
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    transactions = Transaction.objects.filter(borrower=beneficiary).order_by('-checkout_time')
    return render(request, 'inventory/beneficiary_detail.html', {'beneficiary': beneficiary, 'transactions': transactions})
