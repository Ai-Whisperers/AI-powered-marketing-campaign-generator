"""
Test script for BriefParserService.
"""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

# Add code directory to sys.path
sys.path.append(str(Path(__file__).parent))

# Load env vars
load_dotenv()

from api.services.brief_parser import get_brief_parser


async def test_parser():
    print("Initializing Brief Parser...")
    parser = get_brief_parser()

    # Create test project structure
    from api.services.file_operations import get_file_service
    files = get_file_service()
    files.create_project_structure("test-project-parser", "Test Project")

    brief_content = """
    # Campaign Brief: Nestlé Coffee
    
    **Client:** Nestlé
    **Product:** Nescafé
    
    **Challenge:** Increase consumption of Nescafé among young adults (18-25) in Paraguay who perceive instant coffee as "old fashioned".
    
    **Target Audience:**
    - Young adults 18-25
    - Students and young professionals
    - Urban areas (Asunción, Ciudad del Este)
    - Tech-savvy, value convenience but want quality
    
    **Requirements:**
    - Must use the red mug asset.
    - Tone should be energetic and modern.
    - No mention of competitors.
    """

    print("Parsing brief...")
    try:
        # We use a fake project ID for testing
        result = await parser.parse_brief("test-project-parser", brief_content)

        print("\n--- Parse Result ---")
        print(f"Challenge: {result.challenge.main_challenge}")
        print(f"Target: {result.target.primary}")
        print(f"Directions: {len(result.directions)} generated")
        print(f"Mandatories: {result.requirements.mandatories}")
        print("\nSUCCESS: Brief parsed successfully with Instructor!")

    except Exception as e:
        print(f"\nERROR: {e}")

if __name__ == "__main__":
    asyncio.run(test_parser())
