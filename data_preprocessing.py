import pandas as pd
import unicodedata
import pickle
from pathlib import Path

excel_input_path = 'data/data_for_annotation.xlsx'
pickle_output_path = 'data/annotated_preprocessed.pkl'

# read excel and convert to list of dictionaries
df = pd.read_excel(excel_input_path)
df_dict = df.to_dict(orient='index')
df_list = [value for _, value in df_dict.items()]

# divide into individual emails
df_emails_list = []
email_lines = []
person_id = df_list[0]['Person ID']
task_id = df_list[0]['Task ID']
for line_dict in df_list:
    if line_dict['Person ID'] != person_id or line_dict['Task ID'] != task_id:
        df_emails_list.append(email_lines)
        email_lines = []
        person_id = line_dict['Person ID']
        task_id = line_dict['Task ID']
    email_lines.append(line_dict)

df_emails_list.append(email_lines)

# remove certain lines
new_df_emails_list = []
for email_lines in df_emails_list:
    new_email_lines = []
    for line_dict in email_lines:
        add_line = True
        if line_dict['Line'].startswith('学籍番号'):
            add_line = False
        elif unicodedata.normalize('NFKC', line_dict['Line']).isdigit():
            add_line = False

        if add_line:
            new_email_lines.append(line_dict)
    new_df_emails_list.append(new_email_lines)

df_emails_list = new_df_emails_list

# Concat sentences spanning multiple lines
new_df_emails_list = []
for email_lines in df_emails_list:
    title_concat = False
    is_title = False
    sent_concat = False

    sent_endings = ['。', '！', '？']
    concat_formal = ''
    concat_informal = ''
    concat_span = []

    all_concats = {}
    for index, line_dict in enumerate(email_lines):
        is_title = False
        if not (title_concat or sent_concat):
            if line_dict['Line'][0] == '[' and line_dict['Line'][-1] != ']':
                title_concat = True
            elif line_dict['Line'][0] == '[':
                is_title = True
            elif line_dict['Line'][-1] not in sent_endings and len(line_dict['Line']) > 10:
                sent_concat = True

        if title_concat or sent_concat:
            concat_span.append(index)
            concat_formal += line_dict['Line']
            concat_informal += line_dict['Inf']

            if title_concat and line_dict['Line'][-1] == ']':
                title_concat = False
            elif sent_concat and line_dict['Line'][-1] in sent_endings:
                sent_concat = False

            # if we end the concat here:
            if not (title_concat or sent_concat):
                all_concats[tuple(concat_span)] = {'form': concat_formal, 'inf': concat_informal}
                concat_formal = ''
                concat_informal = ''
                concat_span = []

    # do the concatting of spans
    # for index, line_dict in enumerate(email_lines):
    #     if index
    for span, forms in all_concats.items():
        email_lines[span[0]]['Line'] = forms['form']
        email_lines[span[0]]['Inf'] = forms['inf']
        for span_index in span[1:]:
            email_lines[span_index] = None

    new_df_emails_list.append([line for line in email_lines if line is not None])

df_emails_list = new_df_emails_list

[[print(s['Line'] + '\n- ' + s['Inf']) for s in email_lines] for email_lines in df_emails_list]

# remove title brackets
for email_lines in df_emails_list:
    for line_dict in email_lines:
        line_dict['Line'] = line_dict['Line'].replace('[', '')
        line_dict['Line'] = line_dict['Line'].replace(']', '')
        line_dict['Inf'] = line_dict['Inf'].replace('[', '')
        line_dict['Inf'] = line_dict['Inf'].replace(']', '')

# reorganize lines

all_emails = []
for email_lines in df_emails_list:
    email_dict = {'Task ID': email_lines[0]['Task ID'], 'Form': [], 'Inf': []}
    for line_dict in email_lines:
        email_dict['Form'].append(line_dict['Line'])
        email_dict['Inf'].append(line_dict['Inf'])
    all_emails.append(email_dict)

# save to pickle
if pickle_output_path != '':
    pkl_path = Path(pickle_output_path)
    if pkl_path.exists():
        print("Output pickle already exists.")
    else:
        print("Saving pickle...")
        with open(pickle_output_path, 'wb') as f:
            pickle.dump(all_emails, f)
