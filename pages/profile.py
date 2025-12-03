import streamlit as st
import json
import os

# Paths for JSON files (CORRECTED for Cloud Deployment Structure)
# File must be located at the root of the repository/code folder: WebApp/code/data/profiles.json
PROFILE_DATA_PATH = "code/data/profiles.json" 

def load_profile_data():
    """Load personal profile data from profiles.json."""
    if os.path.exists(PROFILE_DATA_PATH):
        try:
            with open(PROFILE_DATA_PATH, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            # If the file is corrupted or empty, initialize an empty dict
            st.warning("The profile data file is corrupted or empty. Initializing...")
            return {}
    else:
        # If the file itself is missing, return an empty dict
        return {}

def save_profile_data(data):
    """Save personal profile data to profiles.json."""
    # Note: In Streamlit Cloud, this saves to the ephemeral file system.
    # Data will persist during a session but may be lost on next container restart.
    with open(PROFILE_DATA_PATH, "w") as file:
        json.dump(data, file, indent=4)

def profile_page():
    st.title("User Profile")

    # Ensure user is logged in
    if 'username' not in st.session_state:
        st.error("No username found in session state. Please log in again.")
        return

    username = st.session_state['username']
    st.subheader(f"Welcome, {username}!")

    # 1. Load Profile Data
    profile_data = load_profile_data()

    # Get the user's data or initialize a clean profile if missing
    user_data = profile_data.get(username, {})
    
    if not user_data:
        st.warning("No profile found for the user. Initializing profile with default values...")
        user_data = {
            "email": "",
            "password": st.session_state.get('password', 'default_password'), # Load initial password from login
            "host_is_superhost": False,
            "host_listings_count": 0,
            "host_identity_verified": False,
            "bathrooms": 1,
            "bedrooms": 1,
            "arrondissement": 1,
            "room_type": "Entire home/apt", # Changed default for better UI start
            "num_rooms": 2,
            "amenities": [], 
            "rent": False,
            "Number of rooms renting": 2,
            "furnished": False
        }
        profile_data[username] = user_data # Save initialized profile to main data dict
        save_profile_data(profile_data) # Save to file immediately after initialization

    
    st.write("Update your information to allow us to be as precise as possible!")
    st.markdown("---")
    
    # --- 2. KORRIGIERTE STRUKTUR: EINZELNES FORMULAR FÜR ALLE UPDATES ---
    with st.form(key='profile_update_form'):
        
        # --- A. ACCOUNT & HOST DETAILS ---
        st.markdown("##### Account & Host Status")
        col_acc1, col_acc2 = st.columns(2)
        
        # Note: We must display the password placeholder as empty for security
        new_email = col_acc1.text_input("Email", value=user_data.get("email", ""))
        new_password_input = col_acc2.text_input("New Password (Leave blank to keep current)", type="password", value="")

        st.markdown("---")
        
        col_host1, col_host2, col_host3 = st.columns(3)
        new_superhost = col_host1.checkbox("Host is Superhost", value=user_data.get("host_is_superhost", False))
        new_listings = col_host2.number_input("Number of Listings", min_value=0, value=user_data.get("host_listings_count", 0))
        new_identity_verified = col_host3.checkbox("Identity Verified", value=user_data.get("host_identity_verified", False))


        # --- B. PROPERTY CHARACTERISTICS ---
        st.markdown("##### Property Characteristics")
        
        col_prop1, col_prop2 = st.columns(2)
        new_arr = col_prop1.number_input("Arrondissement (1-20)", min_value=1, max_value=20, value=user_data.get("arrondissement", 1))
        
        room_types = ["Entire home/apt", "Private room", "Shared room", "Hotel room"]
        new_room_type = col_prop2.selectbox("Room Type", room_types, index=room_types.index(user_data.get("room_type", "Entire home/apt")))

        new_bathrooms = st.number_input("Bathrooms", min_value=0, value=user_data.get("bathrooms", 1))
        new_bedrooms = st.number_input("Bedrooms", min_value=0,value=user_data.get("bedrooms", 1))
        new_num_rooms = st.number_input("Total Number of Rooms", min_value=1, value=user_data.get("num_rooms", 2))


        # --- C. RENTING & AMENITIES ---
        st.markdown("##### Amenities & Renting Status")
        available_amenities = ["Kitchen", "WiFi", "Bathtub", "Elevator", "Air conditioning", "Pets allowed", "TV", "Private entrance", "Balcony", "City skyline view"]
        new_amenities = st.multiselect("Amenities", available_amenities, default=user_data.get("amenities", []))

        # Renting Status
        new_rent_status = st.checkbox("Do you rent your property?", value=user_data.get("rent", False))
        new_renting_rooms = st.number_input("Number of rooms you rent", min_value=0, value=user_data.get("Number of rooms renting", 2))
        new_furnished_status = st.checkbox("Is the rented space furnished?", value=user_data.get("furnished", False))


        # --- SUBMIT BUTTON ---
        submit_button = st.form_submit_button("Save All Changes", type="primary")

        if submit_button:
            # 1. Update all fields in the profile dictionary
            
            # --- VALIDATION ---
            if not new_email or not new_arr:
                 st.error("Please ensure Email and Arrondissement are filled out.")
                 st.stop()

            user_data["email"] = new_email
            if new_password_input:
                user_data["password"] = new_password_input # Only update if a new value was entered
            
            user_data["host_is_superhost"] = new_superhost
            user_data["host_listings_count"] = new_listings
            user_data["host_identity_verified"] = new_identity_verified
            user_data["arrondissement"] = new_arr
            user_data["room_type"] = new_room_type
            user_data["bathrooms"] = new_bathrooms
            user_data["bedrooms"] = new_bedrooms
            user_data["num_rooms"] = new_num_rooms
            user_data["amenities"] = new_amenities
            user_data["rent"] = new_rent_status
            user_data["Number of rooms renting"] = new_renting_rooms
            user_data["furnished"] = new_furnished_status
            
            # 2. Save to file
            profile_data[username] = user_data
            save_profile_data(profile_data)
            st.success("Profile updated successfully!")
            st.rerun() 
    
    
    # --- Logout button (outside the form) ---
    st.markdown("---")
    if st.button("Logout", key="logout_profile"):
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['page'] = 'home'
        st.success("You have been logged out.")
        st.rerun()
