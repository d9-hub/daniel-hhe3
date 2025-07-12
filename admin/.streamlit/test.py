import pandas as pd
import streamlit as st

# Example data
locations = [
    {'location_id': '1', 'location': '10.24, 23.3', 'has_garbage': '1', 'created_at': '2025-01-21 07:13:29', 'user_id': '1'},
    {'location_id': '2', 'location': '16.24, 43.3', 'has_garbage': '0', 'created_at': '2025-01-21 07:14:34', 'user_id': '1'},
    {'location_id': '3', 'location': '37.78825, -122.4324', 'has_garbage': '1', 'created_at': '2025-01-22 04:50:38', 'user_id': '1'},
    {'location_id': '4', 'location': '37.78825, -122.4324', 'has_garbage': '0', 'created_at': '2025-01-22 04:50:38', 'user_id': '1'}
]

# Display locations in Markdown for reference (optional)
st.markdown("### Locations Data")
st.write(locations)

# Filter garbage locations
garbage_locations = []
for loc in locations:
    try:
        # Ensure location is properly formatted
        if loc["has_garbage"] == "1" and "location" in loc:
            latitude, longitude = map(float, loc["location"].split(","))
            garbage_locations.append({"latitude": latitude, "longitude": longitude})
    except ValueError:
        st.error(f"Invalid location format: {loc['location']}")

# Display garbage locations on a map
if garbage_locations:
    df = pd.DataFrame(garbage_locations)
    st.map(df)
else:
    st.info("No garbage locations found!")
