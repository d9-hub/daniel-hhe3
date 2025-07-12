import streamlit as st
import requests
import binascii
import json
import pandas as pd
import hashlib
import geocoder
from util import fetch_has, fetch_hasno

# Base API URL
# API_BASE = "https://Harare City Council GeoTag.astraminds.co.zw"

Api_Key = "68747470733a2f2f67656f7461672e61737472616d696e64732e636f2e7a77"
API_BASE = binascii.unhexlify(Api_Key).decode()

# Initialize session state variables
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

st.markdown("""
<style>
    .image-container {
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(0, 51, 160, 0.05);
        border-radius: 10px;
    }
    .image-container img {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    .image-container img:hover {
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# Image Section
st.markdown("""
<div class="image-container">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Coat_of_arms_of_Harare.svg/1200px-Coat_of_arms_of_Harare.svg.png" alt="NedBank Insights" style="width: 10%;">
</div>
""", unsafe_allow_html=True)

def login_page():
    st.title("Harare City Council GeoTag Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        # Prepare data for the login API
        data = {"username": username, "password": password}
        try:
            response = requests.post(f"{API_BASE}/login_user.php", json=data)
            result = response.json()

            # Check if login was successful by looking for "user_id"
            if "user_id" in result:
                st.session_state.user_id = result["user_id"]
                st.session_state.user_name = username
                st.success(result.get("message", "Login successful!"))
                st.session_state.page = "dashboard"
                st.rerun()

            else:
                st.error(result.get("message", "Login failed."))
        except Exception as e:
            st.error("Error during login: " + str(e))
    
    st.markdown("---")
    st.info("Don't have an account? Click the button below to create one.")
    if st.button("Go to Create Account"):
        st.session_state.page = "create_account"

def create_account_page():
    st.title("Create Account")
    fullname = st.text_input("UserName")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Create Account"):
        data = {
            "username": fullname.strip(),
            "email": email.strip(),
            "password": password.strip(),  # Plain password
        }

        try:
            response = requests.post(f"{API_BASE}/create_user.php", json=data)
            st.write("Raw Response:", response.text)  # Debugging output

            result = response.json()
            if result.get("status") == "success":
                st.success(result.get("message", "Account created successfully!"))
            else:
                st.error(result.get("message", "Error creating account!"))
        except requests.exceptions.RequestException as e:
            st.error(f"Request Error: {e}")
        except ValueError:  # Handles invalid JSON response
            st.error("Invalid JSON response from server. Check API output.")

    st.markdown("---")
    if st.button("Back to Login"):
        st.session_state.page = "login"

def viewhas_now(userid):
    data = fetch_has(userid)
    if data:
        # Convert JSON response to DataFrame
        df = pd.DataFrame(data)

        # Convert 'created_at' to datetime format
        df['created_at'] = pd.to_datetime(df['created_at'])

        # Drop the 'has_garbage' column if it exists
        df = df.drop(columns=['has_garbage'], errors='ignore')
        
        # Display data in a table
        st.subheader("List of Locations Without Garbage")
        st.dataframe(df)

        # Create a folium map
        # st.subheader("Map of Garbage-Free Locations")
        # map_center = [0, 0]  # Default center
        # if not df.empty and 'location' in df.columns:
        #     first_location = df.iloc[0]['location'].split(',')
        #     map_center = [float(first_location[0]), float(first_location[1])]

    else:pass
        # st.error("Failed to fetch Reported data. Please try again later.")

def viewhasno_now(userid):
    data = fetch_hasno(userid)
    if data:
        # Convert JSON response to DataFrame
        df = pd.DataFrame(data)

        # Convert 'created_at' to datetime format
        df['created_at'] = pd.to_datetime(df['created_at'])
        
        # Drop the 'has_garbage' column if it exists
        df = df.drop(columns=['has_garbage'], errors='ignore')
        # Display data in a table
        st.subheader("List of Locations With Garbage")
        st.dataframe(df)

        # Create a folium map
        # st.subheader("Map of Garbage-Free Locations")
        # map_center = [0, 0]  # Default center
        # if not df.empty and 'location' in df.columns:
        #     first_location = df.iloc[0]['location'].split(',')
        #     map_center = [float(first_location[0]), float(first_location[1])]

    else:pass
        # st.error("Failed to fetch Reported data. Please try again later.")

def dashboard_page():
    st.title("Harare City Council GeoTag Dashboard")
    st.write(f"Welcome, \nUser Name: {st.session_state.user_name},\n User ID: {st.session_state.user_id}")
    
    st.subheader("Report Garbage")
    st.write("Press the button below to report an area with garbage. Your current geolocation will be used.")
    if st.button("Report Garbage at Your Location"):
        # Use geocoder to attempt to fetch the user's location based on their IP
        g = geocoder.ip('me')
        if g.ok and g.latlng:
            lat, lon = g.latlng
            location = f"{lat}, {lon}"
            st.write(f"Location detected: Latitude {lat}, Longitude {lon}")
            with st.spinner('Uploading...'):
                data = {
                    "user_id": st.session_state.user_id,
                    "location": location,
                    "has_garbage": 1
                }
                try:
                    response = requests.post(f"{API_BASE}/post_location.php", json=data)
                    result = response.json()
                    st.success(result.get("message", "Reported successfully!"))
                except Exception as e:
                    st.error("Error reporting location: " + str(e))


        else:
            st.error("Could not detect your location. Please try again.")
    
    st.markdown("---")          
    viewhasno_now(st.session_state.user_id)
    viewhas_now(st.session_state.user_id)
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.user_id = None
        st.session_state.page = "login"

# Page navigation based on session state
if st.session_state.page == "login":
    login_page()
elif st.session_state.page == "create_account":
    create_account_page()
elif st.session_state.page == "dashboard":
    dashboard_page()

