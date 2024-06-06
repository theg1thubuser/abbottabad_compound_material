import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
import requests
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Image Insights")
st.title("Image Metadata Insights")
st.markdown("""
            This application provides insights into all images from the compound files where metadata regarding time and/or camera could be extracted. 
                        
            The interactive plot displays the number of images captured over the selected time period. Below the plot, you'll find a grid of images that fall within the chosen date range. 
                        
            The app will dynamically update the plot and image grid based on your selections.
            
            """)

with st.expander("Click here for more information on using the date filter and metadata toggle."):
    functionality_text = """

    <p>

    <h4>How to Use</h4>

    1. __Select Date Range__: Use the date input fields in the sidebar to specify a start and end date for filtering images.
    2. __Display Metadata__: Toggle the "Display camera, date, and time information" option to choose whether to show camera make, date, and time details below each image.
    3. __Browse Images__: Scroll through the grid of images within the selected date range. Each image is captioned with its file name and any available metadata.
    4. __Adjust Date Range__: You can dynamically update the date range by changing the start and end dates in the sidebar, and the app will respond accordingly.


    Example Use Case

    - __Objective__: Find images captured on a specific date.</li>
    - __Steps__: Set the start and end dates to the same date, and the app will display all images captured on that date.</li>

    </p>
    """
    st.markdown(functionality_text, unsafe_allow_html=True)

# base_directory
pages_directory = Path.cwd()
base_directory = pages_directory

# Load and filter DataFrame
df_data = pd.read_csv(f'{base_directory}/data/df.csv')
# Filter out rows with NaN values in  'timestamp'  and reset index
df_timestamp = df_data.dropna(subset=['timestamp'])
df_timestamp.reset_index(inplace=True)
# Select specific columns
filtered_columns = ['new_file_name', 'full_url', 'timestamp', 'camera_make', 'camera_model']
# Convert 'timestamp' column to datetime format
df = df_timestamp[filtered_columns]
df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y:%m:%d %H:%M:%S', errors='coerce')
df = df[df['timestamp'].notna()]

# Replace variants of manufacturers with common labels
manufacturer_mapping = {
    'canon': 'Canon',
    'olympus': 'Olympus',
    'nokia': 'Nokia',
    'sony': 'Sony',
    'nikon': 'Nikon',
    'fujifilm': 'Fujifilm',
    'casio': 'Casio',
    'hewlett-packard': 'HP',
    'hp': 'HP',
    'samsung': 'Samsung',
    'konica': 'Konica',
    'panasonic': 'Panasonic',
    'pentax': 'Pentax',
}

df['camera_make'] = df['camera_make'].str.lower().map(manufacturer_mapping).fillna('Other')

# Sidebar user inputs
st.sidebar.title("Data Filter")
st.sidebar.write("Select a date range to filter images")

start_date = st.sidebar.date_input("Type or select start date", 
                                   min_value=df['timestamp'].min().date(), 
                                   max_value=df['timestamp'].max().date(),
                                   value=df['timestamp'].min().date())
end_date = st.sidebar.date_input("Type or select end date", 
                                 min_value=df['timestamp'].min().date(), 
                                 max_value=df['timestamp'].max().date(),
                                 value=df['timestamp'].max().date())

# Filter df based on user inputs
filtered_df = df[(df['timestamp'] >= pd.to_datetime(start_date, format='%Y:%m:%d %H:%M:%S', errors='coerce')) & 
                 (df['timestamp'] <= pd.to_datetime(end_date, format='%Y:%m:%d %H:%M:%S', errors='coerce'))]

# Sidebar for filtering camera makes and models
camera_info_on = st.sidebar.checkbox('Display camera, date and time information (if available)')

if camera_info_on:
    camera_makes = st.sidebar.multiselect("Select camera makes", df['camera_make'].unique())
    if camera_makes:
        filtered_df = filtered_df[filtered_df['camera_make'].isin(camera_makes)]
        
        # Update camera model options based on selected makes
        available_models = filtered_df['camera_model'].unique()
        camera_models = st.sidebar.multiselect("Select camera models", available_models)
        if camera_models:
            filtered_df = filtered_df[filtered_df['camera_model'].isin(camera_models)]

# Group by date and count occurrences
occurrences = filtered_df['timestamp'].dt.date.value_counts().sort_index()

# Create a time series plot using Plotly Graph Objects
fig = go.Figure(data=[go.Scatter(x=occurrences.index, y=occurrences.values, mode='lines+markers')])
fig.update_layout(
    title='Number Of Images Over Selected Time Period',
    xaxis_title='Date',
    yaxis_title='Count',
    xaxis=dict(tickformat='%Y-%m-%d'),
)
st.plotly_chart(fig, use_container_width=True)

st.subheader(f"Images from {start_date} to {end_date}")

with st.spinner("Loading images ..."):
    st.write(' ')
    # Display images in a grid
    num_columns = 3
    columns = st.columns(num_columns)

    for idx, row in filtered_df.iterrows():
        try:
            file_name = row['new_file_name']  
            image_url = row['full_url']  
            response = requests.get(image_url)
            image = Image.open(BytesIO(response.content))
            column = columns[idx % num_columns]
            if camera_info_on:
                camera_make = '- Camera: ' + str(row['camera_make'])
                camera_model = str(row['camera_model'])
                timestamp = '- Date: ' + str(row['timestamp'])
                column.image(image, caption=f"{file_name} {camera_make} {camera_model if not pd.isnull(row['camera_model']) else ' '} {timestamp}", 
                             use_column_width=True)
            else:
                column.image(image, caption=f"{file_name} ", use_column_width=True)
        except KeyError:
            st.error(f"Image not found in mapping: {file_name}")
        except Exception as e:
            st.error(f"Error loading image: {e}")
