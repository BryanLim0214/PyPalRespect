/**
 * Dashboard page showing exercises and progress.
 */
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../stores';
import { exerciseApi, progressApi } from '../services/api';
import type { Exercise, ProgressSummary } from '../types';
import clsx from 'clsx';

export function DashboardPage() {
    const { user } = useAuthStore();
    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [progress, setProgress] = useState<ProgressSummary | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(() => {
        async function loadData() {
            try {
                const [exerciseList, progressData] = await Promise.all([
                    exerciseApi.list(user?.grade_level),
                    progressApi.getSummary(),
                ]);
                setExercises(exerciseList);
                setProgress(progressData);
            } catch (error) {
                console.error('Failed to load dashboard data:', error);
            } finally {
                setIsLoading(false);
            }
        }
        loadData();
    }, [user?.grade_level]);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="w-8 h-8 border-4 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    return (
        <div className="space-y-8">
            {/* Welcome section */}
            <div>
                <h1 className="text-2xl font-bold">Welcome back, {user?.username}</h1>
                <p className="text-[var(--color-text-secondary)]">
                    Ready to learn some Python?
                </p>
            </div>

            {/* Progress overview */}
            {progress && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <StatCard label="Completed" value={progress.exercises_completed} />
                    <StatCard label="Total Points" value={progress.total_points} />
                    <StatCard label="Hints Used" value={progress.total_hints_used} />
                    <StatCard label="Day Streak" value={progress.current_streak} />
                </div>
            )}

            {/* Exercises grid */}
            <div>
                <h2 className="text-xl font-semibold mb-4">Exercises</h2>

                {exercises.length === 0 ? (
                    <div className="card text-center py-8">
                        <p className="text-[var(--color-text-secondary)] mb-4">
                            No exercises available yet.
                        </p>
                        <p className="text-sm text-[var(--color-text-muted)]">
                            Ask your teacher to add some exercises, or check back later.
                        </p>
                    </div>
                ) : (
                    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                        {exercises.map((exercise) => (
                            <ExerciseCard key={exercise.id} exercise={exercise} />
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
}

function StatCard({ label, value }: { label: string; value: number }) {
    return (
        <div className="card text-center">
            <p className="text-3xl font-bold text-[var(--color-primary)]">{value}</p>
            <p className="text-sm text-[var(--color-text-secondary)]">{label}</p>
        </div>
    );
}

function ExerciseCard({ exercise }: { exercise: Exercise }) {
    const difficultyColors = [
        'bg-[var(--color-success)]',
        'bg-[var(--color-success)]',
        'bg-[var(--color-warning)]',
        'bg-[var(--color-warning)]',
        'bg-[var(--color-error)]',
    ];

    // Parse interest tags if available
    const interestTags: string[] = exercise.interest_tags
        ? JSON.parse(exercise.interest_tags)
        : [];

    return (
        <Link to={`/exercise/${exercise.id}`} className="card hover:border-[var(--color-primary)] transition-colors">
            <div className="flex items-start justify-between mb-2">
                <h3 className="font-semibold">{exercise.title}</h3>
                <span
                    className={clsx(
                        'px-2 py-0.5 text-xs font-medium text-white rounded',
                        difficultyColors[exercise.difficulty - 1]
                    )}
                >
                    Level {exercise.difficulty}
                </span>
            </div>
            <p className="text-sm text-[var(--color-text-secondary)] mb-3 line-clamp-2">
                {exercise.description}
            </p>
            {/* Interest tags */}
            {interestTags.length > 0 && (
                <div className="flex flex-wrap gap-1 mb-3">
                    {interestTags.slice(0, 3).map((tag) => (
                        <span
                            key={tag}
                            className="px-2 py-0.5 text-xs bg-[var(--color-bg-secondary)] text-[var(--color-text-muted)] rounded-full"
                        >
                            {tag}
                        </span>
                    ))}
                </div>
            )}
            <div className="flex items-center justify-between text-xs text-[var(--color-text-secondary)] font-medium">
                <span>{exercise.estimated_minutes} min</span>
                <span>{exercise.step_count} steps</span>
                <span className="capitalize">{exercise.concept}</span>
            </div>
        </Link>
    );
}
