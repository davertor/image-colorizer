# Import general purpose libraries
import os, re, time
import streamlit as st
import PIL
import cv2
import numpy as np
import uuid
from zipfile import ZipFile, ZIP_DEFLATED
from io import BytesIO
from random import randint

# Import util functions from deoldify
# NOTE:  This must be the first call in order to work properly!
from deoldify import device
from deoldify.device_id import DeviceId
#choices:  CPU, GPU0...GPU7
device.set(device=DeviceId.CPU)
from deoldify.visualize import *

# Import util functions from app_utils
from app_utils import get_model_bin



SESSION_STATE_VARIABLES = [
    'model_folder', 'max_img_size', 'uploaded_file_key'
]
for i in SESSION_STATE_VARIABLES:
    if i not in st.session_state:
        st.session_state[i] = None
        
#### SET INPUT PARAMS ###########
if not st.session_state.model_folder: st.session_state.model_folder = 'models/'
if not st.session_state.max_img_size: st.session_state.max_img_size = 800
################################

@st.cache(allow_output_mutation=True, show_spinner=False)
def load_model(model_dir, option):
    if option.lower() == 'artistic':
        model_url = 'https://data.deepai.org/deoldify/ColorizeArtistic_gen.pth'
        get_model_bin(model_url, os.path.join(model_dir, "ColorizeArtistic_gen.pth"))
        colorizer = get_image_colorizer(artistic=True)
    elif option.lower() == 'stable':
        model_url = "https://www.dropbox.com/s/usf7uifrctqw9rl/ColorizeStable_gen.pth?dl=0"
        get_model_bin(model_url, os.path.join(model_dir, "ColorizeStable_gen.pth"))
        colorizer = get_image_colorizer(artistic=False)

    return colorizer

def resize_img(input_img, max_size):
    img = input_img.copy()
    img_height, img_width = img.shape[0],img.shape[1]

    if max(img_height, img_width) > max_size:
        if img_height > img_width:
            new_width = img_width*(max_size/img_height)
            new_height = max_size
            resized_img = cv2.resize(img,(int(new_width), int(new_height)))
            return resized_img

        elif img_height <= img_width:
            new_width = img_height*(max_size/img_width)
            new_height = max_size
            resized_img = cv2.resize(img,(int(new_width), int(new_height)))
            return resized_img

    return img

def get_image_download_link(img, filename, button_text):
    button_uuid = str(uuid.uuid4()).replace('-', '')
    button_id = re.sub('\d+', '', button_uuid)

    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return get_button_html_code(img_str, filename, 'txt', button_id, button_text)

def get_button_html_code(data_str, filename, filetype, button_id, button_txt='Download file'):
    custom_css = f""" 
    <style>
        #{button_id} {{
            background-color: rgb(255, 255, 255);
            color: rgb(38, 39, 48);
            padding: 0.25em 0.38em;
            position: relative;
            text-decoration: none;
            border-radius: 4px;
            border-width: 1px;
            border-style: solid;
            border-color: rgb(230, 234, 241);
            border-image: initial;

        }} 
        #{button_id}:hover {{
            border-color: rgb(246, 51, 102);
            color: rgb(246, 51, 102);
        }}
        #{button_id}:active {{
            box-shadow: none;
            background-color: rgb(246, 51, 102);
            color: white;
            }}
    </style> """
    
    href =  custom_css + f'<a href="data:file/{filetype};base64,{data_str}" id="{button_id}" download="{filename}">{button_txt}</a>'
    return href

def display_single_image(uploaded_file, img_size=800):
    st_title_message.markdown("**Processing your image, please wait** ⌛")
    img_name = uploaded_file.name

    # Open the image
    pil_img = PIL.Image.open(uploaded_file)
    img_rgb = np.array(pil_img)
    resized_img_rgb = resize_img(img_rgb, img_size)
    resized_pil_img = PIL.Image.fromarray(resized_img_rgb)

    # Send the image to the model
    output_pil_img = colorizer.plot_transformed_pil_image(resized_pil_img, render_factor=35, compare=False)

    # Plot images
    st_input_img.image(resized_pil_img, 'Input image', use_column_width=True)
    st_output_img.image(output_pil_img, 'Output image', use_column_width=True)

    # Show download button
    st_download_button.markdown(get_image_download_link(output_pil_img, img_name, 'Download Image'), unsafe_allow_html=True)

    # Reset the message
    st_title_message.markdown("**To begin, please upload an image** 👇")

def process_multiple_images(uploaded_files, img_size=800):

    num_imgs = len(uploaded_files)

    output_images_list = []
    img_names_list = []
    idx = 1

    st_progress_bar.progress(0)

    for idx, uploaded_file in enumerate(uploaded_files, start=1):
        st_title_message.markdown("**Processing image {}/{}. Please wait** ⌛".format(idx,
                                                                                    num_imgs))

        img_name = uploaded_file.name
        img_type = uploaded_file.type

        # Open the image
        pil_img = PIL.Image.open(uploaded_file)
        img_rgb = np.array(pil_img)
        resized_img_rgb = resize_img(img_rgb, img_size)
        resized_pil_img = PIL.Image.fromarray(resized_img_rgb)

        # Send the image to the model
        output_pil_img = colorizer.plot_transformed_pil_image(resized_pil_img, render_factor=35, compare=False)

        output_images_list.append(output_pil_img)
        img_names_list.append(img_name.split('.')[0])

        percent = int((idx / num_imgs)*100)
        st_progress_bar.progress(percent)

    # Zip output files
    zip_path = 'processed_images.zip'
    zip_buf = zip_multiple_images(output_images_list, img_names_list, zip_path)

    st_download_button.download_button(
        label='Download ZIP file',
        data=zip_buf.read(),
        file_name=zip_path,
        mime="application/zip"
    )

    # Show message
    st_title_message.markdown("**Images are ready for download** 💾")

def zip_multiple_images(pil_images_list, img_names_list, dest_path):
    # Create zip file on memory
    zip_buf = BytesIO()

    with ZipFile(zip_buf, 'w', ZIP_DEFLATED) as zipObj:
        for pil_img, img_name in zip(pil_images_list, img_names_list):
            with BytesIO() as output:
                # Save image in memory
                pil_img.save(output, format="PNG")
                
                # Read data
                contents = output.getvalue()

                # Write it to zip file
                zipObj.writestr(img_name+".png", contents)
    zip_buf.seek(0)
    return zip_buf



###########################
###### STREAMLIT CODE #####
###########################

# General configuration
# st.set_page_config(layout="centered")
st.set_page_config(layout="wide")
st.set_option('deprecation.showfileUploaderEncoding', False)
st.markdown('''
<style>
    .uploadedFile {display: none}
<style>''',
unsafe_allow_html=True)

# Main window configuration
st.title("Black and white colorizer")
st.markdown("This app puts color into your black and white pictures")
st_title_message = st.empty()
st_progress_bar = st.empty()
st_file_uploader = st.empty()
st_input_img = st.empty()
st_output_img = st.empty()
st_download_button = st.empty()

st_title_message.markdown("**Model loading, please wait** ⌛")

# # Sidebar
st_color_option = st.sidebar.selectbox('Select colorizer mode',
                                    ('Artistic', 'Stable'))
                                    
# st.sidebar.title('Model parameters')
# det_conf_thres = st.sidebar.slider("Detector confidence threshold", 0.1, 0.9, value=0.5, step=0.1)
# det_nms_thres = st.sidebar.slider("Non-maximum supression IoU", 0.1, 0.9, value=0.4, step=0.1)

# Load models
try:
    print('before loading the model')
    colorizer = load_model(st.session_state.model_folder, st_color_option)
    print('after loading the model')

except Exception as e: 
    colorizer = None
    print('Error while loading the model. Please refresh the page')
    print(e)
    st_title_message.markdown("**Error while loading the model. Please refresh the page**")

if colorizer is not None:
    st_title_message.markdown("**To begin, please upload an image** 👇")
    
    #Choose your own image
    uploaded_files = st_file_uploader.file_uploader("Upload a black and white photo", 
                                            type=['png', 'jpg', 'jpeg'],
                                            accept_multiple_files=True,
                                            key=f"{st.session_state['uploaded_file_key']}"
                                            )
    
    if uploaded_files:
            
        # # Get only newest elements
        # new_files = uploaded_files[st.session_state.img_counter:]
        # st.session_state.img_counter = len(uploaded_files) - st.session_state.img_counter
        
        if len(uploaded_files) == 1:
            display_single_image(uploaded_files[0], st.session_state.max_img_size)
        elif len(uploaded_files) > 1:
            process_multiple_images(uploaded_files, st.session_state.max_img_size)
        
        st.session_state['uploaded_file_key'] = str(randint(1000, 100000000))  # remove the uploaded file from the UI
        


