from __future__ import annotations

from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProjectStatus(str, Enum):
    DRAFT = "Draft"
    COMPLETED = "Completed"


class ProjectCreateRequest(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=1000)
    status: ProjectStatus = Field(default=ProjectStatus.DRAFT)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None = None
    status: ProjectStatus
    created_at: datetime
    updated_at: datetime
