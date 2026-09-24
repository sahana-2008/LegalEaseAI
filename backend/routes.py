from fastapi import APIRouter, HTTPException

from backend.models import DocumentRequest, DocumentResponse
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()
generator = GeminiDocumentGenerator()


@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        result = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates,
        )

        return DocumentResponse(
            success=True,
            document_type=request.document_type,
            content=result.content,
            demo_mode=result.demo_mode,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Document generation failed: {exc}",
        ) from exc