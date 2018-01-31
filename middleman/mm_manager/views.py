from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.
@login_required(login_url='/login')
def index(request):
    is_mm = hasattr(request.user.garlicuser, 'middleman')

    if is_mm == True:
        num_requests = Trade.objects.filter(middleman=request.user.garlicuser.middleman).count()

    num_trades = (Trade.objects.filter(person_1=request.user.username) | Trade.objects.filter(person_2=request.user.username)).count()


    return render(request, 'index.html', {'is_mm': is_mm, 'num_requests': num_requests, 'num_trades': num_trades})

@login_required(login_url='/login')
def mm_register(request):

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
    middlemen = Middleman.objects.order_by('-rating').exclude(garlic_user=request.user.garlicuser)
    # Create the initial exchange order
    # Allow for middleman search. If none available, still allow trade to create
    # Unique link generated corresponding to the trade. Can post to reddit. People can access trade that way

    return render(request, 'create-trade.html', {'mm': middlemen})