/**
 * Teacher view of a single student's progress.
 */
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { teacherApi } from '../services/api';
import type { StudentDetail } from '../types';

export function TeacherStudentDetailPage() {
    const { id } = useParams<{ id: string }>();
    const [student, setStudent] = useState<StudentDetail | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function load() {
            if (!id) return;
            try {
                const data = await teacherApi.getStudent(parseInt(id));
                setStudent(data);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load student');
            } finally {
                setIsLoading(false);
            }
        }
        load();
    }, [id]);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="w-8 h-8 border-4 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (error || !student) {
        return (
            <div className="card">
                <p className="text-[var(--color-error)]">{error || 'Student not found'}</p>
                <Link to="/teacher" className="text-[var(--color-primary)] hover:underline">
                    Back to dashboard
                </Link>
            </div>
        );
    }

    const totalFrustration = student.recent_sessions.reduce(
        (sum, s) => sum + s.frustration_events,
        0,
    );

    return (
        <div className="space-y-6">
            <div>
                <Link to="/teacher" className="text-sm text-[var(--color-primary)] hover:underline">
                    ← Back to dashboard
                </Link>
                <h1 className="text-2xl font-bold mt-2">{student.username}</h1>
                <p className="text-[var(--color-text-secondary)]">
                    Grade {student.grade_level} · Joined {new Date(student.created_at).toLocaleDateString()}
                </p>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Stat label="Completed" value={student.exercises_completed} />
                <Stat label="Attempted" value={student.exercises_attempted} />
                <Stat label="Points" value={student.total_points} />
                <Stat label="Streak" value={student.current_streak} />
            </div>

            {totalFrustration >= 5 && (
                <div className="card border-l-4 border-amber-500">
                    <p className="font-semibold text-amber-700 dark:text-amber-300">
                        Heads up
                    </p>
                    <p className="text-sm text-[var(--color-text-secondary)]">
                        {student.username} has shown frustration {totalFrustration} times recently. A
                        quick one-on-one check-in might help.
                    </p>
                </div>
            )}

            <section>
                <h2 className="text-xl font-semibold mb-4">Exercise progress</h2>
                {student.exercises.length === 0 ? (
                    <div className="card">
                        <p className="text-sm text-[var(--color-text-secondary)]">
                            No exercises attempted yet.
                        </p>
                    </div>
                ) : (
                    <div className="card overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="border-b border-[var(--color-border)] text-left">
                                    <th className="py-2 px-2">Exercise</th>
                                    <th className="py-2 px-2">Concept</th>
                                    <th className="py-2 px-2">Status</th>
                                    <th className="py-2 px-2">Step</th>
                                    <th className="py-2 px-2">Hints</th>
                                    <th className="py-2 px-2">Points</th>
                                    <th className="py-2 px-2">Last updated</th>
                                </tr>
                            </thead>
                            <tbody>
                                {student.exercises.map((ex) => (
                                    <tr
                                        key={ex.exercise_id}
                                        className="border-b border-[var(--color-border)] last:border-0"
                                    >
                                        <td className="py-2 px-2 font-medium">{ex.title}</td>
                                        <td className="py-2 px-2 capitalize">{ex.concept || '—'}</td>
                                        <td className="py-2 px-2">
                                            {ex.completed ? (
                                                <span className="px-2 py-0.5 text-xs rounded bg-emerald-100 dark:bg-emerald-900 text-emerald-700 dark:text-emerald-300">
                                                    Completed
                                                </span>
                                            ) : (
                                                <span className="px-2 py-0.5 text-xs rounded bg-[var(--color-bg-secondary)] text-[var(--color-text-secondary)]">
                                                    In progress
                                                </span>
                                            )}
                                        </td>
                                        <td className="py-2 px-2">{ex.current_step}</td>
                                        <td className="py-2 px-2">{ex.hints_used}</td>
                                        <td className="py-2 px-2">{ex.points_earned}</td>
                                        <td className="py-2 px-2 text-[var(--color-text-muted)]">
                                            {new Date(ex.last_updated).toLocaleDateString()}
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </section>

            <section>
                <h2 className="text-xl font-semibold mb-4">Recent sessions</h2>
                {student.recent_sessions.length === 0 ? (
                    <div className="card">
                        <p className="text-sm text-[var(--color-text-secondary)]">
                            No sessions recorded yet.
                        </p>
                    </div>
                ) : (
                    <div className="card overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="border-b border-[var(--color-border)] text-left">
                                    <th className="py-2 px-2">Started</th>
                                    <th className="py-2 px-2">Status</th>
                                    <th className="py-2 px-2">Code runs</th>
                                    <th className="py-2 px-2">Hints</th>
                                    <th className="py-2 px-2">Frustration</th>
                                </tr>
                            </thead>
                            <tbody>
                                {student.recent_sessions.map((s) => (
                                    <tr
                                        key={s.id}
                                        className="border-b border-[var(--color-border)] last:border-0"
                                    >
                                        <td className="py-2 px-2">
                                            {new Date(s.started_at).toLocaleString()}
                                        </td>
                                        <td className="py-2 px-2">
                                            {s.completed ? 'Completed' : 'Open'}
                                        </td>
                                        <td className="py-2 px-2">{s.code_runs}</td>
                                        <td className="py-2 px-2">{s.hint_requests}</td>
                                        <td className="py-2 px-2">{s.frustration_events}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                )}
            </section>
        </div>
    );
}

function Stat({ label, value }: { label: string; value: number }) {
    return (
        <div className="card text-center">
            <p className="text-3xl font-bold text-[var(--color-primary)]">{value}</p>
            <p className="text-sm text-[var(--color-text-secondary)]">{label}</p>
        </div>
    );
}
