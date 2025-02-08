#get translated category and item
# get description
# get price
import json
import pandas as pd


def construct_menu(initial_file, eng_file, descr_file, output_file='eng_menu.json'):
    price = pd.read_csv(initial_file)['price']
    eng_cat_item = pd.read_csv(eng_file)
    descriptions = pd.read_csv(descr_file)['description']

    eng_cat_item['price'] = price
    eng_cat_item['description'] = descriptions

    # Convert to JSON structure
    result = {
        'categories': [
            {
                'category': category,
                'items': group[['item', 'price', 'description']].rename(columns={'item': 'name'}).to_dict('records')
            }
            for category, group in eng_cat_item.groupby('category')
        ],
        'restaurant_name': "VIVA TIKILA"
    }
    with open(output_file,'w') as f:
        json.dump(result, f)

    print('Menu constructed!')

    

if __name__ == '__main__':
    construct_menu('menu/menu.csv', 'menu/eng_menu.csv', 'menu/eng_descr.csv')