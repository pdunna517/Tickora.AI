from fastapi import APIRouter

from app.routes import auth, users, projects, sprints, tickets, standups, settings, ai, reports, uploads, project_team, ai_agent

api_router = APIRouter()

@api_router.get("/health", tags=["status"])
def health_check():
    return {"status": "ok"}

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(project_team.router, prefix="/projects/{project_id}/team", tags=["project-team"])
api_router.include_router(sprints.router, prefix="/sprints", tags=["sprints"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(standups.router, prefix="/standups", tags=["standups"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai-legacy"])
api_router.include_router(ai_agent.router, prefix="/ai", tags=["ai-agent"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
api_router.include_router(uploads.router, prefix="/uploads", tags=["uploads"])
