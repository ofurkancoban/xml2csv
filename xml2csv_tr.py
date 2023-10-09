import pandas as pd
import xml.etree.ElementTree as ET
import os

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

# Giriş ve çıktı klasörlerini tanımlayın
input_folder = "input_xml"  # XML dosyalarının bulunduğu klasör yolu
output_folder = "output_csv"  # Çıktı CSV dosyalarının kaydedileceği klasör yolu

# Eğer output klasörü yoksa oluştur
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# input_folder içindeki tüm XML dosyalarını işle
for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):
        xml_path = os.path.join(input_folder, filename)
        df = xml_to_df(xml_path)

        # Dosya adını .xml uzantısından arındırarak .csv uzantısı ekleyin
        csv_filename = f"{filename[:-4]}.csv"
        csv_path = os.path.join(output_folder, csv_filename)

        df.to_csv(csv_path, index=False)
        print(f"Data from {filename} has been saved to {csv_filename}")

print("All files processed!")