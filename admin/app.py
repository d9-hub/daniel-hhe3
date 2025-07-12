import streamlit as st
import requests
import smtplib
import random
import pandas as pd
import folium
from streamlit_folium import folium_static
from datetime import datetime
from api_utils import create_admin, login_admin, fetch_locations, fetch_has, fetch_hasno, send_otp
import firebase_admin
from firebase_admin import credentials, firestore

verification_codes = {}

try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except:pass

# Streamlit app settings
st.set_page_config(page_title="Harare City Council Waste Management", layout="wide")

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

# Session State Initialization
if "user_id" not in st.session_state:
    st.session_state.user_id = None

# Harare-specific configuration
HARARE_CENTER = [-17.8297, 31.0522]  # Coordinates for Harare city center

def create_detailed_map(locations):
    """Create a Folium map with satellite imagery and detailed markers"""
    m = folium.Map(location=HARARE_CENTER, zoom_start=13, tiles="cartodbpositron")
    
    # Add satellite imagery layer
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri World Imagery',
        name='Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add buildings layer (example coordinates)
    harare_buildings = {
        "Eastgate Mall": (-17.8176, 31.0444),
        "Harare International Airport": (-17.9318, 31.0926),
        "Parliament of Zimbabwe": (-17.8276, 31.0467),
        "National Sports Stadium": (-17.8167, 31.0167)
    }
    
    for building, coords in harare_buildings.items():
        folium.Marker(
            coords,
            popup=f"<b>{building}</b>",
            icon=folium.Icon(color='gray', icon='building', prefix='fa')
        ).add_to(m)
    
    # Add garbage locations
    for loc in locations:
        try:
            if loc["has_garbage"] == "1":
                lat, lon = map(float, loc["location"].split(","))
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=8,
                    color='#ff0000',
                    fill=True,
                    fill_color='#ff0000',
                    popup=f"Reported at: {loc.get('created_at', 'N/A')}<br>User: {loc.get('user_id', 'Unknown')}"
                ).add_to(m)
        except Exception as e:
            st.error(f"Error processing location: {e}")
    
    folium.LayerControl().add_to(m)
    return m

def view_map():
    st.title("Harare City Council Waste Management Dashboard")
    
    # Fetch and process data
    locations = fetch_locations()
    if not locations:
        st.error("Failed to fetch location data.")
        return
    
    # Create layout columns
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Display the enhanced map
        st.subheader("Real-time Waste Detection Map")
        m = create_detailed_map(locations)
        folium_static(m, width=800, height=600)
    
    with col2:
        # Statistics panel
        st.subheader("Area Statistics")
        total_reports = len(locations)
        active_issues = sum(1 for loc in locations if loc["has_garbage"] == "1")
        
        st.metric("Total Reports", total_reports)
        st.metric("Affected Areas", active_issues)

def createacc():
    st.title("Admin Account Creation")

    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    # Initialize session state variable if not set
    if "ottp" not in st.session_state:
        st.session_state.ottp = None  

    if st.button("Send Verification Code"):
        if email:
            st.session_state.ottp = str(send_otp(email))  # Store OTP in session state
            st.success("Verification code sent! Check your email.")
        else:
            st.error("Please enter a valid email.")
    # st.success(st.session_state.ottp)
    verification_code = st.text_input("Enter Verification Code")

    if st.button("Verify and Create Account"):
        if st.session_state.ottp and verification_code and st.session_state.ottp.strip() == verification_code.strip():
            response = create_admin(username, email, password)
            st.success(response["message"]) if response.get("success") else st.error(response["message"])
            st.success("Email verified! Account created successfully.")
        else:
            st.error("Invalid verification code!")


def admin_login():
    st.title("Admin Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        if email and password:
            response = login_admin(email, password)
            if response.get("success"):
                st.session_state.user_id = response["user_id"]
                st.success("Login successful!")
                st.rerun()
            else:
                st.error(response["message"])
        else:
            st.error("Please enter both email and password!")

def viewhas_now():
    data = fetch_has()
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

    else:pass
        # st.error("Failed to fetch data. Please try again later.")

def viewhasno_now():
    data = fetch_hasno()
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

    else:
        st.error("Failed to fetch data. Please try again later.")


# App Navigation

st.sidebar.title("Harare City Council Waste Management")
if st.session_state.user_id:
    if st.sidebar.button("Logout"):
        st.session_state.user_id = None
        st.rerun()

options = ["Admin Creation", "Admin Login", "View Map"]
choice = st.sidebar.radio("Select Page", options)

# Page routing
if choice == "Admin Creation":
    # admin_creation()
    createacc()
elif choice == "Admin Login":
    if st.session_state.user_id:
        st.success("Already logged in")
    else:
        admin_login()
elif choice == "View Map":
    if st.session_state.user_id:
        view_map()        
        viewhasno_now()
        viewhas_now()
    else:
        st.error("Please login to access the dashboard")

# Style enhancements
st.markdown("""
    <style>
    .stMetric {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        float: right; /* Anchors the element to the right */
        clear: both; /* Ensures proper positioning */
    }

    .st-emotion-cache-1y4p8pa {
        padding: 2rem 1rem;
    }
    </style>

""", unsafe_allow_html=True)