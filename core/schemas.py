"""Pydantic schemas for person management."""
from pydantic import BaseModel, field_validator, Field


class BasePersonSchema(BaseModel):
    """Base schema for person data."""
    name: str = Field(...,description="Enter person's name")

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        """Validate the person's name."""
        if len(value) > 32:
            raise ValueError("Name must not exceed 32 characters")
        if not value.isalpha():
            raise ValueError("Name must contain only alphabetic characters")
        return value


class PersonCreateSchema(BasePersonSchema):
    """Schema for creating a person."""


class PersonResponseSchema(BasePersonSchema):
    """Schema for returning person data."""
    id: int


class PersonUpdateSchema(BasePersonSchema):
    """Schema for updating a person."""
