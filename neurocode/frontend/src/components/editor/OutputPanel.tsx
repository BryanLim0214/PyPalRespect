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
                <div className="space-y-3">
                    <div className="flex items-center justify-between">
                        <h4 className="font-semibold text-base">Test Results</h4>
                        <span className="text-sm text-[var(--color-text-secondary)]">
                            {result.test_results.filter((t: TestResult) => t.passed).length}/{result.test_results.length} passed
                        </span>
                    </div>
                    <div className="space-y-2">
                        {result.test_results.map((test: TestResult) => (
                            <TestResultItem key={test.test_number} test={test} />
                        ))}
                    </div>
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
                'p-4 rounded-lg border-l-4',
                test.passed
                    ? 'bg-green-50 dark:bg-green-950/30 border-green-500'
                    : 'bg-amber-50 dark:bg-amber-950/30 border-amber-500'
            )}
        >
            <div className="flex items-center gap-2 mb-2">
                {test.passed ? (
                    <svg className="w-5 h-5 text-green-600 dark:text-green-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                ) : (
                    <svg className="w-5 h-5 text-amber-600 dark:text-amber-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                )}
                <span
                    className={clsx(
                        'font-semibold',
                        test.passed 
                            ? 'text-green-700 dark:text-green-300' 
                            : 'text-amber-700 dark:text-amber-300'
                    )}
                >
                    Test {test.test_number}: {test.passed ? 'Passed' : 'Not quite right'}
                </span>
            </div>
            {!test.passed && (
                <div className="ml-7 space-y-2 text-sm">
                    <div className="flex items-start gap-2">
                        <span className="text-[var(--color-text-secondary)] font-medium min-w-[70px]">Expected:</span>
                        <code className="bg-white dark:bg-gray-800 px-2 py-1 rounded border border-gray-200 dark:border-gray-700 font-mono text-green-700 dark:text-green-400 break-all">
                            {test.expected}
                        </code>
                    </div>
                    <div className="flex items-start gap-2">
                        <span className="text-[var(--color-text-secondary)] font-medium min-w-[70px]">Got:</span>
                        <code className="bg-white dark:bg-gray-800 px-2 py-1 rounded border border-gray-200 dark:border-gray-700 font-mono text-amber-700 dark:text-amber-400 break-all">
                            {test.actual || '(empty)'}
                        </code>
                    </div>
                </div>
            )}
        </div>
    );
}
