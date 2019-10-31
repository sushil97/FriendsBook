from django import forms
from wallet.models import Transaction, OTP


class TransactionInfoForm(forms.ModelForm):

    class Meta():
        model = Transaction
        fields = ()

class OTPInfoForm(forms.ModelForm):

    class Meta():
        model = OTP
        fields=()