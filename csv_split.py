import csv
import kuzukiri


segmenter = kuzukiri.Segmenter()

all_lines = []

with open("../keigo_data/data.csv", encoding='utf-16') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        all_lines.append(row)

# get headers
# for key, value in all_lines[0].items():
#     print(key, value)

new_all_lines = []
task_header_list = ['タスク 1\n[件名] 本文', 'タスク 3\n[件名] 本文', 'タスク 4\n[件名] 本文']

for index_line, line in enumerate(all_lines):
    if line['母語'] == '日本語':
        # print('---------------------------------------------------')
        # print(line['タスク 1\n[件名] 本文'])
        #
        # prune to 依頼タスク (1, 3, 4)

        for task_number, task_name in enumerate(task_header_list):
            task_text = line[task_name]
            print(task_text)

            sentences = segmenter.split(task_text)
            sentences = [x.strip() for x in sentences]
            sentences = [x for x in sentences if x != '']

            print(sentences)

            for sentence in sentences:
                new_dict = {
                    'Person ID': index_line,
                    'Task ID': task_number,
                    'Line': sentence
                }
                new_all_lines.append(new_dict)


with open("../keigo_data/data_for_annotation.csv", 'w') as f:
    fieldnames = ['Person ID', 'Task ID', 'Line', 'Inf']
    writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
    writer.writeheader()
    for line in new_all_lines:
        writer.writerow(line)

print(len(new_all_lines))

print("All done!")