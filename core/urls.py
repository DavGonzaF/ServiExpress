from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    
    path('gestionar-proveedores/', views.gestionar_proveedores, name='gestionar_proveedores'),
    path('agregar-proveedor/', views.agregar_proveedor, name='agregar_proveedor'),
    path('listar-proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path('editar-proveedor/<int:proveedor_id>/', views.editar_proveedor, name='editar_proveedor'),
    path('eliminar-proveedor/<int:proveedor_id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    path('gestionar-boletas/', views.gestionar_boletas, name='gestionar_boletas'),
    
    path('gestionar-usuarios/', views.gestionar_usuarios, name='gestionar_usuarios'),
    path('registro/', views.registro, name='registro'),
    path('agregar-usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('editar-usuario/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar-usuario/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    path('servicios/', views.servicios, name='servicios'),
    path('gestionar-servicios/', views.gestionar_servicios, name='gestionar_servicios'),
    path('agregar-servicio/', views.agregar_servicio, name='agregar_servicio'),
    path('editar-servicio/<int:servicio_id>/', views.editar_servicio, name='editar_servicio'),
    path('eliminar-servicio/<int:servicio_id>/', views.eliminar_servicio, name='eliminar_servicio'),
    path('agregar-al-carrito/<int:servicio_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('ver-carrito/', views.ver_carrito, name='ver_carrito'),
    path('eliminar-item-carrito/<int:item_id>/', views.eliminar_item_carrito, name='eliminar_item_carrito'),
    path('generar-boleta/', views.generar_boleta, name='generar_boleta'),
    
    
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/', views.logout_user, name='logout_user'),
    
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)