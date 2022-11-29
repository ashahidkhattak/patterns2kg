---
component-id: P2KG
name: P2KG - Pattern to Knowledge garph JAMS Pipline
description: This code takes the patterns generate by the FONN tool in the form of pickle file and then creates Knowlege graph of the all the patterns found in different tunes.
type: Repository
release-date: 01/12/2022
release-number: v0.1.0.1-dev
work-package: 
- WP3
licence:  CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
links:
- https://github.com/polifonia-project/P2KG-JAMS Pipeline
- https://zenodo.org/record/
credits:
- https://github.com/danDiamo
- https://github.com/ashahidkhattak
- https://github.com/jmmcd
---

# P2KG - Patter to Knowledge Graph JAMS Pipeline 

- Targetting the goals of Polifonia WP3, P2KG JAMS Pipeline creates the knowlege graph of patterns generate by FONN tools. The details of directory and files are given below:
- **Directories**
  - ``config`` 
    - ``config.yml`` => this file contains settings related to pickle file location and JAMS annotations such as ``music_pattern_directory`` and ``corpus_name`` etc. You need to update these settings before executing the pipeline 
    - ``jams2rdf_config.yml`` => this file contains settings related to JAMS to RDF process, for example, ``rdf_directory`` instruct code where to create the rdf files.
  - ``schemas``
    - ``pattern_fonn.json`` => this JAMS schema file, it is required for creating proper JAMS file. For each tune (in the pickle file) a corresponding JAMS file will be generated.
  - ``sparql_anything``
    - ``jams_ontology_pattern.sparql`` => this is the query the SPARQL Anything Engine require to create an RDF file for a given JAMS file. 
    - ``sa.jar`` => this is SPARQL Anything engine, you can can download the latest release from [SPARQL-Anything GitHub link](https://github.com/SPARQL-Anything/sparql.anything/releases/tag/v0.8.0).  
  - ``tests`` => this folder contain test cases (TODO- to be developed) 
  - ``JAMS`` and ``RDF`` directories were during execution



NOTE: You will find all the settings with respect to [Meertern Tune Corpus] (http://www.liederenbank.nl/mtc/).
## P2KG JAMS Pipeline:

1. **P2KG - Steps**
   * 1.1. Input: Patterns generated using FONN tool in the form of pickle file.
   * 1.2. Process: [JAMS Annotation] (https://jams.readthedocs.io/en/stable/) - JAMS files are created using custom pattern schema, you can find in the ``schema`` folder. 
   * 1.3. Process: [SPARQL Anything Engine] (https://sparql-anything.cc/) - It takes JAMS file and create KG. 
   * 1.4. Output: Knowlege Graph of pattern is created, a demo of created KG can be accessed on [polifonia server] (https://polifonia.disi.unibo.it/fonn/sparql). 
   
## P2KG - Requirements

To ensure P2KG runs correctly, please install the following libraries:

``` pip install -r requirements.txt ```

##  Attribution

If you use the code in this repository, please cite this software as follow: 
```
@software{patterns2Kg_jams_pipeline_2022,
	address = {Galway, Ireland},
	title = {{P2KG} - {P}attern-2-{KG} {Knowledge Graph}},
	shorttitle = {{P2KG}},
	url = {https://github.com/polifonia-project/P2KG},
	publisher = {National University of Ireland, Galway},
	author = {Shahid Abdul, Diamond Danny, McDermott, James and Pushkar Jajoria},
	year = {2022},
}
```

## License
This work is licensed under CC BY 4.0, https://creativecommons.org/licenses/by/4.0/
