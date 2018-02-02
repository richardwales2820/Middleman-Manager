from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from .models import *
from .forms import *
import datetime

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

            user.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.garlicuser.address = form.cleaned_data.get('address')
            user.save()
            raw_password = form.cleaned_data.get('password')
            #user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect(index)
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

# Create your views here.
@login_required(login_url='/login')
def index(request):
    is_mm = hasattr(request.user.garlicuser, 'middleman')
    num_requests = 0

    if is_mm == True:
        num_requests = Trade.objects.filter(middleman=request.user.garlicuser.middleman).count()

    num_trades = (Trade.objects.filter(person_1=request.user.garlicuser) | Trade.objects.filter(person_2=request.user.garlicuser)).count()

    return render(request, 'index.html', {'is_mm': is_mm, 'num_requests': num_requests, 'num_trades': num_trades, 'addr': request.user.garlicuser.address})

@login_required(login_url='/login')
def mm_register(request):
    mm = None

    if hasattr(request.user.garlicuser, 'middleman'):
        mm = request.user.garlicuser.middleman

    if request.method == 'POST':
        fee = float(request.POST.get('fee')) if request.POST.get('fee') else 0

        if mm:
            mm.fee = fee
            mm.bio=request.POST.get('bio')
            
        else:
            mm = Middleman(garlic_user=request.user.garlicuser, fee=fee, bio=request.POST.get('bio'), rating=0.0)
        
        mm.save()
        
        return redirect(index)
    
    fee = 'Fee'
    bio = '(Optional) Info'

    if mm:
        fee = mm.fee
        bio = mm.bio if mm.bio != None else bio

    return render(request, 'mm-register.html', {'fee': fee, 'bio': bio})

@login_required(login_url='/login')
def find_mm(request):
    middlemen = Middleman.objects.order_by('-rating').exclude(garlic_user=request.user.garlicuser)

    return render(request, 'middlemen.html', {'mm': middlemen})

@login_required(login_url='/login')
def create_trade(request):
    if request.method == 'POST':
        form = TradeForm(request.user.garlicuser.id, request.POST)
        #if form.is_valid():
        print(request.POST)
        trade = form.save(commit=False)
        trade.time_created = datetime.datetime.now()
        trade.person_1 = request.user.garlicuser
        trade.middleman_id = request.POST.get('middleman')

        trade.save()
        return redirect(index)

    form = TradeForm(request.user.garlicuser.id)
    #form.middleman = Middleman.objects.exclude(garlic_user=request.user.garlicuser)

    return render(request, 'create-trade.html', {'form': form})

@login_required(login_url='/login')
def view_trades(request):
    trades = Trade.objects.filter(person_1=request.user.garlicuser) | Trade.objects.filter(person_2=request.user.garlicuser)

    return render(request, 'trades.html', {'trades': trades})

@login_required(login_url='/login')
def trade_details(request, id):
    trade = Trade.objects.get(id=id)

    return render(request, 'trade-details.html', {'trade': trade})