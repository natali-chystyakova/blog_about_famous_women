from django import forms
from .models import Woman
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cat"].empty_label = "Категория не выбрана"

    class Meta:
        model = Woman
        fields = ["title", "slug", "content", "photo", "is_published", "cat"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input"}),
            "content": forms.Textarea(attrs={"cols": 60, "rows": 10}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) > 200:
            raise ValidationError("Длина превышает 200 символов")
        return title


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(widget=forms.Textarea(attrs={"cols": 60, "rows": 10}))
    captcha = CaptchaField()
