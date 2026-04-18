/**
 * Registration page supporting both student (COPPA) and teacher sign-up.
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../stores';
import clsx from 'clsx';

const AVAILABLE_INTERESTS = [
    { id: 'games', label: 'Games', color: 'bg-purple-500' },
    { id: 'music', label: 'Music', color: 'bg-pink-500' },
    { id: 'space', label: 'Space', color: 'bg-indigo-500' },
    { id: 'art', label: 'Art', color: 'bg-orange-500' },
    { id: 'sports', label: 'Sports', color: 'bg-green-500' },
    { id: 'animals', label: 'Animals', color: 'bg-amber-500' },
];

type Role = 'student' | 'teacher';

export function RegisterPage() {
    const [role, setRole] = useState<Role>('student');
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirmPassword: '',
        birthYear: '',
        gradeLevel: '7',
        parentEmail: '',
        displayName: '',
        school: '',
    });
    const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
    const [formError, setFormError] = useState('');
    const { register, isLoading, error, clearError } = useAuthStore();
    const navigate = useNavigate();

    const currentYear = new Date().getFullYear();
    const age = formData.birthYear ? currentYear - parseInt(formData.birthYear) : 0;
    const needsParentConsent = role === 'student' && age > 0 && age < 13;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
        clearError();
        setFormError('');
    };

    const toggleInterest = (interestId: string) => {
        setSelectedInterests((prev) =>
            prev.includes(interestId)
                ? prev.filter((i) => i !== interestId)
                : [...prev, interestId],
        );
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        clearError();
        setFormError('');

        if (formData.password !== formData.confirmPassword) {
            setFormError('Passwords do not match');
            return;
        }

        if (formData.password.length < 6) {
            setFormError('Password must be at least 6 characters');
            return;
        }

        if (role === 'student') {
            if (!formData.birthYear) {
                setFormError('Please enter your birth year');
                return;
            }
            if (needsParentConsent && !formData.parentEmail) {
                setFormError('Parent email is required for students under 13');
                return;
            }
            if (selectedInterests.length === 0) {
                setFormError('Please pick at least one thing you like');
                return;
            }
        }

        const result = await register({
            username: formData.username,
            password: formData.password,
            birthYear: role === 'student' ? parseInt(formData.birthYear) : 1990,
            gradeLevel: role === 'student' ? parseInt(formData.gradeLevel) : 0,
            parentEmail: formData.parentEmail || undefined,
            interests: role === 'student' ? selectedInterests : undefined,
            role,
            displayName: role === 'teacher' ? formData.displayName || formData.username : undefined,
            school: role === 'teacher' ? formData.school || undefined : undefined,
        });

        if (result.success) {
            if (result.needsConsent) {
                navigate('/consent-pending');
            } else if (result.role === 'teacher') {
                navigate('/teacher');
            } else {
                navigate('/dashboard');
            }
        }
    };

    return (
        <div className="min-h-screen bg-[var(--color-bg)] flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-8">
                    <h1 className="text-3xl font-bold text-[var(--color-primary)]">PyPal</h1>
                    <p className="text-[var(--color-text-secondary)] mt-2">Create your account</p>
                </div>

                <div className="card">
                    <div className="flex gap-2 mb-6 p-1 bg-[var(--color-bg-secondary)] rounded-lg">
                        <button
                            type="button"
                            onClick={() => setRole('student')}
                            className={clsx(
                                'flex-1 px-4 py-2 rounded-md text-sm font-medium transition-colors',
                                role === 'student'
                                    ? 'bg-[var(--color-bg-card)] text-[var(--color-text)] shadow-sm'
                                    : 'text-[var(--color-text-secondary)]',
                            )}
                        >
                            I'm a student
                        </button>
                        <button
                            type="button"
                            onClick={() => setRole('teacher')}
                            className={clsx(
                                'flex-1 px-4 py-2 rounded-md text-sm font-medium transition-colors',
                                role === 'teacher'
                                    ? 'bg-[var(--color-bg-card)] text-[var(--color-text)] shadow-sm'
                                    : 'text-[var(--color-text-secondary)]',
                            )}
                        >
                            I'm a teacher
                        </button>
                    </div>

                    {(error || formError) && (
                        <div className="bg-[var(--color-error)] bg-opacity-10 text-[var(--color-error)] p-3 rounded-lg mb-4 text-sm">
                            {error || formError}
                        </div>
                    )}

                    <form onSubmit={handleSubmit} className="space-y-4">
                        <div>
                            <label htmlFor="username" className="block text-sm font-medium mb-1">
                                Username
                            </label>
                            <input
                                id="username"
                                name="username"
                                type="text"
                                value={formData.username}
                                onChange={handleChange}
                                className="input"
                                required
                                minLength={3}
                                autoComplete="username"
                            />
                        </div>

                        {role === 'teacher' && (
                            <>
                                <div>
                                    <label htmlFor="displayName" className="block text-sm font-medium mb-1">
                                        Display name
                                    </label>
                                    <input
                                        id="displayName"
                                        name="displayName"
                                        type="text"
                                        value={formData.displayName}
                                        onChange={handleChange}
                                        className="input"
                                        placeholder="Ms. Rivera"
                                    />
                                </div>
                                <div>
                                    <label htmlFor="school" className="block text-sm font-medium mb-1">
                                        School (optional)
                                    </label>
                                    <input
                                        id="school"
                                        name="school"
                                        type="text"
                                        value={formData.school}
                                        onChange={handleChange}
                                        className="input"
                                        placeholder="Washington Middle School"
                                    />
                                </div>
                            </>
                        )}

                        {role === 'student' && (
                            <>
                                <div className="grid grid-cols-2 gap-4">
                                    <div>
                                        <label htmlFor="birthYear" className="block text-sm font-medium mb-1">
                                            Birth year
                                        </label>
                                        <input
                                            id="birthYear"
                                            name="birthYear"
                                            type="number"
                                            value={formData.birthYear}
                                            onChange={handleChange}
                                            className="input"
                                            required
                                            min="2005"
                                            max="2020"
                                            placeholder="2012"
                                        />
                                    </div>
                                    <div>
                                        <label htmlFor="gradeLevel" className="block text-sm font-medium mb-1">
                                            Grade
                                        </label>
                                        <select
                                            id="gradeLevel"
                                            name="gradeLevel"
                                            value={formData.gradeLevel}
                                            onChange={handleChange}
                                            className="input"
                                            required
                                        >
                                            <option value="6">6th Grade</option>
                                            <option value="7">7th Grade</option>
                                            <option value="8">8th Grade</option>
                                        </select>
                                    </div>
                                </div>

                                {needsParentConsent && (
                                    <div className="bg-[var(--color-warning)] bg-opacity-10 p-4 rounded-lg">
                                        <p className="text-sm text-[var(--color-warning)] mb-3">
                                            Students under 13 need a parent's permission to use PyPal.
                                        </p>
                                        <label htmlFor="parentEmail" className="block text-sm font-medium mb-1">
                                            Parent's email
                                        </label>
                                        <input
                                            id="parentEmail"
                                            name="parentEmail"
                                            type="email"
                                            value={formData.parentEmail}
                                            onChange={handleChange}
                                            className="input"
                                            required={needsParentConsent}
                                            placeholder="parent@example.com"
                                        />
                                    </div>
                                )}

                                <div>
                                    <label className="block text-sm font-medium mb-2">
                                        What do you like? (Pick at least one)
                                    </label>
                                    <div className="flex flex-wrap gap-2">
                                        {AVAILABLE_INTERESTS.map((interest) => (
                                            <button
                                                key={interest.id}
                                                type="button"
                                                onClick={() => toggleInterest(interest.id)}
                                                className={clsx(
                                                    'px-3 py-2 rounded-lg text-sm font-medium transition-all',
                                                    selectedInterests.includes(interest.id)
                                                        ? `${interest.color} text-white`
                                                        : 'bg-[var(--color-bg-secondary)] text-[var(--color-text-secondary)]',
                                                )}
                                            >
                                                {interest.label}
                                            </button>
                                        ))}
                                    </div>
                                </div>
                            </>
                        )}

                        <div>
                            <label htmlFor="password" className="block text-sm font-medium mb-1">
                                Password
                            </label>
                            <input
                                id="password"
                                name="password"
                                type="password"
                                value={formData.password}
                                onChange={handleChange}
                                className="input"
                                required
                                minLength={6}
                                autoComplete="new-password"
                            />
                        </div>

                        <div>
                            <label htmlFor="confirmPassword" className="block text-sm font-medium mb-1">
                                Confirm password
                            </label>
                            <input
                                id="confirmPassword"
                                name="confirmPassword"
                                type="password"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                className="input"
                                required
                                autoComplete="new-password"
                            />
                        </div>

                        <button type="submit" disabled={isLoading} className="btn btn-primary w-full">
                            {isLoading ? 'Creating account...' : `Create ${role} account`}
                        </button>
                    </form>

                    <p className="text-center text-sm text-[var(--color-text-secondary)] mt-6">
                        Already have an account?{' '}
                        <Link to="/login" className="text-[var(--color-primary)] font-medium hover:underline">
                            Sign in
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
