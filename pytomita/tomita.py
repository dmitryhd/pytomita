# -*- coding: utf-8 -*-

from __future__ import print_function

import os
import os.path as path
from io import open
import subprocess
from collections import defaultdict
import xml.etree.ElementTree


class TomitaParser(object):

    # TODO: remove some symbols from documents \r, \t, \. \, ...
    # TODO: generate fact_descriptions by fact file
    # TODO: return dataframe with Fact_Property: ('a', 'b')

    def __init__(self, binary_path, directory='.', num_threads=2):
        self.binary_path = binary_path
        self.base_dir = directory
        self.facts_file = path.join(self.base_dir, 'facttypes.proto')
        self.keywords_file = path.join(self.base_dir, 'kwtypes.proto')
        self.gazetteer_file = path.join(self.base_dir, 'dict.gzt')
        self.config_file = path.join(self.base_dir, 'config.proto')
        self.documents_file = path.join(self.base_dir, 'documents_dlp.txt')
        self.output_file = path.join(self.base_dir, 'facts.xml')
        self.fact_files = []
        self.num_threads = num_threads
        # TODO: mkdir if not exists.

    def set_facts(self, facts):
        facts = u'import "base.proto"; import "facttypes_base.proto"; ' + facts
        with open(self.facts_file, 'w', encoding='utf8') as fd:
            fd.write(facts)

    def set_keywords(self, keywords):
        keywords = u'import "base.proto"; import "articles_base.proto"; ' + \
                   keywords
        with open(self.keywords_file, 'w', encoding='utf8') as fd:
            fd.write(keywords)

    def set_gazetteer(self, gazetteer):
        gazetteer = u'''
        encoding "utf8";
        import "base.proto";
        import "articles_base.proto";
        import "kwtypes.proto";
        import "facttypes.proto";
        ''' + gazetteer
        with open(self.gazetteer_file, 'w', encoding='utf8') as fd:
            fd.write(gazetteer)

    def set_config(self, config):
        config_template = u'''
            encoding "utf8";
            TTextMinerConfig {
              Dictionary = "dict.gzt";
              Input = {
                File = "documents_dlp.txt"; // файл с анализируемым текстом
                Type = dpl;                 // режим чтения
              }

            // Articles and Facts begins:
        ''' + config + '\n' + 'NumThreads = {};\n'.format(self.num_threads) \
                          + u'''
            // Articles and Facts end.
                Output = {
                    File = "facts.xml";
                }
            }
        '''
        with open(self.config_file, 'w', encoding='utf8') as fd:
            fd.write(config_template)

    def set_fact_file(self, fact_desc, file_name):
        requirements = u'#encoding "utf-8" \n' + fact_desc
        fact_file_path = path.join(self.base_dir, file_name)
        self.fact_files.append(file_name)
        with open(fact_file_path, 'w', encoding='utf8') as fd:
            fd.write(requirements)

    def set_documents(self, documents):
        with open(self.documents_file, 'w', encoding='utf8') as fd:
            for doc in documents:
                doc = doc.replace('\n', ' ')
                fd.write(doc + '\n')

    def run(self):
        """
        deletes output file and creates new
        :raises: subprocess.CalledProcessError if tomita parser failed
        :returns: True if run was successful
        """
        if os.path.isfile(self.output_file):
            os.unlink(self.output_file)
        original_dir = os.getcwd()
        try:
            os.chdir(self.base_dir)
            try:
                output = subprocess.check_output(
                    self.binary_path + ' ' + 'config.proto',
                    shell=True,
                    universal_newlines=True,
                    stderr=subprocess.STDOUT,
                )
            except subprocess.CalledProcessError as e:
                print('Got exception {}'.format(e))
                print('Tomita output {}'.format(e.output))
                raise e
        finally:
            os.chdir(original_dir)
        success = 'End.  (Processing files.)' in output
        return success

    def get_xml(self):
        """ :return: xml.etree.ElementTree root """
        return xml.etree.ElementTree.parse(self.output_file).getroot()

    def parse(self, fact_descriptions):
        """
        :param fact_descriptions: {'DrivingLicense': ['Category']}
        :return: dict with keys as document id numbers.
        If document doesn't contain facts it just skipped in dictionary

        Example:
        expected_result = {
            1: {'Category': ['C', 'СE']},
            3: {'Category': ['C']}
        }
        """
        root = self.get_xml()
        doc_facts = {}
        for document in root.findall('document'):
            document_id = int(document.attrib['di'])
            doc_facts[document_id] = defaultdict(list)
            facts = document.find('facts')
            for fact_name in fact_descriptions:
                attributes = facts.findall(fact_name)
                for attr in attributes:
                    for attribute_name in fact_descriptions[fact_name]:
                        value = attr.find(attribute_name).attrib.get('val')
                        doc_facts[document_id][attribute_name].append(value)
            doc_facts[document_id] = dict(doc_facts[document_id])
        return doc_facts

    def clean(self):
        """ Deletes all files from working directory. """
        files_to_delete = [
            self.facts_file,
            self.keywords_file,
            self.gazetteer_file,
            self.config_file,
            self.documents_file,
            self.output_file,
            path.join(self.base_dir, 'requirements.bin'),
            path.join(self.base_dir, 'dict.gzt.bin'),
            path.join(self.base_dir, 'dict.gzt.bin'),
        ]

        files_to_delete.extend(
            [path.join(self.base_dir, file) for file in self.fact_files])
        for file in files_to_delete:
            try:
                os.unlink(file)
            except OSError:
                pass
