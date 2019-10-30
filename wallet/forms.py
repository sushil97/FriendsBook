from django import forms
from wallet.models import Transaction

class TransactionInfoForm(forms.ModelForm):

    class Meta():
        model = Transaction
        fields = ()
