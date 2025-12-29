/**
 * HintPanel component with 4-level hint escalation.
 */
import { useState } from 'react';
import { tutorApi } from '../../services/api';
import type { HintResponse } from '../../types';
import clsx from 'clsx';

interface HintPanelProps {
    code: string;
    errorMessage?: string;
    onHintUsed?: () => void;
}

export function HintPanel({ code, errorMessage, onHintUsed }: HintPanelProps) {
    const [currentHint, setCurrentHint] = useState<HintResponse | null>(null);
    const [hintLevel, setHintLevel] = useState(1);
    const [isLoading, setIsLoading] = useState(false);

    const hintLabels = [
        { level: 1, label: 'Gentle Nudge', description: 'A small hint to point you in the right direction' },
        { level: 2, label: 'Direction', description: 'Shows you the general area to focus on' },
        { level: 3, label: 'Specific Help', description: 'Tells you exactly what to look at' },
        { level: 4, label: 'Full Solution', description: 'Shows the complete answer' },
    ];

    const handleGetHint = async () => {
        setIsLoading(true);

        try {
            const response = await tutorApi.getHint({
                code,
                error_message: errorMessage,
                hint_level: hintLevel,
            });

            setCurrentHint(response);

            if (response.next_level_available && hintLevel < 4) {
                setHintLevel(hintLevel + 1);
            }

            onHintUsed?.();
        } catch (error) {
            setCurrentHint({
                hint: 'Could not get a hint right now. Please try again.',
                hint_level: hintLevel,
                next_level_available: true,
            });
        } finally {
            setIsLoading(false);
        }
    };

    const resetHints = () => {
        setCurrentHint(null);
        setHintLevel(1);
    };

    return (
        <div className="card">
            <div className="flex items-center justify-between mb-4">
                <h3 className="font-semibold text-lg">Need Help?</h3>
                {currentHint && (
                    <button
                        onClick={resetHints}
                        className="text-sm text-[var(--color-text-secondary)] hover:text-[var(--color-text)]"
                    >
                        Reset
                    </button>
                )}
            </div>

            {/* Hint level indicator */}
            <div className="flex gap-1 mb-4">
                {hintLabels.map(({ level }) => (
                    <div
                        key={level}
                        className={clsx(
                            'h-2 flex-1 rounded-full',
                            level < hintLevel
                                ? 'bg-[var(--color-primary)]'
                                : level === hintLevel
                                    ? 'bg-[var(--color-primary)] bg-opacity-50'
                                    : 'bg-[var(--color-bg-secondary)]'
                        )}
                    />
                ))}
            </div>

            {/* Current hint display */}
            {currentHint && (
                <div className="bg-[var(--color-bg-secondary)] p-4 rounded-lg mb-4">
                    <div className="flex items-center gap-2 mb-2">
                        <span className="text-xs font-medium px-2 py-1 bg-[var(--color-primary)] bg-opacity-10 text-[var(--color-primary)] rounded">
                            Level {currentHint.hint_level}
                        </span>
                        <span className="text-sm text-[var(--color-text-secondary)]">
                            {hintLabels[currentHint.hint_level - 1]?.label}
                        </span>
                    </div>
                    <p className="text-sm whitespace-pre-wrap">{currentHint.hint}</p>
                </div>
            )}

            {/* Get hint button */}
            <button
                onClick={handleGetHint}
                disabled={isLoading || (currentHint !== null && !currentHint.next_level_available)}
                className={clsx(
                    'btn w-full',
                    currentHint ? 'btn-secondary' : 'btn-primary'
                )}
            >
                {isLoading
                    ? 'Getting hint...'
                    : currentHint
                        ? currentHint.next_level_available
                            ? `Get More Help (Level ${hintLevel})`
                            : 'No more hints available'
                        : 'Get a Hint'}
            </button>

            {/* Next hint description */}
            {!currentHint && (
                <p className="text-xs text-[var(--color-text-muted)] mt-2 text-center">
                    {hintLabels[0].description}
                </p>
            )}
            {currentHint && currentHint.next_level_available && hintLevel <= 4 && (
                <p className="text-xs text-[var(--color-text-muted)] mt-2 text-center">
                    {hintLabels[hintLevel - 1]?.description}
                </p>
            )}
        </div>
    );
}
