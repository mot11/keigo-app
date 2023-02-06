from pathlib import Path
import pickle
import Mykytea
import evaluate


def eval_conjugator():
    conjugated_pkl_path = 'data/pred_all.pkl'

    # load, organize, and tokenize data
    with open(conjugated_pkl_path, 'rb') as f:
        all_emails = pickle.load(f)

    mk = Mykytea.Mykytea("")

    # for email_dict in all_emails:
    #     print('------------------------')
    #     print(email_dict['Form_kyt'])
    #     print('------------------------')
    #     print(email_dict['Conjugator_polite_pred'])

    # dump results and calculate bleu

    sacrebleu = evaluate.load("sacrebleu")


    for email_dict in all_emails:
        print('='*20)
        [print(line) for line in email_dict['Form']]
        print('-' * 20)
        [print(line) for line in email_dict['Inf']]
        print('=' * 20)

    task_emails_count = {0: {}, 1: {}, 2: {}}
    for key, value in task_emails_count.items():
        value['emails'] = 0
        value['lines'] = 0
        value['form_length'] = 0
        value['inf_length'] = 0

    for email_dict in all_emails:
        task_emails_count[email_dict['Task ID']]['emails'] += 1
        task_emails_count[email_dict['Task ID']]['lines'] += len(email_dict['Form'])
        task_emails_count[email_dict['Task ID']]['form_length'] += sum([len(x) for x in email_dict['Form']])
        task_emails_count[email_dict['Task ID']]['inf_length'] += sum([len(x) for x in email_dict['Inf']])


    print(task_emails_count)


    for email_dict in all_emails:
        if 'GPT_pred_kyt' not in email_dict:
            email_dict['GPT_pred_kyt'] = []
            email_dict['GPT_pred_kyt_ignore_short_long'] = []

            for line_id, line in enumerate(email_dict['GPT_pred']):
                gpt_kyt_tokens = mk.getWS(line)
                gpt_kyt_line = ' '.join(gpt_kyt_tokens)
                email_dict['GPT_pred_kyt'].append(gpt_kyt_line)

                # replace with inf_kyt if length is less than 50% or longer than 200% (and above 10 characters)
                inf_tokens = email_dict['Inf_kyt'][line_id].split()
                if len(inf_tokens) > len(gpt_kyt_tokens)*2 or (len(inf_tokens)*2 < len(gpt_kyt_tokens) and len(gpt_kyt_tokens) > 10):
                    email_dict['GPT_pred_kyt_ignore_short_long'].append(email_dict['Inf_kyt'][line_id])
                else:
                    email_dict['GPT_pred_kyt_ignore_short_long'].append(gpt_kyt_line)


    for task_no in (0, 1, 2):
        for conj_type in ('Conjugator_polite_pred', 'Conjugator_formal_pred', 'Inf_kyt', 'GPT_pred_kyt', 'GPT_pred_kyt_ignore_short_long'):

            gold_sent, pred_sent = dump_all(all_emails, 'Form_kyt', conj_type, task_no)
            results = sacrebleu.compute(predictions=pred_sent, references=gold_sent, tokenize='none')
            print(task_no, conj_type, results)



def dump_all(all_emails, gold, pred, task):
    gold_sent = []
    pred_sent = []
    for email_dict in all_emails:
        if email_dict['Task ID'] == task:
            gold_sent.extend(email_dict[gold])
            pred_sent.extend(email_dict[pred])

    return gold_sent, pred_sent



if __name__ == '__main__':
    eval_conjugator()
