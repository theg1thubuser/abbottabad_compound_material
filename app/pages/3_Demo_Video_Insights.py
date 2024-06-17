import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.graph_objects as go

# Base directory
pages_directory = Path.cwd()
base_directory = pages_directory

st.set_page_config(page_title="Demo: Video Insights")
st.title("Video Insights")

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

st.subheader(f"Videos from {start_date} to {end_date}")

st.write(filtered_df[['new_file_name', 'timestamp', 'full_url']].sort_values(by='timestamp'))

# Sidebar toggle to display selected videos 
display_videos_on  = st.sidebar.checkbox('Display videos for selected time period')

if display_videos_on:
    # Display and play videos from URLs
    for idx, row in filtered_df.iterrows():
        video_url_base = row['full_url']  
        st.write(f"{row['new_file_name']} - Date: {row['timestamp']}")

        try:
            # Try displaying the video directly using st.video
            st.video(video_url_base)
        except Exception as e:
            # If st.video fails, fallback to multiple source formats
            st.write("Attempting to display using alternative formats")
            video_html = f"""
            <video width="640" height="264" controls>
                <source src="{video_url_base}" type="video/mp4">
                <source src="{video_url_base}" type="video/webm">
                <source src="{video_url_base}" type="video/ogg">
                <source src="{video_url_base}" type="video/3gpp">
                Your browser does not support the video tag.
            </video>
            """
            st.markdown(video_html, unsafe_allow_html=True)