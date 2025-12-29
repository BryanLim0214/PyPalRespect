/**
 * MainLayout component with navigation.
 */
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore, useThemeStore } from '../../stores';
import { PointsDisplay } from '../adhd';

export function MainLayout() {
    const { user, logout } = useAuthStore();
    const { themeMode, setThemeMode } = useThemeStore();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    return (
        <div className="min-h-screen bg-[var(--color-bg)]">
            {/* Navigation */}
            <nav className="bg-[var(--color-bg-card)] border-b border-[var(--color-border)] sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        {/* Logo */}
                        <Link to="/dashboard" className="flex items-center gap-2">
                            <span className="text-xl font-bold text-[var(--color-primary)]">PyPal</span>
                        </Link>

                        {/* Center nav */}
                        <div className="flex items-center gap-6">
                            <Link
                                to="/dashboard"
                                className="text-sm font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text)]"
                            >
                                Dashboard
                            </Link>
                            <Link
                                to="/settings"
                                className="text-sm font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text)]"
                            >
                                Settings
                            </Link>
                        </div>

                        {/* Right side */}
                        <div className="flex items-center gap-4">
                            {user && <PointsDisplay points={user.total_points} streak={user.current_streak} />}

                            {/* Theme toggle */}
                            <button
                                onClick={() => setThemeMode(themeMode === 'light' ? 'dark' : 'light')}
                                className="p-2 rounded-lg hover:bg-[var(--color-bg-secondary)]"
                                aria-label="Toggle theme"
                            >
                                {themeMode === 'light' ? (
                                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z" />
                                    </svg>
                                ) : (
                                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                                        <path
                                            fillRule="evenodd"
                                            d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
                                            clipRule="evenodd"
                                        />
                                    </svg>
                                )}
                            </button>

                            {/* User menu */}
                            <div className="flex items-center gap-2">
                                <span className="text-sm font-medium">{user?.username}</span>
                                <button
                                    onClick={handleLogout}
                                    className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-error)]"
                                >
                                    Logout
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </nav>

            {/* Main content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Outlet />
            </main>
        </div>
    );
}
