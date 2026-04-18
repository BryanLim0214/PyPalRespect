/**
 * Main App component with role-based React Router.
 */
import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Outlet } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { useAuthStore, useThemeStore } from './stores';
import { MainLayout } from './components';
import {
    LoginPage,
    RegisterPage,
    DashboardPage,
    ExercisePage,
    SettingsPage,
    ConsentPendingPage,
    TeacherDashboardPage,
    TeacherStudentDetailPage,
    TeacherExercisesPage,
} from './pages';
import './index.css';

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            staleTime: 5 * 60 * 1000,
            retry: 1,
        },
    },
});

function ProtectedRoute() {
    const { isAuthenticated, isLoading, user, fetchUser } = useAuthStore();

    useEffect(() => {
        fetchUser();
    }, [fetchUser]);

    if (isLoading || (isAuthenticated && !user)) {
        return (
            <div className="min-h-screen flex items-center justify-center bg-[var(--color-bg)]">
                <div className="w-8 h-8 border-4 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (!isAuthenticated) {
        return <Navigate to="/login" replace />;
    }

    return <Outlet />;
}

function TeacherOnly() {
    const { user } = useAuthStore();
    if (user && user.role !== 'teacher') {
        return <Navigate to="/dashboard" replace />;
    }
    return <Outlet />;
}

function StudentOnly() {
    const { user } = useAuthStore();
    if (user && user.role !== 'student') {
        return <Navigate to="/teacher" replace />;
    }
    return <Outlet />;
}

function RoleHome() {
    const { user } = useAuthStore();
    if (!user) return null;
    return <Navigate to={user.role === 'teacher' ? '/teacher' : '/dashboard'} replace />;
}

function AppContent() {
    const { applyToDocument } = useThemeStore();

    useEffect(() => {
        applyToDocument();
    }, [applyToDocument]);

    return (
        <Routes>
            {/* Public routes */}
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/consent-pending" element={<ConsentPendingPage />} />

            {/* Protected routes */}
            <Route element={<ProtectedRoute />}>
                <Route element={<MainLayout />}>
                    <Route path="/settings" element={<SettingsPage />} />

                    {/* Student-only routes */}
                    <Route element={<StudentOnly />}>
                        <Route path="/dashboard" element={<DashboardPage />} />
                        <Route path="/exercise/:id" element={<ExercisePage />} />
                    </Route>

                    {/* Teacher-only routes */}
                    <Route element={<TeacherOnly />}>
                        <Route path="/teacher" element={<TeacherDashboardPage />} />
                        <Route path="/teacher/exercises" element={<TeacherExercisesPage />} />
                        <Route path="/teacher/students/:id" element={<TeacherStudentDetailPage />} />
                    </Route>
                </Route>

                {/* Role-based home redirect */}
                <Route path="/" element={<RoleHome />} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
    );
}

export default function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <BrowserRouter>
                <AppContent />
            </BrowserRouter>
        </QueryClientProvider>
    );
}
