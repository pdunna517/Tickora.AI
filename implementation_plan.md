# Tickora MVP-1 Implementation Plan

## 1. Project Overview
Tickora is an AI-first project management application designed to automate scrum ceremonies and provide intelligent insights into team productivity.

## 2. System Architecture
- **Frontend**: React + TypeScript + Vite
- **Styling**: Vanilla CSS (Premium Aesthetics)
- **State Management**: React Context / Hooks
- **AI Integration**: Direct LLM API calls (OpenAI/Azure)
- **Mock Backend**: For MVP-1, we will use a robust mock service to demonstrate functionality.

## 3. Data Models
### User & Auth
- `UserRole`: Admin | ScrumMaster | TeamMember | Viewer
- `User`: id, email, name, role, avatar

### Project Management
- `ProjectType`: Scrum | Kanban
- `Project`: id, name, type, teamId
- `WorkItemType`: Epic | Initiative | UserStory | Bug | Task | SubTask
- `WorkItem`: id, title, description, type, status, priority, ownerId, projectId, sprintId, blockers[]

### AI & Standups
- `LLMConfig`: provider, apiKey, model, tokenLimit
- `StandupConfig`: time, channel, questions[]
- `StandupResponse`: userId, date, yesterday, today, blockers, rawText

## 4. UI/UX Design
- **Theme**: Dark mode, glassmorphism, vibrant accents (Indigo/Violet).
- **Typography**: Inter / Outfit.
- **Animations**: Framer Motion for smooth transitions.

## 5. Implementation Steps
### Phase 1: Foundation (Step 1-3)
- [ ] Setup project structure and design system.
- [ ] Implement Auth flows (Mock).
- [ ] Team & Project creation UI.
- [ ] LLM Configuration screen.

### Phase 2: Core Work Management (Step 4)
- [ ] Backlog and Board views.
- [ ] Work item creation and editing.
- [ ] Sprint management.

### Phase 3: AI Standups (Step 5-8)
- [ ] Standup scheduling UI.
- [ ] Automated ping simulation.
- [ ] AI processing of responses (Mock/Real).
- [ ] Summary generation and notification.

## 6. Deliverables
- [x] MVP-1 system architecture
- [x] Core data models
- [ ] API structure (in code)
- [ ] AI prompt flows (in code)
- [ ] UI screen list
- [ ] Example standup execution
