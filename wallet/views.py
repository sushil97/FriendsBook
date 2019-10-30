from django.shortcuts import render

# Create your views here.
import random
from distutils import errors

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import DetailView, ListView

from signup.models import UserProfileInfo
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_protect
from django.db import transaction

from wallet.forms import TransactionInfoForm
from wallet.models import Transaction


def wallet_View(request):
    if request.user.is_authenticated:
        user = User.objects.get(id=request.user.id)
        wallet = UserProfileInfo.objects.get(user_id=user.id)

        context = {
            'wallet': wallet,
        }
        return render(request, 'Wallet/wallet.html', context)
    else:
        return HttpResponseRedirect('/login/')


# class WalletView(ListView):
#     model = UserProfileInfo
#     template_name = 'wallet.html'
otp = 0


@transaction.atomic()
def transferView(request):
    if request.user.is_authenticated:
        msg = ""
        if request.method == "POST":
            inut_otp = request.POST['otp']
            otpgen = otp
            print(inut_otp)
            print(otpgen)
            if int(inut_otp) == int(otpgen):
                sender = User.objects.get(username=request.user.username)
                receiver = User.objects.get(username=username)
                senderU = UserProfileInfo.objects.get(user=sender)
                receiverU = UserProfileInfo.objects.get(user=receiver)
                senderU.balance = int(senderU.balance) - int(amount)
                receiverU.balance = int(receiverU.balance) + int(amount)
                senderU.save()
                receiverU.save()
                transaction_form = TransactionInfoForm(data=request.POST)
                trans = transaction_form.save(commit=False)
                print('reached')
                trans.amount = int(amount)
                trans.sender = sender
                trans.receiver = receiver
                trans.save()
                msg = "Transaction Success"
                print('wallet Reached')
                user = User.objects.get(id=request.user.id)
                wallet = UserProfileInfo.objects.get(user_id=user.id)

                context = {
                    'wallet': wallet,
                }
                # user = UserProfileInfo.objects.get(id=request.user.id)
                # wallet = UserProfileInfo.objects.get(user_id=user.id)

                # # except Exception as e:
                # #     print(e)

                # secret_key = b'12345678901234567890'
                # now = int(time.time())
                # for delta in range(10, 110, 20):
                #     print(totp(key=secret_key, step=10, digits=6, t0=(now - delta)))

                return render(request, 'Wallet/success.html', context)
            else:
                return render(request, 'Wallet/fail.html')


    else:
        return HttpResponseRedirect('/login/')


username = "abc"
amount = 0


def transferInit(request):
    if request.user.is_authenticated:
        msg = ""
        if request.method == "POST":
            global username
            global amount
            username = request.POST['username']
            amount = request.POST['amount']
            if User.objects.filter(username=username).exists():
                sender = User.objects.get(username=request.user.username)
                senderU = UserProfileInfo.objects.get(user=sender)
                if int(amount) > int(senderU.balance):
                    return HttpResponseRedirect('/wallet/transfer/')
                else:
                    context = {
                        'username': username,
                        'amount': amount,
                    }
                    genOTP(request)
                    return render(request, 'Wallet/otpVerify.html', context)
            else:
                return HttpResponseRedirect('/wallet/transfer/')
    else:
        return HttpResponseRedirect('/login/')


def genOTP(request):
    # try:
    global otp
    otp = random.randint(100000, 999999)
    subject = 'Transaction Confirmation'
    if 'name' in request.GET:
        name = request.GET['name']
    message = 'Dear {} \n {} is your One Time Password for confirming the transaction!'.format(
        request.user.first_name, otp)
    receiver = str(request.user.email)
    email = EmailMessage(subject, message, to=[receiver, ])
    email.send()
    context = {
        'otpgen': otp,
    }
    return None
    # return render(request, 'wallet/otpVerify.html', context)

# except:
#   response = ['OOPs!! Error Occured @', otp]
#  return HttpResponse(response)
