import React from 'react';
import {
    AlertTriangle,
    Users,
    TrendingUp,
    Activity,
    AlertCircle,
    Bot,
    Clock,
    ChevronRight
} from 'lucide-react';
import { motion } from 'framer-motion';

export function Dashboard() {
    return (
        <div className="p-8 max-w-7xl mx-auto space-y-8">
            {/* Sprint Header */}
            <div className="flex justify-between items-start">
                <div>
                    <h1 className="text-3xl font-bold mb-2">Sprint 14: AI Integration</h1>
                    <div className="flex items-center gap-3 text-sm">
                        <span className="text-text-secondary font-medium">3 DAYS REMAINING</span>
                        <span className="w-1.5 h-1.5 rounded-full bg-text-secondary" />
                        <span className="text-accent-primary font-bold uppercase tracking-wider">ACTIVE</span>
                    </div>
                </div>
                <div className="flex -space-x-3">
                    <div className="w-10 h-10 rounded-full bg-white text-bg-primary flex items-center justify-center font-bold border-2 border-bg-primary z-30">JD</div>
                    <div className="w-10 h-10 rounded-full bg-accent-primary text-white flex items-center justify-center font-bold border-2 border-bg-primary z-20">SK</div>
                    <div className="w-10 h-10 rounded-full bg-bg-tertiary text-text-secondary flex items-center justify-center font-bold border-2 border-bg-primary z-10">+2</div>
                </div>
            </div>

            {/* AI Insights Section */}
            <div className="space-y-4">
                <div className="flex justify-between items-center">
                    <div className="flex items-center gap-2 text-warning font-bold uppercase tracking-wider text-xs">
                        <Bot className="w-4 h-4" /> AI Insights
                    </div>
                    <button className="text-accent-primary text-sm font-bold hover:underline">View All</button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    {/* Risk Card */}
                    <div className="col-span-2 card bg-bg-secondary border-warning/20 relative overflow-hidden group">
                        <div className="absolute top-0 left-0 w-1 h-full bg-warning" />
                        <div className="flex gap-6">
                            <div className="w-16 h-16 rounded-2xl bg-warning flex items-center justify-center flex-shrink-0">
                                <AlertTriangle className="w-8 h-8 text-white" />
                            </div>
                            <div className="space-y-3">
                                <div>
                                    <h3 className="text-lg font-bold text-white">Sprint at risk</h3>
                                    <p className="text-text-secondary text-sm">3 blockers identified</p>
                                </div>
                                <p className="text-text-secondary leading-relaxed max-w-lg">
                                    Velocity dropped by 14% due to API downtime. AI suggests reassigning Task <span className="text-white font-mono">#402</span>.
                                </p>
                            </div>
                        </div>
                    </div>

                    {/* Team Load Card */}
                    <div className="card bg-bg-secondary border-accent-primary/20 relative overflow-hidden">
                        <div className="absolute top-0 left-0 w-1 h-full bg-accent-primary" />
                        <div className="flex flex-col h-full justify-between">
                            <div className="flex items-start justify-between mb-4">
                                <div className="w-12 h-12 rounded-xl bg-accent-primary flex items-center justify-center">
                                    <Users className="w-6 h-6 text-white" />
                                </div>
                            </div>
                            <div>
                                <p className="text-text-secondary leading-relaxed mb-2">
                                    Sarah has 4 active tasks. Consider delegating Review <span className="text-white font-mono">#405</span>.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Progress & Stats */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Progress Circle */}
                <div className="col-span-2 card bg-bg-secondary flex items-center justify-between p-8">
                    <div>
                        <div className="text-xs font-bold text-text-secondary uppercase tracking-wider mb-2">Current Progress</div>
                        <div className="flex items-baseline gap-3 mb-4">
                            <span className="text-5xl font-bold text-white">65%</span>
                            <span className="text-xl text-text-secondary">Done</span>
                        </div>
                        <div className="flex items-center gap-2 text-success font-bold text-sm">
                            <TrendingUp className="w-4 h-4" />
                            <span>+12% vs last week</span>
                        </div>
                    </div>
                    <div className="relative w-32 h-32 flex items-center justify-center">
                        <svg className="w-full h-full -rotate-90">
                            <circle cx="64" cy="64" r="56" stroke="var(--bg-tertiary)" strokeWidth="12" fill="none" />
                            <circle cx="64" cy="64" r="56" stroke="var(--accent-primary)" strokeWidth="12" fill="none" strokeDasharray="351.86" strokeDashoffset="123.15" strokeLinecap="round" />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center">
                            <Activity className="w-8 h-8 text-accent-primary" />
                        </div>
                    </div>
                </div>
            </div>

            {/* Active Blockers */}
            <div className="space-y-4">
                <div className="flex justify-between items-center">
                    <h2 className="text-xl font-bold">Active Blockers</h2>
                    <span className="px-3 py-1 rounded-full bg-danger text-white text-xs font-bold uppercase tracking-wider">2 Critical</span>
                </div>

                <div className="space-y-4">
                    {/* Blocker 1 */}
                    <div className="card bg-bg-secondary p-0 overflow-hidden">
                        <div className="p-6 flex items-start gap-4">
                            <div className="w-12 h-12 rounded-xl bg-danger/10 flex items-center justify-center flex-shrink-0">
                                <AlertCircle className="w-6 h-6 text-danger" />
                            </div>
                            <div className="flex-grow">
                                <div className="flex justify-between items-start mb-1">
                                    <h3 className="text-lg font-bold text-white">Auth API Latency</h3>
                                    <span className="px-2 py-1 rounded bg-bg-tertiary text-text-secondary text-xs font-mono font-bold">P0</span>
                                </div>
                                <p className="text-text-secondary text-sm mb-4">Reported by Alex R.</p>

                                <div className="bg-accent-primary/10 border border-accent-primary/20 rounded-lg p-3 flex gap-3 items-start">
                                    <Bot className="w-5 h-5 text-accent-primary flex-shrink-0 mt-0.5" />
                                    <p className="text-sm text-accent-primary font-medium italic">
                                        "Issue traced to AWS Region us-east-1. Suggest switching to fallback."
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Blocker 2 */}
                    <div className="card bg-bg-secondary p-6 flex items-center gap-4">
                        <div className="w-12 h-12 rounded-xl bg-warning/10 flex items-center justify-center flex-shrink-0">
                            <Clock className="w-6 h-6 text-warning" />
                        </div>
                        <div className="flex-grow">
                            <div className="flex justify-between items-start mb-1">
                                <h3 className="text-lg font-bold text-white">Design Review: Onboarding</h3>
                                <span className="px-2 py-1 rounded bg-bg-tertiary text-text-secondary text-xs font-mono font-bold">P1</span>
                            </div>
                            <p className="text-text-secondary text-sm">Pending since yesterday</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
