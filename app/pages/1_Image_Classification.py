import streamlit as st
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
from pathlib import Path

st.set_page_config(page_title="Image Classification Results")

# base_directory
pages_directory = Path.cwd()
base_directory = pages_directory

# Load DataFrame
df = pd.read_csv(f'{base_directory}/data/df.csv')

st.title("Image Classification Results")
st.markdown("""            
            This application leverages the results of a pre-classified image dataset, where each image has been evaluated using the pre-trained CLIP model (OpenAI) based on a set of predefined categories. 
            
            Each image was scored between 0 and 1 based on its likelihood to match the given categories.
            
            The app allows users to filter and view images according to their classification scores for specific categories, providing insights into the visual content of the images.
            """)

with st.expander("Click here for more information on how to use the image filter in the sidebar."):
    functionality_text = """


    <p> 

    <h4>How to Use</h4>

    1.	__Select Category__: Choose a keyword category from the sidebar dropdown.
    2.	__Set Threshold__: Adjust the threshold slider to filter images based on the classification score. 
    3.	__View Images__: Browse the grid of images that meet the criteria. Each image displays the file name and its score for the selected category.
    4.	__Toggle Metadata__: Optionally, toggle the display the get information (if available) regarding time and camera.

    Example Use Case
    - __Objective__: Identify images that prominently feature “eyes” with a high degree of confidence.
    - __Steps__: Select “eye” from the category dropdown, set the threshold to 0.8, and review the filtered images to analyze the results.
            
    </p>
            
    """
    
    
    st.markdown(functionality_text, unsafe_allow_html=True)

# Sidebar for selecting category and threshold
with st.sidebar.title("Image Filter"):
    st.write("Select a category and a threshold to filter images")

sorted_columns = sorted(df.columns[15:])
category = st.sidebar.selectbox("Select category", sorted_columns)
threshold = st.sidebar.slider("Select threshold", min_value=0.0, max_value=1.0, 
                              value=0.8, step=0.01)

# Filter DataFrame based on selected category and threshold
filtered_df = df[df[category] >= threshold]

st.subheader(f"Images for category '{category}' with score above {threshold}")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Referer": "https://abbottabadcompoundmaterial.streamlit.app/",
    # "Accept-Encoding": "gzip, deflate, br",
}

with st.spinner("Loading images ..."):
    url = "https://www.cia.gov/library/abbottabad-compound/" 
    session = requests.Session() 
    st.write(' ')
    # Display images in a grid
    num_columns = 3
    columns = st.columns(num_columns)

    for idx, row in filtered_df.iterrows():
        try:
            file_name = row['new_file_name']  
            image_url = row['full_url']  
            session.headers.update(headers)
            response = session.get(image_url, 
                                #    headers=headers, 
                                   timeout=30,
                                    stream=True)
            # response = requests.get(image_url, headers=headers, timeout=30)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
            column = columns[idx % num_columns]
            column.image(image, caption=f"{file_name} - score: {row[category]:.2f}", 
                         use_column_width=True)

        except Exception as e:
            st.error(f"Error loading image: {e}")    
        except requests.exceptions.RequestException as e:
            # logging.error(f"Error fetching image from URL: {e}")
            st.error(f"Error loading image: cannot fetch from URL {image_url}")

