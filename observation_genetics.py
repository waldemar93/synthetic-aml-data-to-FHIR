from fhir.resources.observation import Observation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from typing import Literal


def create_karyotype_observation(obs_id: str, patient_id: str, complex_karyotype: bool):
    """
    Creates and returns an Observation resource for cytogenetic karyotype analysis.

    This function constructs an Observation resource to document the results of a cytogenetic karyotype analysis,
    specifying whether a complex or normal karyotype was observed.

    Parameters:
    - obs_id (str): The unique identifier for the observation.
    - patient_id (str): The unique identifier for the patient to whom the observation applies.
    - complex_karyotype (bool): A flag indicating whether a complex cytogenetic karyotype was observed.

    Returns:
    - Observation: A FHIR Observation resource object populated with the provided data.
    """
    observation = Observation.construct()
    observation.status = "final"
    observation.id = obs_id
    observation.subject = Reference.construct(reference=f"urn:uuid:{patient_id}")

    observation_text = 'Complex cytogenetic karyotype observed.' if complex_karyotype \
        else 'Normal cytogenetic karyotype observed.'
    observation.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>: {observation_text}</div>"
    }

    observation.category = [CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/observation-category",
            code="laboratory",
            display="Laboratory"
        )]
    )]

    observation.code = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://loinc.org",
            code="29770-5",
            display="Karyotype [Identifier] in Blood or Tissue Nominal"
        )
        ],
        text="Test whether the cytogenetic karyotype is normal or complex (abnormal)"
    )

    if complex_karyotype:
        observation.valueString = "Complex karyotype observed"
        observation.interpretation = [CodeableConcept.construct(
            coding=[Coding.construct(
                system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                code="A",  # complex karyotype
                display="Abnormal"
            )]
        )]
    else:
        observation.valueString = "Normal karyotype observed"
        observation.interpretation = [CodeableConcept.construct(
            coding=[Coding.construct(
                system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                code="N",  # normal karyotype
                display="Normal"
            )]
        )]
    return observation


def create_genetic_observation(obs_id: str, patient_id: str, gene_name: str,
                               mutation_status: Literal['Detected', 'Not Detected', 'Unknown'],
                               code_system: Literal['LOINC', 'SNOMED'], code_code: str,
                               code_display_name: str, code_text: str):
    """
    Creates and returns an Observation resource for genetic mutation status.

    This function constructs an Observation resource to document the status of a genetic mutation analysis for a specific gene.
    It includes the mutation status (Detected, Not Detected, Unknown), and leverages coding systems like LOINC or SNOMED for
    standardized documentation.

    Parameters:
    - obs_id (str): The unique identifier for the observation.
    - patient_id (str): The unique identifier for the patient to whom the observation applies.
    - gene_name (str): The name of the gene analyzed.
    - mutation_status (Literal['Detected', 'Not Detected', 'Unknown']): The status of the mutation detected.
    - code_system (Literal['LOINC', 'SNOMED']): The coding system used for the observation.
    - code_code (str): The code representing the gene analysis.
    - code_display_name (str): The display name for the code.
    - code_text (str): Textual description or additional information about the observation.

    Returns:
    - Observation: A FHIR Observation resource object populated with the provided data.
    """
    code_system = 'http://loinc.org' if code_system == 'LOINC' else 'http://snomed.info/sct'

    observation = Observation.construct()
    observation.status = "final"
    observation.id = obs_id
    observation.subject = Reference.construct(reference=f"urn:uuid:{patient_id}")

    observation.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>Gene: {gene_name}, Mutation status: {mutation_status}.</div>"
    }

    observation.category = [CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/observation-category",
            code="laboratory",
            display="Laboratory"
        )]
    )]
    observation.code = CodeableConcept.construct(
        coding=[Coding.construct(
            system=code_system,
            code=code_code,  # Placeholder for the gene analysis code
            display=code_display_name,
        )],
        text=code_text
    )

    # Handling the mutation status and assigning standard codes for value and interpretation
    if mutation_status == "Detected":
        observation.valueCodeableConcept = CodeableConcept.construct(
            coding=[Coding.construct(
                system="http://snomed.info/sct",
                code="260373001",  # SNOMED CT for "Detected"
                display="Detected"
            )]
        )
        observation.interpretation = [CodeableConcept.construct(
            coding=[Coding.construct(
                system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                code="POS",  # Genetic finding detected
                display="Positive"
            )]
        )]
    elif mutation_status == "Not Detected":
        observation.valueCodeableConcept = CodeableConcept.construct(
            coding=[Coding.construct(
                system="http://snomed.info/sct",
                code="260415000",  # SNOMED CT for "Not Detected"
                display="Not Detected"
            )]
        )
        observation.interpretation = [CodeableConcept.construct(
            coding=[Coding.construct(
                system="http://terminology.hl7.org/CodeSystem/v3-ObservationInterpretation",
                code="NEG",  # Genetic finding not detected
                display="Negative"
            )]
        )]
    else:  # Handling Unknown results
        observation.dataAbsentReason = CodeableConcept.construct(
            coding=[Coding.construct(
                system="http://terminology.hl7.org/CodeSystem/data-absent-reason",
                code="unknown",
                display="Unknown"
            )]
        )

    return observation


