import os
import os.path as path
from io import open
from contextlib import suppress
# parser.

class TomitaParser(object):
    def __init__(self, directory='/tmp'):
        self.tomita_path = '/home/dkhodakov/build/tomita-parser/build/bin/tomita-parser'
        self.base_dir = directory
        self.facts_file = path.join(self.base_dir, 'facttypes.proto')
        self.keywords_file = path.join(self.base_dir, 'kwtypes.proto')
        self.gazetteer_file = path.join(self.base_dir, 'dict.gzt')
        self.config_file = path.join(self.base_dir, 'config.proto')

    def clean(self):
        with suppress(FileNotFoundError):
            os.unlink(self.facts_file)
        with suppress(FileNotFoundError):
            os.unlink(self.keywords_file)
        with suppress(FileNotFoundError):
            os.unlink(self.gazetteer_file)

    def set_facts(self, facts):
        with open(self.facts_file, 'w') as fd:
            fd.write(facts)

    def set_keywords(self, keywords):
        with open(self.keywords_file, 'w') as fd:
            fd.write(keywords)

    def set_gazetteer(self, gazetteer):
        with open(self.gazetteer_file, 'w') as fd:
            fd.write(gazetteer)

    def set_config(self, config):
        with open(self.config_file, 'w') as fd:
            fd.write(config)

    def set_documents(self, stings):
        pass

    def parse(self):
        return [[], []]


    def set_article(self): # cxx files, N
        pass


    def set_facttypes(self):
        pass