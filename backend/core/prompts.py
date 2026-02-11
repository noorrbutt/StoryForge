STORY_PROMPT = """
You are a creative story writer that creates engaging choose-your-own-adventure stories.
Generate a SHORT branching story with multiple paths and endings in the JSON format I'll specify.

The story should have:
1. A compelling title
2. A starting situation (root node) with EXACTLY 2 options
3. Each option leads to a middle node with EXACTLY 2 more options
4. All 4 final options lead directly to endings
5. At least one ending should be a winning ending

Story structure requirements:
- Root node → 2 options → 2 middle nodes → 4 ending nodes (3 levels deep, 7 total nodes)
- Make at least 1-2 endings winning (isWinningEnding: true)
- Keep each piece of content to 2-3 sentences maximum
- Make the choices meaningful and impactful

Output your story in this exact JSON structure:
{format_instructions}

Don't add any text outside of the JSON structure.
Example structure (you should follow this pattern exactly):
{{
    "title": "The Enchanted Forest",
    "rootNode": {{
        "content": "You stand at the edge of a dark forest. A worn path splits in two directions.",
        "isEnding": false,
        "isWinningEnding": false,
        "options": [
            {{
                "text": "Take the left path toward the glowing lights",
                "nextNode": {{
                    "content": "You reach a fairy circle. The fairies offer you a choice.",
                    "isEnding": false,
                    "isWinningEnding": false,
                    "options": [
                        {{
                            "text": "Accept their magical gift",
                            "nextNode": {{
                                "content": "The fairies grant you safe passage and treasure! You win!",
                                "isEnding": true,
                                "isWinningEnding": true,
                                "options": []
                            }}
                        }},
                        {{
                            "text": "Politely decline and leave",
                            "nextNode": {{
                                "content": "The fairies respect your choice and let you leave peacefully. You survive but find no treasure.",
                                "isEnding": true,
                                "isWinningEnding": false,
                                "options": []
                            }}
                        }}
                    ]
                }}
            }},
            {{
                "text": "Take the right path into the shadows",
                "nextNode": {{
                    "content": "You encounter a sleeping dragon blocking the path. What do you do?",
                    "isEnding": false,
                    "isWinningEnding": false,
                    "options": [
                        {{
                            "text": "Sneak past quietly",
                            "nextNode": {{
                                "content": "You successfully sneak past and find the dragon's hoard! You win!",
                                "isEnding": true,
                                "isWinningEnding": true,
                                "options": []
                            }}
                        }},
                        {{
                            "text": "Try to wake and negotiate",
                            "nextNode": {{
                                "content": "The dragon wakes up angry and chases you away. Game over.",
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
"""

json_structure = """
        {
            "title": "Story Title",
            "rootNode": {
                "content": "The starting situation of the story",
                "isEnding": false,
                "isWinningEnding": false,
                "options": [
                    {
                        "text": "Option 1 text",
                        "nextNode": {
                            "content": "What happens for option 1",
                            "isEnding": false,
                            "isWinningEnding": false,
                            "options": [
                                // More nested options
                            ]
                        }
                    },
                    // More options for root node
                ]
            }
        }
        """