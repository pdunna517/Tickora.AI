import React, { useState } from 'react';
import {
    MoreHorizontal,
    Plus,
    MessageSquare,
    Paperclip,
    Flag,
    Calendar,
    UserCircle
} from 'lucide-react';
import { mockWorkItems, mockUser } from '../lib/mockData';
import { WorkItem, WorkItemStatus } from '../types';

export function BoardView() {
    const [items, setItems] = useState<WorkItem[]>(mockWorkItems);

    const columns: { id: WorkItemStatus; label: string }[] = [
        { id: 'To Do', label: 'To Do' },
        { id: 'In Progress', label: 'In Progress' },
        { id: 'Done', label: 'Done' }
    ];

    return (
        <div className="p-6 h-full flex flex-col">
            {/* Board Header */}
            <div className="flex justify-between items-center mb-6">
                <div>
                    <div className="flex items-center gap-2 text-sm text-text-secondary mb-1">
                        <span>Projects</span>
                        <span>/</span>
                        <span>Tickora MVP</span>
                        <span>/</span>
                        <span>Board</span>
                    </div>
                    <h1 className="text-2xl font-bold text-text-primary">Sprint 1 Board</h1>
                </div>
                <div className="flex items-center gap-3">
                    <div className="flex -space-x-2">
                        <div className="w-8 h-8 rounded-full bg-accent-primary text-white flex items-center justify-center border-2 border-white text-xs font-bold">AR</div>
                        <div className="w-8 h-8 rounded-full bg-gray-200 text-text-secondary flex items-center justify-center border-2 border-white text-xs font-bold">+2</div>
                    </div>
                    <button className="btn btn-secondary">Group By</button>
                    <button className="btn btn-secondary">Insights</button>
                </div>
            </div>

            {/* Kanban Board */}
            <div className="flex-grow flex gap-6 overflow-x-auto pb-4">
                {columns.map((col) => (
                    <div key={col.id} className="min-w-[280px] w-80 bg-bg-secondary rounded-md flex flex-col max-h-full">
                        <div className="p-3 font-semibold text-xs text-text-secondary uppercase tracking-wider flex justify-between items-center sticky top-0 bg-bg-secondary z-10 rounded-t-md">
                            <span>{col.label}</span>
                            <span className="bg-gray-200 px-2 py-0.5 rounded-full text-[10px] text-text-primary">
                                {items.filter(i => i.status === col.id).length}
                            </span>
                        </div>

                        <div className="p-2 space-y-2 overflow-y-auto flex-grow">
                            {items.filter(i => i.status === col.id).map((item) => (
                                <BoardCard key={item.id} item={item} />
                            ))}
                            <button className="w-full py-2 text-left px-2 text-sm text-text-secondary hover:bg-gray-200 rounded transition-colors flex items-center gap-2">
                                <Plus className="w-4 h-4" /> Create issue
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}

function BoardCard({ item }: { item: WorkItem }) {
    const priorityColor = {
        'Low': 'bg-blue-100 text-blue-700',
        'Medium': 'bg-yellow-100 text-yellow-700',
        'High': 'bg-orange-100 text-orange-700',
        'Critical': 'bg-red-100 text-red-700'
    }[item.priority];

    return (
        <div className="bg-white p-3 rounded shadow-sm border border-border-primary hover:bg-gray-50 cursor-pointer group transition-all">
            <div className="flex justify-between items-start mb-2">
                <span className="text-xs font-medium text-text-secondary hover:underline">TICK-{item.id.replace('w', '')}</span>
                <button className="opacity-0 group-hover:opacity-100 text-text-secondary hover:bg-gray-100 p-1 rounded">
                    <MoreHorizontal className="w-4 h-4" />
                </button>
            </div>

            <p className="text-sm text-text-primary font-medium mb-3 leading-snug">
                {item.title}
            </p>

            <div className="flex items-center justify-between mt-2">
                <div className="flex items-center gap-2">
                    <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold uppercase ${priorityColor}`}>
                        {item.priority}
                    </span>
                    {item.type === 'Bug' && <Flag className="w-3 h-3 text-red-500" />}
                </div>

                <div className="flex items-center gap-2">
                    {item.blockerIds.length > 0 && (
                        <div className="flex items-center gap-1 text-red-600" title="Blocked">
                            <Flag className="w-3 h-3 fill-current" />
                        </div>
                    )}
                    <div className="w-6 h-6 rounded-full bg-accent-primary text-white flex items-center justify-center text-[10px] font-bold">
                        AR
                    </div>
                </div>
            </div>
        </div>
    );
}
