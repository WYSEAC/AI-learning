import csv
import os

data_dir = os.path.join(os.path.dirname(__file__), '招聘原始数据')
filename = 'zhaopin_上海_agent_20260517_165853.csv'
file_path = os.path.join(data_dir, filename)

print(f"Testing file: {file_path}")
print()

with open(file_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    print("Headers:", reader.fieldnames)
    print()
    for i, row in enumerate(reader):
        print(f"Row {i}:")
        for key, value in row.items():
            print(f"  {key}: {repr(value[:50]) if value else 'EMPTY'}")
        if i >= 2:
            break
