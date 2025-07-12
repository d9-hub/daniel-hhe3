import requests
import binascii
import json

Api_Key = "68747470733a2f2f67656f7461672e61737472616d696e64732e636f2e7a77"
API_BASE_URL = binascii.unhexlify(Api_Key).decode()

def create_admin(username, email, password):
    """Create an admin account."""
    url = f"{API_BASE_URL}/create_admin.php"
    payload = {"username": username, "email": email, "password": password}
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if response.ok:
            return {"success": True, "message": data["message"]}
        return {"success": False, "message": data.get("message", "Failed to create admin account.")}
    except Exception as e:
        return {"success": False, "message": "Error => From FireBase"}

def login_admin(email, password):
    """Admin login."""
    url = f"{API_BASE_URL}/login_admin.php"
    payload = {"email": email, "password": password}
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if response.ok and data.get("message") == "Login successful":
            return {"success": True, "user_id": data["admin_id"]}
        return {"success": False, "message": data.get("message", "Invalid credentials.")}
    except Exception as e:
        return {"success": False, "message": "Error => From FireBase"}

def fetch_locations():
    """Fetch all locations from the server."""
    url = f"{API_BASE_URL}/view_location.php"
    try:
        response = requests.get(url)
        if response.ok:
            return response.json()
        return None
    except Exception as e:
        return None

def fetch_has():
    """Fetch all locations from the server."""
    url = f"{API_BASE_URL}/hasuser.php"
    try:
        response = requests.get(url)
        if response.ok:
            return response.json()
        return None
    except Exception as e:
        return None

def fetch_hasno():
    """Fetch all locations from the server."""
    url = f"{API_BASE_URL}/hasnouser.php"
    try:
        response = requests.get(url)
        if response.ok:
            return response.json()
        return None
    except Exception as e:
        return None

def send_otp(email):
    url = f"{API_BASE_URL}/sender.php"  # Direct API URL
    payload = {"email": email}  # Request payload

    try:
        response = requests.post(url, json=payload)  # Send POST request with JSON payload
        data = response.json()  # Parse response JSON

        if response.ok and "success" in data:  # Check if response was successful and has 'success'
            return data["otp"]  # Return OTP
        else:
            return f"Error: {data.get('error', 'Failed to send OTP.')}"  # Return error message

    except requests.exceptions.RequestException as e:
        return f"Request Error: {e}"

