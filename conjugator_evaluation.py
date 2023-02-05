from pathlib import Path
import pickle
import Mykytea
import evaluate


def eval_conjugator():
    conjugated_pkl_path = 'data/conjugated_pred.pkl'

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

    for task_no in (0, 1, 2):
        for conj_type in ('Conjugator_polite_pred', 'Conjugator_formal_pred', 'Inf_kyt'):
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
