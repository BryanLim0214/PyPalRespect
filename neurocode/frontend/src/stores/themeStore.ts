/**
 * Theme and accessibility store using Zustand.
 */
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { AccessibilitySettings, ThemeMode } from '../types';

interface ThemeState extends AccessibilitySettings {
    setThemeMode: (mode: ThemeMode) => void;
    setDyslexiaFont: (enabled: boolean) => void;
    setHighContrast: (enabled: boolean) => void;
    setReduceMotion: (enabled: boolean) => void;
    applyToDocument: () => void;
}

export const useThemeStore = create<ThemeState>()(
    persist(
        (set, get) => ({
            themeMode: 'light',
            dyslexiaFont: false,
            highContrast: false,
            reduceMotion: true, // Default ON for ADHD

            setThemeMode: (mode) => {
                set({ themeMode: mode });
                get().applyToDocument();
            },

            setDyslexiaFont: (enabled) => {
                set({ dyslexiaFont: enabled });
                get().applyToDocument();
            },

            setHighContrast: (enabled) => {
                set({ highContrast: enabled });
                get().applyToDocument();
            },

            setReduceMotion: (enabled) => {
                set({ reduceMotion: enabled });
                get().applyToDocument();
            },

            applyToDocument: () => {
                const { themeMode, dyslexiaFont, highContrast, reduceMotion } = get();
                const root = document.documentElement;

                // Theme mode
                root.classList.toggle('dark', themeMode === 'dark');

                // Accessibility classes
                root.classList.toggle('dyslexic-font', dyslexiaFont);
                root.classList.toggle('high-contrast', highContrast);
                root.classList.toggle('reduce-motion', reduceMotion);
            },
        }),
        {
            name: 'theme-storage',
            onRehydrateStorage: () => (state) => {
                // Apply theme on app load
                state?.applyToDocument();
            },
        }
    )
);
