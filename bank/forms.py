# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.validators import MinValueValidator, MinLengthValidator

from .models import Card

    
    
def int_validator(value):
    if not value.isdigit():
        raise forms.ValidationError("Поле должно содержать только цифры")
   
    
def card_number_validator(value):
    int_validator(value)
    if len(value) != 16:
        raise forms.ValidationError("Номер карты должен содержать 16 цифр, \
                                        Вы ввели %d" % len(value))
    
    
    
class CardNumberForm(forms.Form):
    number = forms.CharField(max_length=20,
                             widget=forms.TextInput(attrs={'required': "required"}))
    
    error_messages = {
        'invalid_number': _("Card number %(number)s not found"),
        'incorrect_number': _("Card number %(number)s is incorrect"),
    }
    
    def clean(self):
        number = self.data["number"].replace('-', '')
        card_number_validator(number)
        number = int(number)

        try:
            card = Card.objects.get(number=number)
        except Card.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['invalid_number'],
                code='invalid_number',
                params={'number': self.data["number"]},
            )
            
        if not card.is_active:
            raise forms.ValidationError("Карта заблокирована")    
            
        self.cleaned_data["number"] = number
        return self.cleaned_data

    
    
class PincodeForm(forms.Form):
    pincode = forms.CharField(min_length=4, max_length=4, 
                validators=[MinLengthValidator, int_validator],
                widget=forms.PasswordInput(
                    attrs={'required': "", "autocomplete": "off", "size": 6}),
                )
    
    def clean(self):
        int_validator(self.data["pincode"])
        self.cleaned_data["pincode"] = int(self.data["pincode"])
        return self.cleaned_data
    
    
    
class WithdrawForm(forms.Form):
    amount = forms.IntegerField(label="Сумма снятия",
                min_value = 1,
                #validators=[MinValueValidator],
                widget=forms.TextInput(
                    attrs={'required': "", "size": 6}),
                )
    
    