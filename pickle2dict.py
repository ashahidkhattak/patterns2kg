import json
import pickle
import pandas as pd
import time
import yaml

class GenPatternsDictionary:
    pickle_file_name = ""
    json_file_name = ""
    data = ""
    pattern_dict = {}
    def __init__(self, pickle_file_name, JSON_file_name):
        print("The first step of JAMS Pipeline stated: pickle to dictionary conversion")
        self.pickle_file_name = pickle_file_name
        self.json_file_name = JSON_file_name

    def process_pickle_to_create_dict(self):
        self.read_pickle_file()
        self.create_dict()
        self.write_dictory_file()

    def read_pickle_file(self) -> None:
        with open(self.pickle_file_name, 'rb') as f:
            self.data = pickle.load(f)

    def create_dict(self):
        data = self.data.reset_index(level=0)
        columns = data.columns
        sub_cols = columns[4:-1]
        #pattern_dict = {}
        counter = 1
        filtered_df = data[data["freq"] >= 2]
        for col in sub_cols:
            print(counter)
            #todo- this for testing the process - will remove this one it done
            if counter == 10:
                break
            rslt_df = filtered_df.loc[filtered_df[col] >= 1, [col, "ngram"]]
            for index, row in rslt_df.iterrows():
                pattern_id = str(index) + ":" + col
                pattern_content = str(row['ngram']).strip("()")
                pattern_frequency_in_tune = row[col]
                pattern_length = pattern_content.count(',') + 1
                pattern_type = "pitch-class-values"
                # print(pattern_id, pattern_content, pattern_frequency_in_tune)
                if pattern_content not in self.pattern_dict:
                    self.pattern_dict[pattern_content] = {}
                self.pattern_dict[pattern_content][pattern_id] = {}
                self.pattern_dict[pattern_content][pattern_id] = \
                    {
                        "pattern_frequency_in_tune": pattern_frequency_in_tune,
                        "pattern_length": pattern_length,
                        "pattern_type": pattern_type,
                    }
            # end = time.localtime()
            # print(start.tm_sec - end.tm_sec , "seconds")
            counter += 1

    def write_dictory_file(self):
        with open(self.json_file_name, "w") as outfile:
            json.dump(self.pattern_dict, outfile)
        print ("The pattern dictionary is created in the file {}".format(self.json_file_name))

if __name__ == "__main__":
    config = yaml.safe_load(open("config/config.yml"))
    direcoty = config['directories']['music_pattern_directory']
    fileName = config['directories']['pickle_file_name']
    json_file_name = config['directories']['json_file_name']
    ptrn2dict = GenPatternsDictionary(direcoty + "/" + fileName, direcoty + "/"+ json_file_name)
    ptrn2dict.process_pickle_to_create_dict()
    print("here I am")