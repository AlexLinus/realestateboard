from django.contrib.auth.models import User
from django import forms
from .models import ClassifiedImage, Classified, Complaints
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

class AddClassifiedForm(forms.ModelForm):
    class Meta:
        model = Classified
        exclude = ['author', 'creation_date', 'pub_date', 'is_active', 'views', 'slug']

    def __init__(self, *args, **kwargs):
        super(AddClassifiedForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class AdminImageWidget(AdminFileWidget):
    def render(self, name, value, attrs=None, renderer=None):
        output = []
        if value and getattr(value, "url", None):
            image_url = value.url
            file_name = str(value)
            output.append(u' <a href="%s" target="_blank"><img src="%s" alt="%s" /></a>' %(image_url, image_url, file_name))
            return mark_safe(u''.join(output))
        else:
            return mark_safe(u''.join(super(AdminFileWidget, self).render(name, value, attrs, renderer)))
            #output.append(super(AdminFileWidget, self).render(name, value, attrs, renderer))

class ImageClassifiedForm(forms.ModelForm):
    image = forms.FileField(widget=AdminImageWidget, label='')
    class Meta:
        model = ClassifiedImage
        fields = ['image']

    def __init__(self, *args, **kwargs):
        super(ImageClassifiedForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control photo-upload'


#class ComplaintsForm(forms.ModelForm):
#     complaint_text = forms.CharField(widget=forms.Textarea, label='Опишите вашу жалобу')
#     captcha_answer = forms.CharField(label='Введите ответ')


class ComplaintsForm(forms.ModelForm):
    class Meta:
        model = Complaints
        fields = ['complaint_body']

    captcha_answer = forms.CharField(label='Введите ответ')

    def __init__(self, *args, **kwargs):
        super(ComplaintsForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class SearchClassifiedForm(forms.ModelForm):
    class Meta:
        model = Classified
        fields = ['nmb_rooms']

    min_price = forms.IntegerField(label='от руб.')
    max_price = forms.IntegerField(label='до руб.')

    def __init__(self, *args, **kwargs):
        super(SearchClassifiedForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label