import os
import json
import pandas as pd


def extract_text(file_path, output='menu/menu.csv'):

    with open(file_path, 'rb') as f:
        data = json.load(f)

    flattened_data = []

    for category in data['categories']:
        category_name = category['category']
        for item in category['items']:
            flattened_data.append({
                'category': category_name,
                'name': item['name'],
                'price': item['price']
            })

    df = pd.DataFrame(flattened_data)
    df.to_csv(output, index=False)

def make_txt_from_df(file_path='menu/menu.csv', output='menu/menu.txt'):

    text_menu = ''
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        text_menu += row['category'] + ', ' + row['name'] + '\n'

    with open(output, 'w') as f:
        f.write(text_menu)


if __name__ == '__main__':
    json_data = input('Enter path to json data: ')
    os.makedirs('menu', exist_ok=True)
    extract_text(json_data)
    make_txt_from_df()