#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Raw example """

import io

with io.open('facttypes.proto', 'w') as f:
    f.write(u'''import "base.proto";
import "facttypes_base.proto";

message DrivingLicense: NFactType.TFact
{
    required string Category = 1;
}
''')

with io.open('dic.gzt', 'w') as f:
    f.write(u'''encoding "utf8";
import "base.proto";
import "articles_base.proto";
import "kwtypes_my.proto";
import "facttypes.proto";

TAuxDicArticle "Требования"
{
    key = { "tomita:requirements.cxx" type=CUSTOM }
}

driving_cat "A" { key = "A" | "А" | "А1"| "А1" lemma = "A" }
driving_cat "B" { key = "B" | "В" | "Б" | "B1" | "BE" lemma="B" }
driving_cat "C" { key = "C" | "С" | "Ц" lemma="C" }
driving_cat "C1" { key = "C1" | "С1" | "Ц1" lemma="C1" }
driving_cat "СE" { key = "E" | "Е" | "CE" | "СЕ" | "ЦЕ" lemma="СE" }
driving_cat "С1E" { key = "C1E" | "С1Е" lemma="С1E" }
driving_cat "D" { key = "D" | "Д" lemma="D" }
driving_cat "D1" { key = "D1" | "Д1" lemma="D1" }
driving_cat "DE" { key = "DE" | "ДЕ" lemma="DE" }
driving_cat "D1E" { key = "D1E" | "Д1Е" lemma="D1E" }


''')

with io.open('kwtypes_my.proto', 'w') as f:
    f.write(u'''import "base.proto";
import "articles_base.proto";
//message my_number : TAuxDicArticle {};

message driving_cat : TAuxDicArticle {};

//message city : TAuxDicArticle {}
''')

with io.open('test_dlp.txt', 'w') as f:
    f.write(u'''
Свободна вакансия водителя на а/м КАМАЗ (тягач с бортовым полуприцепом 13,6м, европеец). Требуется водитель с категориями "С", "Е". С опытом работы на грузовом транспорте с полуприцепом не менее трех лет. Полный рабочий день, работа по городу и краю есть всегда. Оплата труда - сдельная.
категория с,д
категория Е
права категории В
права категории В A D
кат А Б Е
кат A B C Д
''')

with io.open('config.proto', 'w') as f:
    f.write(u'''encoding "utf8";
TTextMinerConfig {
  Dictionary = "dic.gzt";       // корневой словарь газеттира
  PrettyOutput = "debug.html";  // файл с отладочным выводом
  Input = {
    File = "test_dlp.txt";          // файл с анализируемым текстом
    Type = dpl;                 // режим чтения
  }

  Articles = [
    { Name = "Требования" }       // Запустить статью корневого словаря
  ]
  Facts = [
    { Name = "ExpFact" }
    { Name = "DrivingLicense" }
  ]
  Output = {
    File = "facts.xml";         // Записать факты в файл "facts.txt"
   // Format = text;              // используя при этом простой текстовый формат
  }
}''')

with io.open('requirements.cxx', 'w') as f:
    f.write(u'''#encoding "utf-8"
    #GRAMMAR_ROOT S


    DC -> AnyWord<kwtype=driving_cat,quoted> | AnyWord<kwtype=driving_cat>;

    DCI -> DC interp (DrivingLicense.Category);

    DELIM -> Comma | 'и' | 'или';

    CAT -> 'категория' | 'кат'(Punct);


    S -> CAT DCI (DELIM) (DCI) (DELIM) (DCI);


    ''')

# !/usr/local/bin/tomita-parser config.proto


import xml.etree.ElementTree as ET
tree = ET.parse('facts.xml')
root = tree.getroot()

values = []
for document in root.findall('document'):
    values.append([child.find('Category').attrib.get('val') for child in document.find('facts').findall('DrivingLicense')])

class TomitaParser(object):
    def __init__(self, directory='/tmp/'):
        self.tomita_path = '/home/dkhodakov/build/tomita-parser/build/bin/tomita-parser'
        pass

    def set_possible_facts(self):
        pass

    def set_main_config(self): # conf 1
        pass

    def set_documents(self, stings):
        pass

    def parse(self):
        return [[], []]

    def set_gazeteer(self):  # gzt 1
        pass

    def set_article(self): # cxx files, N
        pass

    def set_kwtypes_my(self):
        pass

    def set_facttypes(self):
        pass