from fhir.resources.annotation import Annotation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.reference import Reference
from fhir.resources.condition import Condition
from typing import Literal


def create_aml_condition(cond_id: str, patient_id: str, AML_subtype: Literal['de novo', 'sAML', 'tAML', 'Unknown']):
    """
    Creates a FHIR Condition resource for an Acute Myeloid Leukemia (AML) diagnosis with specified subtype.

    Parameters:
    - cond_id (str): Unique identifier for the condition.
    - patient_id (str): Identifier for the patient to whom the condition applies.
    - AML_subtype (Literal['de novo', 'sAML', 'tAML', 'Unknown']): Subtype of AML diagnosed.

    Returns:
    - Condition: A FHIR Condition resource object with populated fields.

    Raises:
    - AttributeError: If an unsupported AML_subtype is provided.
    """
    condition = Condition.construct()
    condition.id = cond_id
    condition.subject = Reference.construct(reference=f"urn:uuid:{patient_id}")

    if AML_subtype == 'de novo':
        subtype = 'de novo'
    elif AML_subtype == 'sAML':
        subtype = 'Secondary Acute Myeloid Leukemia (sAML)'
    elif AML_subtype == 'tAML':
        subtype = 'Therapy-related acute myeloid leukemia (tAML)'
    elif AML_subtype == 'Unknown':
        subtype = 'Unknown'
    else:
        raise AttributeError(f'Wrong AML_subtype provided: "{AML_subtype}". AML_subtype needs to be one of the '
                             f'following options: "de novo", "sAML", "tAML", "Unknown".')

    condition.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>: Patient diagnosed with Acute Myeloid Leukemia (AML), "
               f"subtype: {subtype}.</div>"
    }

    condition.clinicalStatus = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-clinical",
            code="active",
            display="Active"
        )]
    )

    condition.verificationStatus = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-ver-status",
            code="confirmed",
            display="Confirmed"
        )]
    )

    condition.category = [CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-category",
            code="encounter-diagnosis",
            display="Encounter Diagnosis"
        )]
    )]

    condition.code = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://snomed.info/sct",
            code="91861009",
            display="Acute myeloid leukemia"
        )],
        text=f"Acute Myeloid Leukemia (AML), subtype: {subtype}"
    )

    condition.note = [Annotation.construct(
        text=f"Patient diagnosed with AML, subtype: {subtype}."
    )]

    return condition


def create_cr1_condition(cond_id: str, patient_id: str):
    """
    Creates a FHIR Condition resource representing a patient's first complete remission (CR1) from Acute Myeloid Leukemia (AML).

    Parameters:
    - cond_id (str): Unique identifier for the condition.
    - patient_id (str): Identifier for the patient to whom the condition applies.

    Returns:
    - Condition: A FHIR Condition resource object with populated fields.
    """
    condition = Condition.construct()
    condition.id = cond_id
    condition.subject = Reference.construct(reference=f"urn:uuid:{patient_id}")

    condition.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>: First Complete Remission (CR1) of Acute Myeloid Leukemia "
               f"(AML) was achieved. </div>"
    }

    condition.clinicalStatus = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-clinical",
            code="remission",
            display="Remission"
        )],
        text="First Complete Remission (CR1)"
    )

    condition.verificationStatus = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-ver-status",
            code="confirmed",
            display="Confirmed"
        )]
    )

    condition.category = [CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-category",
            code="encounter-diagnosis",
            display="Encounter Diagnosis"
        )]
    )]

    condition.code = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://snomed.info/sct",
            code="765205004",
            display="Disorder in remission"
        )],
        text="First Complete Remission (CR1) of Acute Myeloid Leukemia (AML)"
    )

    condition.note = [Annotation.construct(
        text=f"Patient achieved first Complete Remission (CR1) from Acute Myeloid Leukemia (AML)."
    )]

    return condition


def create_examl_condition(cond_id: str, patient_id: str):
    """
    Creates and returns a FHIR Condition resource object for Extramedullary Acute Myelogenous Leukemia (EXAML).

    Parameters:
    - cond_id (str): The unique identifier for the condition.
    - patient_id (str): The unique identifier for the patient.

    Returns:
    - Condition: A FHIR Condition resource object for EXAML, indicating the diagnosis of extramedullary involvement in AML.
    """
    condition = Condition.construct()
    condition.id = cond_id
    condition.subject = Reference.construct(reference=f"urn:uuid:{patient_id}")

    condition.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>: Diagnosed with Extramedullary acute myelogenous leukemia "
               f"(EXAML) </div>"
    }

    condition.clinicalStatus = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-clinical",
            code="active",
            display="Active"
        )]
    )

    condition.verificationStatus = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-ver-status",
            code="confirmed",
            display="Confirmed"
        )]
    )

    condition.category = [CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/condition-category",
            code="encounter-diagnosis",
            display="Encounter Diagnosis"
        )]
    )]

    condition.code = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://snomed.info/sct",
            code="91861009",
            display="Acute myeloid leukemia"
        )],
        text="Extramedullary acute myelogenous leukemia (EXAML)"
    )

    condition.note = [Annotation.construct(
        text=f"Patient diagnosed with Extramedullary acute myelogenous leukemia (EXAML)."
    )]

    return condition



