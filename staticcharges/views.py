from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import requests, json
from django.urls import reverse

from .forms import StaticChargeForm
from .models import *
from django.contrib.auth.models import User
from django.http import JsonResponse
import zebedee
import environ

env = environ.Env()
apikey = env('ZEBEDEE_API_KEY')

def index(request):
    static_charges = StaticCharge.objects.all()
    ctx = {"static_charges" : static_charges}
    return render(request, "staticcharges/index.html", ctx)

def create_static_charge(request):
    if request.method == "GET":

        form = StaticChargeForm()
        ctx = {'form': form }
        return render(request, "staticcharges/form.html", ctx)

    if request.method == "POST":
        form = StaticChargeForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, "staticcharges/form.html")
        url = "https://api.zebedee.io/v0/static-charges"
        heads = {'Content-Type': 'application/json', 'apikey': apikey}
        payload = {
            "allowedSlots": None,
            "minAmount": request.POST["min_amount"] + "000",
            "maxAmount": request.POST["max_amount"] + "000",
            "description": request.POST["description"],
            "identifier" : request.POST["identifier"],
            "callbackUrl": "https://c085-2600-8800-4c41-2200-a5e2-c69e-d613-e406.ngrok-free.app/callback/",
            "successMessage": "Congratulations your payment was successful!"
        }
        res = requests.post(url, headers=heads, data=json.dumps(payload)).json()
        print(res)
        # {'id': 'b6c35a86-9808-4875-80fe-503d591ee1ff', 'unit': 'msats', 'slots': 0, 'minAmount': '1000000', 'maxAmount': '2000000', 'createdAt': '2022-05-20T07:48:48.183Z', 'expiresAt': None, 'internalId': '11af01d092444a317cb33faa6b8304b8', 'description': 'My Static Charge Description', 'callbackUrl': 'https://782f-2600-8800-4c41-2200-4bc-d780-8b60-8419.ngrok.io/callback', 'allowedSlots': 1, 'successMessage': 'Congratulations your donation was successful!', 'status': 'active', 'invoice': {'request': 'lnurl1dp68gurn8ghj7ctsdyh85etzv4jx2efwd9hj7a3s9aex2ut4v4ehgttnw3shg6tr943ksctjvajhxtmzxe3nxdtp8qmz6wfcxquz6dpcxu6j6wpsvejj6dfsxdjr2wf3v4jnzenx25wtcl', 'uri': 'lightning:lnurl1dp68gurn8ghj7ctsdyh85etzv4jx2efwd9hj7a3s9aex2ut4v4ehgttnw3shg6tr943ksctjvajhxtmzxe3nxdtp8qmz6wfcxquz6dpcxu6j6wpsvejj6dfsxdjr2wf3v4jnzenx25wtcl'}}        
        static_charge = form.save(commit=False)
        static_charge.lnurlp = res["data"]["invoice"]["request"]
        static_charge.ext_static_charge_id = res["data"]["id"]
        static_charge.save()
        return render(request, "staticcharges/success.html")

def edit_static_charge(request, id):
    if request.method == "GET":
        sc = get_object_or_404(StaticCharge, ext_static_charge_id=id)
        form = StaticChargeForm(instance=sc)
        ctx = {'form': form }
        return render(request, "staticcharges/form.html", ctx)

    if request.method == "POST":
        form = StaticChargeForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, "staticcharges/form.html")
        url = f"https://api.zebedee.io/v0/static-charges/{id}"
        heads = {'Content-Type': 'application/json', 'apikey': apikey}
        payload = {
            "allowedSlots": 1000,
            "minAmount": request.POST["min_amount"] + "000",
            "maxAmount": request.POST["max_amount"] + "000",
            "description": request.POST["description"],
            "identifier" : request.POST["identifier"],
            "callbackUrl": "https://c085-2600-8800-4c41-2200-a5e2-c69e-d613-e406.ngrok-free.app/callback/",
            "successMessage": "Congratulations your payment was successful!"
        }
        res = requests.patch(url, headers=heads, data=json.dumps(payload)).json()
        print(res)
        # {'id': 'b6c35a86-9808-4875-80fe-503d591ee1ff', 'unit': 'msats', 'slots': 0, 'minAmount': '1000000', 'maxAmount': '2000000', 'createdAt': '2022-05-20T07:48:48.183Z', 'expiresAt': None, 'internalId': '11af01d092444a317cb33faa6b8304b8', 'description': 'My Static Charge Description', 'callbackUrl': 'https://782f-2600-8800-4c41-2200-4bc-d780-8b60-8419.ngrok.io/callback', 'allowedSlots': 1, 'successMessage': 'Congratulations your donation was successful!', 'status': 'active', 'invoice': {'request': 'lnurl1dp68gurn8ghj7ctsdyh85etzv4jx2efwd9hj7a3s9aex2ut4v4ehgttnw3shg6tr943ksctjvajhxtmzxe3nxdtp8qmz6wfcxquz6dpcxu6j6wpsvejj6dfsxdjr2wf3v4jnzenx25wtcl', 'uri': 'lightning:lnurl1dp68gurn8ghj7ctsdyh85etzv4jx2efwd9hj7a3s9aex2ut4v4ehgttnw3shg6tr943ksctjvajhxtmzxe3nxdtp8qmz6wfcxquz6dpcxu6j6wpsvejj6dfsxdjr2wf3v4jnzenx25wtcl'}}        
        update_data = {
            "min_amount": request.POST["min_amount"],
            "max_amount": request.POST["max_amount"],
            "description": request.POST["description"],
            "identifier" : request.POST["identifier"]
        }
        sc = StaticCharge.objects.filter(ext_static_charge_id=id)
        sc.update(**update_data)
        return redirect(reverse('detail-static-charge',  args=[id]))

def view_static_charge(request, id):
    sc = get_object_or_404(StaticCharge, ext_static_charge_id=id)
    url = f"https://api.zebedee.io/v0/static-charges/{id}"
    heads = {'Content-Type': 'application/json', 'apikey': apikey}
    res = requests.get(url, headers=heads).json()
    print(res)
    ctx = {"static_charge" : res["data"]["invoice"]["uri"], "static_charge_id" : res["data"]["id"]}
    return render(request, "staticcharges/detail.html", ctx)


def success(request):

    return render(request, "staticcharges/success.html")


def callback(request):
    data = json.loads(request.body)
    print(data)
    return HttpResponse(True)



def get_lightning_address(request, username):
    try:
        # user = User.objects.get(username=username)
        #lookup static charge associated with the user
        # user_static_charge = StaticCharge.objects.get(user=user)
        # proper way to do it:
        # sc = get_static_charge_data(id=user_static_charge.id)
        sc = get_static_charge_data(id="3b686285-9097-495c-bced-35da89e14f9a")


        # metadata_part_1 = sc["metadata"][1:sc["metadata"].find("],")+2]
        # metadata_part_2 = f'["text/identifier", "{username}@c085-2600-8800-4c41-2200-a5e2-c69e-d613-e406.ngrok-free.app"],'
        # metadata_part_3 = sc["metadata"][sc["metadata"].find("],")+2:-1]
        # sc["metadata"] = "[" + metadata_part_1 + metadata_part_2 + metadata_part_3 + "]"

        return JsonResponse(sc)
    except:
        res = {"status":"ERROR","reason":"The user you're searching for could not be found."}
        return JsonResponse(res)


def get_static_charge_data(id):
    url = f"https://api.zebedee.io/v0/request-static-charges/{id}"
    heads = {'Content-Type': 'application/json', 'apikey': apikey}
    res = requests.get(url, headers=heads).json()
    return res