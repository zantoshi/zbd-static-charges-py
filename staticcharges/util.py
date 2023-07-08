import requests, json
from django.http import HttpResponse


def create_static_charge(apikey, min_amount, max_amount, description, identifier):
    url = "https://api.zebedee.io/v0/static-charges"
    heads = {'Content-Type': 'application/json', 'apikey': apikey}
    payload = {
        # whats the point of slots??
        "allowedSlots": None,
        "identifier" : identifier,
        "minAmount": min_amount * 1000,
        "maxAmount": max_amount * 1000,
        "description": f"{description}",
        # "internalId": "11af01d092444a317cb33faa6b8304b8",
        "callbackUrl": "https://1465-2600-8800-4c41-2200-75ca-4568-97b9-7e74.ngrok.io/callback/static-charge/",
        "successMessage": "Congratulations your payment was successful!"
    }
    res = requests.post(url, headers=heads, data=json.dumps(payload)).json()
    print(res)
    # {'id': 'b6c35a86-9808-4875-80fe-503d591ee1ff', 'unit': 'msats', 'slots': 0, 'minAmount': '1000000', 'maxAmount': '2000000', 'createdAt': '2022-05-20T07:48:48.183Z', 'expiresAt': None, 'internalId': '11af01d092444a317cb33faa6b8304b8', 'description': 'My Static Charge Description', 'callbackUrl': 'https://782f-2600-8800-4c41-2200-4bc-d780-8b60-8419.ngrok.io/callback', 'allowedSlots': 1, 'successMessage': 'Congratulations your donation was successful!', 'status': 'active', 'invoice': {'request': 'lnurl1dp68gurn8ghj7ctsdyh85etzv4jx2efwd9hj7a3s9aex2ut4v4ehgttnw3shg6tr943ksctjvajhxtmzxe3nxdtp8qmz6wfcxquz6dpcxu6j6wpsvejj6dfsxdjr2wf3v4jnzenx25wtcl', 'uri': 'lightning:lnurl1dp68gurn8ghj7ctsdyh85etzv4jx2efwd9hj7a3s9aex2ut4v4ehgttnw3shg6tr943ksctjvajhxtmzxe3nxdtp8qmz6wfcxquz6dpcxu6j6wpsvejj6dfsxdjr2wf3v4jnzenx25wtcl'}}
    return res

def get_static_charge_detail(apikey, external_id):
    url = f"https://api.zebedee.io/v0/static-charges/external_id/{external_id}"
    heads = {'Content-Type': 'application/json', 'apikey': apikey}
    res = requests.get(url, headers=heads).json()
    print(res)
    return res

def get_all_static_charges(apikey):
    url = "https://api.zebedee.io/v0/static-charges"
    heads = {'Content-Type': 'application/json', 'apikey': apikey}
    res = requests.get(url, headers=heads).json()
    print(res)
    return res