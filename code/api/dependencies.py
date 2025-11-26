"""
Dependency functions for FastAPI routes.
"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException

from .config import get_settings
from .container import get_container

settings = get_settings()


# API Key Dependency
async def verify_api_key(x_api_key: str = Header(...)) -> str:
    """Verify API key from header."""
    if x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


APIKeyDep = Annotated[str, Depends(verify_api_key)]


# Service Dependencies
def get_file_service():
    """Get file operations service from container."""
    return get_container().file_service()


def get_brief_parser():
    """Get brief parser service from container."""
    return get_container().brief_parser()


def get_research_service():
    """Get research service from container."""
    return get_container().research_service()


def get_synthesis_service():
    """Get synthesis service from container."""
    return get_container().synthesis_service()


def get_ideas_service():
    """Get ideas service from container."""
    return get_container().ideas_service()


def get_export_service():
    """Get export service from container."""
    return get_container().export_service()


def get_iteration_service():
    """Get iteration service from container."""
    return get_container().iteration_service()


def get_analytics_service():
    """Get analytics service from container."""
    return get_container().analytics_service()


# Type aliases for cleaner route signatures
FileServiceDep = Annotated[object, Depends(get_file_service)]
BriefParserDep = Annotated[object, Depends(get_brief_parser)]
ResearchServiceDep = Annotated[object, Depends(get_research_service)]
SynthesisServiceDep = Annotated[object, Depends(get_synthesis_service)]
IdeasServiceDep = Annotated[object, Depends(get_ideas_service)]
ExportServiceDep = Annotated[object, Depends(get_export_service)]
IterationServiceDep = Annotated[object, Depends(get_iteration_service)]
AnalyticsServiceDep = Annotated[object, Depends(get_analytics_service)]
