from typing import List
from datetime import datetime, time
from sqlalchemy.orm import registry
from sqlmodel import Field, Relationship
from sqlalchemy import BigInteger
from .prw_meta_model import PrwMetaModel, PrwMeta, PrwSourcesMeta


class PrwModel(PrwMetaModel, registry=registry()):
    pass


class PrwPatient(PrwModel, table=True):
    __tablename__ = "prw_patients"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(
        unique=True,
        index=True,
        max_length=24,
        description="ID hash from unique salt and row ID",
    )
    sex: str = Field(regex="^[MFO]$")
    age: int | None = Field(description="Age in years")
    age_in_mo_under_3: int | None = Field(description="Age in months if <3yo")
    city: str | None = None
    state: str | None = None
    pcp: str | None = None

    allergy: str | None = None


class PrwEncounterOutpt(PrwModel, table=True):
    __tablename__ = "prw_encounters_outpt"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(index=True, max_length=24)
    dept: str
    encounter_date: datetime
    encounter_time: str = Field(
        max_length=4, description="Time of encounter as HHSS in 24-hour format"
    )
    encounter_age: int | None = Field(description="Age in years at encounter")
    encounter_age_in_mo_under_3: int | None = Field(
        description="Age in months at encounter if <3yo"
    )
    encounter_type: str
    service_provider: str | None = None
    billing_provider: str | None = None
    with_pcp: bool | None = None
    appt_status: str | None = None
    diagnoses: str | None = None
    diagnoses_icd: str | None = None
    level_of_service: str | None = None


class PrwEncounterInpt(PrwModel, table=True):
    __tablename__ = "prw_encounters_inpt"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(index=True, max_length=24)
    admission_date: datetime | None = None
    discharge_date: datetime | None = None
    diagnosis: str | None = None
    dept: str | None = None


class PrwEncounterEd(PrwModel, table=True):
    __tablename__ = "prw_encounters_ed"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(index=True, max_length=24)
    arrival_date: datetime
    arrival_time: str = Field(
        max_length=4, description="Time of encounter as HHSS in 24-hour format"
    )
    departure_date: datetime
    departure_time: str = Field(max_length=4)
    encounter_age: int | None = Field(description="Age in years at encounter")
    chief_complaint: str | None = None
    diagnosis: str | None = None
    first_attending: str | None = None
    last_attending: str | None = None


class PrwNotesInpt(PrwModel, table=True):
    __tablename__ = "prw_notes_inpt"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(index=True, max_length=24)

    service_date: datetime | None = None
    encounter_age: int | None = Field(
        description="Age in years at service date of note"
    )
    dept: str | None = None
    service: str | None = None
    note_type: str | None = None
    diagnosis: str | None = None
    author_name: str | None = None
    author_type: str | None = None
    first_author_name: str | None = None
    cosigner_name: str | None = None


class PrwNotesEd(PrwModel, table=True):
    __tablename__ = "prw_notes_ed"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(index=True, max_length=24)

    service_date: datetime | None = None
    encounter_age: int | None = Field(
        description="Age in years at service date of note"
    )
    dept: str | None = None
    service: str | None = None
    note_type: str | None = None
    diagnosis: str | None = None
    author_name: str | None = None
    author_type: str | None = None
    first_author_name: str | None = None
    cosigner_name: str | None = None


class PrwMyChart(PrwModel, table=True):
    __tablename__ = "prw_mychart"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(unique=True, index=True, max_length=24)
    mychart_status: str | None = None
    mychart_activation_date: datetime | None


class PrwCharges(PrwModel, table=True):
    __tablename__ = "prw_charges"
    id: int = Field(
        primary_key=True,
        sa_type=BigInteger,
        description="Equal to BillingTransactionFact.BillingTransactionKey",
        sa_column_kwargs={"autoincrement": False},
    )
    prw_id: str | None = Field(index=True, max_length=24)
    encounter_csn: str | None = None
    service_date: datetime | None = None
    post_date: datetime | None = None
    billing_provider: str | None = None
    posting_user: str | None = None
    procedure_code: str | None = None
    modifiers: str | None = None
    quantity: int | None = None
    procedure_desc: str | None = None
    rev_code: str | None = None
    rev_code_desc: str | None = None
    wrvu: float | None = None
    trvu: float | None = None
    reversal_reason: str | None = None
    charge_amount: float | None = None
    is_inactive: bool | None = None
    primary_payor_class: str | None = None
    dept: str | None = None
    location: str | None = None


class PrwImaging(PrwModel, table=True):
    __tablename__ = "prw_imaging"

    id: int | None = Field(default=None, primary_key=True)
    imaging_key: int = Field(
        sa_type=BigInteger,
        description="Equal to ImagingFact.ImagingKey",
    )

    dept: str
    scheduled_date: datetime | None = None
    service_date: datetime | None = None
    modality: str | None = None
    study_status: str | None = None
