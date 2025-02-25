from typing import List
from datetime import date, time
from sqlalchemy.orm import registry
from sqlmodel import Field
from .prw_meta_model import PrwMetaModel


class PrwPanelModel(PrwMetaModel, registry=registry()):
    pass


class PrwPatientPanel(PrwPanelModel, table=True):
    __tablename__ = "prw_patient_panels"

    id: int | None = Field(default=None, primary_key=True)
    prw_id: str = Field(
        unique=True,
        index=True,
        max_length=24,
        description="Reference to prw_patients",
    )
    panel_location: str | None = None
    panel_provider: str | None = None
