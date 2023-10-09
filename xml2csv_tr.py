import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_df(xml_path):
    data_dict = {}
    current_path = []

    for event, elem in ET.iterparse(xml_path, events=("start", "end")):
        if event == "start":
            current_path.append(elem.tag)

            # Özellikleri (attributes) kontrol ediyoruz
            for attr, value in elem.attrib.items():
                # Sadece son iki etiketi ve özelliği kullanarak sütun adını oluşturuyoruz
                tag_name = f"{'_'.join(current_path[-2:])}_{attr}" if len(current_path) > 1 else f"{elem.tag}_{attr}"

                if tag_name not in data_dict:
                    data_dict[tag_name] = []
                data_dict[tag_name].append(value)

        elif event == "end":
            if elem.text and not elem.text.isspace():
                # Yine sadece son iki etiketi kullanarak sütun adını oluşturuyoruz
                tag_name = '_'.join(current_path[-2:]) if len(current_path) > 1 else current_path[-1]

                if tag_name not in data_dict:
                    data_dict[tag_name] = []

                data_dict[tag_name].append(elem.text.strip())

            current_path.pop()
            elem.clear()

    # En uzun listeyi bul
    max_len = max([len(lst) for lst in data_dict.values()])

    # Tüm listeleri aynı uzunluğa getir
    for key, value in data_dict.items():
        data_dict[key] = value + [None] * (max_len - len(value))

    df = pd.DataFrame(data_dict)
    return df


xml_path = "rows (2).xml"  # XML dosya yolunuzu bu alana girin
df = xml_to_df(xml_path)
# print(df)

print(df.columns)

# DataFrame'i CSV dosyasına kaydedin
csv_path = "output.csv"  # CSV dosyasının kaydedileceği yol. İstediğiniz bir yol ile değiştirebilirsiniz.
df.to_csv(csv_path, index=False)
print(f"Data has been saved to {csv_path}")