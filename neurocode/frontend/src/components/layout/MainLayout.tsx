/**
 * MainLayout with role-aware navigation for students and teachers.
 */
import { Link, NavLink, Outlet, useNavigate } from 'react-router-dom';
import { useAuthStore, useThemeStore } from '../../stores';
import { PointsDisplay } from '../adhd';
import clsx from 'clsx';

export function MainLayout() {
    const { user, logout } = useAuthStore();
    const { themeMode, setThemeMode } = useThemeStore();
    const navigate = useNavigate();

    const isTeacher = user?.role === 'teacher';

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    const studentLinks = [
        { to: '/dashboard', label: 'Dashboard' },
        { to: '/settings', label: 'Settings' },
    ];
    const teacherLinks = [
        { to: '/teacher', label: 'Classroom' },
        { to: '/teacher/exercises', label: 'Exercises' },
        { to: '/settings', label: 'Settings' },
    ];
    const links = isTeacher ? teacherLinks : studentLinks;

    return (
        <div className="min-h-screen bg-[var(--color-bg)]">
            <nav className="bg-[var(--color-bg-card)] border-b border-[var(--color-border)] sticky top-0 z-40">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between h-16">
                        <Link to={isTeacher ? '/teacher' : '/dashboard'} className="flex items-center gap-2">
                            <span className="text-xl font-bold text-[var(--color-primary)]">PyPal</span>
                            {isTeacher && (
                                <span className="px-2 py-0.5 text-xs rounded-full bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 font-semibold">
                                    Teacher
                                </span>
                            )}
                        </Link>

                        <div className="flex items-center gap-6">
                            {links.map((link) => (
                                <NavLink
                                    key={link.to}
                                    to={link.to}
                                    end
                                    className={({ isActive }) =>
                                        clsx(
                                            'text-sm font-medium',
                                            isActive
                                                ? 'text-[var(--color-text)]'
                                                : 'text-[var(--color-text-secondary)] hover:text-[var(--color-text)]',
                                        )
                                    }
                                >
                                    {link.label}
                                </NavLink>
                            ))}
                        </div>

                        <div className="flex items-center gap-4">
                            {user && !isTeacher && (
                                <PointsDisplay points={user.total_points} streak={user.current_streak} />
                            )}

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

                            <div className="flex items-center gap-2">
                                <span className="text-sm font-medium">
                                    {user?.display_name || user?.username}
                                </span>
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

            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <Outlet />
            </main>
        </div>
    );
}
