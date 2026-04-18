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
    const completedSteps = Math.min(currentStep - 1, steps.length);
    const progressPercent = Math.round((completedSteps / steps.length) * 100);
    const isAllComplete = currentStep > steps.length;

    return (
        <div className="card">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold">Your Progress</h3>
                {isAllComplete && (
                    <span className="text-xs px-2 py-1 rounded-full bg-emerald-100 dark:bg-emerald-900 text-emerald-700 dark:text-emerald-300 font-medium">
                        Complete!
                    </span>
                )}
            </div>

            {/* Progress bar */}
            <div className="mb-4">
                <div className="flex justify-between text-xs text-[var(--color-text-secondary)] mb-1">
                    <span>
                        {isAllComplete ? 'All steps done!' : `Step ${currentStep} of ${steps.length}`}
                    </span>
                    <span>{progressPercent}%</span>
                </div>
                <div className="progress-bar">
                    <div
                        className={clsx(
                            "progress-fill",
                            isAllComplete && "bg-emerald-500"
                        )}
                        style={{ width: `${progressPercent}%` }}
                    />
                </div>
            </div>

            {/* Step list */}
            <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1 scrollbar-thin">
                {steps.map((step) => {
                    const isComplete = step.number < currentStep;
                    const isCurrent = step.number === currentStep;
                    const isPending = step.number > currentStep;

                    return (
                        <div
                            key={step.number}
                            onClick={() => !isPending && onStepClick?.(step.number)}
                            className={clsx(
                                'w-full text-left p-3 rounded-lg border transition-colors',
                                isComplete && 'bg-emerald-50 dark:bg-emerald-950 border-emerald-200 dark:border-emerald-800',
                                isCurrent && 'bg-blue-600 border-blue-600 shadow-md',
                                isPending && 'bg-[var(--color-bg-secondary)] border-transparent opacity-50',
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
                                        isPending && 'bg-gray-200 dark:bg-gray-700 text-[var(--color-text-muted)]'
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
                                    <div className="flex items-center gap-2">
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
                                    </div>
                                    {isCurrent && step.instruction && (
                                        <p className="text-xs text-blue-100 mt-1 line-clamp-2">
                                            {step.instruction}
                                        </p>
                                    )}
                                </div>

                                {/* Step type indicator */}
                                <div className="flex-shrink-0">
                                    {step.checkpoint ? (
                                        <span className={clsx(
                                            'text-xs px-2 py-0.5 rounded font-medium',
                                            isCurrent 
                                                ? 'bg-white/20 text-white' 
                                                : isComplete
                                                    ? 'bg-emerald-200 dark:bg-emerald-800 text-emerald-700 dark:text-emerald-300'
                                                    : 'bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300'
                                        )}>
                                            Test
                                        </span>
                                    ) : (
                                        <span className={clsx(
                                            'text-xs px-2 py-0.5 rounded font-medium',
                                            isCurrent 
                                                ? 'bg-white/20 text-white' 
                                                : isComplete
                                                    ? 'bg-emerald-200 dark:bg-emerald-800 text-emerald-700 dark:text-emerald-300'
                                                    : 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300'
                                        )}>
                                            Read
                                        </span>
                                    )}
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Legend */}
            <div className="mt-3 pt-3 border-t border-[var(--color-border)] flex items-center gap-4 text-xs text-[var(--color-text-muted)]">
                <div className="flex items-center gap-1">
                    <span className="px-1.5 py-0.5 rounded bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 font-medium">Read</span>
                    <span>= Click "Got it"</span>
                </div>
                <div className="flex items-center gap-1">
                    <span className="px-1.5 py-0.5 rounded bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300 font-medium">Test</span>
                    <span>= Pass tests</span>
                </div>
            </div>
        </div>
    );
}
