/**
 * Focus timer store for ADHD-friendly break reminders.
 */
import { create } from 'zustand';

interface TimerState {
    isRunning: boolean;
    elapsedSeconds: number;
    breakIntervalMinutes: number;
    sessionLengthMinutes: number;
    showBreakReminder: boolean;
    breaksTaken: number;

    start: () => void;
    pause: () => void;
    reset: () => void;
    tick: () => void;
    setBreakInterval: (minutes: number) => void;
    setSessionLength: (minutes: number) => void;
    dismissBreakReminder: () => void;
    takeBreak: () => void;
}

export const useTimerStore = create<TimerState>((set, get) => ({
    isRunning: false,
    elapsedSeconds: 0,
    breakIntervalMinutes: 20, // Research-based default
    sessionLengthMinutes: 30,
    showBreakReminder: false,
    breaksTaken: 0,

    start: () => set({ isRunning: true }),

    pause: () => set({ isRunning: false }),

    reset: () =>
        set({
            elapsedSeconds: 0,
            showBreakReminder: false,
            breaksTaken: 0,
        }),

    tick: () => {
        const { isRunning, elapsedSeconds, breakIntervalMinutes, showBreakReminder } = get();

        if (!isRunning) return;

        const newElapsed = elapsedSeconds + 1;
        const breakIntervalSeconds = breakIntervalMinutes * 60;

        // Check if it's time for a break reminder
        const shouldShowBreak =
            !showBreakReminder &&
            newElapsed > 0 &&
            newElapsed % breakIntervalSeconds === 0;

        set({
            elapsedSeconds: newElapsed,
            showBreakReminder: shouldShowBreak ? true : showBreakReminder,
        });
    },

    setBreakInterval: (minutes) => set({ breakIntervalMinutes: minutes }),

    setSessionLength: (minutes) => set({ sessionLengthMinutes: minutes }),

    dismissBreakReminder: () => set({ showBreakReminder: false }),

    takeBreak: () =>
        set((state) => ({
            showBreakReminder: false,
            breaksTaken: state.breaksTaken + 1,
        })),
}));

// Timer interval handler
let timerInterval: ReturnType<typeof setInterval> | null = null;

export function startTimerInterval() {
    if (timerInterval) return;

    timerInterval = setInterval(() => {
        useTimerStore.getState().tick();
    }, 1000);
}

export function stopTimerInterval() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}
