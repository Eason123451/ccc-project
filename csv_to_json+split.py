import pandas as pd
import json
import math

def csv_to_json_split(csv_file, json_prefix, num_parts):
    df = pd.read_csv(csv_file)

    total_rows = len(df)
    rows_per_part = math.ceil(total_rows / num_parts)
    parts = [df[i:i + rows_per_part] for i in range(0, total_rows, rows_per_part)]

    for i, part in enumerate(parts):
        json_file = f"{json_prefix}_{i+1}.json"
        part.to_json(json_file, orient='records', indent=4)

csv_file = "C:\\Users\\Windows\\Desktop\\ccc\\es twitter\\tweets_cleaned.csv"
json_prefix = "C:\\Users\\Windows\\Desktop\\ccc\\es twitter\\cleaned_json_twiiter_data_part"
num_parts = 9

csv_to_json_split(csv_file, json_prefix, num_parts)
