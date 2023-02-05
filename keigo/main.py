from subprocess import run, PIPE
import Mykytea


def main():

    test_lines = ['半分に切った。', '明日も晴れるだろう。', '私の名前は田中だ。']
    kytea_test_lines = []
    new_test_lines = []
    mk = Mykytea.Mykytea("")
    for line in test_lines:
        kytea_tokenized = mk.getTagsToString(line)
        kytea_test_lines.append(' '.join(mk.getWS(line)))
        p = run(['python', '../japanese-verb-conjugator/conjugator.py', '-f', 'polite'], stdout=PIPE, input=kytea_tokenized, encoding='utf-8')
        new_line = p.stdout

        new_test_lines.append(new_line.strip())

    print(test_lines)
    print(kytea_test_lines)
    print(new_test_lines)




if __name__ == '__main__':
    main()
