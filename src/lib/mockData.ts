import { User, Project, WorkItem, Sprint, Team } from '../types';

export const mockUser: User = {
    id: 'u1',
    email: 'admin@tickora.ai',
    name: 'Alex Rivera',
    role: 'Admin',
    avatar: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Alex'
};

export const mockTeam: Team = {
    id: 't1',
    name: 'Engineering Alpha',
    members: [mockUser]
};

export const mockProjects: Project[] = [
    {
        id: 'p1',
        name: 'Tickora MVP-1',
        type: 'Scrum',
        teamId: 't1'
    }
];

export const mockSprints: Sprint[] = [
    {
        id: 's1',
        projectId: 'p1',
        name: 'Sprint 1: Foundation',
        startDate: '2026-01-01',
        endDate: '2026-01-14',
        status: 'Active'
    }
];

export const mockWorkItems: WorkItem[] = [
    {
        id: 'w1',
        projectId: 'p1',
        sprintId: 's1',
        type: 'User Story',
        title: 'Implement Auth Flow',
        description: 'User signup with email/SSO and verification',
        status: 'Done',
        priority: 'High',
        ownerId: 'u1',
        blockerIds: [],
        createdAt: '2026-01-01T10:00:00Z',
        updatedAt: '2026-01-05T15:00:00Z'
    },
    {
        id: 'w2',
        projectId: 'p1',
        sprintId: 's1',
        type: 'User Story',
        title: 'AI Standup Integration',
        description: 'Automated standup pings and response recording',
        status: 'In Progress',
        priority: 'Critical',
        ownerId: 'u1',
        blockerIds: [],
        createdAt: '2026-01-02T11:00:00Z',
        updatedAt: '2026-01-10T09:00:00Z'
    },
    {
        id: 'w3',
        projectId: 'p1',
        sprintId: 's1',
        type: 'Bug',
        title: 'Fix LLM API Timeout',
        description: 'LLM calls are timing out after 30s',
        status: 'To Do',
        priority: 'Medium',
        ownerId: 'u1',
        blockerIds: [],
        createdAt: '2026-01-09T14:00:00Z',
        updatedAt: '2026-01-09T14:00:00Z'
    }
];
