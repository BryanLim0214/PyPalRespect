/**
 * Teacher dashboard. Shows class overview, student list, and recent trends.
 */
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../stores';
import { teacherApi } from '../services/api';
import type { ClassroomOverview, StudentSummary, EngagementDay } from '../types';

export function TeacherDashboardPage() {
    const { user } = useAuthStore();
    const [overview, setOverview] = useState<ClassroomOverview | null>(null);
    const [students, setStudents] = useState<StudentSummary[]>([]);
    const [trend, setTrend] = useState<EngagementDay[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        async function load() {
            try {
                const [overviewData, studentList, engagement] = await Promise.all([
                    teacherApi.overview(),
                    teacherApi.listStudents(),
                    teacherApi.engagement(14),
                ]);
                setOverview(overviewData);
                setStudents(studentList);
                setTrend(engagement.trend);
            } catch (err) {
                setError(err instanceof Error ? err.message : 'Failed to load classroom data');
            } finally {
                setIsLoading(false);
            }
        }
        load();
    }, []);

    if (isLoading) {
        return (
            <div className="flex items-center justify-center min-h-[400px]">
                <div className="w-8 h-8 border-4 border-[var(--color-primary)] border-t-transparent rounded-full animate-spin" />
            </div>
        );
    }

    if (error) {
        return (
            <div className="card">
                <p className="text-[var(--color-error)]">{error}</p>
            </div>
        );
    }

    const maxSessions = Math.max(1, ...trend.map((d) => d.sessions));

    return (
        <div className="space-y-8">
            <div>
                <h1 className="text-2xl font-bold">
                    Welcome, {user?.display_name || user?.username}
                </h1>
                <p className="text-[var(--color-text-secondary)]">
                    Here is what your students have been up to.
                </p>
            </div>

            {overview && (
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <StatCard label="Students" value={overview.total_students} />
                    <StatCard label="Active (7 days)" value={overview.active_last_7_days} />
                    <StatCard label="Exercises" value={overview.total_exercises} />
                    <StatCard label="Completions" value={overview.total_completions} />
                </div>
            )}

            <section>
                <h2 className="text-xl font-semibold mb-4">Engagement (last 14 days)</h2>
                <div className="card">
                    {trend.length === 0 ? (
                        <p className="text-sm text-[var(--color-text-secondary)]">
                            No sessions yet. Once students start coding, activity will appear here.
                        </p>
                    ) : (
                        <div className="flex items-end gap-1 h-32">
                            {trend.map((day) => (
                                <div
                                    key={day.date}
                                    className="flex-1 flex flex-col items-center justify-end"
                                    title={`${day.date}: ${day.sessions} sessions, ${day.completed} completed`}
                                >
                                    <div
                                        className="w-full bg-[var(--color-primary)] rounded-t"
                                        style={{
                                            height: `${(day.sessions / maxSessions) * 100}%`,
                                            minHeight: day.sessions > 0 ? '4px' : '0',
                                        }}
                                    />
                                    <span className="text-[10px] text-[var(--color-text-muted)] mt-1">
                                        {day.date.slice(5)}
                                    </span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            </section>

            <section>
                <div className="flex items-center justify-between mb-4">
                    <h2 className="text-xl font-semibold">Students ({students.length})</h2>
                </div>
                {students.length === 0 ? (
                    <div className="card text-center py-8">
                        <p className="text-[var(--color-text-secondary)] mb-2">
                            No students have registered yet.
                        </p>
                        <p className="text-sm text-[var(--color-text-muted)]">
                            Share the student sign-up link with your class to get started.
                        </p>
                    </div>
                ) : (
                    <div className="card overflow-x-auto">
                        <table className="w-full text-sm">
                            <thead>
                                <tr className="border-b border-[var(--color-border)] text-left">
                                    <th className="py-2 px-2">Student</th>
                                    <th className="py-2 px-2">Grade</th>
                                    <th className="py-2 px-2">Completed</th>
                                    <th className="py-2 px-2">Attempts</th>
                                    <th className="py-2 px-2">Points</th>
                                    <th className="py-2 px-2">Streak</th>
                                    <th className="py-2 px-2">Last active</th>
                                    <th className="py-2 px-2"></th>
                                </tr>
                            </thead>
                            <tbody>
                                {students.map((s) => (
                                    <tr
                                        key={s.id}
                                        className="border-b border-[var(--color-border)] last:border-0 hover:bg-[var(--color-bg-secondary)]"
                                    >
                                        <td className="py-2 px-2 font-medium">{s.username}</td>
                                        <td className="py-2 px-2">{s.grade_level}</td>
                                        <td className="py-2 px-2">{s.exercises_completed}</td>
                                        <td className="py-2 px-2">{s.exercises_attempted}</td>
                                        <td className="py-2 px-2">{s.total_points}</td>
                                        <td className="py-2 px-2">{s.current_streak}</td>
                                        <td className="py-2 px-2 text-[var(--color-text-muted)]">
                                            {s.last_active ? formatRelative(s.last_active) : '—'}
                                        </td>
                                        <td className="py-2 px-2">
                                            <Link
                                                to={`/teacher/students/${s.id}`}
                                                className="text-[var(--color-primary)] font-medium hover:underline"
                                            >
                                                View
                                            </Link>
                                        </td>
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

function StatCard({ label, value }: { label: string; value: number }) {
    return (
        <div className="card text-center">
            <p className="text-3xl font-bold text-[var(--color-primary)]">{value}</p>
            <p className="text-sm text-[var(--color-text-secondary)]">{label}</p>
        </div>
    );
}

function formatRelative(iso: string): string {
    const diff = Date.now() - new Date(iso).getTime();
    const mins = Math.floor(diff / 60000);
    if (mins < 1) return 'just now';
    if (mins < 60) return `${mins}m ago`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
}
