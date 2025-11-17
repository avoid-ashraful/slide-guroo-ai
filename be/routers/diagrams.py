"""
API router for diagram generation
"""
from fastapi import APIRouter, HTTPException
import logging

from models import DiagramRequest, DiagramResponse, DiagramType
from services.diagram_service import DiagramService

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize diagram service
diagram_service = DiagramService()

@router.post("/generate", response_model=DiagramResponse)
async def generate_diagram(request: DiagramRequest):
    """
    Generate a Mermaid diagram for a concept

    Args:
        request: Diagram request with concept and preferences

    Returns:
        Mermaid diagram code and metadata
    """
    logger.info(f"Generating diagram for concept: {request.concept}")

    try:
        result = await diagram_service.generate_diagram(
            concept=request.concept,
            diagram_type=request.diagram_type.value if request.diagram_type else None,
            context=request.context
        )

        # Map string to enum
        diagram_type_map = {
            'flowchart': DiagramType.FLOWCHART,
            'mindmap': DiagramType.MINDMAP,
            'timeline': DiagramType.TIMELINE,
            'tree': DiagramType.TREE,
            'network': DiagramType.NETWORK,
            'sequence': DiagramType.SEQUENCE
        }
        diagram_type_enum = diagram_type_map.get(
            result['diagram_type'],
            DiagramType.FLOWCHART
        )

        return DiagramResponse(
            diagram_code=result['diagram_code'],
            diagram_type=diagram_type_enum,
            explanation=result['explanation']
        )

    except Exception as e:
        logger.error(f"Error generating diagram: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating diagram: {str(e)}")

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "diagrams"}
