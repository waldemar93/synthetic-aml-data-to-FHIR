# synthetic-aml-data-to-fhir
This repository demonstrates how synthetic data from https://zenodo.org/records/8334265 (Synthetic AML clinical trial data) can be transformed into the FHIR format. The synthetically generated files are found in the `input` folder.
The mapping of the original variables to their respective LOINC or SNOMED codes can be found in `input/mapping_fhir.xlsx`. 

Run the `etl.py` to transform all the data into FHIR resources. This version uses FHIR standard profiles. Each created FHIR Bundle is a Collection of all the Resources belonging to a specific patient. The created FHIR resources are stored in the `output` folder.

The transformed resources are also available at .