import React, { useState } from 'react';
import { Eye, EyeOff, ChevronDown, CheckSquare } from 'lucide-react';

interface SignupViewProps {
    onSignup: () => void;
    onLoginClick: () => void;
}

export function SignupView({ onSignup, onLoginClick }: SignupViewProps) {
    const [showPassword, setShowPassword] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [agreed, setAgreed] = useState(false);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!agreed) return;

        setIsLoading(true);
        setTimeout(() => {
            setIsLoading(false);
            onSignup();
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
                        <h1 className="text-3xl font-bold tracking-tight">Create Account</h1>
                        <p className="text-text-secondary">Join the AI-first project management platform.</p>
                    </div>
                </div>

                {/* Form */}
                <form onSubmit={handleSubmit} className="space-y-5">
                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-text-primary ml-1">Full Name</label>
                        <input
                            type="text"
                            placeholder="Enter your full name"
                            className="input-field pl-4"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-text-primary ml-1">Email Address</label>
                        <input
                            type="email"
                            placeholder="name@company.com"
                            className="input-field pl-4"
                            required
                        />
                    </div>

                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-text-primary ml-1">Password</label>
                        <div className="relative">
                            <input
                                type={showPassword ? "text" : "password"}
                                placeholder="Min. 8 characters"
                                className="input-field pl-4 pr-12"
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

                    <div className="space-y-2">
                        <label className="text-sm font-semibold text-text-primary ml-1">Role</label>
                        <div className="relative">
                            <select className="input-field pl-4 pr-10 appearance-none cursor-pointer">
                                <option value="" disabled selected>Select your initial role</option>
                                <option value="scrum_master">Scrum Master</option>
                                <option value="product_owner">Product Owner</option>
                                <option value="developer">Developer</option>
                                <option value="designer">Designer</option>
                            </select>
                            <ChevronDown className="absolute right-4 top-1/2 -translate-y-1/2 w-5 h-5 text-text-secondary pointer-events-none" />
                        </div>
                    </div>

                    <div className="flex items-start gap-3 pt-2">
                        <button
                            type="button"
                            onClick={() => setAgreed(!agreed)}
                            className={`mt-0.5 flex-shrink-0 w-5 h-5 rounded border flex items-center justify-center transition-colors ${agreed ? 'bg-accent-primary border-accent-primary text-white' : 'border-text-secondary hover:border-text-primary'
                                }`}
                        >
                            {agreed && <CheckSquare className="w-3.5 h-3.5" />}
                        </button>
                        <p className="text-sm text-text-secondary leading-snug">
                            I agree to the <a href="#" className="text-accent-primary hover:underline">Terms of Service</a> and <a href="#" className="text-accent-primary hover:underline">Privacy Policy</a>.
                        </p>
                    </div>

                    <button
                        type="submit"
                        disabled={isLoading || !agreed}
                        className="w-full btn btn-primary justify-center py-3.5 text-base rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                        {isLoading ? 'Creating Account...' : 'Create Account'}
                    </button>
                </form>

                {/* Divider */}
                <div className="relative">
                    <div className="absolute inset-0 flex items-center">
                        <div className="w-full border-t border-border-primary"></div>
                    </div>
                    <div className="relative flex justify-center text-xs uppercase">
                        <span className="bg-bg-primary px-4 text-text-secondary font-semibold tracking-wider">Or sign up with</span>
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
                    <button onClick={onLoginClick} className="text-accent-primary font-bold hover:underline">
                        Sign up free
                    </button>
                </p>
            </div>
        </div>
    );
}
