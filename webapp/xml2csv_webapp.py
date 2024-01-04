import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import os
import tempfile

# Function to convert XML to DataFrame
def xml_to_df(xml_path):
    data_dict = {}
    current_path = []

    for event, elem in ET.iterparse(xml_path, events=("start", "end")):
        if event == "start":
            current_path.append(elem.tag)
            for attr, value in elem.attrib.items():
                tag_name = f"{'_'.join(current_path[-2:])}_{attr}" if len(current_path) > 1 else f"{elem.tag}_{attr}"
                if tag_name not in data_dict:
                    data_dict[tag_name] = []
                data_dict[tag_name].append(value)

        elif event == "end":
            if elem.text and not elem.text.isspace():
                tag_name = '_'.join(current_path) if current_path else elem.tag
                if tag_name not in data_dict:
                    data_dict[tag_name] = []
                data_dict[tag_name].append(elem.text.strip())
            current_path.pop()
            elem.clear()

    max_len = max(len(lst) for lst in data_dict.values())
    for lst in data_dict.values():
        lst.extend([None] * (max_len - len(lst)))

    return pd.DataFrame(data_dict)


# Set page to wide mode as default
st.set_page_config(
    layout="wide",
    page_title="XML2CSV by ofurkancoban",
    page_icon="🇹🇷"
)

def add_hover_effects():
    st.markdown("""
        <style>
            a img { 
                transition: transform 0.2s ease; /* Smooth transition */
            }
            a img:hover {
                transform: scale(2); /* Slightly enlarge the icon */
                opacity: 0.7; /* Make the icon a bit transparent */
            }
        </style>
        """, unsafe_allow_html=True)

# Apply the custom CSS for hover effects
add_hover_effects()
def add_title_hover_effect():
    st.markdown("""
        <style>
            /* Custom style for the main title with class 'title-hover' */
            .title-hover{
                 transition: transform 0.2s ease; /* Smooth transition */
            }
            .title-hover:hover {
                transform: scale(1.3); /* Slightly enlarge the icon */
                opacity: 0.7; /* Make the icon a bit transparent */
            }
        </style>
        """, unsafe_allow_html=True)

# Apply the custom CSS for hover effects
add_title_hover_effect()


# Custom CSS to inject larger fonts
def set_font(font_name):
    st.markdown(f"""
    <style>
        html, body, [class*="st-"] {{
            font-family: '{font_name}', sans-serif;
        }}
        h1 {{
            text-align: center;
        }}
    </style>
    """, unsafe_allow_html=True)
# Set font for entire app
set_font("Verdana")



# Initialize Streamlit application
st.markdown('<div class="title-hover" style="text-align: center;font-size:300%;margin-bottom: 40px"><b>XML to CSV Converter</b></div>', unsafe_allow_html=True)

# Social media information
icons = {
    "GitHub": "https://raw.githubusercontent.com/ofurkancoban/xml2csv/master/img/github.png",  # Replace with your GitHub icon or URL
    "LinkedIn": "https://raw.githubusercontent.com/ofurkancoban/xml2csv/master/img/linkedin-in.png",  # Replace with your LinkedIn icon or URL
    "Kaggle": "https://raw.githubusercontent.com/ofurkancoban/xml2csv/master/img/kaggle.png"  # Replace with your Kaggle icon or URL
}

urls = [
    "https://github.com/ofurkancoban",
    "https://www.linkedin.com/in/ofurkancoban",
    "https://www.kaggle.com/ofurkancoban"
]

# Centering the icons
cols = st.columns([1, 1, 1, 1])
icon_cols = [cols[1], cols[2], cols[3]]  # Pick the middle columns for icons
for col, (name, icon_path), url in zip(icon_cols, icons.items(), urls):
    with col:
        st.markdown(f"<a href='{url}' target='_blank'><img src='{icon_path}' width='30'></a>", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Choose XML files", accept_multiple_files=True, type=['xml'])

# Check file size for each uploaded file
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Check file size (Streamlit uploads files as BytesIO objects)
        size_mb = uploaded_file.size / (1024 * 1024)  # Convert bytes to MB
        if size_mb > 20:
            st.error(f"File {uploaded_file.name} is too large ({size_mb:.2f} MB). Please upload files smaller than 20 MB.")
            continue  # Skip this file and move to the next one


if uploaded_files:
    progress_bar = st.progress(0)
    percentage_text = st.empty()
    line = st.markdown("_______________________________________________________")
dataframes = {}

if uploaded_files:
    total_files = len(uploaded_files)
    for index, uploaded_file in enumerate(uploaded_files, start=1):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xml") as tmpfile:
            tmpfile.write(uploaded_file.getbuffer())
            temp_file_path = tmpfile.name

        df = xml_to_df(temp_file_path)
        dataframes[uploaded_file.name] = df
        os.remove(temp_file_path)

        progress = int((index / total_files) * 100)
        progress_bar.progress(progress)
        percentage_text.markdown(f"<div style='text-align: left;font-size:200%'><b>Processing: {index}/{total_files} files ({progress}%)</b></div>", unsafe_allow_html=True)
        line.markdown(f"------------------------------------",
            unsafe_allow_html=True)

    for file_name, df in dataframes.items():
        rows, cols = df.shape  # Get the number of rows and columns
        with st.container():
            col1, col2 = st.columns([0.80, 0.20])

            with col1:
                # Display file name
                st.markdown(f"<div style=font-size:150%> {file_name}</div>", unsafe_allow_html=True)

            with col2:  # Download button in the far right
                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name=f'{file_name[:-4]}.csv',
                    mime='text/csv',
                    use_container_width = True
                )

            with st.expander(f"🔍  View Data - [ Rows: {rows} x Columns: {cols} ]"):
                st.dataframe(df)


# streamlit run xml2csv_webapp.py