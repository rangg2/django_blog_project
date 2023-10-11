from django import forms
from .models import Board
from ckeditor.widgets import CKEditorWidget


class PostForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={
                "style": "border: 1px solid #dbdbdb; width: 735px; height:30px; margin-bottom:10px",
                "placeholder": " 제목",
            }
        ),
    )
    content = forms.CharField(
        widget=CKEditorWidget(config_name="default", attrs={"id": "content"}),
        label="",
    )
    
    class Meta:
        model = Board
        exclude = ['created_at','user_id','views','publish','image']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CustomLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'login-input'}),
        label='',
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-input'}),
        label='',
    )