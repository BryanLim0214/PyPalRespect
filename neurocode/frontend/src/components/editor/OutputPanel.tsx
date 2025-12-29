/**
 * OutputPanel component for displaying code execution results.
 */
import type { CodeRunResult, TestResult } from '../../types';
import clsx from 'clsx';

interface OutputPanelProps {
    result: CodeRunResult | null;
    isRunning: boolean;
}

export function OutputPanel({ result, isRunning }: OutputPanelProps) {
    if (isRunning) {
        return (
            <div className="card">
                <div className="flex items-center gap-2 text-[var(--color-text-secondary)]">
                    <div className="w-4 h-4 border-2 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
                    <span>Running your code...</span>
                </div>
            </div>
        );
    }

    if (!result) {
        return (
            <div className="card">
                <p className="text-[var(--color-text-muted)]">
                    Click "Run Code" to see the output here.
                </p>
            </div>
        );
    }

    return (
        <div className="card space-y-4">
            <div className="flex items-center justify-between">
                <h3 className="font-semibold text-lg">Output</h3>
                <span
                    className={clsx(
                        'px-2 py-1 text-sm rounded font-medium',
                        result.success
                            ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 border border-green-200 dark:border-green-800'
                            : 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200 border border-red-200 dark:border-red-800'
                    )}
                >
                    {result.success ? 'Success' : 'Error'}
                </span>
            </div>

            {/* Output text */}
            {result.output && (
                <pre className="bg-[var(--color-bg-secondary)] p-4 rounded-lg overflow-x-auto text-sm font-mono whitespace-pre-wrap">
                    {result.output}
                </pre>
            )}

            {/* Error message - softer styling for ADHD (less jarring) */}
            {result.error && (
                <div className="bg-red-50 dark:bg-red-950 border border-red-200 dark:border-red-800 rounded-lg p-4">
                    <div className="flex items-start gap-2">
                        <svg className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                        </svg>
                        <p className="text-red-800 dark:text-red-200 font-mono text-sm whitespace-pre-wrap">
                            {result.error}
                        </p>
                    </div>
                </div>
            )}

            {/* Test results */}
            {result.test_results && result.test_results.length > 0 && (
                <div className="space-y-2">
                    <h4 className="font-medium">Test Results</h4>
                    {result.test_results.map((test: TestResult) => (
                        <TestResultItem key={test.test_number} test={test} />
                    ))}
                </div>
            )}

            {/* Execution time */}
            <p className="text-xs text-[var(--color-text-muted)]">
                Execution time: {result.execution_time_ms}ms
            </p>
        </div>
    );
}

function TestResultItem({ test }: { test: TestResult }) {
    return (
        <div
            className={clsx(
                'p-3 rounded-lg border',
                test.passed
                    ? 'bg-[var(--color-success)] bg-opacity-5 border-[var(--color-success)]'
                    : 'bg-[var(--color-error)] bg-opacity-5 border-[var(--color-error)]'
            )}
        >
            <div className="flex items-center gap-2">
                <span
                    className={clsx(
                        'font-medium',
                        test.passed ? 'text-[var(--color-success)]' : 'text-[var(--color-error)]'
                    )}
                >
                    Test {test.test_number}: {test.passed ? 'Passed' : 'Failed'}
                </span>
            </div>
            {!test.passed && (
                <div className="mt-2 text-sm space-y-1">
                    <p>
                        <span className="text-[var(--color-text-secondary)]">Expected:</span>{' '}
                        <code className="bg-[var(--color-bg-secondary)] px-1 rounded">{test.expected}</code>
                    </p>
                    <p>
                        <span className="text-[var(--color-text-secondary)]">Got:</span>{' '}
                        <code className="bg-[var(--color-bg-secondary)] px-1 rounded">{test.actual}</code>
                    </p>
                </div>
            )}
        </div>
    );
}
