from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from citas_app.forms import FiltroCitasForm, NuevaCitaForm
from datos.conexion import inicializar_bd
from datos.repositorio_citas import (
    actualizar_estado_cita,
    crear_cita,
    eliminar_cita,
    listar_citas,
    listar_servicios,
)
from dominio.excepciones import ErrorDominio


def panel_citas(request):
    inicializar_bd()
    form_filtro = FiltroCitasForm(request.GET or None)

    estado_seleccionado = "Todas"
    fecha_texto = None

    if form_filtro.is_valid():
        estado_seleccionado = form_filtro.cleaned_data.get("estado") or "Todas"
        fecha_obj = form_filtro.cleaned_data.get("fecha")
        if fecha_obj:
            fecha_texto = fecha_obj.strftime("%Y-%m-%d")

    try:
        citas = listar_citas(estado=estado_seleccionado, fecha=fecha_texto)
        todas_las_citas = listar_citas()
    except ErrorDominio as exc:
        messages.error(request, str(exc))
        citas = []
        todas_las_citas = []

    resumen = {
        "total": len(todas_las_citas),
        "pendientes": sum(1 for c in todas_las_citas if c["estado"] == "Pendiente"),
        "confirmadas": sum(1 for c in todas_las_citas if c["estado"] == "Confirmada"),
        "completadas": sum(1 for c in todas_las_citas if c["estado"] == "Completada"),
    }

    contexto = {
        "citas": citas,
        "form_filtro": form_filtro,
        "resumen": resumen,
        "servicios": listar_servicios(),
        "estado_filtro": estado_seleccionado,
        "fecha_filtro": fecha_texto or "",
    }
    return render(request, "citas_app/panel_citas.html", contexto)


def nueva_cita(request):
    inicializar_bd()

    if request.method == "POST":
        form = NuevaCitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            try:
                cita_creada = crear_cita(
                    nombre_cliente=datos["nombre_cliente"],
                    telefono_cliente=datos["telefono_cliente"],
                    servicio_id=int(datos["servicio_id"]),
                    fecha_hora=datos["fecha_hora"],
                    notas_cliente=datos.get("notas_cliente", ""),
                )
                messages.success(
                    request,
                    f"Cita registrada para {cita_creada.cliente.nombre} ({cita_creada.fecha_hora_formateada()}).",
                )
                return redirect("panel_citas")
            except ErrorDominio as exc:
                messages.error(request, str(exc))
    else:
        form = NuevaCitaForm()

    return render(request, "citas_app/form_cita.html", {"form": form})


@require_POST
def cambiar_estado(request, cita_id: int, nuevo_estado: str):
    try:
        actualizada = actualizar_estado_cita(cita_id, nuevo_estado)
        if actualizada:
            messages.success(request, f"Estado actualizado a '{nuevo_estado}'.")
        else:
            messages.error(request, "No se encontró la cita indicada.")
    except ErrorDominio as exc:
        messages.error(request, str(exc))
    return redirect("panel_citas")


@require_POST
def borrar_cita(request, cita_id: int):
    try:
        eliminada = eliminar_cita(cita_id)
        if eliminada:
            messages.success(request, "Cita eliminada correctamente.")
        else:
            messages.error(request, "No se encontró la cita para eliminar.")
    except ErrorDominio as exc:
        messages.error(request, str(exc))
    return redirect("panel_citas")


