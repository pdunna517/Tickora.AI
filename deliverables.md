# Tickora MVP-1 Deliverables

## 1. System Architecture
Tickora is built on a modern full-stack architecture:
- **Frontend**: React 18 with TypeScript and Vite for lightning-fast development.
- **Styling**: Custom CSS with a focus on glassmorphism, dark mode, and premium aesthetics.
- **State Management**: React Hooks and Context for seamless data flow.
- **Animations**: Framer Motion for smooth, interactive transitions.
- **AI Integration**: Modular design supporting OpenAI, Azure OpenAI, and custom cloud LLMs.

## 2. Core Data Models
Defined in `src/types/index.ts`:
- `User`: Roles (Admin, Scrum Master, Team Member, Viewer).
- `Project`: Types (Scrum, Kanban).
- `WorkItem`: Types (Epic, Story, Bug, Task, Sub-task) with status and blocker tracking.
- `Standup`: Automated scheduling and response mapping.

## 3. API Structure (Proposed)
- `POST /api/auth/signup`: User registration and SSO.
- `POST /api/llm/config`: Secure LLM integration.
- `POST /api/standups/process`: AI-powered response extraction.
- `GET /api/standups/summary`: Real-time team progress insights.

## 4. AI Prompt Flows
### Standup Extraction Prompt
```text
System: You are a Scrum Master Assistant.
User: [Raw Standup Response]
Task: Extract "Yesterday", "Today", and "Blockers". 
Output: JSON format with mapped task IDs.
```

### Summary Generation Prompt
```text
System: You are an AI Project Manager.
Input: [All Team Responses]
Task: Summarize progress, highlight critical blockers, and suggest ad-hoc meetings.
```

## 5. UI Screen List
- **Landing Page**: Premium product overview.
- **Dashboard**: High-level project and sprint metrics.
- **AI Standup**: Interactive chat interface for daily check-ins.
- **Settings**: LLM configuration and integration management.
- **Project Board**: (Coming Soon) Scrum/Kanban visualizer.

## 6. Example Standup Execution
1. **Ping**: System sends notification to user.
2. **Response**: User provides free-form text in the AI Standup view.
3. **Processing**: AI extracts updates and identifies blockers (e.g., "Database Migration").
4. **Action**: System flags the blocker on the dashboard and notifies the Scrum Master.

---
**Tickora MVP-1** is now ready for review and further development.
