/**
 * StepProgress component for micro-task tracking.
 */
import type { Step } from '../../types';
import clsx from 'clsx';

interface StepProgressProps {
    steps: Step[];
    currentStep: number;
    onStepClick?: (stepNumber: number) => void;
}

export function StepProgress({ steps, currentStep, onStepClick }: StepProgressProps) {
    return (
        <div className="card">
            <h3 className="font-semibold mb-4">Your Progress</h3>

            {/* Progress bar */}
            <div className="mb-4">
                <div className="flex justify-between text-xs text-[var(--color-text-secondary)] mb-1">
                    <span>
                        Step {Math.min(currentStep, steps.length)} of {steps.length}
                    </span>
                    <span>{Math.round((currentStep / steps.length) * 100)}%</span>
                </div>
                <div className="progress-bar">
                    <div
                        className="progress-fill"
                        style={{ width: `${(currentStep / steps.length) * 100}%` }}
                    />
                </div>
            </div>

            {/* Step list */}
            <div className="space-y-2">
                {steps.map((step) => {
                    const isComplete = step.number < currentStep;
                    const isCurrent = step.number === currentStep;
                    const isPending = step.number > currentStep;

                    return (
                        <button
                            key={step.number}
                            onClick={() => onStepClick?.(step.number)}
                            disabled={isPending}
                            className={clsx(
                                'w-full text-left p-3 rounded-lg border transition-colors',
                                isComplete && 'bg-emerald-50 dark:bg-emerald-950 border-emerald-200 dark:border-emerald-800',
                                isCurrent && 'bg-blue-600 border-blue-600',
                                isPending && 'bg-[var(--color-bg-secondary)] border-transparent opacity-60',
                                !isPending && 'cursor-pointer hover:opacity-90'
                            )}
                        >
                            <div className="flex items-start gap-3">
                                {/* Step indicator */}
                                <div
                                    className={clsx(
                                        'w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0',
                                        isComplete && 'bg-emerald-500 text-white',
                                        isCurrent && 'bg-white text-blue-600',
                                        isPending && 'bg-[var(--color-bg-secondary)] text-[var(--color-text-muted)]'
                                    )}
                                >
                                    {isComplete ? (
                                        <svg className="w-3 h-3" fill="currentColor" viewBox="0 0 20 20">
                                            <path
                                                fillRule="evenodd"
                                                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                                                clipRule="evenodd"
                                            />
                                        </svg>
                                    ) : (
                                        step.number
                                    )}
                                </div>

                                {/* Step content */}
                                <div className="flex-1 min-w-0">
                                    <p
                                        className={clsx(
                                            'font-medium text-sm',
                                            isComplete && 'text-emerald-700 dark:text-emerald-300',
                                            isCurrent && 'text-white',
                                            isPending && 'text-[var(--color-text-muted)]'
                                        )}
                                    >
                                        {step.title}
                                    </p>
                                    {isCurrent && (
                                        <p className="text-xs text-blue-100 mt-1">
                                            {step.instruction}
                                        </p>
                                    )}
                                </div>

                                {/* Checkpoint indicator */}
                                {step.checkpoint && (
                                    <span className={clsx(
                                        'text-xs px-2 py-0.5 rounded',
                                        isCurrent ? 'bg-white/20 text-white' : 'bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300'
                                    )}>
                                        Checkpoint
                                    </span>
                                )}
                            </div>
                        </button>
                    );
                })}
            </div>
        </div>
    );
}
