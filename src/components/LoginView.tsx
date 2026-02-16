import React, { useState } from 'react';
import { Eye, EyeOff } from 'lucide-react';

interface LoginViewProps {
    onLogin: () => void;
    onBack: () => void;
    onSignupClick: () => void;
}

export function LoginView({ onLogin, onBack, onSignupClick }: LoginViewProps) {
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setTimeout(() => {
            setIsLoading(false);
            onLogin();
        }, 1000);
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-4 relative overflow-hidden">
            {/* Background Glow */}
            <div className="absolute top-[-20%] left-1/2 -translate-x-1/2 w-[600px] h-[600px] bg-accent-primary/20 blur-[120px] rounded-full -z-10" />

            <div className="w-full max-w-[420px] space-y-8">
                {/* Header */}
                <div className="text-center space-y-6">
                    <div className="w-20 h-20 mx-auto bg-transparent flex items-center justify-center">
                        <img src="/logo.png" alt="Tickora" className="w-full h-full object-contain" />
                    </div>
                    <div className="space-y-2">
                        <h1 className="text-3xl font-bold tracking-tight">Welcome back</h1>
                        <p className="text-text-secondary">Log in to manage your agile workflows</p>
                    </div>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-text-primary ml-1">Email Address</label>
                        <div className="relative">
                            <input
                                type="email"
                                placeholder="name@company.com"
                                className="input-field pl-4"
                                required
                            />
                        </div>
                    </div>

                    <div className="space-y-2">
                        <div className="flex justify-between items-center ml-1">
                            <label className="text-sm font-semibold text-text-primary">Password</label>
                            <button type="button" className="text-xs font-semibold text-accent-primary hover:text-accent-secondary">
                                Forgot password?
                            </button>
                        </div>
                        <div className="relative">
                            <input
                                type={showPassword ? "text" : "password"}
                                placeholder="••••••••"
                                className="input-field pl-4 pr-12 tracking-widest"
                                required
                            />
                            <button
                                type="button"
                                onClick={() => setShowPassword(!showPassword)}
                                className="absolute right-4 top-1/2 -translate-y-1/2 text-text-secondary hover:text-text-primary transition-colors"
                            >
                                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                            </button>
                        </div>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading}
                        className="w-full btn btn-primary justify-center py-3.5 text-base rounded-xl"
                    >
                        {isLoading ? 'Logging in...' : 'Log In'}
                    </button>
                </form>

                {/* Divider */}
                <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t border-border-primary"></div>
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                        <span className="bg-bg-primary px-4 text-text-secondary font-semibold tracking-wider">Or continue with</span>
                    </div>
                </div>

                {/* Social Login */}
                <div className="grid grid-cols-2 gap-4">
                    <button className="flex items-center justify-center gap-3 py-3 px-4 bg-bg-secondary border border-border-primary rounded-xl hover:bg-bg-tertiary transition-colors">
                        <img src="/google.png" alt="Google" className="w-5 h-5" />
                        <span className="text-sm font-semibold">Google</span>
                    </button>
                    <button className="flex items-center justify-center gap-3 py-3 px-4 bg-bg-secondary border border-border-primary rounded-xl hover:bg-bg-tertiary transition-colors">
                        <img src="/outlook.png" alt="Outlook" className="w-5 h-5" />
                        <span className="text-sm font-semibold">Outlook</span>
                    </button>
                </div>

                {/* Footer */}
                <p className="text-center text-sm text-text-secondary">
                    Don't have an account?{' '}
                    <button onClick={onSignupClick} className="text-accent-primary font-bold hover:underline">
                        Sign up free
                    </button>
                </p>
            </div>
        </div>
    );
}
