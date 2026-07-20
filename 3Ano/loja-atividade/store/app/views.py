from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ProductForm, UserModelForm, UserForm, ManufacturerForm
from .models import Product, UserModel, Category, Manufacturer

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

def users(request: HttpRequest) -> HttpResponse:
    users = UserModel.objects.filter(profile=2)

    context = {
        "users": users
    }

    return render(request, "app/users.html", context)

def categories(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.all().order_by("name")

    context = {
        "categories": categories
    }

    return render(request, "app/categories.html", context)

def create_category(request: HttpRequest) -> HttpResponse:
    message = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            message = {"type": "danger", "text": "Nome inválido"}
        elif Category.objects.filter(name__iexact=name).exists():
            message = {"type": "warning", "text": "Categoria já existe"}
        else:
            Category.objects.create(name=name)
            return redirect("categories")

    context = {
        "message": message,
        "category": None
    }

    return render(request, "app/category_form.html", context)

def edit_category(request: HttpRequest, pk: int) -> HttpResponse:
    category = get_object_or_404(Category, pk=pk)
    message = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            message = {"type": "danger", "text": "Nome inválido"}
        elif Category.objects.filter(name__iexact=name).exclude(pk=pk).exists():
            message = {"type": "warning", "text": "Categoria já existe"}
        else:
            category.name = name
            category.save()
            return redirect("categories")

    context = {
        "message": message,
        "category": category
    }

    return render(request, "app/category_form.html", context)

def delete_category(request: HttpRequest, pk: int) -> HttpResponse:
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        category.delete()
        return redirect("categories")

    context = {
        "category": category
    }

    return render(request, "app/category_delete.html", context)

def manufacturers(request: HttpRequest) -> HttpResponse:
    manufacturers = Manufacturer.objects.all().order_by("name")

    context = {
        "manufacturers": manufacturers
    }

    return render(request, "app/manufacturers.html", context)

def create_manufacturer(request: HttpRequest) -> HttpResponse:
    form = ManufacturerForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("manufacturers")

    context = {
        "form": form
    }

    return render(request, "app/manufacturer_form.html", context)

def edit_manufacturer(request: HttpRequest, pk: int) -> HttpResponse:
    manufacturer = get_object_or_404(Manufacturer, pk=pk)
    form = ManufacturerForm(request.POST or None, instance=manufacturer)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("manufacturers")

    context = {
        "form": form
    }

    return render(request, "app/manufacturer_form.html", context)

def delete_manufacturer(request: HttpRequest, pk: int) -> HttpResponse:
    manufacturer = get_object_or_404(Manufacturer, pk=pk)

    if request.method == "POST":
        manufacturer.delete()
        return redirect("manufacturers")

    context = {
        "manufacturer": manufacturer
    }

    return render(request, "app/manufacturer_delete.html", context)

def edit_user(request: HttpRequest) -> HttpResponse:
    user = get_object_or_404(UserModel, user=request.user)

    email_unused = True
    message = None
    if request.method == 'POST':
        usermodel_form = UserModelForm(request.POST, instance=user)
        user_form = UserForm(request.POST, instance=request.user) # type: ignore
        
        verify_email = UserModel.objects.filter(user__email=request.POST['email']).exclude(user__id=request.user.id).first() # type: ignore

        email_unused = verify_email is None
    else:
        usermodel_form = UserModelForm(instance=user)
        user_form = UserForm(instance=request.user) # type: ignore

    if usermodel_form.is_valid() and user_form.is_valid() and email_unused:
        usermodel_form.save()
        user_form.save()

        message = { 'type': 'success', 'text': 'Dados atualizados com sucesso' }
    else:
        if request.method == 'POST':
            if email_unused:
                message = { 'type': 'danger', 'text': 'Dados inválidos' }
            else:
                message = { 'type': 'warning', 'text': 'E-mail já usado' }

    context = {
        "form": usermodel_form,
        "user_form": user_form,
        "message": message
    }

    return render(request, "app/edit_user.html", context)
