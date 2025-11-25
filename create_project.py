#!/usr/bin/env python3
"""
Quick script to create Ueno Bank project via API
"""
import requests
import json

# API configuration
API_URL = "http://localhost:8000"
API_KEY = "test-key"

# Create project
response = requests.post(
    f"{API_URL}/projects",
    headers={
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    },
    json={
        "name": "Ueno Bank Paraguay 2025",
        "client": "Ueno Bank",
        "country": "Paraguay",
        "language": "es",
        "campaign_type": "digital"
    }
)

print("Status Code:", response.status_code)
print("Response:")
print(json.dumps(response.json(), indent=2))

if response.status_code == 201:
    project = response.json()
    project_id = project["id"]
    print(f"\n✓ Project created successfully!")
    print(f"Project ID: {project_id}")

    # Now upload the brief
    with open("briefs-originales/UENO_BANK_BRIEF.md", "r", encoding="utf-8") as f:
        brief_content = f.read()

    print(f"\n📄 Uploading brief ({len(brief_content)} chars)...")

    brief_response = requests.post(
        f"{API_URL}/projects/{project_id}/brief",
        headers={
            "Content-Type": "application/json",
            "X-API-Key": API_KEY
        },
        json={
            "content": brief_content
        }
    )

    print("Brief Upload Status:", brief_response.status_code)
    if brief_response.status_code == 200:
        print("✓ Brief uploaded successfully!")
        print("\nBrief Analysis:")
        print(json.dumps(brief_response.json(), indent=2, ensure_ascii=False))
    else:
        print("Brief Upload Response:")
        print(brief_response.text)
else:
    print("Error creating project")
