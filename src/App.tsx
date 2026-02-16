import React, { useState } from 'react'
import {
    Zap,
    ChevronRight,
    Menu,
    X,
    Search,
    Bell,
    HelpCircle,
    Settings
} from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { Sidebar } from './components/Sidebar'
import { Dashboard } from './components/Dashboard'
import { StandupView } from './components/StandupView'
import { SettingsView } from './components/SettingsView'
import { BoardView } from './components/BoardView'
import { LoginView } from './components/LoginView'
import { SignupView } from './components/SignupView'

type ViewState = 'landing' | 'login' | 'signup' | 'app';

function App() {
    const [view, setView] = useState<ViewState>('landing');
    const [activeTab, setActiveTab] = useState('dashboard'); // Default to dashboard for new design
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const handleLogin = () => {
        setView('app');
    };

    if (view === 'login') {
        return (
            <LoginView
                onLogin={handleLogin}
                onBack={() => setView('landing')}
                onSignupClick={() => setView('signup')}
            />
        );
    }

    if (view === 'signup') {
        return (
            <SignupView
                onSignup={handleLogin}
                onLoginClick={() => setView('login')}
            />
        );
    }

    if (view === 'app') {
        return (
            <div className="flex min-h-screen bg-bg-primary text-text-primary font-sans">
                <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

                <div className="flex-grow flex flex-col h-screen overflow-hidden">
                    {/* Top Navigation Bar */}
                    <header className="h-16 border-b border-border-primary flex items-center justify-between px-6 bg-bg-secondary shrink-0 z-20">
                        <div className="flex items-center gap-4 w-1/3">
                            <div className="relative w-full max-w-md">
                                <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-secondary" />
                                <input
                                    type="text"
                                    placeholder="Search"
                                    className="w-full pl-10 pr-4 py-2 rounded-xl border border-border-primary bg-bg-primary text-sm focus:outline-none focus:border-accent-primary transition-all text-text-primary placeholder:text-text-muted"
                                />
                            </div>
                        </div>

                        <div className="flex items-center gap-4">
                            <button className="text-text-secondary hover:text-white transition-colors">
                                <HelpCircle className="w-5 h-5" />
                            </button>
                            <button className="text-text-secondary hover:text-white transition-colors relative">
                                <Bell className="w-5 h-5" />
                                <span className="absolute top-0 right-0 w-2 h-2 bg-danger rounded-full border-2 border-bg-secondary"></span>
                            </button>
                            <button className="text-text-secondary hover:text-white transition-colors">
                                <Settings className="w-5 h-5" />
                            </button>
                            <div className="w-9 h-9 rounded-full bg-accent-primary text-white flex items-center justify-center text-xs font-bold cursor-pointer hover:bg-accent-secondary transition-colors border-2 border-bg-primary">
                                AR
                            </div>
                        </div>
                    </header>

                    {/* Main Content Area */}
                    <main className="flex-grow overflow-y-auto bg-bg-primary">
                        <AnimatePresence mode="wait">
                            <motion.div
                                key={activeTab}
                                initial={{ opacity: 0, y: 5 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -5 }}
                                transition={{ duration: 0.15 }}
                                className="h-full"
                            >
                                {activeTab === 'dashboard' && <Dashboard />}
                                {activeTab === 'board' && <BoardView />}
                                {activeTab === 'standups' && <StandupView />}
                                {activeTab === 'settings' && <SettingsView />}
                                {['backlog', 'team'].includes(activeTab) && (
                                    <div className="p-8 flex flex-col items-center justify-center h-[80vh] text-center">
                                        <div className="w-16 h-16 bg-bg-secondary rounded-full flex items-center justify-center mb-4 border border-border-primary">
                                            <Zap className="text-accent-primary w-8 h-8" />
                                        </div>
                                        <h2 className="text-xl font-bold text-text-primary mb-2">{activeTab.charAt(0).toUpperCase() + activeTab.slice(1)} Coming Soon</h2>
                                        <p className="text-text-secondary max-w-md">
                                            We're currently building the {activeTab} module for MVP-1. Stay tuned for updates!
                                        </p>
                                    </div>
                                )}
                            </motion.div>
                        </AnimatePresence>
                    </main>
                </div>
            </div>
        )
    }

    return (
        <div className="min-h-screen flex flex-col bg-bg-primary text-text-primary">
            {/* Navigation */}
            <nav className="sticky top-0 z-50 px-6 py-4 flex items-center justify-between border-b border-border-primary bg-bg-secondary/80 backdrop-blur-md">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 bg-accent-primary rounded-lg flex items-center justify-center">
                        <img src="/logo.png" alt="Tickora" className="w-5 h-5 object-contain brightness-0 invert" />
                    </div>
                    <span className="text-xl font-bold tracking-tight text-white">Tickora</span>
                </div>

                <div className="hidden md:flex items-center gap-8 text-sm font-medium text-text-secondary">
                    <a href="#" className="hover:text-white transition-colors">Features</a>
                    <a href="#" className="hover:text-white transition-colors">Solutions</a>
                    <a href="#" className="hover:text-white transition-colors">Pricing</a>
                    <a href="#" className="hover:text-white transition-colors">Resources</a>
                </div>

                <div className="flex items-center gap-4">
                    <button
                        className="hidden md:block text-sm font-semibold text-text-primary hover:text-white transition-colors"
                        onClick={() => setView('login')}
                    >
                        Log in
                    </button>
                    <button
                        className="btn btn-primary"
                        onClick={() => setView('signup')}
                    >
                        Get Started
                    </button>
                    <button
                        className="md:hidden p-2"
                        onClick={() => setIsMenuOpen(!isMenuOpen)}
                    >
                        {isMenuOpen ? <X /> : <Menu />}
                    </button>
                </div>
            </nav>

            {/* Hero Section */}
            <main className="flex-grow relative overflow-hidden">
                {/* Background Glows */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[1000px] h-[600px] bg-accent-primary/10 blur-[120px] rounded-full -z-10" />

                <section className="px-6 pt-20 pb-32">
                    <div className="max-w-6xl mx-auto text-center">
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ duration: 0.6 }}
                        >
                            <span className="px-3 py-1 rounded-full bg-accent-primary/10 text-xs font-bold uppercase text-accent-primary mb-6 inline-block border border-accent-primary/20">
                                Next-Gen Project Management
                            </span>
                            <h1 className="text-5xl md:text-7xl font-extrabold mb-6 leading-tight text-white">
                                Manage projects with <br />
                                <span className="text-transparent bg-clip-text bg-gradient-to-r from-accent-primary to-accent-secondary">AI Intelligence</span>
                            </h1>
                            <p className="text-xl text-text-secondary max-w-2xl mx-auto mb-10 leading-relaxed">
                                Tickora automates your standups, tracks blockers in real-time, and generates
                                intelligent summaries so you can focus on building what matters.
                            </p>
                            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                                <button
                                    className="btn btn-primary px-8 py-4 text-lg rounded-xl"
                                    onClick={() => setView('signup')}
                                >
                                    Start Free Trial <ChevronRight className="w-5 h-5" />
                                </button>
                                <button className="btn btn-secondary px-8 py-4 text-lg rounded-xl">
                                    Watch Demo
                                </button>
                            </div>
                        </motion.div>

                        {/* Mock Dashboard Preview */}
                        <motion.div
                            className="mt-20 bg-bg-secondary rounded-2xl p-2 shadow-2xl border border-border-primary relative max-w-5xl mx-auto"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            transition={{ delay: 0.3, duration: 0.8 }}
                        >
                            <div className="bg-bg-primary rounded-xl overflow-hidden aspect-[16/9] flex items-center justify-center border border-border-primary">
                                <div className="text-center">
                                    <Zap className="w-16 h-16 text-accent-primary mx-auto mb-4" />
                                    <h3 className="text-xl font-bold text-white">Interactive Demo</h3>
                                    <p className="text-text-secondary">Sign up to explore the full platform</p>
                                </div>
                            </div>
                        </motion.div>
                    </div>
                </section>
            </main>
        </div>
    )
}

export default App
