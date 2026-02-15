"""
Test the story creation API endpoint
Run while server is running
"""

import requests
import time
import json

BASE_URL = "http://127.0.0.1:8000/api"

print("=" * 60)
print("TESTING STORY CREATION API")
print("=" * 60)

# Test 1: Health check
print("\n1. Testing health endpoint...")
try:
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"   ✓ Health check: {response.json()}")
except Exception as e:
    print(f"   ✗ Health check failed: {e}")
    print("   Make sure server is running: uvicorn main:app --reload --port 8000")
    exit(1)

# Test 2: Create story
print("\n2. Creating a story...")
try:
    response = requests.post(
        f"{BASE_URL}/stories/create",
        json={"theme": "fantasy"},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        job = response.json()
        print(f"   ✓ Story job created!")
        print(f"   Job ID: {job['job_id']}")
        print(f"   Status: {job['status']}")
        
        # Test 3: Poll for completion
        print("\n3. Waiting for story generation...")
        job_id = job['job_id']
        max_attempts = 30
        
        for attempt in range(max_attempts):
            time.sleep(1)
            status_response = requests.get(f"{BASE_URL}/stories/jobs/{job_id}")
            status_data = status_response.json()
            
            print(f"   Attempt {attempt + 1}: {status_data['status']}", end="\r")
            
            if status_data['status'] == 'completed':
                print(f"\n   ✓ Story completed!")
                print(f"   Story ID: {status_data['story_id']}")
                
                # Test 4: Get the story
                print("\n4. Fetching complete story...")
                story_response = requests.get(f"{BASE_URL}/stories/{status_data['story_id']}/complete")
                story = story_response.json()
                
                print(f"\n   Title: {story['title']}")
                print(f"   Root node: {story['root_node']['content'][:100]}...")
                print(f"   Options: {len(story['root_node']['options'])}")
                
                print("\n" + "=" * 60)
                print("✓✓ SUCCESS! Story generation works!")
                print("=" * 60)
                break
                
            elif status_data['status'] == 'failed':
                print(f"\n   ✗ Story generation failed!")
                print(f"   Error: {status_data.get('error', 'Unknown error')}")
                break
        else:
            print(f"\n   ⚠ Story generation timed out after {max_attempts} seconds")
            
    else:
        print(f"   ✗ Failed to create story")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   ✗ Error: {e}")
    import traceback
    traceback.print_exc()