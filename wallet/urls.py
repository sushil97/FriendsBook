from django.urls import path

from . import views

urlpatterns = [
    # path('', views.WalletView.as_view(), name='Wallet'),
    path('', views.wallet_View, name='wallet'),
    path('balance', views.transferView, name='transfer'),
    # path('genOTP', views.genOTP, name='genotp'),
    path('paymentInit', views.transferInit, name='paymentInit'),
    path('upgradePay', views.transferInitUpgrade, name='upgradePay'),
    path('transfer_upgrade', views.transferViewUpgrade, name='transfer_upgrade')

]
