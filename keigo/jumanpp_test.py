from pyknp import Juman, MList, Morpheme, KNP, BList
from kotodama import kotodama

def preprocess(text: str) -> str:
    text = text.replace(" ", "")
    text = text.replace("   ", "")
    text = text.replace("＃", "")
    text = text.replace("#", "")
    return text

def juman_parse(text) -> MList:
    text = preprocess(text)
    try:
        juman = Juman("jumanpp", multithreading=True)
        parse_result = juman.analysis(text)
    except:
        print("jumanpp error!")
        print(text)
        raise SyntaxError
    return parse_result

def knp_parse(text) -> BList:
    text = preprocess(text)
    try:
        knp = KNP()
        parse_result = knp.parse(text)
    except:
        print("KNP error!")
        print(text)
        raise SyntaxError
    return parse_result

def print_mlist(mlist):
    for morpheme in mlist:
        print(morpheme.genkei, morpheme.midasi, morpheme.yomi, morpheme.hinsi, morpheme.bunrui, morpheme.fstring)

def keigo_pipe(sentence: MList):
    new_sent = []
    for index, morpheme in enumerate(sentence):
        if morpheme.hinsi == '名詞':
            new_sent.append(meishi_process(sentence, index, morpheme))
        elif morpheme.hinsi == '動詞':
            new_sent.append(doushi_process(sentence, index, morpheme))
        elif morpheme.hinsi == '助動詞':
            new_sent.append(jodoushi_process(sentence, index, morpheme))
        elif morpheme.hinsi in ['接尾辞', '動詞性接尾辞','判定詞']:
            new_sent.append(setsubiji_process(sentence, index, morpheme))
        else:
            new_sent.append(morpheme.midasi)

    return new_sent

def meishi_process(sentence, index, word: Morpheme) -> str:
    out_str = ''
    out_str = word.midasi
    return out_str

def doushi_process(sentence, index, word: Morpheme) -> str:
    out_str = ''
    aux_verb = {"です・ます"}
    verb = word.genkei
    try:
        out_str = kotodama.transformVerb(verb, aux_verb)
    except ValueError:
        out_str = word.midasi
    return out_str

def jodoushi_process(sentence, index, word: Morpheme) -> str:
    out_str = ''
    out_str = word.midasi
    return out_str

def setsubiji_process(sentence, index, word: Morpheme) -> str:
    out_str = word.midasi
    if index > 0:
        if sentence[index - 1].hinsi == '動詞' and word.midasi in ['だ', 'だった', 'です', 'でした', 'ます', 'ました', 'る']:
            out_str = ''
        elif sentence[index - 1].hinsi == '名詞':
            if word.midasi in ['だ']:
                out_str = 'です'
            elif word.midasi in ['だった']:
                out_str = 'でした'

    return out_str

test_juman = juman_parse("私は彼と一緒に本を読んだ。")
test_knp = knp_parse("私は彼と一緒に本を読んだ。")

#
# test_sent = juman_parse("田中さんにあげる。")
# print_mlist(test_sent)
#
# keigo_sent = keigo_pipe(test_sent)
# print(keigo_sent)
#
# keigo_sent = keigo_pipe(juman_parse("田中さんにあげました。"))
# print(keigo_sent)

orig_sent = "ドアの鍵をかける。"
print('Input:', orig_sent)

keigo_sent = keigo_pipe(juman_parse(orig_sent))
print('Keigo:', ''.join(keigo_sent), '(', keigo_sent, ')')