from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    mission: Optional[str] = None
    size: Optional[int] = None  # number of employees or volunteers
    annual_budget: Optional[float] = None
    location: Optional[str] = None
    keywords: Optional[str] = None  # comma-separated tags

    grants: List["GrantOpportunity"] = Relationship(back_populates="organization")


class GrantOpportunity(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    source: str
    external_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    agency: Optional[str] = None
    eligibility_criteria: Optional[str] = None
    deadline: Optional[datetime] = None
    url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    organization_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    organization: Optional[Organization] = Relationship(back_populates="grants")

    scores: List["EligibilityScore"] = Relationship(back_populates="grant")
    drafts: List["ProposalDraft"] = Relationship(back_populates="grant")


class EligibilityScore(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organization_id: int = Field(foreign_key="organization.id")
    grant_id: int = Field(foreign_key="grantopportunity.id")
    score: float
    note: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    organization: Optional[Organization] = Relationship()
    grant: Optional[GrantOpportunity] = Relationship(back_populates="scores")


class ProposalDraft(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    grant_id: int = Field(foreign_key="grantopportunity.id")
    organization_id: int = Field(foreign_key="organization.id")
    section: Optional[str] = None
    content: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    grant: Optional[GrantOpportunity] = Relationship(back_populates="drafts")
    organization: Optional[Organization] = Relationship()
