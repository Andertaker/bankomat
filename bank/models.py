# -*- coding: utf-8 -*-
from django.utils import timezone
from django.db import models
from django.utils.translation import ugettext_lazy as _


OPERATIONS = (
    (1, "Просмотр баланса"),
    (2, "Снятие наличных"),
    (3, "Пополнение баланса"),
)


class WithdrawError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)



class Card(models.Model):
    #username = models.CharField(max_length=16, unique=True, null=True, default=None)
    number = models.PositiveIntegerField(max_length=16, unique=True)
    pincode = models.PositiveIntegerField(max_length=4)
    error_attempts = models.PositiveSmallIntegerField("Кол-во неудачных попыток ввода пин-кода", default=0)
    is_active = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    rest = models.IntegerField(default=0)
    
    def __unicode__(self):
        s = str(self.number)
        s = "%s-%s-%s-%s" % (s[0:4], s[4:8], s[8:12], s[12:16])
        return s
    
    def card_number(self):
        return self.__unicode__()
    
    def balance(self):
        o = Operations()
        o.card_id = self.id
        o.code = 1
        o.rest = self.rest
        o.save()
        return o
        
    def withdraw(self, amount):
        if amount > 0:
            if amount > self.rest:
                raise WithdrawError(u"Недостаточно средств")
            
            self.rest -= amount
            self.save()
            
            o = Operations()
            o.card_id = self.id
            o.code = 2
            o.amount = -amount
            o.rest = self.rest
            o.save()
            return o



class Operations(models.Model):
    card = models.ForeignKey(Card)
    code = models.PositiveIntegerField(choices=OPERATIONS)
    amount = models.IntegerField(default=0)
    rest = models.IntegerField()
    date = models.DateTimeField(default=timezone.now)

    
    