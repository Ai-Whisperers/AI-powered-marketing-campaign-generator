"""
Dependency Injection Container.

Centralizes service instantiation and dependency management.
"""

from dependency_injector import containers, providers

from .config import get_project_config, get_settings
from .services.ai_client import AIClientManager, PromptLoader
from .services.analytics_service import AnalyticsService
from .services.brief_parser import BriefParserService
from .services.cache import AIResponseCache
from .services.export_service import ExportService
from .services.file_operations import FileOperationsService
from .services.ideas_service import IdeasService
from .services.iteration_service import IterationService
from .services.research_service import ResearchService
from .services.synthesis_service import SynthesisService
from .services.template_renderer import TemplateRenderer


class Container(containers.DeclarativeContainer):
    """Application DI container."""

    # Configuration
    config = providers.Singleton(get_settings)
    project_config = providers.Singleton(get_project_config)

    # Core Services
    ai_cache = providers.Singleton(AIResponseCache)

    prompt_loader = providers.Singleton(PromptLoader)

    ai_manager = providers.Singleton(AIClientManager)

    file_service = providers.Singleton(FileOperationsService)

    template_renderer = providers.Singleton(TemplateRenderer)

    # Business Services
    brief_parser = providers.Factory(BriefParserService)

    research_service = providers.Factory(ResearchService)

    synthesis_service = providers.Factory(SynthesisService)

    ideas_service = providers.Factory(IdeasService)

    export_service = providers.Factory(ExportService)

    iteration_service = providers.Factory(IterationService)

    analytics_service = providers.Factory(
        AnalyticsService, ai_manager=ai_manager, file_service=file_service
    )


# Global container instance
container = Container()


# Backward compatibility functions
def get_container() -> Container:
    """Get the DI container."""
    return container
