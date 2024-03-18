from fhir.resources.observation import Observation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from typing import Literal


def create_observation_lab(obs_id: str, patient_id: str, variable: Literal['HB', 'PLT', 'WBC'],
                           code_system: Literal['LOINC', 'SNOMED'], code_code: str, code_display_name: str,
                           value: float):
    """
    Creates a FHIR Observation resource representing laboratory measurements.

    This function constructs an Observation resource for a specified laboratory measurement (e.g., Hemoglobin (HB),
    Platelets (PLT), White Blood Cells (WBC)). It includes the measurement value and unit, as well as codings
    for the type of measurement taken.

    Parameters:
    - obs_id (str): A unique identifier for the observation instance.
    - patient_id (str): The unique identifier of the patient to whom the observation applies.
    - variable (Literal['HB', 'PLT', 'WBC']): The type of laboratory measurement being documented.
    - code_system (Literal['LOINC', 'SNOMED']): The coding system used for the observation code.
    - code_code (str): The code representing the laboratory measurement according to the specified coding system.
    - code_display_name (str): The human-readable name associated with the observation code.
    - value (float): The numerical result of the laboratory measurement.

    Returns:
    - Observation: A FHIR Observation resource object populated with laboratory measurement data.
    """
    code_system = 'http://loinc.org' if code_system == 'LOINC' else 'http://snomed.info/sct'
    observation = Observation.construct()
    observation.status = "final"
    observation.id = obs_id
    observation.subject = Reference.construct(reference=f"urn:uuid:{patient_id}")

    observation.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>: {variable}:{value}.</div>"
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
            code=code_code,
            display=code_display_name
        )
        ]
    )

    value_quantity = Quantity.construct()
    if variable == 'WBC' or variable == 'PLT':
        value_quantity.value = value
        value_quantity.unit = '10^6/L'
        value_quantity.system = 'http://unitsofmeasure.org'
        value_quantity.code = '10*6/L'

    elif variable == 'HB':
        value_quantity.value = value
        value_quantity.unit = 'mmol/L'
        value_quantity.system = 'http://unitsofmeasure.org'
        value_quantity.code = 'mmol/L'

    else:
        raise AttributeError(f'Wrong variable ("{variable}") provided. '
                             f'The variable needs to be one of these values: "HB", "PLT", "WBC"')

    observation.valueQuantity = value_quantity

    return observation
