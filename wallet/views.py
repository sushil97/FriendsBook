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

from wallet.forms import TransactionInfoForm, OTPInfoForm
from wallet.models import Transaction, OTP


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



transacid = 1
@transaction.atomic()
def transferView(request):
    if request.user.is_authenticated:
        msg = ""
        global transaction_flag
        if OTP.objects.filter(user=request.user).exists():
            otp = OTP.objects.get(user=request.user)
            if request.method == "POST":
                inut_otp = request.POST['otp']
                otpgen = otp.otp
                print(inut_otp)
                print(otpgen)
                if int(inut_otp) == int(otpgen):
                    global otpMatch
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
                    random_num = random.randint(100000, 999999)
                    while Transaction.objects.filter(trans_id=random_num).exists():
                        random_num = random.randint(100000, 999999)
                    trans.trans_id =random_num
                    print(trans.trans_id)
                    trans.save()
                    transaction_id = Transaction.objects.get(trans_id=random_num)
                    senderU.transaction_count = senderU.transaction_count + 1
                    senderU.save()

                    msg = "Transaction Success"
                    print('wallet Reached')
                    user = User.objects.get(id=request.user.id)
                    wallet = UserProfileInfo.objects.get(user_id=user.id)

                    context = {
                        'wallet': wallet,
                        'transaction_id': transaction_id
                    }
                    transaction_flag = True
                    OTP.objects.filter(user=request.user).delete()
                    return render(request, 'Wallet/success.html', context)
                else:
                    OTP.objects.filter(user=request.user).delete()
                    return render(request, 'Wallet/fail.html')
            else:
                OTP.objects.filter(user=request.user).delete()
                return HttpResponseRedirect('/wallet/transfer/')
        else:
            return HttpResponseRedirect('/wallet/transfer/')
    else:
        return HttpResponseRedirect('/login/')

@transaction.atomic()
def transferViewUpgrade(request):
    if request.user.is_authenticated:
        msg = ""
        if OTP.objects.filter(user=request.user).exists():
            otp = OTP.objects.get(user=request.user)
            if request.method == "POST":
                inut_otp = request.POST['otp']
                otpgen = otp.otp
                print(inut_otp)
                print(otpgen)
                if int(inut_otp) == int(otpgen):
                    sender = User.objects.get(username=request.user.username)
                    senderU = UserProfileInfo.objects.get(user=sender)
                    senderU.balance = int(senderU.balance) - int(amount)
                    senderU.transaction_count = senderU.transaction_count + 1
                    senderU.save()
                    if int(amount) == 5000:
                        senderU.user_type = "Commercial"
                        senderU.save()
                    elif int(amount) == 150:
                        senderU.user_type = "Platinum"
                        senderU.save()
                    elif int(amount) == 100:
                        senderU.user_type = "Gold"
                        senderU.save()
                    else:
                        senderU.user_type = "Silver"
                        senderU.save()
                    transaction_form = TransactionInfoForm(data=request.POST)
                    if transaction_form.is_valid():
                        trans = transaction_form.save(commit=False)
                        print('reached')
                        trans.amount = int(amount)
                        print(int(amount))
                        trans.sender = sender
                        random_num = random.randint(100000, 999999)
                        while Transaction.objects.filter(trans_id=random_num).exists():
                            random_num = random.randint(100000, 999999)
                        trans.trans_id = random_num
                        trans.save()
                    else:
                        print(transaction_form.errors)
                    msg = "Transaction Success"
                    print('wallet Reached')
                    user = User.objects.get(id=request.user.id)
                    wallet = UserProfileInfo.objects.get(user_id=user.id)
                    transaction_id = Transaction.objects.get(trans_id=random_num)
                    context = {
                        'wallet': wallet,
                        'transaction_id':transaction_id
                    }
                    OTP.objects.filter(user=request.user).delete()
                    return render(request, 'Wallet/success.html', context)
                else:
                    OTP.objects.filter(user=request.user).delete()
                    return render(request, 'Wallet/fail.html')
            else:
                OTP.objects.filter(user=request.user).delete()
                return HttpResponseRedirect('/wallet/transfer/')
        else:
            return HttpResponseRedirect('/wallet/transfer/')
    else:
        return HttpResponseRedirect('/login/')


username = "abc"

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
                if senderU.user_type == "Casual":
                    if senderU.transaction_count < 15:
                        if int(amount) > int(senderU.balance):
                            return render_to_response('Wallet/Retry.html',{'user':request.user})
                        else:
                            context = {
                                'username': username,
                                'amount': amount,
                            }
                            genOTP(request)
                            return render(request, 'Wallet/otpVerify.html', context)
                    else:
                        return render_to_response('Wallet/Monthly_limit.html',{'user':request.user})
                elif senderU.user_type == "Silver" or senderU.user_type == "Gold" or senderU.user_type == "Platinum":
                    if senderU.transaction_count < 30:
                        if int(amount) > int(senderU.balance):
                            return render_to_response('Wallet/Retry.html',{'user':request.user})
                        else:
                            context = {
                                'username': username,
                                'amount': amount,
                            }
                            genOTP(request)
                            return render(request, 'Wallet/otpVerify.html', context)
                    else:
                        return render_to_response('Wallet/Monthly_limit.html',{'user':request.user})
                else:
                    if int(amount) > int(senderU.balance):
                        return render_to_response('Wallet/Retry.html',{'user':request.user})
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
            return HttpResponseRedirect('/wallet/transfer/')
    else:
        return HttpResponseRedirect('/login/')


amount = 0

def transferInitUpgrade(request):
    if request.user.is_authenticated:
        msg = ""
        if request.method == "POST":
            sender = User.objects.get(username=request.user.username)
            senderU = UserProfileInfo.objects.get(user=sender)
            global amount
            amount = request.POST['amount']
            print(amount)
            if senderU.user_type == "Casual":
                if senderU.transaction_count < 15:
                    if int(amount) > int(senderU.balance):
                        return render_to_response('Wallet/Retry.html',{'user':request.user})
                    else:
                        context = {
                            'username': username,
                            'amount': amount,
                        }
                        genOTP(request)
                        return render(request, 'Wallet/otpUpgrade.html', context)
                else:
                    return render_to_response('Wallet/Monthly_limit.html',{'user':request.user})
            elif senderU.user_type == "Silver" or senderU.user_type == "Gold" or senderU.user_type == "Platinum":
                if senderU.transaction_count < 30:
                    if int(amount) > int(senderU.balance):
                        return render_to_response('Wallet/Retry.html',{'user':request.user})
                    else:
                        context = {
                            'username': username,
                            'amount': amount,
                        }
                        genOTP(request)
                        return render(request, 'Wallet/otpUpgrade.html', context)
                else:
                    return render_to_response('Wallet/Monthly_limit.html',{'user':request.user})
            else:
                if int(amount) > int(senderU.balance):
                    return render_to_response('Wallet/Retry.html',{'user':request.user})
                else:
                    context = {
                        'username': username,
                        'amount': amount,
                    }
                    genOTP(request)
                    return render(request, 'Wallet/otpUpgrade.html', context)

        else:
            return HttpResponseRedirect('/wallet/transfer/')
    else:
        return HttpResponseRedirect('/login/')

def genOTP(request):
    # try:
    otp = random.randint(100000, 999999)
    subject = 'Transaction Confirmation'
    if 'name' in request.GET:
        name = request.GET['name']
    message = 'Dear {} \n {} is your One Time Password for confirming the transaction!'.format(
        request.user.first_name, otp)
    receiver = str(request.user.email)
    email = EmailMessage(subject, message, to=[receiver, ])
    email.send()
    otp_form = OTPInfoForm(data=request.POST)
    otp_f = otp_form.save(commit=False)
    otp_f.user=request.user
    otp_f.otp=otp
    otp_f.save()
    context = {
        'otpgen': otp,
    }
    return None

def launch_transaction_status(request):
    if request.user.is_authenticated:
        return render(request, 'Wallet/transaction_status.html')
    else:
        return HttpResponseRedirect('/login/')

@csrf_exempt
def check_status(request):
    if request.user.is_authenticated:
        transaction_found=False
        if request.method=='POST':
            id=request.POST['search']
            if Transaction.objects.filter(trans_id=id).exists():
                user =request.user
                transactionid = Transaction.objects.get(trans_id=id)
                transaction_found=True
                return render_to_response('Wallet/transaction_status.html',{'transaction_found':transaction_found,
                                                                        'transaction':transactionid,
                                                                            'user':user})
            else:
                return HttpResponseRedirect('/timeline/')
        else:
            return render_to_response("Wallet/transaction_status.html")
    else:
        return HttpResponseRedirect('/login/')