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

ai_service = AIService()
