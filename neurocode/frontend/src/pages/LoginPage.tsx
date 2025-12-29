/**
 * Login page with registration option.
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../stores';

export function LoginPage() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const { login, isLoading, error, clearError } = useAuthStore();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        clearError();

        const success = await login(username, password);
        if (success) {
            navigate('/dashboard');
        }
    };

    return (
        <div className="min-h-screen bg-[var(--color-bg)] flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-[var(--color-primary)]">NeuroCode</h1>
                    <p className="text-[var(--color-text-secondary)] mt-2">
                        Learn Python at your own pace
                    </p>
                </div>

                <div className="card">
                    <h2 className="text-xl font-semibold mb-6">Sign In</h2>

                    {error && (
                        <div className="bg-[var(--color-error)] bg-opacity-10 text-[var(--color-error)] p-3 rounded-lg mb-4 text-sm">
                            {error}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label htmlFor="username" className="block text-sm font-medium mb-1">
                                Username
                            </label>
                            <input
                                id="username"
                                type="text"
                                value={username}
                                onChange={(e) => setUsername(e.target.value)}
                                className="input"
                                required
                                autoComplete="username"
                            />
                        </div>

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium mb-1">
                                Password
                            </label>
                            <input
                                id="password"
                                type="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="input"
                                required
                                autoComplete="current-password"
                            />
                        </div>

                        <button type="submit" disabled={isLoading} className="btn btn-primary w-full">
                            {isLoading ? 'Signing in...' : 'Sign In'}
                        </button>
                    </form>

                    <p className="text-center text-sm text-[var(--color-text-secondary)] mt-6">
                        Don't have an account?{' '}
                        <Link to="/register" className="text-[var(--color-primary)] font-medium hover:underline">
                            Create one
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
