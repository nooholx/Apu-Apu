from django import forms
from django.forms import widgets
from .models import Board

class LoginForm(forms.Form):
    # LoginForm 에서 입력받을 값은 2개 (아이디, 패스워드)
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class RegistForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['b_title', 'b_note', 'b_writer']  # '__all__'
        widgets = {
            'b_title': forms.TextInput(attrs={'class': 'form-control'}),
            'b_note': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'b_writer': forms.TextInput(attrs={'class': 'form-control'}),
        }