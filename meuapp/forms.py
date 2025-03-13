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

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user  # Armazena o usuário para usar depois
        if user:
            self.instance.servidor = user  # Define o servidor diretamente

    def clean(self):
        cleaned_data = super().clean()
        if not self.user:
            raise forms.ValidationError("O servidor é obrigatório.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.servidor = self.user  # Garante que o servidor seja salvo corretamente
        if commit:
            instance.save()
        return instance
