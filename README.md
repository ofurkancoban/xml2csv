# ➡️ [Try the XML to CSV Converter](http://xml2csv.streamlit.app) ⬅️
# 🌟 Introducing: XML to CSV Converter Web App! 🌟

We are thrilled to announce the launch of our **brand new web application** that simplifies your data conversion needs! Say goodbye to cumbersome data handling processes and welcome a seamless experience with our XML to CSV Converter.

## 🚀 Features at a Glance:
- **📤 Multi-file Upload**: Convert multiple files at once for efficiency.
- **🚀 Progress Tracking**: Stay updated with a real-time progress bar.
- **🔍 File Size Validation**: Ensure optimal performance with file size checks.
- **🔎 Data Preview**: Peek into your converted data before downloading.
- **💾 Download CSV**: Securely download your converted files in CSV format.

## 🎉 Try it Now!
Get started with your data transformation journey today! Click below to access the web app:

# ➡️ [Try the XML to CSV Converter](http://xml2csv.streamlit.app) ⬅️



# 🔄 XML to CSV Converter Web App
## 📜 Overview
This web application, built with Streamlit, provides a user-friendly interface to convert XML files into CSV format. Users can upload multiple XML files, view the conversion progress, and download the resulting CSV files.

## ✨ Features
- **📤 Multi-file Upload**: Upload and process multiple XML files simultaneously.
- **🚀 Progress Tracking**: View the progress of file conversion with a progress bar.
- **🔍 File Size Validation**: Ensures files are within the acceptable size limit (20 MB(You can change the limit from config.toml file.)).
- **🔎 Data Preview**: Preview the converted data before downloading.
- **💾 Download CSV**: Download the converted files as CSV directly from the app.

## 🚀 How to Use
1. Run the app using `streamlit run xml2csv_webapp.py`.
2. Upload one or more XML files using the file uploader.
3. Monitor the progress bar as the app processes the files.
4. Download the resulting CSV files once processing is complete.

## 🔧 Running the App
Ensure you have Streamlit and other necessary libraries installed. Run the app with the following command:

```shell
streamlit run xml2csv_webapp.py
```


--------------------



![xml2csv](https://github.com/ofurkancoban/xml2csv/blob/master/img/xml2csv.gif)
# 📌This script automatically assigns the tags and attributes of XML files to the columns of a Dataframe and converts them into CSV files.

# Automated Data Transformation: From XML to CSV

XML (Extensible Markup Language), with its inherent hierarchical structure, is widely adopted for data storage and transportation. The nested nature of tags combined with their attributes offers rich expressiveness, making XML suitable for various applications. However, for data analysis and visualization, a more tabular structure, like CSV (Comma-Separated Values), is often preferred. Transitioning from XML to CSV can pose challenges due to the complexities within XML structures. The provided Python script streamlines this transformation process by leveraging automation.

### **1. The Intricacies of XML**

XML's strength lies in its structure. Tags can have nested tags, and each tag can have attributes. For instance:

```xml
<release id="31070">
    <artist>
        <id>5844</id>
        <name>Erkin Koray</name>
    </artist>
</release>
```

Here, **`release`** is a parent tag with an attribute **`id`**, and nested within it is another tag, **`artist`**, that also holds data.

### **2. The Power of Automated Parsing**

The brilliance of the provided Python script lies in its ability to navigate the intricacies of XML.

**a. Hierarchical Parsing & Dynamic Column Creation**

The code moves iteratively through the XML hierarchy, capturing every piece of information. For every tag it encounters, the script checks for attributes, forming unique DataFrame columns, like **`release_id`**. The textual content within tags is also captured, each getting its designated column.

**b. Handling Nested Structures**

By maintaining a path throughout its parsing journey, the script identifies nesting levels, ensuring nested data is uniquely represented. For example, the **`id`** inside an **`artist`** tag becomes **`artist_id`**.

### **3. The Value of Automated Extraction**

**a. Flexibility**

Regardless of the XML's complexity, the code remains adaptive. It doesn't need a predefined schema but rather molds itself based on the input.

**b. Data Integrity**

Every tag and attribute from the XML is captured with precision, ensuring no data loss and maintaining high data integrity.

**c. Efficiency**

Relying on predefined structures can lead to errors and missed data points. In contrast, automated extraction guarantees swift and accurate conversions, saving both time and effort.

### **4. Benefits of the CSV Format**

**a. Accessibility**

Almost every data processing tool supports CSV, from Excel to SQL databases and programming libraries.

**b. Simplified Analysis**

With data in a tabular format, analyses become straightforward. Libraries like Pandas in Python further simplify operations on CSV data.

**c. Storage Efficiency**

Compared to XML's verbose nature, CSV usually results in more compact file sizes, making data storage more efficient.

---
Thank you for reading, and I look forward to engaging with the community further!
