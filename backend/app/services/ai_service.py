class AIService:
    def generate_epics(self, project_context: str):
        return [
            {"title": "Epic 1: Core Foundation", "description": "Setup basic infrastructure"},
            {"title": "Epic 2: User Management", "description": "Auth and profiles"}
        ]
    
    def ticket_assist(self, ticket_content: str):
        return {
            "improved_description": f"Refined: {ticket_content}",
            "suggested_points": 3,
            "tasks": ["Task A", "Task B"]
        }

    
    def generate_summary(self, prompt: str):
        # In a real implementation, this would call an LLM API
        # For now, we simulate a structured response
        return {
            "summary_text": f"AI Summary based on responses:\n{prompt[:100]}...",
            "blockers_json": [
                {"user": "System", "issue": "Example blocker if applicable"}
            ]
        }

ai_service = AIService()
