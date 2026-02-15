# api/index.py - Vercel Serverless Entry Point
import sys
import os

# Get the directory containing this file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the parent directory (project root)
parent_dir = os.path.dirname(current_dir)

# Add parent directory to Python path so we can import backend
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

print(f"[DEBUG] Current dir: {current_dir}")
print(f"[DEBUG] Parent dir: {parent_dir}")
print(f"[DEBUG] sys.path: {sys.path}")

try:
    # Now import the FastAPI app from backend
    from backend.main import app
    print("[SUCCESS] Imported backend.main.app successfully!")
except ImportError as e:
    print(f"[ERROR] Failed to import backend.main: {e}")
    import traceback
    traceback.print_exc()
    
    # Try alternative import
    try:
        print("[DEBUG] Trying alternative import...")
        import backend.main as backend_main
        app = backend_main.app
        print("[SUCCESS] Alternative import worked!")
    except Exception as e2:
        print(f"[ERROR] Alternative import also failed: {e2}")
        raise

# Vercel will use this app