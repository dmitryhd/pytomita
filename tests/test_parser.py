import sys
import os.path as path
import unittest

# Add upper directory to path
current_dir = path.dirname(path.realpath(__file__))
sys.path.append(path.join(current_dir, '..'))

import tomita


class TestParser(unittest.TestCase):

    def setUp(self):
        self.facts = u"""
        import "base.proto";
        import "facttypes_base.proto";
        message DrivingLicense: NFactType.TFact { required string Category = 1; }
        """
        self.keywords = u'''import "base.proto";
        import "articles_base.proto";
        message driving_cat : TAuxDicArticle {};
        '''
        self.gazetteer =u'''encoding "utf8";
        import "base.proto";
        import "articles_base.proto";
        import "kwtypes.proto";
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
        '''
        self.config = u"""
        encoding "utf8";
        TTextMinerConfig {
          Dictionary = "dict.gzt";       // корневой словарь газеттира
          Input = {
            File = "documents_dlp.txt";          // файл с анализируемым текстом
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
            File = "facts.xml";
          }
        }
        """
        self.requirements = u'''#encoding "utf-8"
        #GRAMMAR_ROOT S
        DC -> AnyWord<kwtype=driving_cat,quoted> | AnyWord<kwtype=driving_cat>;
        DCI -> DC interp (DrivingLicense.Category);
        DELIM -> Comma | 'и' | 'или';
        CAT -> 'категория' | 'кат'(Punct);
        S -> CAT DCI (DELIM) (DCI) (DELIM) (DCI);
        '''
        self.documents = [
            'Требуется водитель с категориями "С", "Е"',
            'категория с,д',
            'категория Е',
            'права категории В',
            'права категории В A D',
            'кат А Б Е',
            'ничего тут нет',
            'кат A B C Д',
        ]

    def tearDown(self):
        parser = tomita.TomitaParser()
        parser.clean()

    def test_set_facts(self):
        parser = tomita.TomitaParser()
        parser.set_facts(self.facts)
        self.assertEqual(parser.base_dir, '/tmp')
        fact_path = path.join(parser.base_dir, 'facttypes.proto')
        self.assertTrue(path.isfile(fact_path))

    def test_set_keywords(self):
        parser = tomita.TomitaParser()
        parser.set_keywords(self.keywords)
        self.assertTrue(path.isfile(parser.keywords_file))

    def test_set_gazetteer(self):
        parser = tomita.TomitaParser()
        parser.set_gazetteer(self.gazetteer)
        self.assertTrue(path.isfile(parser.gazetteer_file))

    def test_set_config(self):
        parser = tomita.TomitaParser()
        parser.set_config(self.config)
        self.assertTrue(path.isfile(parser.config_file))

    def test_set_requirements(self):
        parser = tomita.TomitaParser()
        parser.set_requirements(self.requirements)
        self.assertTrue(path.isfile(parser.requirements_file))

    def test_set_documents(self):
        parser = tomita.TomitaParser()
        parser.set_documents(self.documents)
        self.assertTrue(path.isfile(parser.documents_file))

    def get_parser(self):
        parser = tomita.TomitaParser()
        parser.set_facts(self.facts)
        parser.set_config(self.config)
        parser.set_keywords(self.keywords)
        parser.set_gazetteer(self.gazetteer)
        parser.set_requirements(self.requirements)
        parser.set_documents(self.documents)
        return parser

    def test_run(self):
        # TODO: test where tomita returns error in parsing config.
        parser = self.get_parser()
        result_status = parser.run()
        self.assertTrue(result_status)
        self.assertTrue(path.isfile(parser.output_file))

    def test_parse(self):
        parser = self.get_parser()
        result_status = parser.run()
        self.assertTrue(result_status)
        fact_descriptions = {'DrivingLicense': ['Category']}
        res = parser.parse(fact_descriptions)
        expected_result = {
            1: {'Category': ['C', 'СE']},
            2: {'Category': ['C', 'D']},
            3: {'Category': ['СE']},
            4: {'Category': ['B']},
            5: {'Category': ['B', 'A', 'D']},
            6: {'Category': ['A', 'B', 'СE']},
            8: {'Category': ['A', 'B', 'C']}}
        self.assertEqual(res, expected_result)
