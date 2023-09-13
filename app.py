# Import necessary modules
import streamlit as st
from joblib import load
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Load the trained model
model = load('./best_model.joblib')

# App title
st.title('Strava Post Author Predictor')

# Header
st.markdown("---")
st.markdown("### How to use this app:")
st.markdown(
    "Fill in the details about the Strava post below and click on the 'Predict Author' button to see the probabilities of who the author might be. See [the documentation](https://github.com/ml-rowlands/Whose-Post-is-it-Anyway/) for more information."
)

# Sidebar for user input
with st.sidebar:
    st.header("User Input Features")

    # Textual features (text input)
    name = st.text_input('Title:', 'Morning Run')

    # Categorical features (dropdown)
    sport_type = st.selectbox('Sport Type:', ['Run', 'Trail Run','Ride', 'Nordic Ski', 'Backcountry Ski'])
    private = st.selectbox('Privacy:', ['Private', 'Public'])

    # Numerical features (sliders)
    st.subheader("Numerical Features")
    with st.expander("Run Data"):
        distance = st.slider('Distance (km):', min_value=0, max_value=50)
        elapsed_time_m = st.slider('Workout Time (min):', min_value=0, max_value=600)
        average_heartrate = st.slider('Average Heartrate(bpm):', min_value=100, max_value=200)
        max_speed = st.slider('Max Speed (km/hr):', min_value=0, max_value=35)
        total_elevation_gain = st.slider('Vert (m):', min_value=0, max_value=10000)
        elev_high = st.slider('High Point Elevation (m):', min_value=0, max_value=5000)
        
    with st.expander("Social Data"):
        kudos_count = st.slider('Kudos Count:', min_value=0, max_value=100)
        athlete_count = st.slider("Total Group Size:", min_value=0, max_value=10)

# Calculate speed
sport_type = sport_type.replace(" ", "")
elapsed_time = elapsed_time_m * 60
average_speed = distance / (elapsed_time + 0.1)

    
    
# Prediction button
if st.button('Predict Author'):
    # Initialize progress bar with text
    st.write("Processing...")
    progress_bar = st.progress(0)

    # Bundle and preprocess the input data
    user_data_dict = {
        'average_heartrate': [average_heartrate],
        'distance': [distance],
        'name': [name],
        'kudos_count': [kudos_count],
        'sport_type': [sport_type],
        'private': [private],
        'elapsed_time': [elapsed_time],
        'total_elevation_gain': [total_elevation_gain],
        'average_speed': [average_speed],
        'max_speed': [max_speed],
        'elev_high': [elev_high],
        'athlete_count': [athlete_count]
    }
    
    user_data = pd.DataFrame(user_data_dict)

    # Update progress bar
    progress_bar.progress(50)
    st.write("Generating Prediction...")

    # Make the prediction
    pred = model.predict_proba(user_data)

    # Update progress bar
    progress_bar.progress(100)
    st.write("Prediction Complete!")

    # Display the prediction probabilities as a bar chart
    st.subheader('Prediction Probabilities')
    class_labels = model.classes_
    probabilities = pred[0]
    
    
    # Create a more professional bar chart
    fig, ax = plt.subplots(figsize=(12, 8))
    bars = ax.barh(class_labels, probabilities, color='dodgerblue')

    # Add data labels
    for bar in bars:
        width = bar.get_width()
        label_x_pos = width
        ax.text(label_x_pos, bar.get_y() + bar.get_height()/2, f'{width:.2f}', va='center')

    # Add grid lines and style the plot
    ax.grid(True, linestyle='--', linewidth=0.5, color='gray')
    ax.set_xlabel('Probability', fontsize=14)
    ax.set_ylabel('Athlete', fontsize=14)
    ax.set_title('Predicted Probabilities for Each Athlete', fontsize=16)

    st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("Made with :heart: by Michael Rowlands")