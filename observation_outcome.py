from fhir.resources.annotation import Annotation
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.quantity import Quantity
from fhir.resources.reference import Reference
from fhir.resources.observation import Observation
from typing import Literal


def create_binary_event_observation(obs_id: str, patient_id: str, event: Literal['OSSTAT', 'EFSSTAT'], value: bool):
    """
    Creates a FHIR Observation resource to represent a binary event (e.g., occurrence or non-occurrence of an event)
    related to a patient's clinical outcomes, specifically for Overall Survival (OSSTAT) and Event-Free Survival (EFSSTAT).

    Parameters:
    - obs_id (str): Unique identifier for the observation.
    - patient_id (str): Unique identifier for the patient to whom the observation applies.
    - event (Literal['OSSTAT', 'EFSSTAT']): Specifies the type of event being observed. 'OSSTAT' for Overall Survival,
      'EFSSTAT' for Event-Free Survival.
    - value (bool): Indicates whether the specified event occurred (True) or did not occur (False).

    Returns:
    - Observation: A FHIR Observation resource object with populated attributes according to the specified parameters.
    """
    observation = Observation.construct()
    observation.status = "final"
    observation.id = obs_id
    observation.subject = Reference.construct(reference=f"urn:uuid:{patient_id}")

    if event == 'OSSTAT':
        observation_text = ('Event: Overall Survival (OSSTAT) occurred, meaning that the patient died during '
                            'this study.') if value else ('Event: Overall Survival (OSSTAT) did not occur, '
                                                          'meaning that the patient was alive at the end of the study '
                                                          'period or lost to follow-up (censored).')
    elif event == 'EFSSTAT':
        observation_text = ('Event: Event Free Survival (EFSSTAT) occurred, meaning that at least one '
                            'event occurred during this study.') if value else ('Event: Event Free Survival '
                                                                                '(EFSSTAT) did not occur,  meaning that '
                                                                                'no event occurred until the end of the '
                                                                                'study period or lost to follow-up '
                                                                                '(censored).')
    else:
        raise AttributeError(f'Wrong event ("{event}") provided. '
                             f'The event needs to be one of these values: "OSSTAT", "EFSSTAT".')

    observation.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>: {observation_text}</div>"
    }

    observation.category = [CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/observation-category",
            code="survey",
            display="Survey"
        )]
    )]

    observation.code = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://snomed.info/sct",
            code="278844005",
            display="General clinical state"
        )
        ],
        text="Overall Survival Status (OSSTAT)" if event == 'OSSTAT' else "Event Free Survival Status (EFSSTAT)"
    )

    if event == 'OSSTAT':
        if not value:
            observation.valueBoolean = False
            observation.interpretation = [CodeableConcept.construct(
                coding=[Coding.construct(
                    system="http://snomed.info/sct",
                    code="438949009",
                    display="Alive"
                )],
                text='Alive or censored'
            )]
            observation.note = [Annotation.construct(
                text=("Event: Overall Survival (OSSTAT) did not occur, meaning that the patient was alive at the end of "
                      "the study period or lost to follow-up (censored)."))]

        else:
            observation.valueBoolean = True
            observation.interpretation = [CodeableConcept.construct(
                coding=[Coding.construct(
                    system="http://snomed.info/sct",
                    code="419099009",  # complex karyotype
                    display="Dead"
                )]
            )]
            observation.note = [Annotation.construct(
                text='Event: Overall Survival (OSSTAT) occurred, meaning that the patient died during this study.')]

    if event == 'EFSTAT':
        if not value:
            observation.valueBoolean = False
            observation.interpretation = [CodeableConcept.construct(
                text=('Event: Event Free Survival (EFSSTAT) did not occur,  meaning that no event occurred until the '
                      'end of the study period or lost to follow-up (censored).')
            )]
            observation.note = [Annotation.construct(
                text=(('Event: Event Free Survival (EFSSTAT) did not occur,  meaning that no event occurred until the '
                      'end of the study period or lost to follow-up (censored).')))]
        else:
            observation.valueBoolean = True
            observation.interpretation = [CodeableConcept.construct(
                text=('Event: Event Free Survival (EFSSTAT) occurred, meaning that at least one event occurred during '
                      'this study.')
            )]
            observation.note = [Annotation.construct(
                text=('Event: Event Free Survival (EFSSTAT) occurred, meaning that at least one event occurred during '
                      'this study.'))]

    return observation


def create_event_time_observation(obs_id: str, patient_id: str, event: Literal['OSTM', 'EFSTM'], value: float):
    """
    Generates a FHIR Observation resource that documents the duration of time until a significant clinical event occurs
    (e.g., Overall Survival Time or Event-Free Survival Time) from the beginning of a study.

    Parameters:
    - obs_id (str): Unique identifier for the observation.
    - patient_id (str): Unique identifier for the patient to whom the observation applies.
    - event (Literal['OSTM', 'EFSTM']): Specifies the type of survival time being observed. 'OSTM' for Overall Survival Time,
      'EFSTM' for Event-Free Survival Time.
    - value (float): The duration of time (in months) from the start of the study until the occurrence of the event.

    Returns:
    - Observation: A FHIR Observation resource object with populated attributes according to the specified parameters.
    """
    observation = Observation.construct()
    observation.status = "final"
    observation.id = obs_id
    observation.subject = Reference.construct(reference=f"urn:uuid:{patient_id}")

    if event == 'OSTM':
        observation_text = (f'Event duration of the Overall Survival (OSSTAT) events is {value} months, '
                            f'since the beginning of the study.')

    elif event == 'EFSTM':
        observation_text = (f'Event duration of the Event Free Survival (EFSSTAT) is {value} months, since the '
                            f'beginning of the study..')

    else:
        raise AttributeError(f'Wrong event ("{event}") provided. '
                             f'The event needs to be one of these values: "OSTM", "EFSTM".')

    observation.text = {
        "status": "generated",
        "div": f"<div xmlns='http://www.w3.org/1999/xhtml'>: {observation_text}</div>"
    }

    observation.category = [CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://terminology.hl7.org/CodeSystem/observation-category",
            code="survey",
            display="Survey"
        )]
    )]

    observation.code = CodeableConcept.construct(
        coding=[Coding.construct(
            system="http://snomed.info/sct",
            code="445320007",
            display="Survival time"
        )
        ],
        text="Overall Survival Time (OSTM)" if event == 'OSTM' else "Event Free Survival Time (EFSTM)"
    )

    value_quantity = Quantity.construct()
    value_quantity.value = value
    value_quantity.unit = 'months'
    value_quantity.system = 'http://unitsofmeasure.org'
    value_quantity.code = 'mo'

    observation.valueQuantity = value_quantity

    observation.note = [Annotation.construct(
        text=observation_text)]

    return observation



