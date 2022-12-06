import yaml
import pickle2dict as ptrn2dict
import pickle2jams as pickle2jams
import jams2rdf as jams2rdf
from multiprocessing import Process
class JAMSPipeline:
    config = []
    dict2jams_config = []
    jams2rdf_config = []
    directroy = ""
    pickle_file_name = ""
    JSON_file_name = ""
    def __init__(self):
        # this line will load the configuration settings from config.yml file
        self.config = yaml.safe_load(open("config/config.yml"))
        self.jams2rdf_config = yaml.safe_load(open("config/jams2rdf_config.yml"))

        self.direcoty = self.config['directories']['music_pattern_directory']
        self.pickle_file_name = self.config['directories']['pickle_file_name']
        self.JSON_file_name = self.config['directories']['json_file_name']

    # Abandoned - Step1 (pickle_to_dictionary): This create dictionary (in form of JSON) from the given pickle file
    def pickle_to_dictionary(self) -> None:
        pickle_file_name = self.direcoty + "/" + self.pickle_file_name
        json_file_name = self.direcoty + "/" + self.JSON_file_name
        obj = ptrn2dict.GenPatternsDictionary(pickle_file_name, json_file_name)
        obj.process_pickle_to_create_dict()

    # Step1 (Pickle_to_JAMS): This create JAMS files for each tune recording in  JSON file (created in step no.1)
    def pickle_to_JAMS(self) -> None:
        pickle_file_name = self.direcoty + "/" + self.pickle_file_name
        #json_file_name = self.JSON_file_name
        genTunesJAMSFiles = pickle2jams.GenerateTunesJamsFile(pickle_file_name, self.config)
        genTunesJAMSFiles.createJAMSFiles()

    # Step2 (JAMS_to_RDF): This method calls JAMS2RDF class for generating RDF files for JAMS files (created in step no.1)
    def JAMS_to_RDF(self) -> None:
        jamsrdf = jams2rdf.JAMS2RDF(self.jams2rdf_config, self.config['directories']['JAMS_files_dir'])
        jamsrdf.iterateThroughDirectory()

    def start_pipleline(self):
        pickle_file_name = self.direcoty + "/" + self.pickle_file_name
        genTunesJAMSFiles = pickle2jams.GenerateTunesJamsFile(pickle_file_name, self.config)
        #genTunesJAMSFiles.createJAMSFiles()
        p1 = Process(target=genTunesJAMSFiles.createJAMSFiles)
        p1.start()
        jamsrdf = jams2rdf.JAMS2RDF(self.jams2rdf_config, self.config['directories']['JAMS_files_dir'], genTunesJAMSFiles)
        p2 = Process(target=jamsrdf.iterateThroughDirectory)
        p2.start()

if __name__ == "__main__":
    JAMS_pipeline = JAMSPipeline()
    JAMS_pipeline.start_pipleline()