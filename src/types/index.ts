export type UserRole = 'Admin' | 'Scrum Master' | 'Team Member' | 'Viewer';

export interface User {
    id: string;
    email: string;
    name: string;
    role: UserRole;
    avatar?: string;
    teamId?: string;
}

export type ProjectType = 'Scrum' | 'Kanban';

export interface Team {
    id: string;
    name: string;
    members: User[];
}

export interface Project {
    id: string;
    name: string;
    type: ProjectType;
    teamId: string;
}

export type WorkItemType = 'Epic' | 'Initiative' | 'User Story' | 'Bug' | 'Task' | 'Sub-task';
export type WorkItemStatus = 'To Do' | 'In Progress' | 'In Review' | 'Done' | 'Blocked';
export type WorkItemPriority = 'Low' | 'Medium' | 'High' | 'Critical';

export interface WorkItem {
    id: string;
    projectId: string;
    sprintId?: string;
    type: WorkItemType;
    title: string;
    description: string;
    status: WorkItemStatus;
    priority: WorkItemPriority;
    ownerId?: string;
    parentId?: string;
    blockerIds: string[];
    createdAt: string;
    updatedAt: string;
}

export interface Sprint {
    id: string;
    projectId: string;
    name: string;
    startDate: string;
    endDate: string;
    status: 'Planned' | 'Active' | 'Completed';
}

export interface LLMConfig {
    provider: 'OpenAI' | 'Azure OpenAI' | 'Copilot' | 'Cloud LLM';
    apiKey: string;
    model: string;
    tokenLimit: number;
    privacyControls: {
        dataRetention: boolean;
        piiRedaction: boolean;
    };
}

export interface StandupConfig {
    id: string;
    teamId: string;
    time: string; // HH:mm
    channel: 'Slack' | 'Teams' | 'Email';
    questions: string[];
}

export interface StandupResponse {
    id: string;
    userId: string;
    standupId: string;
    date: string;
    yesterday: string;
    today: string;
    blockers: string;
    rawResponse: string;
    processed: boolean;
}

export interface StandupSummary {
    id: string;
    standupId: string;
    date: string;
    yesterdaySummary: string;
    todaySummary: string;
    blockersSummary: string;
    aiInsights: string;
}
