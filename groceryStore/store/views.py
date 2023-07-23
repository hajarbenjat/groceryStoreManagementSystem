# views.py

from django.shortcuts import render, redirect
from .models import Product, Sale
from .forms import ProductForm, SaleForm



def main_page(request):
    return render(request, 'main_page.html')


def inventory(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity_to_add = int(request.POST.get('quantity_to_add'))

        # Retrieve the product and add the new quantity
        product = Product.objects.get(pk=product_id)
        product.quantity += quantity_to_add
        product.save()

        return redirect('inventory')

    else:
        products = Product.objects.all()
        sales = Sale.objects.all()
        product_form = ProductForm()
    return render(request, 'inventory.html', {'products': products, 'sales': sales, 'product_form': product_form})


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product_name = form.cleaned_data['name']
            quantity = form.cleaned_data['quantity']

            # Check if the product already exists
            existing_product = Product.objects.filter(name=product_name).first()
            if existing_product:
                # Update the existing product's quantity
                existing_product.quantity += quantity
                existing_product.save()
            else:
                # Create a new product
                form.save()

            return redirect('inventory')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})

def make_sale(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity_sold = form.cleaned_data['quantity_sold']

            # Check if the selling quantity is greater than the available quantity
            if quantity_sold > product.quantity:
                return render(request, 'make_sale.html', {'form': form, 'error_message': 'Not enough quantity in stock.'})

            total_amount = product.price * quantity_sold

            # Update inventory quantity
            product.quantity -= quantity_sold
            product.save()

            # Save the sale transaction
            Sale.objects.create(product=product, quantity_sold=quantity_sold, total_amount=total_amount)

            return redirect('inventory')
    else:
        form = SaleForm()
    return render(request, 'make_sale.html', {'form': form})