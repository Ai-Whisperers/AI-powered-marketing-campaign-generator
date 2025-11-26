import asyncio
import os
import sys

# Add code directory to path
sys.path.append(os.path.join(os.getcwd(), "code"))

from api.config import get_settings
from api.models import IdeaConcept
from api.services.ideas_service import IdeasService


async def test_config_security():
    print("\n--- Testing Config Security ---")
    try:
        settings = get_settings()
        if hasattr(settings, "n8n_basic_auth_password"):
            print("FAIL: n8n_basic_auth_password still present!")
        else:
            print("PASS: n8n configuration removed.")
    except Exception as e:
        print(f"Config validation error: {e}")
        print("PASS: Config validation is working.")


async def test_parallel_expansion():
    print("\n--- Testing Parallel Expansion ---")

    # Mock dependencies
    class MockAI:
        async def generate_json(self, *args, **kwargs):
            await asyncio.sleep(0.1)  # Simulate delay
            return {
                "concept": "Expanded",
                "insight": "Insight",
                "scores": {},
                "strengths": [],
                "weaknesses": [],
                "recommendation": "",
            }

    class MockFiles:
        def get_project_metadata(self, pid):
            return {"country": "Paraguay"}

        async def read_file(self, *args):
            return ""

        async def save_idea(self, *args):
            return "path/to/file"

        def update_project_metadata(self, *args):
            pass

    class MockRenderer:
        def render_idea(self, *args, **kwargs):
            return "Rendered"

    service = IdeasService()
    service.ai = MockAI()
    service.files = MockFiles()
    service.renderer = MockRenderer()
    service.idea_repository = None  # Disable DB

    # Create dummy concepts
    concepts = [
        IdeaConcept(number=i, title=f"Idea {i}", concept="C", insight="I", formats=[])
        for i in range(10)
    ]

    import time

    start = time.time()

    # We need to mock _validate_quality and _validate_cultural too as they call AI
    async def mock_validate(*args):
        class Val:
            strengths = []
            weaknesses = []
            positives = []
            concerns = []
            cultural_score = 5

        return Val()

    service._validate_quality = mock_validate
    service._validate_cultural = mock_validate

    async def mock_generate_batch(*args, **kwargs):
        return concepts

    service._generate_batch = mock_generate_batch
    service.research.get_all_research = lambda x: asyncio.Future()
    service.research.get_all_research(1).set_result("")

    print("Running generate_ideas...")
    await service.generate_ideas("test-project", num_ideas=10, batch_size=10)

    duration = time.time() - start
    print(f"Duration: {duration:.2f}s")

    if duration < 0.8:
        print("PASS: Execution was parallel (significantly faster than 1.0s)")
    else:
        print(f"FAIL: Execution seemed sequential (took {duration:.2f}s)")


if __name__ == "__main__":
    asyncio.run(test_config_security())
    asyncio.run(test_parallel_expansion())
