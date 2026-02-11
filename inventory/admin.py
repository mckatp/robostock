from django.contrib import admin
from .models import Category, Component, Beneficiary, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'name', 'category', 'quantity', 'box_number', 'last_updated')
    list_filter = ('category',)
    search_fields = ('name', 'serial_number', 'description')

@admin.register(Beneficiary)
class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'email', 'added_by')
    list_filter = ('role',)
    search_fields = ('name', 'email')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('component', 'borrower', 'quantity_taken', 'checkout_time', 'return_time', 'authorized_by')
    list_filter = ('return_time', 'checkout_time')
    search_fields = ('component__name', 'borrower__name')
