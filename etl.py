import os
from uuid import uuid4
import pandas as pd
from fhir.resources.bundle import Bundle, BundleEntry
from condition import create_aml_condition, create_cr1_condition, create_examl_condition
from observation_genetics import create_karyotype_observation, create_genetic_observation
from observation_lab import create_observation_lab
from observation_outcome import create_binary_event_observation, create_event_time_observation
from patient import create_patient_resource


mapping = pd.read_excel('input/mapping_fhir.xlsx')


def create_bundle(patient_row):
    """
    Constructs a FHIR Bundle resource that aggregates multiple resources including Patient, Conditions, and Observations
    related to Acute Myeloid Leukemia (AML) and its specific characteristics for a given patient record. The bundle includes
    the patient's basic information, AML diagnosis, complete remission status, extramedullary AML status, overall survival status,
    event-free survival status, survival times, karyotype information, molecular genetics and cytogenetics observations,
    and laboratory values.

    Parameters:
    - patient_row (dict): A dictionary representing a row from a patient data table with keys corresponding to patient attributes.

    Returns:
    - Bundle: A FHIR Bundle resource object containing entries for patient information, conditions, observations, and other relevant data
      derived from the `patient_row`.

    Notes:
    The function dynamically constructs resources based on the data provided in `patient_row`, including handling of different AML subtypes,
    determination of complete remission status, and the presence of extramedullary AML. It also includes observations for overall survival and
    event-free survival status and times, karyotype analysis, genetic mutations, and laboratory values. The function ensures that each entry
    in the bundle is assigned a unique UUID and constructs appropriate references between resources.
    """
    bundle = Bundle.construct(type='collection')
    bundle.id = str(uuid4())
    bundle_entries = []

    patient_r = create_patient_resource(str(uuid4()), patient_row['AGE'], patient_row['SEX'],
                                        old_id=patient_row['SUBJID'])
    bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + patient_r.id, resource=patient_r))

    # diagnosis (with subtype)
    subtype = 'Unknown' if pd.isna(patient_row['AMLSTAT']) else patient_row['AMLSTAT']
    aml_cond_r = create_aml_condition(str(uuid4()), patient_r.id, age=patient_row['AGE'], AML_subtype=subtype)
    bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + aml_cond_r.id, resource=aml_cond_r))

    # CR1 --> condition resource, just if CR1 was achieved
    if patient_row['CR1'] == 1:
        cr1_cond_r = create_cr1_condition(str(uuid4()), patient_r.id)
        bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + cr1_cond_r.id, resource=cr1_cond_r))

    # EXAML --> condition resource, just if True; otherwise no condition generated (also in case were it is not known)
    if patient_row['EXAML'] == 1:
        examl_cond_r = create_examl_condition(str(uuid4()), patient_r.id)
        bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + examl_cond_r.id, resource=examl_cond_r))

    # OSSTAT
    osstat_obs_r = create_binary_event_observation(str(uuid4()), patient_r.id, event='OSSTAT',
                                                   value=patient_row['OSSTAT'])
    bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + osstat_obs_r.id, resource=osstat_obs_r))

    # EFSSTAT
    efsstat_obs_r = create_binary_event_observation(str(uuid4()), patient_r.id, event='EFSSTAT',
                                                    value=patient_row['EFSSTAT'])
    bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + efsstat_obs_r.id, resource=efsstat_obs_r))

    # survival times
    val = patient_row['OSTM']
    if isinstance(val, str):
        val = float(val.replace(',', '.'))
    ostm_obs_r = create_event_time_observation(str(uuid4()), patient_r.id, event='OSTM',
                                                value=val)
    bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + ostm_obs_r.id, resource=ostm_obs_r))

    val = patient_row['EFSTM']
    if isinstance(val, str):
        val = float(val.replace(',', '.'))
    efstm_obs_r = create_event_time_observation(str(uuid4()), patient_r.id, event='EFSTM',
                                                value=val)
    bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + efstm_obs_r.id, resource=efstm_obs_r))

    # karyotype - there are two variables in the original data (CGCX - complex, CGNX: normal)
    karyo_complex = True if patient_row['CGCX'] == 1 else False
    obs_karyo_r = create_karyotype_observation(str(uuid4()), patient_r.id, karyo_complex)
    bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + obs_karyo_r.id, resource=obs_karyo_r))

    processed_cols = {'AGE', 'SEX', 'SUBJID', 'AMLSTAT', 'CR1', 'EXAML', 'OSSTAT', 'EFSSTAT', 'OSTM', 'EFSTM', 'CGCX',
                      'CGNK'}

    # molecular genetics and cytogenetics
    for col in mapping[(mapping['Type'] == 'molecular genetics') | (mapping['Type'] == 'cytogenetics')]['Variable']:
        if col in processed_cols:
            continue

        mapping_var = mapping[mapping['Variable'] == col].iloc[0]
        if patient_row[col] == 1:
            mutation_status = 'Detected'
        elif patient_row[col] == 0:
            mutation_status = 'Not Detected'
        else:
            mutation_status = 'Unknown'

        text = f'{col} [{mapping_var["Type"]};{mapping_var["Label"]}]'
        obs_r = create_genetic_observation(obs_id=str(uuid4()), patient_id=patient_r.id, gene_name=col,
                                           mutation_status=mutation_status,
                                           code_system=mapping_var['Vocabulary'].strip(),
                                           code_code=str(mapping_var['Vocabulary Code']).strip(),
                                           code_display_name=mapping_var['Vocabulary Display Name'].strip(),
                                           code_text=text
                                           )
        bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + obs_r.id, resource=obs_r))
        processed_cols.add(col)

    # laboratory values (with units)
    for col in mapping[mapping['Type'] == 'laboratory value']['Variable']:
        if col in processed_cols:
            continue

        mapping_var = mapping[mapping['Variable'] == col].iloc[0]

        val = patient_row[col]
        if isinstance(val, str):
            val = float(val.replace(',', '.'))

        obs_l = create_observation_lab(obs_id=str(uuid4()), patient_id=patient_r.id, variable=col,
                                       code_system=mapping_var['Vocabulary'].strip(),
                                       code_code=str(mapping_var['Vocabulary Code']).strip(),
                                       code_display_name=mapping_var['Vocabulary Display Name'].strip(),
                                       value=val)
        bundle_entries.append(BundleEntry(fullUrl='urn:uuid:' + obs_l.id, resource=obs_l))
        processed_cols.add(col)

    left_cols = [col for col in mapping['Variable'] if col not in processed_cols]
    assert len(left_cols) == 0

    bundle.entry = bundle_entries
    return bundle


# Read in ctab source data
os.makedirs('output/ctab', exist_ok=True)
df = pd.read_csv('input/synthetic_aml_data_ctab.csv', sep=";")
for i in range(len(df)):
    pat_row = df.iloc[i]
    pat_bundle = create_bundle(pat_row).json(indent=4)
    file_path = 'bundle_' + pat_row['SUBJID'] + '.json'
    with open('output/ctab/' + file_path, 'w') as f:
        f.write(pat_bundle)
    print('bundle_' + pat_row['SUBJID'] + '.json created')

# Read nflow source data
os.makedirs('output/nflow', exist_ok=True)
df = pd.read_csv('input/synthetic_aml_data_nflow.csv', sep=";")
for i in range(len(df)):
    pat_row = df.iloc[i]
    pat_bundle = create_bundle(pat_row).json(indent=4)
    file_path = 'bundle_' + pat_row['SUBJID'] + '.json'
    with open('output/nflow/' + file_path, 'w') as f:
        f.write(pat_bundle)
    print('bundle_' + pat_row['SUBJID'] + '.json created')
