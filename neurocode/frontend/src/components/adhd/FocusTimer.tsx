/**
 * FocusTimer component for ADHD break reminders.
 */
import { useEffect } from 'react';
import { useTimerStore, startTimerInterval, stopTimerInterval } from '../../stores';

export function FocusTimer() {
    const {
        isRunning,
        elapsedSeconds,
        breakIntervalMinutes,
        sessionLengthMinutes,
        showBreakReminder,
        breaksTaken,
        start,
        pause,
        reset,
        dismissBreakReminder,
        takeBreak,
    } = useTimerStore();

    useEffect(() => {
        startTimerInterval();
        return () => stopTimerInterval();
    }, []);

    const formatTime = (seconds: number) => {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    };

    const progress = Math.min(
        (elapsedSeconds / (sessionLengthMinutes * 60)) * 100,
        100
    );

    const nextBreakIn = Math.max(
        0,
        breakIntervalMinutes * 60 - (elapsedSeconds % (breakIntervalMinutes * 60))
    );

    return (
        <div className="card">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold">Focus Timer</h3>
                <span className="text-2xl font-mono font-bold text-[var(--color-primary)]">
                    {formatTime(elapsedSeconds)}
                </span>
            </div>

            {/* Session progress */}
            <div className="mb-4">
                <div className="flex justify-between text-xs text-[var(--color-text-secondary)] mb-1">
                    <span>Session Progress</span>
                    <span>{Math.round(progress)}%</span>
                </div>
                <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${progress}%` }} />
                </div>
            </div>

            {/* Break info */}
            <div className="text-sm text-[var(--color-text-secondary)] mb-4">
                <p>Next break in: {formatTime(nextBreakIn)}</p>
                <p>Breaks taken: {breaksTaken}</p>
            </div>

            {/* Controls */}
            <div className="flex gap-2">
                {isRunning ? (
                    <button onClick={pause} className="btn btn-secondary flex-1">
                        Pause
                    </button>
                ) : (
                    <button onClick={start} className="btn btn-primary flex-1">
                        {elapsedSeconds > 0 ? 'Resume' : 'Start'}
                    </button>
                )}
                <button onClick={reset} className="btn btn-secondary">
                    Reset
                </button>
            </div>

            {/* Break reminder modal */}
            {showBreakReminder && (
                <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                    <div className="card max-w-md mx-4 text-center">
                        <h2 className="text-xl font-bold mb-4">Time for a Break</h2>
                        <p className="text-[var(--color-text-secondary)] mb-6">
                            You've been coding for {breakIntervalMinutes} minutes. Taking short breaks helps
                            you stay focused and learn better.
                        </p>
                        <div className="space-y-2">
                            <button onClick={takeBreak} className="btn btn-primary w-full">
                                Take a 5-minute break
                            </button>
                            <button
                                onClick={dismissBreakReminder}
                                className="btn btn-secondary w-full"
                            >
                                Keep coding (5 more minutes)
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
