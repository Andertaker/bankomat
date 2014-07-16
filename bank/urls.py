from django.conf.urls import patterns, include, url
from django.contrib import admin

from .views import CardView, PincodeView, operations, \
    balance, WithdrawView



admin.autodiscover()

urlpatterns = patterns('',
    #url(r'^$', 'django.contrib.auth.views.login', {"authentication_form": AuthenticationForm}, name='login'),
    
    url(r'^$', CardView.as_view(), name='number'),
    url(r'^pincode/(?P<card_number>[\d]+)$', PincodeView.as_view(), name='pincode'),
    url(r'^operations/(?P<card_number>[\d]+)$', operations, name='operations'),
    url(r'^balance/(?P<card_number>[\d]+)$', balance, name='balance'),
    url(r'^withdraw/(?P<card_number>[\d]+)$', WithdrawView.as_view(), name='withdraw'),

    url(r'^admin/', include(admin.site.urls)),
)




