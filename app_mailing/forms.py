from datetime import datetime

from django import forms

from app_mailing.models import Mailing, MailMessage


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        exclude = ['mailing_owner']

    def clean_date_start(self):
        date_start = self.cleaned_data.get('date_start')
        if date_start < datetime.now().date():
            raise forms.ValidationError('К сожалению, мы не умеем отправлять письма в прошлое...')
        return date_start

    def clean_date_finish(self):
        date_start = self.cleaned_data.get('date_start')
        if not date_start:
            date_start = datetime.now().date()
        date_finish = self.cleaned_data.get('date_finish')
        if date_finish < date_start:
            raise forms.ValidationError('Время идет в другую сторону... укажите дату окончания позже даты начала')

        return date_finish

    def __init__(self, *args, **kwargs):
        curr_user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['date_start'].initial = datetime.now()
        self.fields['date_finish'].initial = datetime.now()
        if curr_user:
            self.fields['message'].queryset = MailMessage.objects.filter(author=curr_user)
        else:
            self.fields['message'].queryset = MailMessage.objects.none()


class MailingStopForm(forms.ModelForm):

    class Meta:
        model = Mailing
        fields = ['date_start', 'date_finish', 'periodicity', 'message']

    def clean(self):
        self.errors.clear()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_start'].widget.attrs['readonly'] = True
        self.fields['date_finish'].widget.attrs['readonly'] = True
        self.fields['periodicity'].widget.attrs['disabled'] = True
        self.fields['message'].widget.attrs['disabled'] = True
        self.fields['periodicity'].widget.is_required = False
        self.fields['message'].widget.is_required = False


class MailMessageForm(forms.ModelForm):
    class Meta:
        model = MailMessage
        fields = '__all__'
        exclude = ['author']
