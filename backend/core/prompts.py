STORY_PROMPT = """
You are a creative story writer. Generate a SHORT choose-your-own-adventure story.

STRUCTURE (EXACTLY 7 NODES):
- 1 root node → 2 options
- 2 middle nodes → 2 options each  
- 4 ending nodes

REQUIREMENTS:
- Keep each content to 1-2 sentences ONLY
- Make 1-2 endings winning (isWinningEnding: true)
- Make choices meaningful

OUTPUT ONLY VALID JSON - NO OTHER TEXT:
{format_instructions}

EXAMPLE (follow this EXACT structure):
{{
    "title": "The Dark Cave",
    "rootNode": {{
        "content": "You find a cave entrance. Two tunnels branch ahead.",
        "isEnding": false,
        "isWinningEnding": false,
        "options": [
            {{
                "text": "Enter left tunnel",
                "nextNode": {{
                    "content": "You find a treasure chest and a trap door.",
                    "isEnding": false,
                    "isWinningEnding": false,
                    "options": [
                        {{
                            "text": "Open chest",
                            "nextNode": {{
                                "content": "Gold! You win!",
                                "isEnding": true,
                                "isWinningEnding": true,
                                "options": []
                            }}
                        }},
                        {{
                            "text": "Check trap door",
                            "nextNode": {{
                                "content": "You fall into a pit. Game over.",
                                "isEnding": true,
                                "isWinningEnding": false,
                                "options": []
                            }}
                        }}
                    ]
                }}
            }},
            {{
                "text": "Enter right tunnel",
                "nextNode": {{
                    "content": "A sleeping bear blocks the path.",
                    "isEnding": false,
                    "isWinningEnding": false,
                    "options": [
                        {{
                            "text": "Sneak past",
                            "nextNode": {{
                                "content": "Success! You escape with berries. You win!",
                                "isEnding": true,
                                "isWinningEnding": true,
                                "options": []
                            }}
                        }},
                        {{
                            "text": "Wake bear",
                            "nextNode": {{
                                "content": "Bear chases you out. Game over.",
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

CRITICAL: Output ONLY the JSON, nothing else. Keep content brief.
"""