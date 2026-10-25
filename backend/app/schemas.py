from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator

TicketStatus = Literal["open", "in_progress", "resolved", "closed"]
TicketPriority = Literal["low", "medium", "high", "critical"]


def _clean_optional(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value or None


class TicketInput(BaseModel):
    """Body used by POST (create) and PUT (full replacement)."""

    title: str = Field(..., min_length=1, max_length=200, examples=["Login page returns 500"])
    description: str | None = Field(default=None, max_length=5000)
    status: TicketStatus = "open"
    priority: TicketPriority = "medium"
    assignee: str | None = Field(default=None, max_length=100)

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if len(value) < 3:
            raise ValueError("title must be at least 3 characters (surrounding spaces are ignored)")
        return value

    @field_validator("description", "assignee")
    @classmethod
    def validate_optional_text(cls, value: str | None) -> str | None:
        return _clean_optional(value)


class TicketOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    status: TicketStatus
    priority: TicketPriority
    assignee: str | None
    created_at: datetime

    @field_serializer("created_at")
    def serialize_created_at(self, value: datetime) -> str:
        # Send ISO 8601 in UTC with a trailing "Z" so the browser shows local time correctly.
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
