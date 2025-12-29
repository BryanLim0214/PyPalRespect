/**
 * Authentication store using Zustand.
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '../types';
import { authApi, ApiError } from '../services/api';

interface AuthState {
    user: User | null;
    isAuthenticated: boolean;
    isLoading: boolean;
    error: string | null;

    login: (username: string, password: string) => Promise<boolean>;
    register: (data: {
        username: string;
        password: string;
        birthYear: number;
        gradeLevel: number;
        parentEmail?: string;
        interests?: string[];
    }) => Promise<{ success: boolean; needsConsent: boolean }>;
    logout: () => void;
    fetchUser: () => Promise<void>;
    updatePreferences: (data: Partial<User>) => Promise<boolean>;
    clearError: () => void;
}

export const useAuthStore = create<AuthState>()(
    persist(
        (set, _get) => ({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,

            login: async (username, password) => {
                set({ isLoading: true, error: null });
                try {
                    const token = await authApi.login(username, password);
                    localStorage.setItem('access_token', token.access_token);

                    const user = await authApi.getMe();
                    set({ user, isAuthenticated: true, isLoading: false });
                    return true;
                } catch (err) {
                    const message = err instanceof ApiError ? err.message : 'Login failed';
                    set({ error: message, isLoading: false });
                    return false;
                }
            },

            register: async ({ username, password, birthYear, gradeLevel, parentEmail, interests }) => {
                set({ isLoading: true, error: null });
                try {
                    const result = await authApi.register({
                        username,
                        password,
                        birth_year: birthYear,
                        grade_level: gradeLevel,
                        parent_email: parentEmail,
                        interests: interests,
                    });

                    if (result.status === 'consent_required') {
                        set({ isLoading: false });
                        return { success: true, needsConsent: true };
                    }

                    if (result.access_token) {
                        localStorage.setItem('access_token', result.access_token);
                        const user = await authApi.getMe();
                        set({ user, isAuthenticated: true, isLoading: false });
                    }

                    return { success: true, needsConsent: false };
                } catch (err) {
                    const message = err instanceof ApiError ? err.message : 'Registration failed';
                    set({ error: message, isLoading: false });
                    return { success: false, needsConsent: false };
                }
            },

            logout: () => {
                localStorage.removeItem('access_token');
                set({ user: null, isAuthenticated: false, error: null });
            },

            fetchUser: async () => {
                const token = localStorage.getItem('access_token');
                if (!token) {
                    set({ isAuthenticated: false });
                    return;
                }

                set({ isLoading: true });
                try {
                    const user = await authApi.getMe();
                    set({ user, isAuthenticated: true, isLoading: false });
                } catch {
                    localStorage.removeItem('access_token');
                    set({ user: null, isAuthenticated: false, isLoading: false });
                }
            },

            updatePreferences: async (data: Partial<User>) => {
                set({ isLoading: true, error: null });
                try {
                    const updatedUser = await authApi.updatePreferences(data);
                    set({ user: updatedUser, isLoading: false });
                    return true;
                } catch (err) {
                    const message = err instanceof ApiError ? err.message : 'Failed to update preferences';
                    set({ error: message, isLoading: false });
                    return false;
                }
            },

            clearError: () => set({ error: null }),
        }),
        {
            name: 'auth-storage',
            partialize: (state) => ({
                isAuthenticated: state.isAuthenticated,
            }),
        }
    )
);
