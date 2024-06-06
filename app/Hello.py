import streamlit as st

st.set_page_config(page_title="obl_files")

st.write("# Abbottabad Compound Material")

st.markdown(
    """
    
    Welcome to the interactive exploration of the Abbottabad Compound Material, a collection of images seized by the CIA during the 2011 raid on Osama bin Laden's compound in Pakistan. This app provides a unique window into this historical dataset, allowing you to browse and filter images interactively.

    """)
st.markdown("""
            The aim of this website is to aid analysis and understanding of the images found. 
            
            The authors of this website are not affiliated, associated, authorized, endorsed by, or in any way officially connected with any of the dieplayed or mentioned persons, organizations, or states. 
            Therefore, all views and opinions expressed in the material do not reflect the personal views or opinions of the authors. 
            
            Moreover, the authors disclaim all responsibility and liability for any actions, results, or interpretations arising from the use or application of any information contained herein.
            """)

st.write("## Images Insights") 


st.markdown(
    """

    In order to analyse the data, OpenAI's CLIP model, a powerful tool for image classification, has been employed to categorise each image regarding specific categories. To enhance browsing the material, you can filter the images by both categories and classification scores. 
    
    Furthermore, you can filter some of the images based on date and time as well camera make and model information.

    """)

st.write("## The CIA's November 2017 Release of the Abbottabad Compound Material ") 

st.markdown(
    """
    All images on this website are featured in the November 2017 Release of the Abbottabad Compound Material. [CIA library with all material](https://www.cia.gov/library/abbottabad-compound/index.html) (last accessed: 6 Jun 24)
    
    __Warning__

    Before you start exploring, please note that the material in this file collection may contain content that is offensive and/or emotionally disturbing. This material may not be suitable for all ages. Please view it with discretion.
    
    Prior to accessing this file collection, please understand that this material was seized from a terrorist organization by the US Central Intelligence Agency.
    """)
    
with st.expander("Click here for more information on both the model and classification process."):
    clip_text = """
    <p> 

    <h4>CLIP = Contrastive Language–Image Pretraining</h4>

    <p>CLIP is a model developed by OpenAI. The model bridges the gap between computer vision and natural language processing (NLP). CLIP can understand images and texts together, enabling it to classify images based on textual descriptions.
    
    The model has demonstrated remarkable versatility and robustness in various tasks, such as zero-shot classification, object detection, and even generating image captions. Its ability to understand and process both visual and textual data simultaneously makes it a powerful tool for applications that require a nuanced understanding of images in the context of natural language.
    </p>

    <h4>Here’s How CLIP Works</h4>

    <h5>Training</h5>

    <p>CLIP is trained on a diverse dataset of images and associated textual descriptions from the internet. This allows the model to learn a wide range of visual concepts and their corresponding language representations.</p>
    
    <h5>Encoding</h5>

    <p>CLIP encodes both images and text into a shared embedding space. This means that both visual and textual data are transformed into vectors in the same high-dimensional space.</p>
    
    <h5>Matching</h5>

    <p>For any given image and a set of textual descriptions, CLIP computes the similarity between the image’s vector and each textual vector. The model then ranks the textual descriptions based on their similarity to the image.</p>

    <h4>Classification Process</h4>

    <ol>
        <li><h5>Image Processing</h5>
        Initially, images were processed and evaluated against a list of predefined keywords (e.g., eye, mask, disaster, statue) using the pre-trained CLIP model.</li>
        <li><h5>Keyword Matching</h5>
        Each image was scored (with a score between 0 and 1) based on its likelihood to match the given keywords.</li>
        <li><h5>Score Calculation</h5>
        The model assigns a probability score indicating how well the image matches each keyword. For example, a score of 0.2 represents a weak match, around 0.5 indicates a moderate match, 0.8 or higher suggests a strong match, and values close to 1.0 indicate a very strong match</li>
    </ol>

    <p>
    The classification process using CLIP was done beforehand. The results of the classification can be explored with this website.</p>

    </p>

    </p>

"""
    st.markdown(clip_text, unsafe_allow_html=True)

st.write(' ')
st.write(' ')
st.text("Last edited: 6 Jun 25 by theg1thubuser")
