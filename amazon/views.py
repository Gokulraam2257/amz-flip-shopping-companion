from django.shortcuts import render, redirect
from.forms import *
from django.contrib.auth import login,get_user,logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import JsonResponse
import requests
import datetime
from .amz import search_amz

from .flip import search_flip
# Create your views here.

def get_amazon(request,prod):
    data = search_amz(prod)
   
    return JsonResponse(data,json_dumps_params= {'indent':4, 'separators':(',', ': ')})

def get_flipkart(request,prod):
    data = search_flip(prod)
   
    return JsonResponse(data,json_dumps_params= {'indent':4, 'separators':(',', ': ')})

@login_required
def index(request): 
    if request.method == 'POST':
        try :
            prod = request.POST['search']
            prod2 = search_amz(prod)
            f_prod = prod2['Result'][0]
            #print(f_prod)
            
            prod1 = search_flip(prod)
            f_prod1 = prod1['Result'][0]

            usr = get_user(request)
            #print(usr.id)
            n = datetime.datetime.now()
            #print(n.day)
            if n.day == 1 :
                p = UserProfile.objects.get(user=usr)
                p.monthly_expenses = 0
                p.save()
            
            products_flip = Product(user = usr, prod_name = f_prod1['Name'], price = f_prod1['Price'],source = 'flip')
            products_amz = Product(user = usr, prod_name = f_prod['Name'], price = f_prod['Price'],source = 'amz')

            products_amz.save()
            products_flip.save()
            return render(request, 'index.html',{'prod' : f_prod,'prod1' : f_prod1,'user':usr})
        except :
            return render(request, 'index.html')
    return render(request, 'index.html')

def save_alert(request):
    if request.method == 'GET':
        mes = request.GET['post_id']
        url = request.GET['url']
        name = request.GET['name']
        price = request.GET['price']
        
        
        usr = get_user(request)
        #print(usr.email)
        user_info = UserProfile.objects.get(user=usr)
        number = user_info.whatsapp_number
        mo = user_info.monthly_expenses
        print(mes)
        if 'no' in mes :
            price = int(price)
               
            #print(drop)
            alert = PriceAlert(user = usr, prod_name = name, price = price )
            alert.save()
        elif 'yes' in mes:
            user_info.monthly_expenses = mo+int(price)
            user_info.recent_item_purchase = name
            user_info.total_purchases +=1
            user_info.save()
            if user_info.purchase_limit <= user_info.monthly_expenses:
                print('message send')
                send_msg(usr.username,name,number)
            else:
                print('else')

               
       
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def dashboard(request):
    user_profile = get_user(request)
    user_id = user_profile.id
    if not UserProfile.objects.filter(user= user_id).exists():
        
        form = UserDetailsForm(request.POST)
        if form.is_valid():

            save_user = form.save(commit=False)
            save_user.user = user_profile
            save_user.save()
            return redirect('otp')
        return render(request, 'dashdetails.html',{'form': form})
    else:
        whatsapp = UserProfile.objects.filter(user_id= user_id).values()
        #print(whatsapp[0]['whatsapp_number'])
        number = whatsapp[0]['whatsapp_number'][3:-2]
        hash_no = whatsapp[0]['whatsapp_number'].replace(number,'*****')
        
    return render(request, 'index1.html', {'user_profile': user_profile,'no':whatsapp[0], 'number' : hash_no})
@login_required
def logout_user(request):
    
    logout(request)
    return redirect('login')

global no 
no =0
import random
@login_required
def otp_verify(request):
    global no
    if(request.method == 'POST'):
        otp = request.POST.get('otp','')
        if int(otp) == int(no):
            return redirect('index')
    else:
        usr = get_user(request)
        #print(usr.email)
        user_info = UserProfile.objects.get(user=usr)
        number = user_info.whatsapp_number
        no = random.randrange(1000,9999)
        send_otp(no,number)
    return render(request,'otp.html')

def send_otp(no,number):
    url = 'https://graph.facebook.com/v17.0/110040545382950/messages'
   
    
    h = {"Content-Type": "application/json",                         
     "Authorization": "Bearer EAAIlfUAt6BgBOzPMRQxFpVOuf5J7HvNnFXGXBn8VxoVGj8528AxXDiLVeQq7fR3QYq6ZBSWFBqbmTnw2TtjslWZAwG3GyIgKZBVduhfjzs08MZBMp1WwHTYal47FBldCxShxFhsN5PofksuFcZAY4KQxw5MWgxuwbodPZBC08TukMpg9d7FhMr5sofvth4IASx2q9AMWR0A6ZAgTfp3ZAJtsDVPNPZCVHBsBsc32D"}
    a = '''Hai  you OTP For Registering *FLIPAZON* is *{}*. \n\n Thank You For Using Our Service  
    \n- *Admin*'''.format(no)
    d = {
        "messaging_product": "whatsapp",
        "to": '91'+number,
        "type": "text",
        "text": {
        "preview_url": True,
            "body": a,
        }
        }
    post =requests.post(url,json=d,headers=h)
    s = post.status_code
    js = post.json()
    print(s,js)

def send_msg(usr,name,number):
    url = 'https://graph.facebook.com/v17.0/110040545382950/messages'
   
    usr = usr.capitalize()
    h = {"Content-Type": "application/json",                         
     "Authorization": "Bearer EAAIlfUAt6BgBOzPMRQxFpVOuf5J7HvNnFXGXBn8VxoVGj8528AxXDiLVeQq7fR3QYq6ZBSWFBqbmTnw2TtjslWZAwG3GyIgKZBVduhfjzs08MZBMp1WwHTYal47FBldCxShxFhsN5PofksuFcZAY4KQxw5MWgxuwbodPZBC08TukMpg9d7FhMr5sofvth4IASx2q9AMWR0A6ZAgTfp3ZAJtsDVPNPZCVHBsBsc32D"}
    a = '''Hai *{}*, \n\n your Purchase Limit Is Crossed As You Buyed the *{}* .\n 
    Be Cautious At You Purchase . \n\n Thank You For Using Our Service  
    \n- *Admin*'''.format(usr,name)
    d = {
        "messaging_product": "whatsapp",
        "to": '91'+number,
        "type": "text",
        "text": {
        "preview_url": True,
            "body": a,
        }
        }
    post =requests.post(url,json=d,headers=h)
    s = post.status_code
    js = post.json()
    print(s,js)