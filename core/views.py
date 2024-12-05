from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegistroUsuarioForm
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from .models import CustomUser, ItemBoleta
from .models import Proveedor
from .forms import ProveedorForm
from .forms import ServicioForm
from .models import Servicio, Carrito, ItemCarrito, Boleta
from django.core.paginator import Paginator
from django.utils.timezone import now


CustomUser = get_user_model()

# Verifica si el usuario es administrador
def admin_required(user):
    return user.is_superuser

def home(request):
    return render(request, 'home.html')


@login_required
@user_passes_test(admin_required)  # Restringe acceso solo a administradores
def gestionar_usuarios(request):
    User = get_user_model()  # Obtiene el modelo configurado en AUTH_USER_MODEL
    usuarios = User.objects.filter(is_superuser=False)  # Excluye administradores
    return render(request, 'gestionar_usuarios.html', {'usuarios': usuarios})

@login_required
@user_passes_test(admin_required)
def agregar_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash de la contraseña
            user.save()
            messages.success(request, "Usuario agregado con éxito.")
            return redirect('gestionar_usuarios')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = RegistroUsuarioForm()
    return render(request, 'agregar_usuario.html', {'form': form})

@login_required
@user_passes_test(admin_required)
def editar_usuario(request, usuario_id):
    User = get_user_model()
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gestionar_usuarios')
    else:
        form = RegistroUsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})


@login_required
@user_passes_test(admin_required)
def eliminar_usuario(request, usuario_id):
    if request.method == "POST":
        usuario = get_object_or_404(CustomUser, id=usuario_id)
        usuario.delete()
        messages.success(request, "Usuario eliminado con éxito.")
        return redirect('gestionar_usuarios')
    else:
        messages.error(request, "Operación no permitida.")
        return redirect('gestionar_usuarios')



@login_required
@user_passes_test(admin_required)
def gestionar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'gestionar_proveedores.html', {'proveedores': proveedores})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def listar_proveedores(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'listar_proveedores.html', {'proveedores': proveedores})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def agregar_proveedor(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor agregado con éxito.")
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedores.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def editar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado con éxito.")
            return redirect('listar_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def eliminar_proveedor(request, proveedor_id):
    proveedor = get_object_or_404(Proveedor, id=proveedor_id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, "Proveedor eliminado con éxito.")
        return redirect('listar_proveedores')
    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})

@login_required
@user_passes_test(admin_required)
def gestionar_boletas(request):
    return render(request, 'gestionar_boletas.html')


@login_required
def servicios(request):
    servicios_list = Servicio.objects.all()
    paginator = Paginator(servicios_list, 10)  # 10 servicios por página
    page = request.GET.get('page')
    servicios = paginator.get_page(page)
    return render(request, 'servicios.html', {'servicios': servicios})



# Lista de servicios
def gestionar_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'gestionar_servicios.html', {'servicios': servicios})

def agregar_al_carrito(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, servicio=servicio)
    if not creado:
        item.cantidad += 1
    item.save()
    messages.success(request, f"{servicio.nombre} se agregó al carrito.")
    return redirect('servicios')

# Crear un servicio
def agregar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES)  # Asegúrate de incluir `request.FILES`
        if form.is_valid():
            form.save()
            return redirect('gestionar_servicios')
    else:
        form = ServicioForm()
    return render(request, 'agregar_servicio.html', {'form': form})

# Editar un servicio
def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        form = ServicioForm(request.POST, request.FILES, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('gestionar_servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'editar_servicio.html', {'form': form})

# Eliminar un servicio
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == 'POST':
        servicio.delete()
        return redirect('gestionar_servicios')
    return render(request, 'eliminar_servicio.html', {'servicio': servicio})


def agregar_al_carrito(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    item, creado = ItemCarrito.objects.get_or_create(carrito=carrito, servicio=servicio)
    if not creado:
        item.cantidad += 1  # Incrementa la cantidad si ya existe
    item.save()
    messages.success(request, f"{servicio.nombre} se agregó al carrito.")
    return redirect('servicios')

def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.all()  # Obtenemos todos los items del carrito
    total = sum(item.subtotal for item in items)  # Calculamos el total
    return render(request, 'carrito.html', {'carrito': carrito, 'items': items, 'total': total})


def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(ItemCarrito, id=item_id)
    item.delete()
    messages.success(request, "El servicio se eliminó del carrito.")
    return redirect('ver_carrito')


def generar_boleta(request):
    carrito = Carrito.objects.get(usuario=request.user)
    total = sum(item.subtotal for item in carrito.items.all())

    # Crear la boleta
    boleta = Boleta.objects.create(usuario=request.user, total=total)

    # Transferir los ítems del carrito a la boleta
    for item in carrito.items.all():
        ItemBoleta.objects.create(
            boleta=boleta,
            servicio=item.servicio,
            cantidad=item.cantidad,
            precio_unitario=item.servicio.precio,
        )

    # Vaciar el carrito
    carrito.items.all().delete()
    carrito.total = 0
    carrito.save()

    return render(request, 'boleta_generada.html', {'boleta': boleta})



def registro(request):
    return render(request, 'registro.html')


def registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hashear la contraseña
            user.save()
            login(request, user)  # Iniciar sesión automáticamente tras el registro
            return redirect('servicios')  # Redirigir a servicios tras el registro
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registro.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login')  # Redirige al login después del logout