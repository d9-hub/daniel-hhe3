#  GeoTag Plartform

This is a  app that integrates location services, user login, and garbage reporting using a web API.

### `requirements.txt`**
This file will list all the necessary dependencies to run your Streamlit app.

```txt
streamlit==1.16.0
requests==2.26.0
pandas==1.3.3
geocoder==1.38.1
binascii==1.0.0
hashlib==3.10.0
```

### Step 1: Install Dependencies

Once inside the project directory, run the following command to install the required dependencies:

```bash
pip install -r requirements.txt
```

This will install all necessary libraries like Streamlit, requests, pandas, and others required by the app.

### Step 2: Run the App

Once dependencies are installed, you can run the Streamlit app by executing:

```bash
streamlit run app.py
```

This will start the app and open it in your default web browser.

### Step 3: Using the App

- **Login Page**: The first page will allow you to log in using your credentials. 
- **Location Reporting**: After logging in, the app will detect your location and allow you to report if there's garbage.
