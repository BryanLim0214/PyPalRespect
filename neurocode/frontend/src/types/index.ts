/* User types */
export interface User {
    id: number;
    username: string;
    grade_level: number;
    has_parental_consent: boolean;
    adhd_profile: string | null;
    interests: string | null;
    total_points: number;
    current_streak: number;
    dyslexia_font: boolean;
    high_contrast: boolean;
    reduce_animations: boolean;
    created_at: string;
}

export interface RegisterRequest {
    username: string;
    password: string;
    birth_year: number;
    grade_level: number;
    parent_email?: string;
    interests?: string[];
}

export interface LoginRequest {
    username: string;
    password: string;
}

export interface Token {
    access_token: string;
    token_type: string;
}

/* Exercise types */
export interface Exercise {
    id: number;
    title: string;
    description: string;
    difficulty: number;
    starter_code: string;
    concept: string;
    grade_level: number;
    estimated_minutes: number;
    step_count: number;
    interest_tags: string | null;
    steps: string | null;
}

export interface ExerciseProgress {
    exercise_id: number;
    current_step: number;
    completed: boolean;
    points_earned: number;
    hints_used: number;
    attempt_count: number;
    last_code: string | null;
}

export interface CodeRunResult {
    success: boolean;
    output: string;
    error: string | null;
    execution_time_ms: number;
    test_results?: TestResult[];
}

export interface TestResult {
    test_number: number;
    passed: boolean;
    expected: string;
    actual: string;
    error: string | null;
}

/* Tutor types */
export interface TutorMessage {
    message: string;
    session_id?: number;
    current_step?: number;
    current_code?: string;
}

export interface TutorResponse {
    response: string;
    is_step: boolean;
    step_number: number | null;
    celebration: boolean;
    points_earned: number;
}

export interface HintRequest {
    code: string;
    error_message?: string;
    hint_level: number;
}

export interface HintResponse {
    hint: string;
    hint_level: number;
    next_level_available: boolean;
}

export interface Step {
    number: number;
    title: string;
    instruction: string;
    code_hint?: string;
    checkpoint: boolean;
}

export interface TaskDecomposition {
    steps: Step[];
    estimated_time_minutes: number;
    celebration_message: string;
}

/* Session types */
export interface LearningSession {
    id: number;
    started_at: string;
    ended_at: string | null;
    duration_minutes: number | null;
    completed: boolean;
    hint_requests: number;
    code_runs: number;
    steps_completed: number;
}

export interface ProgressSummary {
    exercises_attempted: number;
    exercises_completed: number;
    total_points: number;
    total_hints_used: number;
    current_streak: number;
}

/* Theme types */
export type ThemeMode = 'light' | 'dark';

export interface AccessibilitySettings {
    dyslexiaFont: boolean;
    highContrast: boolean;
    reduceMotion: boolean;
    themeMode: ThemeMode;
}
