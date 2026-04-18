/**
 * Exercise page with code editor, tutor, and step tracking.
 */
import { useEffect, useState, useMemo } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { exerciseApi, tutorApi } from '../services/api';
import { useAuthStore } from '../stores';
import { CodeEditor, OutputPanel } from '../components/editor';
import { TutorChat, HintPanel } from '../components/tutor';
import { StepProgress, FocusTimer } from '../components/adhd';
import type { Exercise, CodeRunResult, Step, TaskDecomposition } from '../types';

export function ExercisePage() {
    const { id } = useParams<{ id: string }>();
    const navigate = useNavigate();
    const { user } = useAuthStore();

    const [exercise, setExercise] = useState<Exercise | null>(null);
    const [code, setCode] = useState('');
    const [result, setResult] = useState<CodeRunResult | null>(null);
    const [isRunning, setIsRunning] = useState(false);
    const [steps, setSteps] = useState<Step[]>([]);
    const [currentStep, setCurrentStep] = useState(1);
    const [_hintsUsed, setHintsUsed] = useState(0);
    const [isLoading, setIsLoading] = useState(true);

    // Get the current step object
    const currentStepObj = useMemo(() => {
        return steps.find(s => s.number === currentStep);
    }, [steps, currentStep]);

    // Check if current step is a checkpoint (requires code testing)
    const isCheckpointStep = currentStepObj?.checkpoint ?? false;

    useEffect(() => {
        async function loadExercise() {
            if (!id) return;

            try {
                const exerciseData = await exerciseApi.get(parseInt(id));
                setExercise(exerciseData);
                setCode(exerciseData.starter_code || '# Write your code here\n');

                // Parse steps if available, otherwise decompose the task
                if (exerciseData.steps) {
                    try {
                        const parsed = JSON.parse(exerciseData.steps);
                        setSteps(parsed);
                    } catch {
                        await decomposeTask(exerciseData.description);
                    }
                } else {
                    await decomposeTask(exerciseData.description);
                }

                // Load saved progress
                try {
                    const progress = await exerciseApi.getProgress(parseInt(id));
                    if (progress.last_code) setCode(progress.last_code);
                    if (progress.current_step) setCurrentStep(progress.current_step);
                    if (progress.hints_used) setHintsUsed(progress.hints_used);
                } catch {
                    // No saved progress
                }
            } catch (error) {
                console.error('Failed to load exercise:', error);
                navigate('/dashboard');
            } finally {
                setIsLoading(false);
            }
        }

        loadExercise();
    }, [id, navigate]);

    async function decomposeTask(task: string) {
        try {
            // Get user interests for personalized decomposition
            const userInterests = user?.interests ? JSON.parse(user.interests) : undefined;
            const decomposition: TaskDecomposition = await tutorApi.decomposeTask(task, userInterests);
            setSteps(decomposition.steps);
        } catch {
            // Fallback steps
            setSteps([
                { number: 1, title: 'Read the problem', instruction: 'Read the exercise description carefully.', checkpoint: false },
                { number: 2, title: 'Write your code', instruction: 'Write the solution code.', checkpoint: true },
                { number: 3, title: 'Test it', instruction: 'Run your code and check the output.', checkpoint: true },
            ]);
        }
    }

    async function handleRun() {
        if (!exercise) return;

        setIsRunning(true);
        try {
            const runResult = await exerciseApi.runCode(exercise.id, code);
            setResult(runResult);
            // Don't advance progress on Run Code - only on passing tests or manual completion
        } catch (error) {
            setResult({
                success: false,
                output: '',
                error: 'Failed to run code. Please try again.',
                execution_time_ms: 0,
            });
        } finally {
            setIsRunning(false);
        }
    }

    async function handleTest() {
        if (!exercise) return;

        setIsRunning(true);
        try {
            const testResult = await exerciseApi.testCode(exercise.id, code);
            setResult(testResult);

            // For creative exercises (no test_results), allow progression if code ran successfully
            const isCreativeExercise = !testResult.test_results || testResult.test_results.length === 0;
            const allTestsPassed = testResult.test_results && 
                testResult.test_results.length > 0 &&
                testResult.test_results.every((t) => t.passed);

            // Advance if: (tests pass OR creative exercise ran successfully) AND checkpoint step
            const shouldAdvance = (allTestsPassed || (isCreativeExercise && testResult.success)) && 
                isCheckpointStep && 
                currentStep < steps.length;

            if (shouldAdvance) {
                const nextStep = currentStep + 1;
                setCurrentStep(nextStep);
                await exerciseApi.updateProgress(exercise.id, nextStep);
            }
        } catch (error) {
            setResult({
                success: false,
                output: '',
                error: 'Failed to run tests. Please try again.',
                execution_time_ms: 0,
            });
        } finally {
            setIsRunning(false);
        }
    }

    // Manually advance to next step (for non-checkpoint steps like reading/understanding)
    async function handleNextStep() {
        if (!exercise || currentStep >= steps.length) return;

        const nextStep = currentStep + 1;
        setCurrentStep(nextStep);
        await exerciseApi.updateProgress(exercise.id, nextStep);
    }

    // Reset exercise progress
    async function handleReset() {
        if (!exercise) return;
        
        const confirmed = window.confirm(
            'Reset your progress on this exercise?\n\nThis will:\n• Reset to Step 1\n• Clear your code\n• Reset hints used\n\nYou can start fresh!'
        );
        
        if (!confirmed) return;

        try {
            await exerciseApi.resetProgress(exercise.id);
            // Reset local state
            setCurrentStep(1);
            setCode(exercise.starter_code || '# Write your code here\n');
            setResult(null);
            setHintsUsed(0);
        } catch (error) {
            console.error('Failed to reset progress:', error);
        }
    }

    // Check if the exercise is complete
    const isExerciseComplete = currentStep > steps.length;
    
    // Check if exercise has tests
    const hasTests = exercise?.test_cases && exercise.test_cases !== 'null';

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="w-8 h-8 border-4 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (!exercise) {
        return null;
    }

    return (
        <div className="space-y-6 overflow-x-hidden">
            {/* Header */}
            <div className="flex items-start justify-between gap-4">
                <div className="flex-1">
                    <h1 className="text-2xl font-bold">{exercise.title}</h1>
                    <p className="text-[var(--color-text-secondary)]">{exercise.description}</p>
                    <div className="flex items-center gap-2 mt-2">
                        <span className="text-xs px-2 py-1 rounded bg-[var(--color-bg-secondary)] text-[var(--color-text-muted)]">
                            Difficulty: {'⭐'.repeat(exercise.difficulty)}
                        </span>
                        <span className="text-xs px-2 py-1 rounded bg-[var(--color-bg-secondary)] text-[var(--color-text-muted)]">
                            ~{exercise.estimated_minutes} min
                        </span>
                        {!hasTests && (
                            <span className="text-xs px-2 py-1 rounded bg-purple-100 dark:bg-purple-900 text-purple-700 dark:text-purple-300">
                                Creative Exercise
                            </span>
                        )}
                    </div>
                </div>
                <div className="flex items-center gap-2">
                    <button 
                        onClick={handleReset}
                        className="btn btn-secondary text-sm flex items-center gap-1 border-amber-400 hover:bg-amber-50 dark:hover:bg-amber-950"
                        title="Reset progress and start over"
                    >
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                        Reset
                    </button>
                    <button onClick={() => navigate('/dashboard')} className="btn btn-secondary text-sm">
                        Back to Dashboard
                    </button>
                </div>
            </div>

            {/* Main content grid - more compact */}
            <div className="grid gap-4 lg:grid-cols-[1fr,320px]">
                {/* Left column - Editor */}
                <div className="space-y-3">
                    <CodeEditor value={code} onChange={setCode} height="350px" />

                    <div className="flex gap-2">
                        <button
                            type="button"
                            onClick={handleRun}
                            disabled={isRunning}
                            className="btn btn-primary flex-1"
                        >
                            {isRunning ? 'Running...' : 'Run Code'}
                        </button>
                        <button
                            type="button"
                            onClick={handleTest}
                            disabled={isRunning}
                            className="btn btn-secondary flex-1 border-gray-400 hover:bg-gray-100 dark:border-gray-600 dark:hover:bg-gray-800"
                        >
                            Run Tests
                        </button>
                    </div>

                    {/* Step guidance - show what to do based on step type */}
                    {currentStepObj && !isExerciseComplete && (
                        <div className="p-4 rounded-lg border-2 border-dashed border-[var(--color-border)] bg-[var(--color-bg-secondary)]">
                            <div className="flex items-start justify-between gap-4">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className="text-xs font-semibold text-[var(--color-primary)] uppercase tracking-wide">
                                            Step {currentStep}
                                        </span>
                                        {isCheckpointStep && (
                                            <span className="text-xs px-2 py-0.5 rounded-full bg-amber-100 dark:bg-amber-900 text-amber-700 dark:text-amber-300">
                                                Checkpoint - Run Tests to advance
                                            </span>
                                        )}
                                    </div>
                                    <p className="font-semibold text-base">{currentStepObj.title}</p>
                                    <p className="text-sm text-[var(--color-text-secondary)] mt-1">
                                        {currentStepObj.instruction}
                                    </p>
                                    {currentStepObj.code_hint && (
                                        <code className="block mt-2 p-2 bg-gray-800 text-green-400 text-sm font-mono rounded">
                                            {currentStepObj.code_hint}
                                        </code>
                                    )}
                                </div>
                                {/* Show "I understand" button for non-checkpoint steps */}
                                {!isCheckpointStep && (
                                    <button
                                        type="button"
                                        onClick={handleNextStep}
                                        className="btn bg-emerald-600 hover:bg-emerald-700 text-white flex-shrink-0 flex items-center gap-2"
                                    >
                                        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                        </svg>
                                        Got it, Next Step
                                    </button>
                                )}
                            </div>
                        </div>
                    )}

                    {/* Completion message */}
                    {isExerciseComplete && (
                        <div className="p-4 rounded-lg bg-emerald-50 dark:bg-emerald-950 border border-emerald-200 dark:border-emerald-800">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-full bg-emerald-500 flex items-center justify-center">
                                    <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                                    </svg>
                                </div>
                                <div>
                                    <p className="font-semibold text-emerald-700 dark:text-emerald-300">
                                        Exercise Complete!
                                    </p>
                                    <p className="text-sm text-emerald-600 dark:text-emerald-400">
                                        Great job finishing all the steps. Try running the tests to verify your solution!
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}

                    <div className="min-h-[200px]">
                        <OutputPanel result={result} isRunning={isRunning} />
                    </div>
                </div>

                {/* Right column - Sidebar (compact) */}
                <div className="space-y-3">
                    <StepProgress steps={steps} currentStep={currentStep} />
                    <FocusTimer />
                    <HintPanel
                        code={code}
                        errorMessage={result?.error || undefined}
                        onHintUsed={() => setHintsUsed((h) => h + 1)}
                        currentStep={currentStepObj}
                    />
                    <TutorChat
                        currentStep={currentStep}
                        currentCode={code}
                        currentStepObj={currentStepObj}
                    />
                </div>
            </div>
        </div>
    );
}
