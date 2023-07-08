import os

def app_key(request):
    appkey_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'appkey.txt')
    with open(appkey_path, 'r') as f:
        appkey = f.read().strip()
    return {'appkey': appkey}