import React, { useState } from 'react';
import {
    Settings,
    Key,
    Cpu,
    Shield,
    Save,
    Check,
    ExternalLink,
    Zap
} from 'lucide-react';
import { motion } from 'framer-motion';

export function SettingsView() {
    const [provider, setProvider] = useState('openai');
    const [isSaved, setIsSaved] = useState(false);

    const handleSave = () => {
        setIsSaved(true);
        setTimeout(() => setIsSaved(false), 3000);
    };

    return (
        <div className="p-8 max-w-4xl mx-auto space-y-8">
            <header>
                <h1 className="text-3xl font-bold outfit mb-2">Settings</h1>
                <p className="text-text-secondary">Configure your workspace and AI integrations.</p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Sidebar Navigation */}
                <div className="space-y-2">
                    <SettingsTab active icon={<Cpu />} label="LLM Integration" />
                    <SettingsTab icon={<Shield />} label="Data Privacy" />
                    <SettingsTab icon={<Key />} label="API Keys" />
                    <SettingsTab icon={<Settings />} label="Workspace" />
                </div>

                {/* Content Area */}
                <div className="md:col-span-2 space-y-6">
                    <div className="card">
                        <h2 className="text-xl font-bold outfit mb-6">LLM Configuration</h2>

                        <div className="space-y-6">
                            <div className="space-y-2">
                                <label className="text-sm font-medium text-text-secondary">AI Provider</label>
                                <div className="grid grid-cols-2 gap-4">
                                    <ProviderCard
                                        active={provider === 'openai'}
                                        onClick={() => setProvider('openai')}
                                        name="OpenAI"
                                        description="GPT-4o, GPT-3.5"
                                    />
                                    <ProviderCard
                                        active={provider === 'azure'}
                                        onClick={() => setProvider('azure')}
                                        name="Azure OpenAI"
                                        description="Enterprise Instance"
                                    />
                                </div>
                            </div>

                            <div className="space-y-2">
                                <label className="text-sm font-medium text-text-secondary">API Key</label>
                                <div className="relative">
                                    <input
                                        type="password"
                                        placeholder="sk-••••••••••••••••••••••••"
                                        className="w-full bg-bg-primary border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-accent-primary transition-colors text-sm"
                                    />
                                    <Key className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
                                </div>
                                <p className="text-[10px] text-text-muted">Your API key is encrypted and never stored in plain text.</p>
                            </div>

                            <div className="grid grid-cols-2 gap-6">
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-text-secondary">Model Selection</label>
                                    <select className="w-full bg-bg-primary border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-accent-primary transition-colors text-sm appearance-none">
                                        <option>gpt-4o</option>
                                        <option>gpt-4-turbo</option>
                                        <option>gpt-3.5-turbo</option>
                                    </select>
                                </div>
                                <div className="space-y-2">
                                    <label className="text-sm font-medium text-text-secondary">Token Limit</label>
                                    <input
                                        type="number"
                                        defaultValue="2000"
                                        className="w-full bg-bg-primary border border-white/10 rounded-xl px-4 py-3 focus:outline-none focus:border-accent-primary transition-colors text-sm"
                                    />
                                </div>
                            </div>

                            <div className="p-4 rounded-xl bg-accent-primary/5 border border-accent-primary/20 flex items-start gap-4">
                                <div className="w-10 h-10 rounded-lg bg-accent-primary/10 flex items-center justify-center flex-shrink-0">
                                    <Shield className="text-accent-primary w-5 h-5" />
                                </div>
                                <div>
                                    <h4 className="text-sm font-bold mb-1">Data Privacy Controls</h4>
                                    <p className="text-xs text-text-secondary leading-relaxed mb-3">
                                        Enable PII redaction to automatically mask sensitive information before sending data to the LLM.
                                    </p>
                                    <label className="flex items-center gap-2 cursor-pointer">
                                        <div className="relative w-10 h-5 bg-bg-tertiary rounded-full border border-white/10">
                                            <div className="absolute left-1 top-1 w-3 h-3 bg-accent-primary rounded-full transition-all" />
                                        </div>
                                        <span className="text-xs font-medium">Enable PII Redaction</span>
                                    </label>
                                </div>
                            </div>

                            <button
                                onClick={handleSave}
                                className="btn btn-primary w-full justify-center"
                            >
                                {isSaved ? <><Check className="w-5 h-5" /> Settings Saved</> : <><Save className="w-5 h-5" /> Save Configuration</>}
                            </button>
                        </div>
                    </div>

                    <div className="card">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-lg font-bold outfit">Integration Status</h2>
                            <span className="px-2 py-1 rounded-md bg-green-500/20 text-green-500 text-[10px] font-bold uppercase tracking-wider">Connected</span>
                        </div>
                        <div className="space-y-4">
                            <IntegrationItem name="Slack" status="Connected" />
                            <IntegrationItem name="Microsoft Teams" status="Disconnected" action="Connect" />
                            <IntegrationItem name="Google Meet" status="Connected" />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

function SettingsTab({ icon, label, active = false }: { icon: React.ReactNode, label: string, active?: boolean }) {
    return (
        <button className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all ${active ? 'bg-white/10 text-white font-semibold' : 'text-text-secondary hover:bg-white/5 hover:text-white'
            }`}>
            <span className="w-5 h-5">{icon}</span>
            <span className="text-sm">{label}</span>
        </button>
    );
}

function ProviderCard({ name, description, active, onClick }: { name: string, description: string, active: boolean, onClick: () => void }) {
    return (
        <button
            onClick={onClick}
            className={`p-4 rounded-xl border text-left transition-all ${active ? 'border-accent-primary bg-accent-primary/5' : 'border-white/5 bg-bg-tertiary hover:border-white/10'
                }`}
        >
            <div className="flex justify-between items-center mb-1">
                <span className="text-sm font-bold">{name}</span>
                {active && <div className="w-2 h-2 rounded-full bg-accent-primary shadow-[0_0_8px_rgba(99,102,241,0.6)]" />}
            </div>
            <span className="text-[10px] text-text-muted">{description}</span>
        </button>
    );
}

function IntegrationItem({ name, status, action }: { name: string, status: string, action?: string }) {
    return (
        <div className="flex items-center justify-between p-3 rounded-lg bg-bg-tertiary border border-white/5">
            <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded bg-white/5 flex items-center justify-center">
                    <Zap className="w-4 h-4 text-text-muted" />
                </div>
                <span className="text-sm font-medium">{name}</span>
            </div>
            <div className="flex items-center gap-4">
                <span className={`text-[10px] font-bold ${status === 'Connected' ? 'text-green-500' : 'text-text-muted'}`}>{status}</span>
                {action && <button className="text-[10px] font-bold text-accent-primary hover:underline">{action}</button>}
            </div>
        </div>
    );
}
