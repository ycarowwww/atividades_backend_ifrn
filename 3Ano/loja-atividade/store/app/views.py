from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm
from .models import Product

def home(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()

    search_query = request.GET.get("name", "")

    if search_query:
        products = products.filter(name__icontains=search_query)

    context = {
        "products": products,
        "search_query": search_query
    }
    
    return render(request, "app/home.html", context)

def view_product(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)

    form = ProductForm(instance=product)

    for _, field in form.fields.items():
        field.widget.attrs["disabled"] = "disabled"
    
    context = {
        "form": form
    }

    return render(request, "app/view_product.html", context)

def create_product(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm()
    
    context = {
        "form": form
    }
    
    return render(request, "app/create_product.html", context)

def edit_product(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        
        if form.is_valid():
            form.save()
            return redirect("products")
    else:
        form = ProductForm(instance=product)
    
    context = {
        "form": form
    }
    
    return render(request, "app/edit_product.html", context)

def delete_product(request: HttpRequest, pk: int) -> HttpResponse:
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == "POST":
        product.delete()

        return redirect("products")
    else:
        form = ProductForm(instance=product)

    for _, field in form.fields.items():
        field.widget.attrs["disabled"] = "disabled"
    
    context = {
        "form": form
    }
    
    return render(request, "app/delete_product.html", context)

def products(request: HttpRequest) -> HttpResponse:
    products = Product.objects.all()
    
    context = {
        "products": products
    }
    
    return render(request, "app/products.html", context)
