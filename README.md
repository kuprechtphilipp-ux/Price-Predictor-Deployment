# Web Application Structure

This web application is built using **Streamlit** and provides a range of features including user authentication, multiple pages and so on.

## Project Structure

```
WebApp
├── code/
│   │
│   ├── main.py                # Main file that manages routing
│   ├── home.py                # Home page
│   ├── login.py               # Login page
│   ├── pages.                 # Dashboard page
│   │   ├── airbnb.py          # page for airbnb stuff
│   │   ├── profile.py         # Profile management and user data
|   |   ├── renting.py         # page for renting stuff
|   |   ├── comparison.py      # page to compare renting and airbnb listing options
|   |   ├── __init__.py        # need, is empty
│   │   └── __pycache__        # Compiled Python files (auto-generated)
│   ├── .streamlit/            # Streamlit configuration
│   │   └── config.toml        # Streamlit config file --> to set theme
│   ├── __pycache__/           # Compiled Python files (auto-generated)
│   ├── data/                  # Folder for storing user data and profile
│   │   ├── profiles.json      # Personal profile data
│   │   └── users.json         # User authentication data
│   │   └── paris.geojson      # User authentication data
│   ├── auth.py                # Authentication handling
│   ├── utils.py               # Utility functions
└── README.md                  # Project documentation (this file)
```

## Setup Instructions

### 1. Install Dependencies

Install the required Python packages by running:

```bash
pip install streamlit
pip install streamlit-login-auth-ui
```

### 2. Run the Application

After installing the dependencies, you can run the web application by executing in the console (you have to be in right folder - in code folder):

```
streamlit run main.py
```

This will start the Streamlit server and open the web application in your default browser

---

## Application Features

### 1. User Authentication
- **Login and Sign-up**: Users can log in or sign up to access the app.
- **Profile Management**: Users can manage their profile information, including their email, password, and all the airbnb and renting related dataa

### 2. Pages
Multiple pages: renting, airbnb, profile,

- Airbnb: user can play around with values and find out potential income and so on

- Renting: user can play around with values and find out the right renting price

- Comparison: user can play around with values and clearly see which options is best, airbnb listing or renting


### 3. Data Storage

- Profile Data: User profile information containing also login relevant sutff (e.g., size, location, bathrooms, bedrooms, etc) is stored in `profiles.json`.

---

## Configuration

You can modify the app's configuration in the `.streamlit/config.toml` file. For example, you can adjust Streamlit's settings like the theme, i have chosen a dark one with redish tones
---
