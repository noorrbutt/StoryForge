
from sqlalchemy.orm import Session
from backend.models.story import Story, StoryNode
from dotenv import load_dotenv
import os
import json

load_dotenv()

class StoryGenerator:

    @classmethod
    def _get_groq_client(cls):
        """Get Groq client (FREE alternative to OpenAI)"""
        try:
            from groq import Groq
        except ImportError:
            raise Exception("Install groq: pip install groq")
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise Exception("Missing GROQ_API_KEY in .env file. Get one free at https://console.groq.com")
        
        return Groq(api_key=api_key)

    @classmethod
    def generate_story(cls, db: Session, session_id: str, theme: str = "fantasy") -> Story:
        """Generate a deeper story with multiple choice levels"""
        
        client = cls._get_groq_client()
        
        # Balanced prompt - one winning path, one losing path
        prompt = f"""Create a {theme} choose-your-own-adventure story with ONE winning path and ONE losing path.

Structure (7 nodes total):
- Root → 2 choices (Choice A and Choice B)
- Choice A → 2 sub-choices → 2 endings (both BAD)
- Choice B → 2 sub-choices → 2 endings (one GOOD, one BAD)

Result: 3 bad endings, 1 good ending (balanced challenge)

Output ONLY valid JSON:

{{
    "title": "Story Title",
    "rootNode": {{
        "content": "Opening situation with a critical decision.",
        "isEnding": false,
        "isWinningEnding": false,
        "options": [
            {{
                "text": "Wrong approach (seems tempting)",
                "nextNode": {{
                    "content": "This path leads to trouble.",
                    "isEnding": false,
                    "isWinningEnding": false,
                    "options": [
                        {{
                            "text": "First bad option",
                            "nextNode": {{
                                "content": "FAILURE - explain how this failed.",
                                "isEnding": true,
                                "isWinningEnding": false,
                                "options": []
                            }}
                        }},
                        {{
                            "text": "Second bad option",
                            "nextNode": {{
                                "content": "FAILURE - different failure outcome.",
                                "isEnding": true,
                                "isWinningEnding": false,
                                "options": []
                            }}
                        }}
                    ]
                }}
            }},
            {{
                "text": "Right approach (smarter choice)",
                "nextNode": {{
                    "content": "Better path, but still requires careful choice.",
                    "isEnding": false,
                    "isWinningEnding": false,
                    "options": [
                        {{
                            "text": "The winning move",
                            "nextNode": {{
                                "content": "SUCCESS! You won by being smart and careful.",
                                "isEnding": true,
                                "isWinningEnding": true,
                                "options": []
                            }}
                        }},
                        {{
                            "text": "Almost there but...",
                            "nextNode": {{
                                "content": "FAILURE - you were close but made a final mistake.",
                                "isEnding": true,
                                "isWinningEnding": false,
                                "options": []
                            }}
                        }}
                    ]
                }}
            }}
        ]
    }}
}}

Rules:
- Make choices logical (not random)
- The winning path should make sense in hindsight
- Don't make it too obvious which is the "right" first choice
- 3 failures, 1 success = balanced difficulty
- Keep it engaging and suspenseful"""

        try:
            print("[StoryGen] Calling Groq API for deeper story...", flush=True)
            
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a creative story writer. Output only valid JSON with the exact structure requested."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,  # Higher creativity
                max_tokens=2000,  # More tokens for deeper story
                timeout=45
            )
            
            response_text = response.choices[0].message.content
            print(f"[StoryGen] Got response: {len(response_text)} chars", flush=True)
            
            # Extract JSON
            response_text = cls._extract_json(response_text)
            
            # Parse
            story_data = json.loads(response_text)
            
            if "title" not in story_data or "rootNode" not in story_data:
                raise Exception("Invalid structure")
            
            print(f"[StoryGen] Title: {story_data['title']}", flush=True)
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Invalid JSON: {e}", flush=True)
            print(f"Response: {response_text[:500]}", flush=True)
            raise Exception(f"Model returned invalid JSON: {str(e)}")
        except Exception as e:
            print(f"[ERROR] Generation failed: {e}", flush=True)
            raise Exception(f"Failed to generate story: {str(e)}")

        # Save to database
        story_db = Story(title=story_data["title"], session_id=session_id)
        db.add(story_db)
        db.flush()

        try:
            # Process the full tree recursively
            node_count = {"count": 0}
            root_node = cls._process_node(
                db, 
                story_db.id, 
                story_data["rootNode"], 
                is_root=True,
                node_count=node_count
            )
            
            db.commit()
            print(f"[StoryGen] Success! Created {node_count['count']}-node story", flush=True)
            
        except Exception as e:
            print(f"[ERROR] DB save failed: {e}", flush=True)
            db.rollback()
            raise Exception(f"Failed to save story: {str(e)}")

        return story_db

    @classmethod
    def _process_node(cls, db: Session, story_id: int, node_data: dict, is_root: bool = False, node_count: dict = None) -> StoryNode:
        """Recursively process story nodes"""
        if node_count is None:
            node_count = {"count": 0}
        
        node_count["count"] += 1
        
        # Safety check
        if node_count["count"] > 15:
            print(f"[WARNING] Hit node limit", flush=True)
            node_data["isEnding"] = True
            node_data["options"] = []
        
        # Create node
        node = StoryNode(
            story_id=story_id,
            content=node_data.get("content", ""),
            is_root=is_root,
            is_ending=node_data.get("isEnding", False),
            is_winning_ending=node_data.get("isWinningEnding", False),
            options=[]
        )
        db.add(node)
        db.flush()
        
        # Process children recursively
        if not node.is_ending and "options" in node_data and node_data["options"]:
            options_list = []
            
            for option in node_data["options"]:
                next_node_data = option.get("nextNode", {})
                
                # Recursively process child
                child_node = cls._process_node(
                    db, 
                    story_id, 
                    next_node_data, 
                    is_root=False,
                    node_count=node_count
                )
                
                options_list.append({
                    "text": option.get("text", "Continue"),
                    "node_id": child_node.id
                })
            
            node.options = options_list
            db.flush()
        
        return node

    @classmethod
    def _extract_json(cls, text: str) -> str:
        """Extract JSON from response"""
        text = text.strip()
        
        # Remove markdown
        if "```" in text:
            text = text.replace("```json", "").replace("```", "").strip()
        
        # Find JSON
        if not text.startswith('{'):
            start = text.find('{')
            if start != -1:
                text = text[start:]
        
        # Find closing brace
        brace_count = 0
        for i, char in enumerate(text):
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[:i+1]
        
        return text