from __future__ import print_function

import os
import os.path as path
from io import open
from contextlib import suppress
import subprocess
from collections import defaultdict

import xml.etree.ElementTree


class TomitaParser(object):
    """
    Usage:
    """
    # TODO: write simplest example possible.

    def __init__(self, directory='/tmp'):
        self.tomita_path = '/home/dkhodakov/build/tomita-parser/build/bin/tomita-parser'
        self.base_dir = directory
        self.facts_file = path.join(self.base_dir, 'facttypes.proto')
        self.keywords_file = path.join(self.base_dir, 'kwtypes.proto')
        self.gazetteer_file = path.join(self.base_dir, 'dict.gzt')
        self.config_file = path.join(self.base_dir, 'config.proto')
        self.requirements_file = path.join(self.base_dir, 'requirements.cxx')
        self.documents_file = path.join(self.base_dir, 'documents_dlp.txt')
        self.output_file = path.join(self.base_dir, 'facts.xml')
        # TODO: mkdir if not exists.

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

    def set_requirements(self, requirements):
        with open(self.requirements_file, 'w') as fd:
            fd.write(requirements)

    def set_documents(self, documents):
        with open(self.documents_file, 'w') as fd:
            # TODO: strip newlines
            for doc in documents:
                fd.write(doc + '\n')

    def run(self):
        original_dir = os.getcwd()
        try:
            os.chdir(self.base_dir)
            output = subprocess.check_output(
                self.tomita_path + ' ' + 'config.proto',
                shell=True,
                universal_newlines=True,
                stderr=subprocess.STDOUT
            )
        finally:
            os.chdir(original_dir)
        success = 'End.  (Processing files.)' in output
        return success

    def get_xml(self):
        """ :return: xml.etree.ElementTree root """
        return xml.etree.ElementTree.parse(self.output_file).getroot()

    def parse(self, fact_descriptions):
        """
        :param: facts: {'DrivingLicense': ['Category']}
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
                attributes = facts.findall(fact_name)  # DrivingLicense
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
            self.requirements_file,
            self.documents_file,
            self.output_file,
            path.join(self.base_dir, 'requirements.bin'),
            path.join(self.base_dir, 'dict.gzt.bin'),
            path.join(self.base_dir, 'dict.gzt.bin'),
        ]
        for file in files_to_delete:
            with suppress(FileNotFoundError):
                os.unlink(file)
