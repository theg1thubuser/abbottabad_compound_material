import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go
from pytube import YouTube
from moviepy.editor import VideoFileClip
import tempfile

# base_directory
pages_directory = Path.cwd()
base_directory = pages_directory

st.set_page_config(page_title="Demo: Video Insights")
st.title("Video Insights")

# Function to download and save video from URL
def download_video(url, output_path):
    try:
        yt = YouTube(url)
        yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(output_path)
        return True
    except Exception as e:
        print(f"Error downloading video: {e}")
        return False

# Function to display video in Streamlit app
def display_video(video_path):
    video = VideoFileClip(video_path)
    st.video(video_path)

# Load video data
df_data = pd.read_csv(f'{base_directory}/data/video_data.csv')

# Filter out rows with NaN values in 'timestamp' and reset index
df_timestamp = df_data.dropna(subset=['timestamp'])
df_timestamp.reset_index(inplace=True, drop=True)

# Ensure that the 'timestamp' column is properly recognized as a datetime object
df_timestamp['timestamp'] = pd.to_datetime(df_timestamp['timestamp'], format='%Y-%m-%d %H:%M:%S', errors='coerce')

# Filter out NaNs from the timestamp column
df = df_timestamp[df_timestamp['timestamp'].notna()]

# Sidebar user inputs
st.sidebar.title("Data Filter")
st.sidebar.write("Select a date range to filter videos")

start_date = st.sidebar.date_input("Type or select start date", 
                                   min_value=df['timestamp'].min().date(), 
                                   max_value=df['timestamp'].max().date(),
                                   value=df['timestamp'].min().date())
end_date = st.sidebar.date_input("Type or select end date", 
                                 min_value=df['timestamp'].min().date(), 
                                 max_value=df['timestamp'].max().date(),
                                 value=df['timestamp'].max().date())

# Filter df based on user inputs
filtered_df = df[(df['timestamp'] >= pd.to_datetime(start_date)) & 
                 (df['timestamp'] <= pd.to_datetime(end_date))]

# Group by date and count occurrences
occurrences = filtered_df['timestamp'].dt.date.value_counts().sort_index()

# Create a time series plot using Plotly Graph Objects
fig = go.Figure(data=[go.Scatter(x=occurrences.index, y=occurrences.values, mode='lines+markers')])
fig.update_layout(
    title='Number Of Videos Over Selected Time Period',
    xaxis_title='Date',
    yaxis_title='Count',
    xaxis=dict(tickformat='%Y-%m-%d'),
)
st.plotly_chart(fig, use_container_width=True)

st.write(filtered_df[['new_file_name', 'timestamp', 'full_url']]).sort_values(by='timestamp')

st.subheader(f"Videos from {start_date} to {end_date}")

# Create a list to store video URLs and their corresponding captions
video_urls = []
video_captions = []

# Iterate through the DataFrame to find video URLs
for idx, row in filtered_df.iterrows():
    if 'video' in row['new_file_name'].lower():  
        video_url = row['full_url']
        video_urls.append(video_url)
        timestamp = '- Date: ' + str(row['timestamp'])
        video_caption = f"{row['new_file_name']} {timestamp}"
        video_captions.append(video_caption)

# Create a temporary directory to store downloaded videos
temp_dir = tempfile.mkdtemp()

# Download and display videos
for url, caption in zip(video_urls, video_captions):
    video_path = f"{temp_dir}/{url.split('/')[-1]}"
    if download_video(url, video_path):
        display_video(video_path)
        st.write(caption)
    else:
        st.error(f"Error downloading or displaying video from URL: {url}")
