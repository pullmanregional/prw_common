from datetime import datetime
from typing import Optional
from sqlalchemy.orm import registry
from sqlmodel import SQLModel, Field
from .prw_meta_model import PrwMetaModel, PrwMeta, PrwSourcesMeta


class PrwFinanceModel(PrwMetaModel, registry=registry()):
    pass


class PrwVolume(PrwFinanceModel, table=True):
    __tablename__ = "prw_volumes"
    id: Optional[int] = Field(default=None, primary_key=True)
    dept_wd_id: str = Field(max_length=10)
    dept_name: Optional[str] = None
    month: str = Field(max_length=7)
    volume: int
    unit: Optional[str] = None


class PrwMiscVolume(PrwFinanceModel, table=True):
    """
    Contains miscellaneous volumes that are not yet captured by ingested Epic data. This table
    is temporary and will beremoved once the source rows (eg. pharmacy dispenses) are available.
    """

    __tablename__ = "prw_volumes_misc"
    id: Optional[int] = Field(default=None, primary_key=True)
    month: str = Field(max_length=7)
    metric: str = Field(max_length=32)
    volume: int


class PrwUOS(PrwFinanceModel, table=True):
    __tablename__ = "prw_uos"
    id: Optional[int] = Field(default=None, primary_key=True)
    dept_wd_id: str = Field(max_length=10)
    dept_name: Optional[str] = None
    month: str = Field(max_length=7)
    volume: float
    unit: Optional[str] = None


class PrwBudget(PrwFinanceModel, table=True):
    __tablename__ = "prw_budget"
    id: Optional[int] = Field(default=None, primary_key=True)
    dept_wd_id: str = Field(max_length=10)
    dept_name: Optional[str] = None
    year: int
    budget_fte: float
    budget_prod_hrs: float
    budget_contracted_hours: float
    budget_volume: float
    budget_uos: float
    budget_prod_hrs_per_uos: float
    hourly_rate: float


class PrwHours(PrwFinanceModel, table=True):
    __tablename__ = "prw_hours"
    id: Optional[int] = Field(default=None, primary_key=True)
    month: str = Field(max_length=7)
    dept_wd_id: str = Field(max_length=10)
    dept_name: Optional[str] = None
    reg_hrs: float
    overtime_hrs: float
    prod_hrs: float
    nonprod_hrs: float
    total_hrs: float
    total_fte: float


class PrwContractedHoursMeta(PrwFinanceModel, table=True):
    __tablename__ = "prw_contracted_hours_meta"
    id: Optional[int] = Field(default=None, primary_key=True)
    contracted_hours_updated_month: str


class PrwContractedHours(PrwFinanceModel, table=True):
    __tablename__ = "prw_contracted_hours"
    id: Optional[int] = Field(default=None, primary_key=True)
    dept_wd_id: str = Field(max_length=10)
    dept_name: Optional[str] = None
    year: int
    hrs: Optional[float] = None
    ttl_dept_hrs: float


class PrwHoursByPayPeriod(PrwFinanceModel, table=True):
    __tablename__ = "prw_hours_by_pay_period"
    id: Optional[int] = Field(default=None, primary_key=True)
    pay_period: str = Field(max_length=7)
    start_date: datetime
    dept_wd_id: str = Field(max_length=10)
    dept_name: Optional[str] = None
    reg_hrs: float
    overtime_hrs: float
    prod_hrs: float
    nonprod_hrs: float
    total_hrs: float
    total_fte: float


class PrwIncomeStmt(PrwFinanceModel, table=True):
    __tablename__ = "prw_income_stmt"
    id: Optional[int] = Field(default=None, primary_key=True)
    month: str = Field(max_length=7)
    ledger_acct: str
    dept_wd_id: str = Field(max_length=48)
    dept_name: Optional[str] = None
    spend_category: Optional[str] = None
    revenue_category: Optional[str] = None
    actual: float
    budget: float
    actual_ytd: float
    budget_ytd: float


class PrwBalanceSheet(PrwFinanceModel, table=True):
    __tablename__ = "prw_balance_sheet"
    id: Optional[int] = Field(default=None, primary_key=True)
    month: str = Field(max_length=7)
    tree: str = Field(
        description="Tree path for this line item, with levels separated by '|', which forms a hierarchy for line items in balance sheet"
    )
    line_num: int = Field(
        description="Line number for this line item that represents the placement of this line in the balance sheet. Items in a given month with always have contiguous line numbers."
    )
    ledger_acct: str = Field(
        description="Line item in the balance sheet, eg 'Cash and Short Term Investments' or '10405:Patient Refunds'"
    )
    actual: float | None


class PrwAgedAR(PrwFinanceModel, table=True):
    __tablename__ = "prw_aged_ar"
    id: Optional[int] = Field(default=None, primary_key=True)
    date: str = Field(
        max_length=10,
        description="Date that this AR metric was calculated in format YYYY-MM-DD",
    )
    aged_days: str = Field(
        max_length=10,
        description="Age bucket in days (eg '1-30') since patient's discharge date.",
    )
    total: float
    num_accts: int
