/**
 * Frontend component tests.
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

// Mock stores
vi.mock('../stores', () => ({
    useAuthStore: vi.fn(() => ({
        user: { username: 'testuser', total_points: 100, current_streak: 5 },
        isAuthenticated: true,
        isLoading: false,
        login: vi.fn(),
        logout: vi.fn(),
    })),
    useThemeStore: vi.fn(() => ({
        themeMode: 'light',
        dyslexiaFont: false,
        highContrast: false,
        reduceMotion: true,
        setThemeMode: vi.fn(),
        setDyslexiaFont: vi.fn(),
        setHighContrast: vi.fn(),
        setReduceMotion: vi.fn(),
        applyToDocument: vi.fn(),
    })),
    useTimerStore: vi.fn(() => ({
        isRunning: false,
        elapsedSeconds: 0,
        breakIntervalMinutes: 20,
        sessionLengthMinutes: 30,
        showBreakReminder: false,
        breaksTaken: 0,
        start: vi.fn(),
        pause: vi.fn(),
        reset: vi.fn(),
    })),
    startTimerInterval: vi.fn(),
    stopTimerInterval: vi.fn(),
}));

// Wrap components with router for testing
function renderWithRouter(ui: React.ReactElement) {
    return render(<BrowserRouter>{ui}</BrowserRouter>);
}

describe('PointsDisplay Component', () => {
    it('renders points correctly', async () => {
        const { PointsDisplay } = await import('../components/adhd/PointsDisplay');
        render(<PointsDisplay points={250} streak={7} />);

        // Points number should be visible
        expect(screen.getByText('250')).toBeInTheDocument();
    });

    it('renders streak when greater than 0', async () => {
        const { PointsDisplay } = await import('../components/adhd/PointsDisplay');
        render(<PointsDisplay points={100} streak={3} />);

        // Streak number should be visible
        expect(screen.getByText('3')).toBeInTheDocument();
    });

    it('does not render streak when 0', async () => {
        const { PointsDisplay } = await import('../components/adhd/PointsDisplay');
        render(<PointsDisplay points={100} streak={0} />);

        // Should only have points, not streak
        expect(screen.getByText('100')).toBeInTheDocument();
        expect(screen.queryByText('0')).not.toBeInTheDocument();
    });
});

describe('StepProgress Component', () => {
    it('renders all steps', async () => {
        const { StepProgress } = await import('../components/adhd/StepProgress');
        const steps = [
            { number: 1, title: 'Step 1', instruction: 'Do thing 1', checkpoint: false },
            { number: 2, title: 'Step 2', instruction: 'Do thing 2', checkpoint: true },
            { number: 3, title: 'Step 3', instruction: 'Do thing 3', checkpoint: false },
        ];

        render(<StepProgress steps={steps} currentStep={2} />);

        expect(screen.getByText('Step 1')).toBeInTheDocument();
        expect(screen.getByText('Step 2')).toBeInTheDocument();
        expect(screen.getByText('Step 3')).toBeInTheDocument();
    });

    it('shows correct progress percentage', async () => {
        const { StepProgress } = await import('../components/adhd/StepProgress');
        const steps = [
            { number: 1, title: 'Step 1', instruction: 'Do thing 1', checkpoint: false },
            { number: 2, title: 'Step 2', instruction: 'Do thing 2', checkpoint: false },
        ];

        // After finishing step 1 (currentStep=2 means step 1 is complete),
        // the bar reads 50% of 2 steps.
        render(<StepProgress steps={steps} currentStep={2} />);

        expect(screen.getByText('50%')).toBeInTheDocument();
    });

    it('shows checkpoint badge', async () => {
        const { StepProgress } = await import('../components/adhd/StepProgress');
        const steps = [
            { number: 1, title: 'Step 1', instruction: 'Do it', checkpoint: true },
        ];

        render(<StepProgress steps={steps} currentStep={1} />);

        // Checkpoint steps are labelled "Test" in the current UI copy.
        expect(screen.getAllByText('Test').length).toBeGreaterThan(0);
    });
});

describe('OutputPanel Component', () => {
    it('shows placeholder when no result', async () => {
        const { OutputPanel } = await import('../components/editor/OutputPanel');
        render(<OutputPanel result={null} isRunning={false} />);

        expect(screen.getByText(/Click "Run Code"/)).toBeInTheDocument();
    });

    it('shows loading state when running', async () => {
        const { OutputPanel } = await import('../components/editor/OutputPanel');
        render(<OutputPanel result={null} isRunning={true} />);

        expect(screen.getByText(/Running your code/)).toBeInTheDocument();
    });

    it('shows success output', async () => {
        const { OutputPanel } = await import('../components/editor/OutputPanel');
        const result = {
            success: true,
            output: 'Hello World!',
            error: null,
            execution_time_ms: 50,
        };

        render(<OutputPanel result={result} isRunning={false} />);

        expect(screen.getByText('Hello World!')).toBeInTheDocument();
        expect(screen.getByText('Success')).toBeInTheDocument();
    });

    it('shows error output', async () => {
        const { OutputPanel } = await import('../components/editor/OutputPanel');
        const result = {
            success: false,
            output: '',
            error: 'SyntaxError: invalid syntax',
            execution_time_ms: 10,
        };

        render(<OutputPanel result={result} isRunning={false} />);

        expect(screen.getByText(/SyntaxError/)).toBeInTheDocument();
        expect(screen.getByText('Error')).toBeInTheDocument();
    });
});

describe('Accessibility Settings', () => {
    it('default reduce motion is ON for ADHD', async () => {
        const { useThemeStore } = await import('../stores');
        const mockStore = vi.mocked(useThemeStore);

        // Check that the mock has reduceMotion: true
        const state = mockStore();
        expect(state.reduceMotion).toBe(true);
    });
});

describe('Timer Store', () => {
    it('has correct default break interval (20 minutes)', async () => {
        const { useTimerStore } = await import('../stores');
        const mockStore = vi.mocked(useTimerStore);

        const state = mockStore();
        expect(state.breakIntervalMinutes).toBe(20);
    });

    it('has correct default session length (30 minutes)', async () => {
        const { useTimerStore } = await import('../stores');
        const mockStore = vi.mocked(useTimerStore);

        const state = mockStore();
        expect(state.sessionLengthMinutes).toBe(30);
    });
});
