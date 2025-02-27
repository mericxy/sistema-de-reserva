from django import forms
from .models import Reserva

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['ambiente_tipo', 'ambiente_numero', 'data', 'hora_inicio', 'hora_fim', 'descricao']

        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'type': 'time'}),
            'hora_fim': forms.TimeInput(attrs={'type': 'time'}),
            'descricao': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hora_inicio = cleaned_data.get("hora_inicio")
        hora_fim = cleaned_data.get("hora_fim")

        if hora_inicio and hora_fim:
            if hora_inicio.minute % 30 != 0 or hora_fim.minute % 30 != 0:
                raise forms.ValidationError("As reservas devem começar e terminar a cada 30 minutos (ex: 8:00, 8:30).")
        return cleaned_data
