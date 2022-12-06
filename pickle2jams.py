import json
import pickle
import pandas as pd
import time
import jams
import re
import yaml
import os

class GenerateTunesJamsFile:
    config = []
    jams_files_completions_status = 1
    def __init__(self, pickle_file,  config):
        print("The first step of JAMS Pipeline stated: pickle to JAMS creation")
        pattern_dict = {}
        self.filtered_df = pd.DataFrame()
        self.listOfTunes = []
        self.path = ""
        self.pickleFilePath = pickle_file
        patterns_data = {}
        self.config = config
        self.jams_files_completions_status = 1
        if not os.path.isdir(self.config['directories']['JAMS_files_dir']):
            os.makedirs(self.config['directories']['JAMS_files_dir'])
    # getter method
    def get_jams_files_completions_status(self):
        return self.jams_files_completions_status

    def __open_pickle_file(self):
        with open(self.pickleFilePath, 'rb') as f:
            data = pickle.load(f)
        data = data.reset_index(level=0)
        columns = data.columns
        self.listOfTunes = columns[4:-1]
        print("Total JAMS files to be created from the pickle file: ", len(self.listOfTunes))
        self.filtered_df = data[data["freq"] >= 2]

    def __setCurrentTuneJamsMetadata(self, tuneName):
        dir = self.config['directories']['schemas_directory']
        schema = self.config['directories']['schema_file']
        corpus = self.config['jams_annotations']['corpus_name']
        schema_file_name = dir+'/'+schema
        #print(schema_file_name)
        jams.schema.add_namespace(schema_file_name)
        tuneJAMSFile = jams.JAMS()
        tuneNumber = re.findall(r'\d+', tuneName)
        tuneJAMSFile.file_metadata.identifiers = {
            "tune-corpus": corpus,
            "url": self.config['jams_annotations']['tune_base_url']+tuneNumber[0]
        }
        tuneJAMSFile.file_metadata.title = tuneName
        tuneJAMSFile.file_metadata.release = "pattern-demo"
        tuneJAMSFile.file_metadata.duration = 130
        tuneJAMSFile.sandbox.type = "score"
        tuneJAMSFile.sandbox.expanded = "true"
        tuneJAMSFile.sandbox.composers = []
        return tuneJAMSFile

    def __createJAMSAnnotation(self, name_space):
        pattern_annotation = jams.Annotation(namespace=name_space)
        pattern_annotation.annotation_metadata.annotator.name = self.config['jams_annotations']['annotator_name']
        pattern_annotation.annotation_metadata.data_source = self.config['jams_annotations']['data_source']
        pattern_annotation.annotation_metadata.corpus = self.config['jams_annotations']['corpus']
        pattern_annotation.annotation_metadata.version = self.config['jams_annotations']['version']
        pattern_annotation.annotation_metadata.curator.name = self.config['jams_annotations']['annotator_name']
        pattern_annotation.annotation_metadata.curator.email = self.config['jams_annotations']['email']
        pattern_annotation.annotation_metadata.annotation_tools = self.config['jams_annotations']['annotation_tools']
        pattern_annotation.annotation_metadata.annotation_rules = None
        pattern_annotation.annotation_metadata.validation = None
        return pattern_annotation

    def createJAMSFiles(self):
        self.jams_files_completions_status = 0
        try:
            self.__open_pickle_file()
        except Exception as e:
            print(e)
            exit(0)
        print("pickle file loaded")
        counter = 1
        for tuneName in self.listOfTunes:
            print(counter)
            rslt_df = self.filtered_df.loc[self.filtered_df[tuneName] >= 1, [tuneName, "ngram"]]
            tuneJAMSFile = self.__setCurrentTuneJamsMetadata(tuneName)
            pattern_annotation = self.__createJAMSAnnotation(self.config['jams_annotations']['schema_name'])
            for index, row in rslt_df.iterrows():
                pattern_content = str(row['ngram']).strip("()")
                pattern_dict = {
                    "pattern_id": str(index) + ":" + tuneName,
                    "pattern_content": pattern_content,
                    "pattern_type": "pitch-class-values",
                    "pattern_frequency": row[tuneName],
                    "pattern_length": pattern_content.count(',') + 1,
                }
                pattern_annotation.append(time=0.0, duration=0.0, value=pattern_dict, confidence=1)
            tuneJAMSFile.annotations.append(pattern_annotation)
            tuneJAMSFile.save(self.config['directories']['JAMS_files_dir']+ tuneName+".jams", strict=False)
            counter += 1

        # this will be used by rdf generator
        self.jams_files_completions_status = 0

if __name__ == "__main__":
    config = yaml.safe_load(open("config/config.yml"))
    direcoty = config['directories']['music_pattern_directory']
    pickle_file_name = config['directories']['pickle_file_name']
    pickle_file_name = direcoty + "/" + pickle_file_name
    genJAMSFiles = GenerateTunesJamsFile(pickle_file_name, config)
    genJAMSFiles.createJAMSFiles()