from django import forms
from django.utils import timezone
from .models import Client, Message, Mailing

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['email','full_name','comment']
        widgets = { 'comment': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'})}


    def __init__(self, *args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['start_time', 'end_time', 'message', 'recipients']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Извлекаем request из kwargs, если он передан
        request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        # Если есть request и пользователь авторизован, фильтруем queryset
        if request and request.user.is_authenticated:
            self.fields['recipients'].queryset = Client.objects.filter(owner=request.user)
            self.fields['message'].queryset = Message.objects.filter(owner=request.user)
        else:
            self.fields['recipients'].queryset = Client.objects.none()
            self.fields['message'].queryset = Message.objects.none()

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get('start_time')
        end = cleaned_data.get('end_time')
        if start and end:
            if start >= end:
                raise forms.ValidationError('Дата начала должна быть раньше даты окончания.')
            if start < timezone.now():
                raise forms.ValidationError('Дата начала не может быть в прошлом.')
        return cleaned_data

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['theme', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})