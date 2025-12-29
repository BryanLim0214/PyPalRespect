/**
 * Settings page for accessibility options.
 */
import { useState, useEffect } from 'react';
import { useThemeStore, useTimerStore, useAuthStore } from '../stores';
import clsx from 'clsx';

export function SettingsPage() {
    const {
        themeMode,
        dyslexiaFont,
        highContrast,
        reduceMotion,
        setThemeMode,
        setDyslexiaFont,
        setHighContrast,
        setReduceMotion,
    } = useThemeStore();

    const { user, updatePreferences } = useAuthStore();
    const {
        breakIntervalMinutes,
        sessionLengthMinutes,
        setBreakInterval,
        setSessionLength,
    } = useTimerStore();

    const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
    const [isSaving, setIsSaving] = useState(false);
    const [saveMessage, setSaveMessage] = useState('');

    useEffect(() => {
        if (user?.interests) {
            try {
                const loaded = JSON.parse(user.interests);
                if (Array.isArray(loaded)) {
                    setSelectedInterests(loaded);
                }
            } catch (e) {
                console.error('Failed to parse user interests', e);
            }
        }
    }, [user?.interests]);

    const toggleInterest = (interestId: string) => {
        setSelectedInterests(prev =>
            prev.includes(interestId)
                ? prev.filter(i => i !== interestId)
                : [...prev, interestId]
        );
        setSaveMessage('');
    };

    const handleSaveInterests = async () => {
        setIsSaving(true);
        setSaveMessage('');
        // Send array directly as backend expects List[str]
        const success = await updatePreferences({ interests: selectedInterests as any });
        setIsSaving(false);
        if (success) {
            setSaveMessage('Interests saved successfully!');
            setTimeout(() => setSaveMessage(''), 3000);
        } else {
            setSaveMessage('Failed to save. Please try again.');
        }
    };

    return (
        <div className="max-w-2xl mx-auto space-y-8">
            <div>
                <h1 className="text-2xl font-bold">Settings</h1>
                <p className="text-[var(--color-text-secondary)]">
                    Customize your learning experience
                </p>
            </div>

            {/* Appearance */}
            <section className="card">
                <h2 className="text-lg font-semibold mb-4">Appearance</h2>
                <div className="space-y-4">
                    <SettingRow
                        label="Dark Mode"
                        description="Use a dark color scheme"
                    >
                        <ToggleButton
                            checked={themeMode === 'dark'}
                            onChange={(checked) => setThemeMode(checked ? 'dark' : 'light')}
                        />
                    </SettingRow>

                    <SettingRow
                        label="High Contrast"
                        description="Increase contrast for better visibility"
                    >
                        <ToggleButton checked={highContrast} onChange={setHighContrast} />
                    </SettingRow>
                </div>
            </section>

            {/* Accessibility */}
            <section className="card">
                <h2 className="text-lg font-semibold mb-4">Accessibility</h2>
                <div className="space-y-4">
                    <SettingRow
                        label="Dyslexia-Friendly Font"
                        description="Use OpenDyslexic font for easier reading"
                    >
                        <ToggleButton checked={dyslexiaFont} onChange={setDyslexiaFont} />
                    </SettingRow>

                    <SettingRow
                        label="Reduce Motion"
                        description="Minimize animations and transitions"
                    >
                        <ToggleButton checked={reduceMotion} onChange={setReduceMotion} />
                    </SettingRow>
                </div>
            </section>

            {/* Focus Settings */}
            <section className="card">
                <h2 className="text-lg font-semibold mb-4">Focus Timer</h2>
                <div className="space-y-4">
                    <SettingRow
                        label="Break Reminder Interval"
                        description="How often to remind you to take a break"
                    >
                        <select
                            value={breakIntervalMinutes}
                            onChange={(e) => setBreakInterval(parseInt(e.target.value))}
                            className="input w-auto"
                        >
                            <option value="10">10 minutes</option>
                            <option value="15">15 minutes</option>
                            <option value="20">20 minutes</option>
                            <option value="25">25 minutes</option>
                            <option value="30">30 minutes</option>
                        </select>
                    </SettingRow>

                    <SettingRow
                        label="Session Length"
                        description="Suggested total learning time per session"
                    >
                        <select
                            value={sessionLengthMinutes}
                            onChange={(e) => setSessionLength(parseInt(e.target.value))}
                            className="input w-auto"
                        >
                            <option value="15">15 minutes</option>
                            <option value="20">20 minutes</option>
                            <option value="30">30 minutes</option>
                            <option value="45">45 minutes</option>
                            <option value="60">60 minutes</option>
                        </select>
                    </SettingRow>
                </div>
            </section>

            {/* Interests */}
            <section className="card">
                <h2 className="text-lg font-semibold mb-4">Your Interests</h2>
                <p className="text-sm text-[var(--color-text-secondary)] mb-4">
                    Select topics you're interested in to personalize your learning experience
                </p>
                <div className="flex flex-wrap gap-2">
                    {[
                        { id: 'games', label: '🎮 Games', color: 'bg-purple-500' },
                        { id: 'music', label: '🎵 Music', color: 'bg-pink-500' },
                        { id: 'space', label: '🚀 Space', color: 'bg-indigo-500' },
                        { id: 'art', label: '🎨 Art', color: 'bg-orange-500' },
                        { id: 'sports', label: '⚽ Sports', color: 'bg-green-500' },
                        { id: 'animals', label: '🐾 Animals', color: 'bg-amber-500' },
                    ].map((interest) => (
                        <button
                            key={interest.id}
                            type="button"
                            onClick={() => toggleInterest(interest.id)}
                            className={clsx(
                                'px-4 py-2 rounded-lg text-sm font-medium transition-all',
                                selectedInterests.includes(interest.id)
                                    ? `${interest.color} text-white scale-105 shadow-md`
                                    : 'bg-[var(--color-bg-secondary)] text-[var(--color-text-secondary)] hover:bg-[var(--color-border)]'
                            )}
                        >
                            {interest.label}
                        </button>
                    ))}
                </div>

                <div className="mt-6 flex items-center justify-between">
                    <p className={`text-sm transition-opacity ${saveMessage ? 'opacity-100' : 'opacity-0'} ${saveMessage.includes('Failed') ? 'text-[var(--color-error)]' : 'text-[var(--color-success)]'}`}>
                        {saveMessage}
                    </p>
                    <button
                        onClick={handleSaveInterests}
                        disabled={isSaving}
                        className="btn btn-primary"
                    >
                        {isSaving ? 'Saving...' : 'Save Interests'}
                    </button>
                </div>
            </section>
        </div>
    );
}

function SettingRow({
    label,
    description,
    children,
}: {
    label: string;
    description: string;
    children: React.ReactNode;
}) {
    return (
        <div className="flex items-center justify-between py-2">
            <div>
                <p className="font-medium">{label}</p>
                <p className="text-sm text-[var(--color-text-secondary)]">{description}</p>
            </div>
            {children}
        </div>
    );
}

function ToggleButton({
    checked,
    onChange,
}: {
    checked: boolean;
    onChange: (checked: boolean) => void;
}) {
    return (
        <button
            role="switch"
            aria-checked={checked}
            onClick={() => onChange(!checked)}
            className={`
        relative inline-flex h-6 w-11 items-center rounded-full transition-colors
        ${checked ? 'bg-[var(--color-primary)]' : 'bg-[var(--color-bg-secondary)]'}
      `}
        >
            <span
                className={`
          inline-block h-4 w-4 transform rounded-full bg-white transition-transform
          ${checked ? 'translate-x-6' : 'translate-x-1'}
        `}
            />
        </button>
    );
}
