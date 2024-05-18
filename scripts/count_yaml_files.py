import os
import re
from collections import defaultdict

spec_dir = 'fission/specs'

file_counts = defaultdict(int)
file_names = defaultdict(list)

for root, dirs, files in os.walk(spec_dir):
    for file in files:
        if file.endswith('.yaml'):
            match = re.match(r'(\w+)-\w+\.yaml', file)
            if match:
                file_type = match.group(1)
                file_counts[file_type] += 1
                file_names[file_type].append(file)

for file_type, count in file_counts.items():
    print(f'{file_type}: {count}')
    for name in file_names[file_type]:
        print(f'  - {name}')


