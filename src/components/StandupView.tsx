import React, { useState } from 'react';
import {
    ArrowLeft,
    MoreHorizontal,
    Mic,
    Send,
    Bot,
    User,
    ChevronRight
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
    id: string;
    sender: 'bot' | 'user';
    text: string;
    timestamp: Date;
}

export function StandupView() {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            sender: 'bot',
            text: "Good morning! Ready for today's standup? Let's start with what you accomplished yesterday.",
            timestamp: new Date()
        },
        {
            id: '2',
            sender: 'user',
            text: "I finished the API documentation and fixed the login bug we found during the sprint review.",
            timestamp: new Date()
        },
        {
            id: '3',
            sender: 'bot',
            text: "Great work on those! What are you planning to tackle today?",
            timestamp: new Date()
        }
    ]);
    const [inputValue, setInputValue] = useState('');

    const handleSend = () => {
        if (!inputValue.trim()) return;
        const newMessage: Message = {
            id: Date.now().toString(),
            sender: 'user',
            text: inputValue,
            timestamp: new Date()
        };
        setMessages([...messages, newMessage]);
        setInputValue('');
    };

    return (
        <div className="h-full flex flex-col bg-bg-primary relative overflow-hidden">
            {/* Header */}
            <header className="px-6 py-4 flex items-center justify-between bg-bg-primary z-10">
                <div className="flex items-center gap-4">
                    <button className="text-text-secondary hover:text-white">
                        <ArrowLeft className="w-6 h-6" />
                    </button>
                    <div>
                        <h1 className="text-xl font-bold">Daily AI Standup</h1>
                        <div className="flex items-center gap-2 text-xs text-text-secondary">
                            <span>Tickora Bot</span>
                            <span>•</span>
                            <span>Today, Oct 24</span>
                        </div>
                    </div>
                </div>
                <button className="text-text-secondary hover:text-white">
                    <MoreHorizontal className="w-6 h-6" />
                </button>
            </header>

            {/* Progress Bar */}
            <div className="px-6 pb-6">
                <div className="flex justify-between items-center text-sm font-medium mb-2">
                    <span className="text-white">Section: Yesterday's Progress</span>
                    <span className="text-accent-primary">STEP 1 OF 3</span>
                </div>
                <div className="h-1.5 bg-bg-tertiary rounded-full overflow-hidden">
                    <div className="h-full w-1/3 bg-accent-primary rounded-full" />
                </div>
            </div>

            {/* Chat Area */}
            <div className="flex-grow overflow-y-auto px-6 pb-6 space-y-6">
                {messages.map((msg) => (
                    <div key={msg.id} className={`flex gap-4 ${msg.sender === 'user' ? 'flex-row-reverse' : ''}`}>
                        {/* Avatar */}
                        <div className={`w-10 h-10 rounded-full flex items-center justify-center flex-shrink-0 border-2 ${msg.sender === 'bot' ? 'bg-[#F3EAD3] border-[#F3EAD3]' : 'bg-white border-white'
                            }`}>
                            {msg.sender === 'bot' ? (
                                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Bear" alt="Bot" className="w-8 h-8" />
                            ) : (
                                <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Alex" alt="User" className="w-8 h-8" />
                            )}
                        </div>

                        {/* Message Bubble */}
                        <div className="space-y-1 max-w-[80%]">
                            <div className="text-[10px] font-bold text-text-secondary uppercase tracking-wider mb-1">
                                {msg.sender === 'bot' ? 'TICKORA BOT' : 'YOU'}
                            </div>
                            <div className={`p-4 rounded-2xl text-sm leading-relaxed ${msg.sender === 'bot'
                                    ? 'bg-bg-tertiary text-text-primary rounded-tl-none'
                                    : 'bg-accent-primary text-white rounded-tr-none shadow-lg shadow-accent-primary/20'
                                }`}>
                                {msg.text}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            {/* Context Carousel */}
            <div className="px-6 pb-4">
                <div className="flex justify-between items-center mb-3">
                    <span className="text-xs font-bold text-text-secondary uppercase tracking-wider">YOUR ACTIVE TASKS CONTEXT</span>
                    <button className="text-xs font-bold text-accent-primary hover:underline">Swipe to view all</button>
                </div>
                <div className="flex gap-4 overflow-x-auto pb-2 no-scrollbar">
                    {/* Task Card 1 */}
                    <div className="min-w-[240px] bg-bg-secondary border border-border-primary rounded-xl p-4 relative overflow-hidden">
                        <div className="flex justify-between items-start mb-2">
                            <span className="px-2 py-1 rounded bg-accent-primary/20 text-accent-primary text-[10px] font-bold uppercase">In Progress</span>
                            <MoreHorizontal className="w-4 h-4 text-text-secondary" />
                        </div>
                        <h3 className="font-bold text-white text-sm mb-4">Refactor Auth Flow for iOS</h3>
                        <div className="flex items-center gap-2">
                            <div className="flex-grow h-1 bg-bg-tertiary rounded-full overflow-hidden">
                                <div className="h-full w-[45%] bg-accent-primary" />
                            </div>
                            <span className="text-[10px] text-text-secondary font-bold">45%</span>
                        </div>
                    </div>

                    {/* Task Card 2 */}
                    <div className="min-w-[240px] bg-bg-secondary border border-border-primary rounded-xl p-4 relative overflow-hidden">
                        <div className="flex justify-between items-start mb-2">
                            <span className="px-2 py-1 rounded bg-warning/20 text-warning text-[10px] font-bold uppercase">Priority</span>
                            <MoreHorizontal className="w-4 h-4 text-text-secondary" />
                        </div>
                        <h3 className="font-bold text-white text-sm mb-4">Fix Bug #402: Image Loading</h3>
                        <div className="flex items-center gap-2">
                            <div className="flex-grow h-1 bg-bg-tertiary rounded-full overflow-hidden">
                                <div className="h-full w-[10%] bg-warning" />
                            </div>
                            <span className="text-[10px] text-text-secondary font-bold">10%</span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Input Area */}
            <div className="p-4 bg-bg-secondary border-t border-border-primary">
                <div className="relative flex items-center gap-2">
                    <div className="flex-grow relative">
                        <input
                            type="text"
                            value={inputValue}
                            onChange={(e) => setInputValue(e.target.value)}
                            placeholder="Type your update..."
                            className="w-full bg-bg-tertiary border-none rounded-full pl-6 pr-12 py-3.5 text-sm text-white placeholder:text-text-muted focus:ring-1 focus:ring-accent-primary"
                        />
                        <button className="absolute right-2 top-1/2 -translate-y-1/2 p-2 text-accent-primary hover:text-white transition-colors">
                            <Mic className="w-5 h-5" />
                        </button>
                    </div>
                    <button
                        onClick={handleSend}
                        className="w-12 h-12 rounded-full bg-accent-primary flex items-center justify-center text-white shadow-lg shadow-accent-primary/30 hover:scale-105 transition-transform"
                    >
                        <Send className="w-5 h-5" />
                    </button>
                </div>

                {/* Quick Replies */}
                <div className="flex gap-3 mt-4 overflow-x-auto pb-2 no-scrollbar">
                    <button className="whitespace-nowrap px-4 py-2 rounded-full bg-bg-tertiary border border-border-primary text-xs font-medium text-text-secondary hover:text-white hover:border-text-secondary transition-colors">
                        "I'm working on Refactor Auth..."
                    </button>
                    <button className="whitespace-nowrap px-4 py-2 rounded-full bg-bg-tertiary border border-border-primary text-xs font-medium text-text-secondary hover:text-white hover:border-text-secondary transition-colors">
                        "No blockers today"
                    </button>
                </div>
            </div>
        </div>
    );
}
