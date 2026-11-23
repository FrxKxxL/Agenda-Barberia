from django import forms
from datos.repositorio_citas import listar_servicios
from dominio.validaciones import ESTADOS_CITA_VALIDOS


class NuevaCitaForm(forms.Form):
    nombre_cliente = forms.CharField(
        label="Nombre del cliente",
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. Valeria Morales",
                "class": "campo-input",
            }
        ),
    )
    telefono_cliente = forms.CharField(
        label="Teléfono",
        max_length=25,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. 8822-3344",
                "class": "campo-input",
            }
        ),
    )
    servicio_id = forms.ChoiceField(
        label="Servicio",
        choices=[],
        widget=forms.Select(attrs={"class": "campo-input"}),
    )
    fecha_hora = forms.DateTimeField(
        label="Fecha y hora",
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"],
        widget=forms.DateTimeInput(
            attrs={
                "type": "datetime-local",
                "class": "campo-input",
            }
        ),
    )
    notas_cliente = forms.CharField(
        label="Notas o preferencia (opcional)",
        max_length=250,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Ej. Prefiere atención por la mañana",
                "class": "campo-input",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        servicios = listar_servicios()
        self.fields["servicio_id"].choices = [
            (
                str(s["id"]),
                f"{s['nombre']} — ${s['precio']:.2f} ({s['duracion_min']} min)",
            )
            for s in servicios
        ]


class FiltroCitasForm(forms.Form):
    estado = forms.ChoiceField(
        label="Estado",
        required=False,
        choices=[("Todas", "Todos los estados")] + [(e, e) for e in ESTADOS_CITA_VALIDOS],
        widget=forms.Select(attrs={"class": "campo-filtro"}),
    )
    fecha = forms.DateField(
        label="Fecha",
        required=False,
        widget=forms.DateInput(
            attrs={
                "type": "date",
                "class": "campo-filtro",
            }
        ),
    )