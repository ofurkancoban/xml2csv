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

    # Finding the longest list in the dictionary and padding lists to equal length
    max_len = max(len(lst) for lst in data_dict.values())
    for lst in data_dict.values():
        lst.extend([None] * (max_len - len(lst)))

    return pd.DataFrame(data_dict)

# Initialize your Streamlit application
st.title('📁 Multiple XML to CSV Converter')

# Display social media accounts with FontAwesome icons
st.markdown("""
    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <a href="https://github.com/YOUR_USERNAME" target="_blank">
            <i class="fab fa-github fa-2x"></i>
        </a>
        <a href="https://www.linkedin.com/in/YOUR_USERNAME" target="_blank">
            <i class="fab fa-linkedin fa-2x"></i>
        </a>
        <a href="https://www.kaggle.com/YOUR_USERNAME" target="_blank">
            <i class="fab fa-kaggle fa-2x"></i>
        </a>
    </div>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Choose XML files", accept_multiple_files=True, type=['xml'])

if uploaded_files:
    progress_bar = st.progress(0)
    percentage_text = st.empty()

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
        percentage_text.markdown(f"<h2 style='text-align: left; color: white;'>Processing: {index}/{total_files} files ({progress}%)</h2>", unsafe_allow_html=True)

    for file_name, df in dataframes.items():
        rows, cols = df.shape  # Get the number of rows and columns
        with st.container():
            col1, col2 = st.columns([0.8, 0.2])

            with col1:
                st.subheader(f"{file_name} - Rows: {rows}, Columns: {cols}")

            with col2:
                st.download_button(
                    label="Download CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name=f'{file_name[:-4]}.csv',
                    mime='text/csv'
                )

            with st.expander("🔍 View Data"):
                st.dataframe(df)

# Note: To run this script, save it as a .py file and use the command: streamlit run your_script_name.py
