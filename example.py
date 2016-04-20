# -*- coding: utf-8 -*-

import tomita


fact_descriptions = {'DrivingLicense': ['Category']}

facts = u"message DrivingLicense: NFactType.TFact { required string Category = 1; }"

keywords = u'message driving_cat : TAuxDicArticle {};'

gazetteer = u'''
TAuxDicArticle "Требования"
{ key = { "tomita:requirements.cxx" type=CUSTOM } }

driving_cat "A" { key = "A" | "А" | "А1"| "А1" lemma = "A" }
driving_cat "B" { key = "B" | "В" | "Б" | "B1" | "BE" lemma="B" }
'''

config = u'''
Articles = [ { Name = "Требования" } ]
Facts = [
{ Name = "ExpFact" }
{ Name = "DrivingLicense" }
]
'''

requirements = u'''
#GRAMMAR_ROOT S
DC -> AnyWord<kwtype=driving_cat,quoted> | AnyWord<kwtype=driving_cat>;
DCI -> DC interp (DrivingLicense.Category);
DELIM -> Comma | 'и' | 'или';
CAT -> 'категория' | 'кат'(Punct);
S -> CAT DCI (DELIM) (DCI) (DELIM) (DCI);
'''

# Setup
parser = tomita.TomitaParser()
parser.set_facts(facts)
parser.set_config(config)
parser.set_keywords(keywords)
parser.set_gazetteer(gazetteer)
parser.set_fact_file(requirements, 'requirements.cxx')

# Pass data
documents = [
    u'Требуется водитель с категориями "A", "B"',  # document_id = 0
    u'ничего тут нет',                             # document_id = 1
    u'кат Б',                                      # document_id = 2
]
parser.set_documents(documents)
parser.run()
result = parser.parse(fact_descriptions)
print(result)

# {1: {'Category': ['A', 'B']}, 3: {'Category': ['B']}}

parser.clean()
