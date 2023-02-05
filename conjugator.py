from subprocess import run, PIPE
import Mykytea
import pickle
from pathlib import Path


def main():
    test_lines = ['半分に切った。', '明日も晴れるだろう。', '私の名前は田中だ。']
    kytea_test_lines = []
    new_test_lines = []
    mk = Mykytea.Mykytea("")
    for line in test_lines:
        kytea_tokenized = mk.getTagsToString(line)
        kytea_test_lines.append(' '.join(mk.getWS(line)))
        p = run(['python', 'japanese-verb-conjugator/conjugator.py', '-f', 'polite'], stdout=PIPE, input=kytea_tokenized, encoding='utf-8')
        new_line = p.stdout
        new_test_lines.append(new_line.strip())

    print(test_lines)
    print(kytea_test_lines)
    print(new_test_lines)


def run_conjugator():
    annotated_pkl_path = 'data/annotated_preprocessed.pkl'
    conjugated_pkl_path = 'data/conjugated_pred.pkl'

    # load, organize, and tokenize data
    with open(annotated_pkl_path, 'rb') as f:
        all_emails = pickle.load(f)

    mk = Mykytea.Mykytea("")
    for email_dict in all_emails:
        email_dict['Form_kyt'] = []
        email_dict['Inf_kyt'] = []
        email_dict['Conjugator_polite_pred'] = []
        email_dict['Conjugator_formal_pred'] = []
        for line_index in range(len(email_dict['Form'])):

            # tokenize
            form_line = email_dict['Form'][line_index]
            email_dict['Form_kyt'].append(' '.join(mk.getWS(form_line)))

            inf_line = email_dict['Inf'][line_index]
            inf_tokenized = mk.getTagsToString(inf_line)
            email_dict['Inf_kyt'].append(' '.join(mk.getWS(inf_line)))

            # run rule-based formality converter
            p = run(['python', 'japanese-verb-conjugator/conjugator.py', '-f', 'polite'], stdout=PIPE,
                    input=inf_tokenized, encoding='utf-8')
            new_line = p.stdout
            email_dict['Conjugator_polite_pred'].append(new_line.strip())

            p = run(['python', 'japanese-verb-conjugator/conjugator.py', '-f', 'formal'], stdout=PIPE,
                    input=inf_tokenized, encoding='utf-8')
            new_line = p.stdout
            email_dict['Conjugator_formal_pred'].append(new_line.strip())

    # save to pickle
    if conjugated_pkl_path != '':
        pkl_path = Path(conjugated_pkl_path)
        if pkl_path.exists():
            print("Output pickle already exists.")
        else:
            print("Saving pickle...")
            with open(conjugated_pkl_path, 'wb') as f:
                pickle.dump(all_emails, f)


if __name__ == '__main__':
    # main()
    run_conjugator()
