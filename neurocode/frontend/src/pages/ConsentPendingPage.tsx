/**
 * Shown after a student under 13 registers and is waiting for their parent to consent.
 */
import { Link } from 'react-router-dom';

export function ConsentPendingPage() {
    return (
        <div className="min-h-screen bg-[var(--color-bg)] flex items-center justify-center p-4">
            <div className="w-full max-w-md">
                <div className="text-center mb-6">
                    <h1 className="text-3xl font-bold text-[var(--color-primary)]">PyPal</h1>
                </div>

                <div className="card text-center space-y-4">
                    <div className="mx-auto w-12 h-12 rounded-full bg-[var(--color-primary)] bg-opacity-10 flex items-center justify-center">
                        <svg
                            className="w-6 h-6 text-[var(--color-primary)]"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                        >
                            <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2}
                                d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                            />
                        </svg>
                    </div>

                    <h2 className="text-xl font-semibold">Almost there!</h2>
                    <p className="text-sm text-[var(--color-text-secondary)]">
                        We sent an email to your parent or guardian. They need to give
                        permission before you can start coding. Once they confirm, you can
                        log in and begin your Python adventure.
                    </p>

                    <div className="pt-4">
                        <Link
                            to="/login"
                            className="btn btn-primary w-full"
                        >
                            Back to sign in
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
}
