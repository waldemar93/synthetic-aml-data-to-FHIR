from fhir.resources.annotation import Annotation
from fhir.resources.fhirtypes import Date
from fhir.resources.patient import Patient
from typing import Literal


def create_patient_resource(patient_id: str, age: int, sex: Literal['m', 'f'], old_id: str):
    """
    Creates and returns a FHIR Patient resource object.

    This function constructs a Patient resource with an approximated birthdate based on the given age,
    assigns gender based on the input, and includes a narrative text block and an annotation noting
    the approximation method. It is intended for cases where the exact birthdate is unknown.

    Parameters:
    - patient_id (str): The unique identifier for the patient in the current system.
    - age (int): The patient's age, used to approximate the birthdate.
    - sex (Literal['m', 'f']): The patient's sex, 'm' for male and 'f' for female.
    - old_id (str): The patient's identifier in the source system.

    Returns:
    - Patient: A FHIR Patient resource object populated with the provided data.

    Raises:
    - AttributeError: If the sex parameter is not 'm' or 'f'.

    Note:
    The birthdate is approximated by subtracting the age from a hypothetical current date of January 1, 2010.
    The function includes a note within the Patient resource to document this approximation method and the
    original identifier from the source system.
    """
    patient = Patient.construct()
    patient.id = patient_id

    patient.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>Birthdate is approximated based on the given age of {age} "
               f"calculated from a hypothetical data January 1, 2010, due to the original birthdate being unknown. "
               f"In the source system the old id was '{old_id}'.</div>"
    }

    # just age given, no real birthdate existent
    patient.birthDate = Date(2010-age, 1, 1)

    if sex == 'm':
        patient.gender = 'male'
    elif sex == 'f':
        patient.gender = 'female'
    else:
        raise AttributeError(f'sex needs to be either "m" or "f", but "{sex}" was provided.')

    note = Annotation.construct()
    note.text = ("Birthdate is approximated based on age 51 as of January 1, 2020, due to the original birthdate "
                 "being unknown.")

    return patient
