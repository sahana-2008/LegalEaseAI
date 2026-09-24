from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2)
    parties: str = Field(..., min_length=2)
    terms: str = Field(..., min_length=2)
    dates: str = ""


class DocumentResponse(BaseModel):
    success: bool
    document_type: str
    content: str
    demo_mode: bool = False