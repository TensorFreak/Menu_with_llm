import argparse
import os
from groq import Groq
from datetime import datetime

import pandas as pd

from dotenv import load_dotenv


def parse_translation(text, translated_df_path='menu/eng_menu.csv'):
    rows = text.split('\n')
    categories, items = [], []
    for row in rows:
        if len(row) > 10: # skip empty rows
            cat = row[:row.find(',')]
            item = row[row.find(',') + 1: ].strip()
            categories.append(cat)
            items.append(item)

    df = pd.DataFrame.from_dict({'category': categories, 'item': items})
    df.to_csv(translated_df_path, index=False)


def parse_description(text, descriptions_path='menu/eng_descr.csv'):
    rows = text.split('\n')
    descriptions = []
    for row in rows:
        if len(row) > 10: # skip empty rows
            descr = row[row.find('-') + 1: ].strip()
            descriptions.append(descr)

    df = pd.DataFrame.from_dict({'description': descriptions})
    df.to_csv(descriptions_path, index=False)
    


def ask_llm(input_file, task):

    os.makedirs('menu/' + task, exist_ok=True)

    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found")
        return

    load_dotenv()

    api_qroq_key = os.getenv('API_GROQ_KEY')
    client = Groq(api_key=api_qroq_key)

    task_prompt_path = 'prompts/' + task + '/' + os.listdir('prompts/' + task)[0]
    with open(task_prompt_path, 'r') as f:
        system_prompt = f.read()

    try:
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0,
            max_tokens=4000,
            top_p=1,
            stream=False,
            stop=None,
        )

        answer = completion.choices[0].message.content

        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = os.path.basename(input_file).split('.')[0]
        output_file = os.path.join('menu/' + task, f"{base_name}_{task}.txt")

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(answer)

        print(f"Task {task} complete! Saved to: {output_file}")
        
        if task == 'translation':
            parse_translation(answer)
        if task == 'description':
            parse_description(answer)

    except Exception as e:
        print(f"Error during {task}: {str(e)}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="ask llm script")
    parser.add_argument("--task", choices=["translation", "description"], help="The task to execute")
    parser.add_argument("--text", help='File to use')
    args = parser.parse_args()

    ask_llm(args.text, args.task)