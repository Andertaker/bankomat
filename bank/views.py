# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.shortcuts import render
from django import forms

from .forms import CardNumberForm, PincodeForm, WithdrawForm
from .models import Card, Operations, WithdrawError


class CardView(FormView):
    template_name = 'bank/number_form.html'
    form_class = CardNumberForm
    #success_url = '/operations/'
    
    '''
    def get(self, request):
        form = CardNumberForm(Card)
        c = dict(form=CardNumberForm)
        return render(request, 'bank/number.html', c)

    def post(self, request):
        pass
    '''
    ''
    def form_valid(self, form):
        number = form.cleaned_data["number"]
        return HttpResponseRedirect(reverse('pincode', kwargs={"card_number": number,}))
        
        '''
        #print dir(form.fields['number'])
        #print form.fields['number'].to_python()
        number = form.cleaned_data["number"]
        
        print dir(form.fields['number'])

        try:
            card = Card.objects.get(number=number)
        except Card.DoesNotExist:
            #form.errors.append("Not found")
            #form["number"].errors =  ["Not found"]
            #form.fields["number"].error_messages = ["Not found"]
            #form.error_messages["number"] = ["Not found"]
            
            raise forms.ValidationError(
                form.error_messages['invalid_login'],
                code='invalid_login',
                params={'number': "dssdfsd"},
            )
            
            c ={"form":form}
            return render(self.request, self.template_name, c)
        '''
        
        
        
class PincodeView(FormView):
    template_name = 'bank/pincode_form.html'
    form_class = PincodeForm
    #success_url = '/operations/'
    
    def dispatch(self, *args, **kwargs):
        self.card_number = kwargs["card_number"]
        return super(PincodeView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PincodeView, self).get_context_data(**kwargs)
        context["card_number"] = self.card_number
        return context

    def form_valid(self, form):
        card_number = self.card_number
        pincode = form.cleaned_data["pincode"]
        
        card = Card.objects.get(number=card_number)
        if not card.is_active:
            return render(self.request, "bank/card_blocked.html")
        
        
        if card.pincode == pincode:
            card.error_attempts = 0
            card.save()
            return HttpResponseRedirect(reverse('operations', kwargs={"card_number": card_number,}))
        else:
            print card.pincode
            print pincode
            '''
            print dir(form)
            form.is_valid = False
            
            print form.errors.__class__ ##<class 'django.forms.util.ErrorDict'>
            print form["pincode"].errors.__class__  #<class 'django.forms.util.ErrorList'>
            print form.fields["pincode"].error_messages.__class__   #<type 'dict'>
            
            form.errors["a"] = "b"
            #form["pincode"].errors += ["d"]
            form.fields["pincode"].error_messages = ["ff"]
            '''
            
            incorrect_pincode_msg = "Неверный пин-код"
            card.error_attempts += 1
            
            
            if card.error_attempts == 4:
                incorrect_pincode_msg += "\n\
                    Вы 4 раза подряд ввели неправильный пин-код, ваша карта заблокирована"
                card.is_active = False
            
            card.save()
            
            c ={"form":form, "card_number":card_number, "incorrect_pincode_msg": incorrect_pincode_msg}
            return render(self.request, self.template_name, c)
        
        
        
        

def pincode(request, card_number):
    return HttpResponse("pincode")



def operations(request, card_number):
    c ={"card_number":card_number}
    return render(request, 'bank/operations.html', c)



def balance(request, card_number):
    card = Card.objects.get(number=card_number)
    operation = card.balance()
    
    c ={"card": card, "operation": operation}
    return render(request, 'bank/balance.html', c)




class WithdrawView(FormView):
    template_name = 'bank/withdraw_form.html'
    form_class = WithdrawForm

    def dispatch(self, *args, **kwargs):
        self.card_number = kwargs["card_number"]
        return super(WithdrawView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(WithdrawView, self).get_context_data(**kwargs)
        context["card_number"] = self.card_number
        return context

    def form_valid(self, form):
        card_number = self.card_number
        amount = form.cleaned_data["amount"]

        card = Card.objects.get(number=card_number)
        error_msg = ""
        try:
            operation = card.withdraw(amount)
        except WithdrawError as e:
            error_msg = e.value
            c = {"card_number": card_number, "form": form, "error_msg": error_msg}
            return render(self.request, 'bank/withdraw_form.html', c)

        c = {"card": card, "operation": operation}
        return render(self.request, 'bank/withdraw_result.html', c)



def withdraw(request, card_number):
    card = Card.objects.get(number=card_number)
    card = card.balance()
    
    c ={"card": card}
    return render(request, 'bank/balance.html', c)







