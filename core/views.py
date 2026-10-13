# render: junta una plantilla con datos · redirect: manda al navegador a otra URL · get_object_or_404: busca un registro o responde 404
from django.shortcuts import render, redirect, get_object_or_404
# connection: datos de la conexión a la base (lo usa la vista "inicio" de la Semana 3)
from django.db import connection
# login_required: decorador que exige sesión iniciada antes de entrar a la vista
from django.contrib.auth.decorators import login_required
# Servicio: el modelo de la Semana 4, importado desde este mismo directorio
from .models import Servicio
# ServicioForm: el ModelForm que creaste en el paso 01
from .forms import ServicioForm


# inicio: la vista de la Semana 3 que muestra a qué base estás conectado (no cambia)
def inicio(request):
    info_bd = connection.settings_dict
    contexto = {
        'motor': info_bd['ENGINE'],
        'host': info_bd['HOST'],
    }
    return render(request, 'core/inicio.html', contexto)


# servicios: la vista del listado de la Semana 4
def servicios(request):
    lista_servicios = Servicio.objects.all()
    return render(request, 'core/servicios.html', {'servicios': lista_servicios})


# @login_required: si nadie inició sesión, Django lo manda a LOGIN_URL (el login de /admin)
@login_required
def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            nuevo.propietario = request.user
            nuevo.save()
            return redirect('servicios')
    else:
        form = ServicioForm()
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Nuevo servicio'})


@login_required
def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'core/servicio_form.html', {'form': form, 'titulo_pagina': 'Editar servicio'})


@login_required
def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('servicios')
    return render(request, 'core/servicio_confirm_delete.html', {'servicio': servicio})
