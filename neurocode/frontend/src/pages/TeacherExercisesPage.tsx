/**
 * Teacher exercise library. Browse existing exercises and seed the curriculum.
 */
import { useEffect, useState } from 'react';
import { adminApi, exerciseApi } from '../services/api';
import type { Exercise } from '../types';

export function TeacherExercisesPage() {
    const [exercises, setExercises] = useState<Exercise[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [seedMessage, setSeedMessage] = useState<string | null>(null);
    const [isSeeding, setIsSeeding] = useState(false);
    const [error, setError] = useState<string | null>(null);

    async function load() {
        setIsLoading(true);
        try {
            const list = await exerciseApi.list();
            setExercises(list);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to load exercises');
        } finally {
            setIsLoading(false);
        }
    }

    useEffect(() => {
        load();
    }, []);

    async function handleSeed() {
        setIsSeeding(true);
        setSeedMessage(null);
        try {
            const result = await adminApi.seedExercises();
            setSeedMessage(result.message);
            await load();
        } catch (err) {
            setSeedMessage(err instanceof Error ? err.message : 'Seed failed');
        } finally {
            setIsSeeding(false);
        }
    }

    return (
        <div className="space-y-6">
            <div className="flex flex-wrap items-start justify-between gap-4">
                <div>
                    <h1 className="text-2xl font-bold">Exercise library</h1>
                    <p className="text-[var(--color-text-secondary)]">
                        Browse the curriculum your students see. New exercises ship as part of PyPal's
                        built-in library.
                    </p>
                </div>
                <button
                    onClick={handleSeed}
                    disabled={isSeeding}
                    className="btn btn-primary"
                >
                    {isSeeding ? 'Loading curriculum…' : 'Load / refresh curriculum'}
                </button>
            </div>

            {seedMessage && (
                <div className="card text-sm">
                    {seedMessage}
                </div>
            )}

            {error && (
                <div className="card border-l-4 border-[var(--color-error)]">
                    <p className="text-[var(--color-error)]">{error}</p>
                </div>
            )}

            {isLoading ? (
                <div className="flex items-center justify-center min-h-[200px]">
                    <div className="w-8 h-8 border-4 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
                </div>
            ) : exercises.length === 0 ? (
                <div className="card text-center py-8">
                    <p className="text-[var(--color-text-secondary)] mb-2">
                        No exercises loaded yet.
                    </p>
                    <p className="text-sm text-[var(--color-text-muted)]">
                        Click "Load / refresh curriculum" to populate PyPal's built-in lessons.
                    </p>
                </div>
            ) : (
                <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                    {exercises.map((ex) => (
                        <div
                            key={ex.id}
                            className="card"
                        >
                            <div className="flex items-start justify-between mb-2">
                                <h3 className="font-semibold">{ex.title}</h3>
                                <span className="text-xs px-2 py-0.5 rounded bg-[var(--color-bg-secondary)]">
                                    L{ex.difficulty}
                                </span>
                            </div>
                            <p className="text-sm text-[var(--color-text-secondary)] mb-3 line-clamp-3">
                                {ex.description}
                            </p>
                            <div className="flex items-center justify-between text-xs text-[var(--color-text-secondary)]">
                                <span>Grade {ex.grade_level}</span>
                                <span>{ex.estimated_minutes} min</span>
                                <span className="capitalize">{ex.concept}</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
