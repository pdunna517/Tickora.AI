import React from 'react';
import {
    LayoutDashboard,
    Trello,
    ListTodo,
    Users,
    Settings,
    MessageSquare,
    Zap,
    ChevronLeft,
    LogOut,
    Briefcase
} from 'lucide-react';

interface SidebarProps {
    activeTab: string;
    setActiveTab: (tab: string) => void;
}

export function Sidebar({ activeTab, setActiveTab }: SidebarProps) {
    const menuItems = [
        { id: 'dashboard', icon: <LayoutDashboard className="w-5 h-5" />, label: 'Dashboard' },
        { id: 'board', icon: <Trello className="w-5 h-5" />, label: 'Board' },
        { id: 'backlog', icon: <ListTodo className="w-5 h-5" />, label: 'Backlog' },
        { id: 'team', icon: <Users className="w-5 h-5" />, label: 'Team' },
        { id: 'standups', icon: <MessageSquare className="w-5 h-5" />, label: 'Standups' },
        { id: 'settings', icon: <Settings className="w-5 h-5" />, label: 'Project Settings' },
    ];

    return (
        <aside className="w-64 border-r border-border-primary flex flex-col bg-bg-secondary h-screen sticky top-0">
            {/* Project Header */}
            <div className="p-4 flex items-center gap-3 border-b border-border-primary">
                <div className="w-10 h-10 rounded-md bg-white border border-border-primary flex items-center justify-center p-1">
                    <img src="/logo.png" alt="Tickora Logo" className="w-full h-full object-contain" />
                </div>
                <div>
                    <h2 className="text-sm font-bold text-text-primary">Tickora MVP</h2>
                    <p className="text-xs text-text-secondary">Software Project</p>
                </div>
            </div>

            {/* Navigation */}
            <nav className="flex-grow px-2 py-4 space-y-1">
                {menuItems.map((item) => (
                    <button
                        key={item.id}
                        onClick={() => setActiveTab(item.id)}
                        className={`sidebar-link ${activeTab === item.id ? 'active' : ''}`}
                    >
                        {item.icon}
                        <span>{item.label}</span>
                    </button>
                ))}
            </nav>

            {/* Footer */}
            <div className="p-4 border-t border-border-primary">
                <div className="flex items-center gap-3 mb-3">
                    <div className="w-8 h-8 rounded-full bg-accent-primary text-white flex items-center justify-center text-xs font-bold">
                        AR
                    </div>
                    <div>
                        <div className="text-sm font-medium text-text-primary">Alex Rivera</div>
                        <div className="text-xs text-text-secondary">Scrum Master</div>
                    </div>
                </div>
                <button className="text-xs text-text-secondary hover:text-text-primary flex items-center gap-2">
                    <LogOut className="w-3 h-3" /> Log out
                </button>
            </div>
        </aside>
    );
}
