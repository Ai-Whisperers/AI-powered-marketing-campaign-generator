#!/usr/bin/env python3
"""
Maga CLI
========
Unified command line interface for the Campaign Generator.
Replaces the legacy tools/generate_campaign.py script.
"""

import asyncio
import os
import sys

# --- Patch for gpt-researcher compatibility with langchain >= 0.3 ---
import typer
from rich.console import Console
from rich.table import Table

# --------------------------------------------------------------------

# Add code directory to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.config import get_settings
from api.logging_config import setup_logging
from api.services.file_operations import get_file_service
from api.services.ideas_service import get_ideas_service
from api.services.research_service import get_research_service

# Initialize Typer app and Rich console
app = typer.Typer(help="Campaign Generator CLI")
console = Console()


def setup():
    """Initialize configuration and logging."""
    setup_logging(level="INFO", environment="cli")


@app.command()
def info():
    """Show system information."""
    setup()
    config = get_settings()

    table = Table(title="System Information")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("AI Provider", config.ai.primary)
    table.add_row(
        "Model",
        config.ai.anthropic.model if config.ai.primary == "anthropic" else config.ai.openai.model,
    )
    table.add_row("Default Country", config.project.default_country)
    table.add_row("Scoring Criteria", str(len(config.scoring.criteria)))

    console.print(table)


@app.command()
def new(
    brand: str = typer.Option(..., help="Brand name"),
    country: str = typer.Option("Paraguay", help="Target country"),
    project_id: str = typer.Option(None, help="Project identifier (default: brand-country-year)"),
    type: str = typer.Option("digital", help="Campaign type"),
):
    """Create a new campaign project."""
    setup()

    async def _run():
        service = get_file_service()

        # Generate ID if not provided
        pid = project_id
        if not pid:
            from datetime import datetime

            year = datetime.now().year
            safe_brand = "".join(c if c.isalnum() else "-" for c in brand.lower()).strip("-")
            safe_country = "".join(c if c.isalnum() else "-" for c in country.lower()).strip("-")
            pid = f"campana-{safe_brand}-{safe_country}-{year}"

        console.print(f"[bold blue]Creating project: {pid}[/bold blue]")

        try:
            result = await service.create_project_structure(
                project_id=pid,
                project_name=f"Campaña {brand} {country}",
                client=brand,
                country=country,
                campaign_type=type,
            )

            console.print("[bold green]Successfully created project![/bold green]")
            console.print(f"  ID: {result['id']}")
            console.print(f"  Path: {result['path']}")

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    asyncio.run(_run())


@app.command()
def generate(
    project_id: str = typer.Option(..., help="Project identifier (e.g., brand-country-year)"),
    num_ideas: int = typer.Option(15, help="Number of ideas to generate"),
    batch_size: int = typer.Option(5, help="Ideas per batch"),
):
    """Generate campaign ideas."""
    setup()

    async def _run():
        service = get_ideas_service()
        console.print(
            f"[bold blue]Generating {num_ideas} ideas for project: {project_id}[/bold blue]"
        )

        try:
            response = await service.generate_ideas(
                project_id=project_id, num_ideas=num_ideas, batch_size=batch_size
            )

            console.print(
                f"[bold green]Successfully generated {response.ideas_generated} ideas![/bold green]"
            )
            for f in response.files_created:
                console.print(f"  - {f}")

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    asyncio.run(_run())


@app.command()
def score(
    project_id: str = typer.Option(..., help="Project identifier"),
):
    """Score and rank existing ideas."""
    setup()

    async def _run():
        service = get_ideas_service()
        console.print(f"[bold blue]Scoring ideas for project: {project_id}[/bold blue]")

        try:
            response = await service.score_all_ideas(project_id=project_id)

            console.print(f"[bold green]Scored {response.total_ideas} ideas![/bold green]")

            # Show tier distribution
            table = Table(title="Tier Distribution")
            table.add_column("Tier", style="cyan")
            table.add_column("Count", style="magenta")

            for tier, count in response.tier_distribution.items():
                table.add_row(tier, str(count))

            console.print(table)
            console.print(f"Summary saved to: {response.summary_file}")

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    asyncio.run(_run())


@app.command()
def research(
    project_id: str = typer.Option(..., help="Project identifier"),
    url: str = typer.Option(None, help="URL to add as research source"),
    category: str = typer.Option("01-mercado-general", help="Research category"),
):
    """Manage research or add a new source."""
    setup()

    async def _run():
        service = get_research_service()

        if url:
            console.print(f"[bold blue]Adding research source: {url}[/bold blue]")
            from api.models import ResearchSource

            source = ResearchSource(
                url=url, title="Web Source", category=category, type="web"  # Will be fetched
            )

            try:
                response = await service.add_research(project_id, [source])
                console.print("[bold green]Added source successfully![/bold green]")
                for f in response.files_created:
                    console.print(f"  - {f}")
            except Exception as e:
                console.print(f"[bold red]Error:[/bold red] {e}")
                sys.exit(1)
        else:
            # List research (could be implemented)
            console.print("[yellow]Please provide a URL to add research.[/yellow]")

    asyncio.run(_run())


from api.services.video_service import get_video_service

# ... (existing imports)


@app.command()
def video_prompts(
    project_id: str = typer.Option(..., help="Project identifier"),
):
    """Generate Veo 3 video prompts for ideas."""
    setup()

    async def _run():
        service = get_video_service()
        console.print(f"[bold blue]Generating video prompts for project: {project_id}[/bold blue]")

        try:
            files = await service.generate_video_prompts(project_id)

            if files:
                console.print(
                    f"[bold green]Successfully generated {len(files)} prompts![/bold green]"
                )
                for f in files:
                    console.print(f"  - {f}")
            else:
                console.print(
                    "[yellow]No video content found in ideas or generation failed.[/yellow]"
                )

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    asyncio.run(_run())


@app.command()
def generate_videos(
    project_id: str = typer.Option(..., help="Project identifier"),
):
    """Generate actual videos using Veo 3 (costs money)."""
    setup()

    async def _run():
        service = get_video_service()
        console.print(f"[bold blue]Generating videos for project: {project_id}[/bold blue]")
        console.print(
            "[yellow]Warning: This will use Google Cloud Vertex AI and incur costs.[/yellow]"
        )

        try:
            files = await service.generate_videos(project_id)

            if files:
                console.print(
                    f"[bold green]Successfully generated {len(files)} videos![/bold green]"
                )
                for f in files:
                    console.print(f"  - {f}")
            else:
                console.print("[yellow]No videos generated. Check config and prompts.[/yellow]")

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            sys.exit(1)

    asyncio.run(_run())


@app.command()
def generate_branded_videos(
    project_id: str = typer.Option(..., help="Project identifier"),
    parallel: int = typer.Option(3, help="Number of parallel video generations"),
    dry_run: bool = typer.Option(False, help="Estimate cost without generating"),
    prompts_only: bool = typer.Option(False, help="Generate prompts only, skip videos"),
):
    """Generate Veo 3.1 videos for ALL ideas with Nestlé branding."""
    setup()

    async def _run():
        from api.services.batch_video_agent import get_batch_video_agent

        agent = get_batch_video_agent(parallel_limit=parallel)

        console.print(f"[bold blue]Batch Video Generation for: {project_id}[/bold blue]")
        console.print(f"Parallel limit: {parallel}")

        if dry_run:
            console.print("[yellow]DRY RUN MODE - No generation will occur[/yellow]")
        elif prompts_only:
            console.print("[yellow]PROMPTS ONLY - Videos will not be generated[/yellow]")
        else:
            console.print("[yellow]⚠️  WARNING: This will use Veo 3.1 API and incur costs![/yellow]")

        try:
            report = await agent.generate_all_videos(
                project_id=project_id, dry_run=dry_run, generate_videos=not prompts_only
            )

            # Display results
            console.print("\n[bold green]Batch Video Generation Report[/bold green]")
            console.print(f"Total ideas: {report.total_ideas}")
            console.print(f"Prompts generated: {report.prompts_generated}")
            console.print(f"Videos generated: {report.videos_generated}")
            console.print(f"Estimated cost: ${report.total_cost_estimate:.2f} USD")

            if report.errors:
                console.print(f"\n[yellow]Errors: {len(report.errors)}[/yellow]")
                for error in report.errors[:5]:  # Show first 5 errors
                    console.print(f"  - {error}")

            if not dry_run:
                console.print("\n[bold green]✓ Generation complete![/bold green]")
                console.print(f"Check project directory for generated files")

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
            import traceback

            console.print(traceback.format_exc())
            sys.exit(1)

    asyncio.run(_run())


if __name__ == "__main__":
    app()
