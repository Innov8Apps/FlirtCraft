"""
Base Pydantic schemas for FlirtCraft API responses.
"""

from typing import Any, Dict, Optional, Union
from datetime import datetime
from pydantic import BaseModel, Field
from uuid import UUID


class BaseResponse(BaseModel):
    """Base response schema for all API endpoints."""
    
    success: bool = Field(..., description="Whether the request was successful")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    class Config:
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            UUID: lambda uuid: str(uuid)
        }


class SuccessResponse(BaseResponse):
    """Success response schema with data payload."""
    
    success: bool = Field(True, description="Request successful")
    data: Any = Field(..., description="Response data")
    message: Optional[str] = Field(None, description="Optional success message")
    meta: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")


class ErrorResponse(BaseResponse):
    """Error response schema with error details."""
    
    success: bool = Field(False, description="Request failed")
    error: Dict[str, Any] = Field(..., description="Error details")
    
    @classmethod
    def create(
        cls,
        message: str,
        code: str = "UNKNOWN_ERROR",
        details: Optional[Dict[str, Any]] = None,
        status_code: int = 500
    ):
        """Create an error response."""
        return cls(
            error={
                "code": code,
                "message": message,
                "details": details or {},
                "status_code": status_code
            }
        )


class ValidationErrorResponse(ErrorResponse):
    """Validation error response with field-specific errors."""
    
    @classmethod
    def create(
        cls,
        field_errors: Dict[str, str],
        message: str = "Validation failed"
    ):
        """Create a validation error response."""
        return cls(
            error={
                "code": "VALIDATION_ERROR",
                "message": message,
                "details": {"field_errors": field_errors},
                "status_code": 422
            }
        )


# Common schemas for API operations
class PaginationParams(BaseModel):
    """Common pagination parameters."""
    
    page: int = Field(1, ge=1, description="Page number (1-indexed)")
    per_page: int = Field(20, ge=1, le=100, description="Items per page")
    
    @property
    def offset(self) -> int:
        """Calculate offset for database queries."""
        return (self.page - 1) * self.per_page


class PaginatedResponse(BaseModel):
    """Paginated response wrapper."""
    
    items: list = Field(..., description="List of items")
    total: int = Field(..., description="Total number of items")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Items per page")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there is a next page")
    has_prev: bool = Field(..., description="Whether there is a previous page")
    
    @classmethod
    def create(
        cls,
        items: list,
        total: int,
        page: int,
        per_page: int
    ):
        """Create a paginated response."""
        pages = (total + per_page - 1) // per_page  # Ceiling division
        
        return cls(
            items=items,
            total=total,
            page=page,
            per_page=per_page,
            pages=pages,
            has_next=page < pages,
            has_prev=page > 1
        )


class HealthCheckResponse(BaseModel):
    """Health check response schema."""
    
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    environment: str = Field(..., description="Environment name")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    database: Optional[Dict[str, Any]] = Field(None, description="Database health info")
    dependencies: Optional[Dict[str, Any]] = Field(None, description="External dependencies status")


# Common field validators and types
class EmailStr(str):
    """Email string type with validation."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        
        # Basic email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v):
            raise ValueError('invalid email format')
        
        return v.lower().strip()


class SecurePassword(str):
    """Secure password type with validation."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        
        if len(v) < 8:
            raise ValueError('password must be at least 8 characters long')
        
        # Check for required character types
        import re
        if not re.search(r'[A-Z]', v):
            raise ValueError('password must contain at least one uppercase letter')
        
        if not re.search(r'[a-z]', v):
            raise ValueError('password must contain at least one lowercase letter')
        
        if not re.search(r'[0-9]', v):
            raise ValueError('password must contain at least one number')
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', v):
            raise ValueError('password must contain at least one special character')
        
        return v