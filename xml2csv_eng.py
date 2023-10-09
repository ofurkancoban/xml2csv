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
                # Constructing column name using the last two tags and the attribute, if available
                tag_name = f"{'_'.join(current_path[-2:])}_{attr}" if len(current_path) > 1 else f"{elem.tag}_{attr}"

                if tag_name not in data_dict:
                    data_dict[tag_name] = []
                data_dict[tag_name].append(value)

        elif event == "end":
            if elem.text and not elem.text.isspace():
                # Again, constructing column name using the last two tags
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

# Defining input and output folders
input_folder = "input_xml"  # Path to the folder containing XML files
output_folder = "output_csv"  # Path to the folder where CSV files will be saved

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Process all XML files in the input_folder
for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):
        xml_path = os.path.join(input_folder, filename)
        df = xml_to_df(xml_path)

        # Stripping the .xml extension and adding .csv
        csv_filename = f"{filename[:-4]}.csv"
        csv_path = os.path.join(output_folder, csv_filename)

        df.to_csv(csv_path, index=False)
        print(f"Data from {filename} has been saved to {csv_filename}")

print("All files processed!")
