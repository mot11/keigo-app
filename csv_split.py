import csv

all_lines = []

with open("../keigo_data/data.csv", encoding='utf-16') as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        all_lines.append(row)

# get headers
# for key, value in all_lines[0].items():
#     print(key, value)

new_all_lines = []
for line in all_lines:
    if line['母語'] == '日本語':
        # print('---------------------------------------------------')
        # print(line['タスク 1\n[件名] 本文'])
        #
        # prune to 依頼タスク (1, 3, 4)
        new_dict = {
            'Task 1': line['タスク 1\n[件名] 本文'],
            'Task 3': line['タスク 3\n[件名] 本文'],
            'Task 4': line['タスク 4\n[件名] 本文']
        }
        new_all_lines.append(new_dict)


with open("../keigo_data/data_for_annotation.csv", 'w') as f:
    fieldnames = ['Task 1', 'Task 1 Inf', 'Task 3', 'Task 3 Inf', 'Task 4', 'Task 4 Inf']
    writer = csv.DictWriter(f, fieldnames=fieldnames, restval='')
    writer.writeheader()
    for line in new_all_lines:
        writer.writerow(line)

print(len(new_all_lines))

print("All done!")