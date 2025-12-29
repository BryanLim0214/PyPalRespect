/**
 * Exercise page with code editor, tutor, and step tracking.
 */
import { useEffect, useState } from 'react';
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

            if (runResult.success && currentStep < steps.length) {
                const nextStep = currentStep + 1;
                setCurrentStep(nextStep);
                await exerciseApi.updateProgress(exercise.id, nextStep);
            }
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
        <div className="space-y-6">
            {/* Header */}
            <div className="flex items-start justify-between">
                <div>
                    <h1 className="text-2xl font-bold">{exercise.title}</h1>
                    <p className="text-[var(--color-text-secondary)]">{exercise.description}</p>
                </div>
                <button onClick={() => navigate('/dashboard')} className="btn btn-secondary">
                    Back to Dashboard
                </button>
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
                    />
                    <TutorChat
                        currentStep={currentStep}
                        currentCode={code}
                    />
                </div>
            </div>
        </div>
    );
}
