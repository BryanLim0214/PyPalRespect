/**
 * API service layer for communicating with the NeuroCode backend.
 */
import type {
    User,
    RegisterRequest,
    Token,
    Exercise,
    ExerciseProgress,
    CodeRunResult,
    TutorMessage,
    TutorResponse,
    HintRequest,
    HintResponse,
    TaskDecomposition,
    LearningSession,
    ProgressSummary,
} from '../types';

const API_BASE = '/api';

class ApiError extends Error {
    status: number;

    constructor(status: number, message: string) {
        super(message);
        this.name = 'ApiError';
        this.status = status;
    }
}

async function request<T>(
    endpoint: string,
    options: RequestInit = {}
): Promise<T> {
    console.log(`[PyPal API] ${options.method || 'GET'} ${endpoint}`);
    const token = localStorage.getItem('access_token');

    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...((options.headers as Record<string, string>) || {}),
    };

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Request failed' }));
        throw new ApiError(response.status, error.detail || 'Request failed');
    }

    if (response.status === 204) {
        return {} as T;
    }

    return response.json();
}

/* Auth API */
export const authApi = {
    register: (data: RegisterRequest) =>
        request<{ status: string; access_token?: string; consent_token?: string }>(
            '/auth/register',
            { method: 'POST', body: JSON.stringify(data) }
        ),

    login: async (username: string, password: string): Promise<Token> => {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({ detail: 'Login failed' }));
            throw new ApiError(response.status, error.detail);
        }

        return response.json();
    },

    getMe: () => request<User>('/auth/me'),

    updatePreferences: (data: Partial<User>) =>
        request<User>('/auth/me', { method: 'PATCH', body: JSON.stringify(data) }),
};

/* Exercise API */
export const exerciseApi = {
    list: (gradeLevel?: number) => {
        const params = gradeLevel ? `?grade_level=${gradeLevel}` : '';
        return request<Exercise[]>(`/exercises/${params}`);
    },

    get: (id: number) => request<Exercise>(`/exercises/${id}`),

    runCode: (exerciseId: number, code: string) =>
        request<CodeRunResult>(`/exercises/${exerciseId}/run`, {
            method: 'POST',
            body: JSON.stringify({ code }),
        }),

    testCode: (exerciseId: number, code: string) =>
        request<CodeRunResult>(`/exercises/${exerciseId}/test`, {
            method: 'POST',
            body: JSON.stringify({ code }),
        }),

    getProgress: (exerciseId: number) =>
        request<ExerciseProgress>(`/exercises/${exerciseId}/progress`),

    updateProgress: (exerciseId: number, step: number) =>
        request<{ status: string }>(`/exercises/${exerciseId}/progress?step=${step}`, {
            method: 'PATCH',
        }),
};

/* Tutor API */
export const tutorApi = {
    sendMessage: (data: TutorMessage) =>
        request<TutorResponse>('/tutor/message', {
            method: 'POST',
            body: JSON.stringify(data),
        }),

    getHint: (data: HintRequest) =>
        request<HintResponse>('/tutor/hint', {
            method: 'POST',
            body: JSON.stringify(data),
        }),

    decomposeTask: (task: string, interests?: string[]) =>
        request<TaskDecomposition>('/tutor/decompose', {
            method: 'POST',
            body: JSON.stringify({ task, student_interests: interests }),
        }),

    testConnection: () => request<{ status: string; model: string }>('/tutor/test'),
};

/* Progress API */
export const progressApi = {
    getSummary: () => request<ProgressSummary>('/progress/summary'),

    getSessions: (limit = 10) =>
        request<LearningSession[]>(`/progress/sessions?limit=${limit}`),

    startSession: (exerciseId?: number) =>
        request<{ id: number; started_at: string }>('/progress/sessions', {
            method: 'POST',
            body: JSON.stringify({ exercise_id: exerciseId }),
        }),

    endSession: (sessionId: number) =>
        request<{ id: number; duration_minutes: number }>(`/progress/sessions/${sessionId}/end`, {
            method: 'POST',
        }),

    logBreak: (sessionId: number, durationSeconds: number) =>
        request<{ status: string }>(`/progress/sessions/${sessionId}/break?duration_seconds=${durationSeconds}`, {
            method: 'POST',
        }),

    getStreak: () => request<{ current_streak: number; total_points: number }>('/progress/streak'),
};

/* Admin API */
export const adminApi = {
    seedExercises: () =>
        request<{ message: string }>('/admin/seed-exercises', { method: 'POST' }),
};

export { ApiError };
