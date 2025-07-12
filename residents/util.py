import requests
import binascii
import json

Api_Key = "68747470733a2f2f67656f7461672e61737472616d696e64732e636f2e7a77"
API_BASE_URL = binascii.unhexlify(Api_Key).decode()


def fetch_has(userid):
    print(userid)
    data = {"user_id": userid}
    try:
        response = requests.post(f"{API_BASE_URL}/hasusermine.php", json=data)
        
        if response.ok:
            return response.json()  # Return the JSON response from the server
        else:
            print("Error:", response.status_code)  # Print error if not OK
            return None
    except Exception as e:
        print("Exception occurred:", str(e))
        return None


def fetch_hasno(userid):
    print(userid)
    data = {"user_id": userid}
    try:
        response = requests.post(f"{API_BASE_URL}/hasnousermine.php", json=data)
        
        if response.ok:
            return response.json()  # Return the JSON response from the server
        else:
            print("Error:", response.status_code)  # Print error if not OK
            return None
    except Exception as e:
        print("Exception occurred:", str(e))
        return None

