"""
API Routes Package
"""

from .projects import router as projects_router
from .brief import router as brief_router
from .research import router as research_router
from .ideas import router as ideas_router
from .export import router as export_router
from .iteration import router as iteration_router
from .analytics import router as analytics_router

__all__ = [
    "projects_router",
    "brief_router",
    "research_router",
    "ideas_router",
    "export_router",
    "iteration_router",
    "analytics_router",
]
