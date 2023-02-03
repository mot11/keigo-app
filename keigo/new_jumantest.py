from pyknp import Juman, MList, Morpheme, KNP, BList

text = "これはテストです。"
knp = KNP()
parse_result = knp.parse(text)

print(parse_result)
p