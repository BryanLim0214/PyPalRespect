/**
 * Registration page with COPPA compliance.
 */
import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuthStore } from '../stores';
import clsx from 'clsx';

const AVAILABLE_INTERESTS = [
    { id: 'games', label: '🎮 Games', color: 'bg-purple-500' },
    { id: 'music', label: '🎵 Music', color: 'bg-pink-500' },
    { id: 'space', label: '🚀 Space', color: 'bg-indigo-500' },
    { id: 'art', label: '🎨 Art', color: 'bg-orange-500' },
    { id: 'sports', label: '⚽ Sports', color: 'bg-green-500' },
    { id: 'animals', label: '🐾 Animals', color: 'bg-amber-500' },
];

export function RegisterPage() {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        confirmPassword: '',
        birthYear: '',
        gradeLevel: '7',
        parentEmail: '',
    });
    const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
    const [formError, setFormError] = useState('');
    const { register, isLoading, error, clearError } = useAuthStore();
    const navigate = useNavigate();

    const currentYear = new Date().getFullYear();
    const age = formData.birthYear ? currentYear - parseInt(formData.birthYear) : 0;
    const needsParentConsent = age > 0 && age < 13;

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
        setFormData((prev) => ({ ...prev, [e.target.name]: e.target.value }));
        clearError();
        setFormError('');
    };

    const toggleInterest = (interestId: string) => {
        setSelectedInterests(prev =>
            prev.includes(interestId)
                ? prev.filter(i => i !== interestId)
                : [...prev, interestId]
        );
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        clearError();
        setFormError('');

        // Validation
        if (formData.password !== formData.confirmPassword) {
            setFormError('Passwords do not match');
            return;
        }

        if (formData.password.length < 6) {
            setFormError('Password must be at least 6 characters');
            return;
        }

        if (needsParentConsent && !formData.parentEmail) {
            setFormError('Parent email is required for students under 13');
            return;
        }

        if (selectedInterests.length === 0) {
            setFormError('Please select at least one interest');
            return;
        }

        const result = await register({
            username: formData.username,
            password: formData.password,
            birthYear: parseInt(formData.birthYear),
            gradeLevel: parseInt(formData.gradeLevel),
            parentEmail: formData.parentEmail || undefined,
            interests: selectedInterests,
        });

        if (result.success) {
            if (result.needsConsent) {
                navigate('/consent-pending');
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
                    <h2 className="text-xl font-semibold mb-6">Sign Up</h2>

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
                            />
                        </div>

                        <div className="grid grid-cols-2 gap-4">
                            <div>
                                <label htmlFor="birthYear" className="block text-sm font-medium mb-1">
                                    Birth Year
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
                                    Grade Level
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
                                    Students under 13 need a parent's permission to use NeuroCode.
                                </p>
                                <label htmlFor="parentEmail" className="block text-sm font-medium mb-1">
                                    Parent's Email
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

                        {/* Interest Selection */}
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
                                                ? `${interest.color} text-white scale-105`
                                                : 'bg-[var(--color-bg-secondary)] text-[var(--color-text-secondary)] hover:bg-[var(--color-border)]'
                                        )}
                                    >
                                        {interest.label}
                                    </button>
                                ))}
                            </div>
                            {selectedInterests.length === 0 && (
                                <p className="text-xs text-[var(--color-text-muted)] mt-1">
                                    This helps us make exercises more fun for you!
                                </p>
                            )}
                        </div>

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
                            />
                        </div>

                        <div>
                            <label htmlFor="confirmPassword" className="block text-sm font-medium mb-1">
                                Confirm Password
                            </label>
                            <input
                                id="confirmPassword"
                                name="confirmPassword"
                                type="password"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                className="input"
                                required
                            />
                        </div>

                        <button type="submit" disabled={isLoading} className="btn btn-primary w-full">
                            {isLoading ? 'Creating account...' : 'Create Account'}
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
