import tkinter as tk
from tkinter import filedialog
import pandas as pd
import xml.etree.ElementTree as ET
import os

def xml_to_df(xml_path):
    data_dict = {}
    current_path = []

    for event, elem in ET.iterparse(xml_path, events=("start", "end")):
        if event == "start":
            current_path.append(elem.tag)

            # Checking for attributes
            for attr, value in elem.attrib.items():
                tag_name = f"{'_'.join(current_path[-2:])}_{attr}" if len(current_path) > 1 else f"{elem.tag}_{attr}"
                if tag_name not in data_dict:
                    data_dict[tag_name] = []
                data_dict[tag_name].append(value)

        elif event == "end":
            if elem.text and not elem.text.isspace():
                tag_name = '_'.join(current_path[-2:]) if len(current_path) > 1 else current_path[-1]
                if tag_name not in data_dict:
                    data_dict[tag_name] = []
                data_dict[tag_name].append(elem.text.strip())

            current_path.pop()
            elem.clear()

    # Finding the longest list
    max_len = max([len(lst) for lst in data_dict.values()])

    # Making all lists of the same length
    for key, value in data_dict.items():
        data_dict[key] = value + [None] * (max_len - len(value))

    df = pd.DataFrame(data_dict)
    return df

def convert_to_csv():
    xml_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
    if xml_path:
        df = xml_to_df(xml_path)
        csv_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if csv_path:
            df.to_csv(csv_path, index=False)
            label_info.config(text=f'Dönüştürüldü: {csv_path}')

root = tk.Tk()
root.title("XML to CSV Converter")

button_select = tk.Button(root, text="XML Dosyası Seç ve Dönüştür", command=convert_to_csv)
button_select.pack()

label_info = tk.Label(root, text="")
label_info.pack()

root.mainloop()
