"""
Full Pipeline Test Script

Tests the complete campaign generation workflow without n8n.
Runs all steps: create project, parse brief, research, ideas, export.
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime
from pathlib import Path

# API Base URL
API_URL = "http://localhost:8000"

# Data folder for test inputs
DATA_DIR = Path(__file__).parent / "data" / "test_inputs"


def load_test_data(filename: str) -> dict:
    """Load test data from JSON file."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        print(f"WARNING: Test data file not found: {filepath}")
        return {}


def get_test_brief() -> str:
    """Get test brief content from file or use default."""
    data = load_test_data("sample_brief.json")
    if data and "content" in data:
        return data["content"]

    # Fallback to embedded brief
    return """
Café Central es una cadena de cafeterías premium en Paraguay que busca lanzar una campaña para su nueva línea de cafés de especialidad. El objetivo es posicionarse como la opción preferida para los amantes del café que buscan calidad y experiencia única.

**Público objetivo:**
- Profesionales de 25-45 años
- NSE ABC1
- Ubicados en Asunción y área metropolitana
- Apasionados por el café de calidad

**Mensajes clave:**
1. Granos de origen único seleccionados
2. Tostado artesanal en pequeños lotes
3. Experiencia de barista profesional
4. Ambiente acogedor para trabajo y reuniones

**Canales:**
- Instagram y TikTok
- Influencers locales de lifestyle
- Publicidad digital geolocalizada

**Presupuesto:** $25,000 USD
**Timeline:** 2 meses

**Restricciones:**
- No usar comparaciones directas con competencia
- Mantener tono sofisticado pero accesible
- Fotografía real, no stock
"""


def get_test_project() -> dict:
    """Get test project data from file or use default."""
    data = load_test_data("sample_project.json")
    if data:
        return data

    # Fallback to default project
    return {
        "name": "Café Central Specialty Launch",
        "client": "Café Central",
        "campaign_type": "Product Launch",
        "country": "Paraguay",
        "language": "es"
    }


async def test_pipeline():
    """Run the complete campaign generation pipeline."""

    print("=" * 60)
    print("CAMPAIGN GENERATOR - FULL PIPELINE TEST")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    async with httpx.AsyncClient(timeout=900.0) as client:  # 15 minute timeout for ideas generation

        # Load test data
        project_data = get_test_project()
        brief_content = get_test_brief()

        print(f"Test data directory: {DATA_DIR}")
        print(f"Project: {project_data.get('name', 'Unknown')}")
        print()

        # Step 1: Create Project
        print("STEP 1: Creating Project...")
        print("-" * 40)

        response = await client.post(
            f"{API_URL}/projects",
            json=project_data
        )

        if response.status_code != 200:
            print(f"ERROR: {response.text}")
            return

        project = response.json()
        project_id = project["id"]
        print(f"Project created: {project_id}")
        print(f"Name: {project['name']}")
        print()

        # Step 2: Parse Brief
        print("STEP 2: Parsing Brief...")
        print("-" * 40)

        response = await client.post(
            f"{API_URL}/projects/{project_id}/brief/parse",
            json={"content": brief_content}
        )

        if response.status_code != 200:
            print(f"ERROR: {response.text}")
            return

        brief = response.json()
        print(f"Challenge: {brief.get('challenge', {}).get('main_challenge', 'N/A')[:100]}...")
        print(f"Target: {brief.get('target', {}).get('primary', 'N/A')[:100]}...")
        print(f"Directions: {len(brief.get('directions', []))} creative directions")
        print()

        # Step 3: Auto-fetch Research (generates queries, searches, fetches content)
        print("STEP 3: Auto-fetching Research...")
        print("-" * 40)
        print("(This searches the web and fetches real content - may take a minute)")

        response = await client.post(
            f"{API_URL}/projects/{project_id}/research/auto-fetch",
            json={
                "num_queries": 8,
                "results_per_query": 2
            }
        )

        if response.status_code != 200:
            print(f"WARNING: Auto-fetch failed: {response.text}")
            print("Continuing without web research...")
        else:
            fetch_result = response.json()
            print(f"Status: {fetch_result.get('status', 'N/A')}")
            print(f"Queries generated: {fetch_result.get('queries_generated', 0)}")
            print(f"Search results: {fetch_result.get('search_results', 0)}")
            print(f"Sources added: {fetch_result.get('sources_added', 0)}")
            files_created = fetch_result.get('files_created', [])
            if files_created:
                print(f"Files created: {len(files_created)}")
                for f in files_created[:3]:
                    print(f"  - {f}")
                if len(files_created) > 3:
                    print(f"  ... and {len(files_created) - 3} more")
        print()

        # Step 4: Synthesize Research
        print("STEP 4: Synthesizing Research...")
        print("-" * 40)

        response = await client.post(
            f"{API_URL}/projects/{project_id}/research/synthesize",
            json={}
        )

        if response.status_code != 200:
            print(f"ERROR: {response.text}")
            return

        synthesis = response.json()
        print(f"Files created: {len(synthesis.get('files_created', []))}")
        if synthesis.get('quick_reference'):
            qr = synthesis['quick_reference']
            print(f"Challenge: {qr.get('challenge_one_liner', 'N/A')[:80]}...")
            print(f"Insights: {len(qr.get('key_insights', []))} key insights")
            print(f"Do's: {len(qr.get('dos', []))} items")
            print(f"Don'ts: {len(qr.get('donts', []))} items")
        print()

        # Step 5: Generate Ideas
        print("STEP 5: Generating Ideas...")
        print("-" * 40)

        response = await client.post(
            f"{API_URL}/projects/{project_id}/ideas/generate",
            json={
                "num_ideas": 5,  # Reduced for faster testing
                "batch_size": 5
            }
        )

        if response.status_code != 200:
            print(f"ERROR: {response.text}")
            return

        ideas_result = response.json()
        print(f"Ideas generated: {ideas_result.get('ideas_generated', 0)}")
        files_created = ideas_result.get('files_created', [])
        print(f"Files created: {len(files_created)}")
        if files_created:
            for f in files_created[:5]:
                print(f"  - {f}")
            if len(files_created) > 5:
                print(f"  ... and {len(files_created) - 5} more")
        print()

        # Step 6: Score Ideas
        print("STEP 6: Scoring Ideas...")
        print("-" * 40)

        response = await client.post(
            f"{API_URL}/projects/{project_id}/ideas/score",
            json={}
        )

        if response.status_code != 200:
            print(f"ERROR: {response.text}")
            return

        score_result = response.json()
        print(f"Total ideas scored: {score_result.get('total_ideas', 0)}")

        tier_dist = score_result.get('tier_distribution', {})
        print(f"Tier distribution:")
        for tier, count in sorted(tier_dist.items()):
            print(f"  {tier}: {count} ideas")

        top_ideas = score_result.get('top_ideas', [])
        if top_ideas:
            print(f"\nTop 5 Ideas:")
            for i, idea in enumerate(top_ideas[:5], 1):
                print(f"  {i}. [{idea.get('overall_score', 0):.1f}] {idea.get('title', 'N/A')[:50]}...")
        print()

        # Step 7: Analyze Idea Gaps
        print("STEP 7: Analyzing Idea Gaps...")
        print("-" * 40)

        response = await client.post(
            f"{API_URL}/projects/{project_id}/ideas/analyze-gaps",
            json={}
        )

        if response.status_code != 200:
            print(f"ERROR: {response.text}")
            return

        gaps_result = response.json()
        print(f"Quality score: {gaps_result.get('quality_score', 0)}")

        weak_dims = gaps_result.get('weak_dimensions', [])
        if weak_dims:
            print(f"Weak dimensions:")
            for dim in weak_dims[:3]:
                avg_score = dim.get('average_score', 0)
                try:
                    score_str = f"{float(avg_score):.1f}"
                except (ValueError, TypeError):
                    score_str = str(avg_score)
                print(f"  - {dim.get('dimension', 'N/A')}: {score_str}")

        recs = gaps_result.get('recommendations', {})
        if recs.get('generate_more'):
            print(f"Recommendation: Generate {recs.get('num_additional', 0)} more ideas")
            print(f"Focus areas: {', '.join(recs.get('focus_areas', []))}")
        print()

        # Step 8: Generate Targeted Ideas (if recommended)
        if gaps_result.get('recommendations', {}).get('generate_more'):
            print("STEP 8: Generating Targeted Ideas...")
            print("-" * 40)

            focus = gaps_result.get('weak_dimensions', [{}])[0].get('dimension', 'viral_potential')

            response = await client.post(
                f"{API_URL}/projects/{project_id}/ideas/generate-targeted",
                json={
                    "focus": focus,
                    "num_ideas": 5
                }
            )

            if response.status_code == 200:
                targeted_result = response.json()
                print(f"Generated {len(targeted_result.get('ideas', []))} targeted ideas")
                print(f"Focus: {targeted_result.get('focus_addressed', focus)}")
                print(f"Total ideas now: {targeted_result.get('total_ideas_now', 0)}")
            else:
                print(f"WARNING: Targeted generation failed: {response.text}")
            print()

        # Step 9: Export PDF
        print("STEP 9: Exporting PDF...")
        print("-" * 40)

        response = await client.post(
            f"{API_URL}/projects/{project_id}/export/pdf",
            json={
                "format": "pdf",
                "include_research": True,
                "top_ideas_count": 10
            }
        )

        if response.status_code != 200:
            print(f"ERROR: {response.text}")
            return

        pdf_result = response.json()
        print(f"PDF created: {pdf_result.get('file_path', 'N/A').split('/')[-1]}")
        print(f"Size: {pdf_result.get('file_size', 0) / 1024:.1f} KB")
        print()

        # Step 10: Export PowerPoint
        print("STEP 10: Exporting PowerPoint...")
        print("-" * 40)

        response = await client.post(
            f"{API_URL}/projects/{project_id}/export/pptx",
            json={
                "format": "pptx",
                "include_research": True,
                "top_ideas_count": 10
            }
        )

        if response.status_code != 200:
            print(f"ERROR: {response.text}")
            return

        pptx_result = response.json()
        print(f"PPTX created: {pptx_result.get('file_path', 'N/A').split('/')[-1]}")
        print(f"Size: {pptx_result.get('file_size', 0) / 1024:.1f} KB")
        print()

        # Summary
        print("=" * 60)
        print("PIPELINE COMPLETE")
        print("=" * 60)
        print(f"Project ID: {project_id}")
        print(f"Total Ideas: {score_result.get('total_ideas', 0)}")
        print(f"Top Score: {top_ideas[0].get('overall_score', 0) if top_ideas else 0:.1f}")
        print(f"Exports: PDF + PPTX")
        print()
        print(f"View exports at: {API_URL}/projects/{project_id}/export")
        print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    print("\nStarting full pipeline test...\n")

    try:
        asyncio.run(test_pipeline())
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
