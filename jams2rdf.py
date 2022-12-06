import os
import sys
import yaml
from subprocess import check_output, CalledProcessError
import glob, os
import os.path
from rdflib import Graph, URIRef

class JAMS2RDF:
    query_current = ""
    query_test = ""
    namespace = ""
    rdf_directory = ""
    jams_files_dirctory = ""
    config = []

    # constructor of the class for initialiazing various class level variables
    def __init__(self, config, jams_files_dirctory):
        self.query_current = config['directories']['query_current_file']
        self.query_test = config['directories']['query_test_file']
        self.rdf_directory = config['directories']['rdf_directory']
        if not os.path.isdir(self.rdf_directory):
            os.makedirs(self.rdf_directory)
        self.namespace = config['settings']['namespace']
        self.jams_files_dirctory = jams_files_dirctory
        self.config = config

    # jams2rdf is the main function for converting a JAMS file into RDF, according to jams
    # ontology and by using the SPARQL Anything software.
    # In particular, this code calls the SPARQL Anything code, written in Java
    # and runs it against a SPARQL Anything query, specifically developed for
    # converting JAMS files.
    def jams2rdf(self, input_file: str, output=None, output_format: str = 'ttl'):
        input_filename_with_ext = os.path.basename(input_file)
        jams_file, ext = os.path.splitext(input_filename_with_ext)
        input_file_dir_name = os.path.dirname(input_file)
        input_file = input_file_dir_name +"/"+ input_filename_with_ext
        with open(self.query_test, 'r') as r:
            query_for_file = r.read().replace("%FILEPATH%", input_file)
            with open(self.query_current, 'w') as w:
                w.write(query_for_file)
        g = Graph()
        try:
            out = check_output(["java", "-jar",
                                self.config["directories"]["sparql_anything_jar_file"],
                                "-q",
                                self.query_current
                                ])
            g.parse(out)
        except CalledProcessError as e:
            print(e)
            print("Output graph is empty for {}".format(input_file))

        # Replace root node name
        foo_uri = URIRef(self.namespace + 'foo')
        jams_collection = self.config['settings']['jams_collection']

        resource_uri = URIRef(self.namespace + jams_collection + '/' + input_filename_with_ext)
        for s, p, o in g.triples((foo_uri, None, None)):
            g.add((resource_uri, p, o))
            g.remove((s, p, o))

        if output:
            with open(output, 'w') as wo:
                wo.write(g.serialize(format=output_format))

        os.remove(self.query_current)

    # this function will iterate over JAMS directory
    def iterateThroughDirectory(self):
            counter = 1
            for filename in glob.iglob(self.jams_files_dirctory+ "*.jams", recursive=True):
                if os.path.isfile(filename):  # filter dirs
                    counter = counter + 1
                    print(counter, filename)
                    filenamewithext = os.path.basename(filename)
                    jams_file, ext = os.path.splitext(filenamewithext)
                    outfilePath = self.rdf_directory + "/" + jams_file + ".ttl"
                    file_exists = os.path.exists(outfilePath)
                    if not file_exists:
                        self.jams2rdf(filename, outfilePath)

if __name__ == "__main__":
    config = yaml.safe_load(open("config/jams2rdf_config.yml"))
    jams2rdf = JAMS2RDF(config)
    jams2rdf.iterateThroughDirectory()

#if __name__ == "__main__":
#    if len(sys.argv) < 2 or len(sys.argv) > 3:
#        print("Usage: {0} <input file> [<output file>]".format(sys.argv[0]))
#        exit(2)
#    elif len(sys.argv) == 2:
        # Conversion to stdout
#        infilename = sys.argv[1]
#        jams2rdf(os.path.abspath(infilename))
#    elif len(sys.argv) == 3:
        # Conversion to file
#        infilename = sys.argv[1]
#        outfilename = sys.argv[2]
#        jams2rdf(os.path.abspath(infilename), outfilename)
#    exit(0)
