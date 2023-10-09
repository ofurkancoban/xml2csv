import pandas as pd
import xml.etree.ElementTree as ET

def xml_to_df(xml_path):
    data_dict = {}
    current_path = []

    for event, elem in ET.iterparse(xml_path, events=("start", "end")):
        if event == "start":
            current_path.append(elem.tag)

            # Checking attributes
            for attr, value in elem.attrib.items():
                # Creating column name using last two tags and attribute, if available
                tag_name = f"{'_'.join(current_path[-2:])}_{attr}" if len(current_path) > 1 else f"{elem.tag}_{attr}"

                if tag_name not in data_dict:
                    data_dict[tag_name] = []
                data_dict[tag_name].append(value)

        elif event == "end":
            if elem.text and not elem.text.isspace():
                # Again, creating column name using last two tags
                tag_name = '_'.join(current_path[-2:]) if len(current_path) > 1 else current_path[-1]

                if tag_name not in data_dict:
                    data_dict[tag_name] = []

                data_dict[tag_name].append(elem.text.strip())

            current_path.pop()
            elem.clear()

    # Finding the longest list
    max_len = max([len(lst) for lst in data_dict.values()])

    # Making all lists the same length
    for key, value in data_dict.items():
        data_dict[key] = value + [None] * (max_len - len(value))

    df = pd.DataFrame(data_dict)
    return df

xml_path = "rows.xml"  # Insert your XML file path here
df = xml_to_df(xml_path)
# print(df)

print(df.columns)

# Save DataFrame to a CSV file
csv_path = "output.csv"  # Path where CSV file will be saved. You can change it to a path of your choice.
df.to_csv(csv_path, index=False)
print(f"Data has been saved to {csv_path}")
