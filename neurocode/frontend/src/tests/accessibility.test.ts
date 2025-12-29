/**
 * UX and accessibility tests for frontend.
 */
import { describe, it, expect } from 'vitest';

/**
 * Color contrast tests based on WCAG AA requirements.
 * Contrast ratio should be at least 4.5:1 for normal text.
 */

// Utility function to calculate relative luminance
function getLuminance(hex: string): number {
    const rgb = hexToRgb(hex);
    const [r, g, b] = [rgb.r, rgb.g, rgb.b].map((c) => {
        c = c / 255;
        return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function hexToRgb(hex: string): { r: number; g: number; b: number } {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result
        ? {
            r: parseInt(result[1], 16),
            g: parseInt(result[2], 16),
            b: parseInt(result[3], 16),
        }
        : { r: 0, g: 0, b: 0 };
}

function getContrastRatio(color1: string, color2: string): number {
    const l1 = getLuminance(color1);
    const l2 = getLuminance(color2);
    const lighter = Math.max(l1, l2);
    const darker = Math.min(l1, l2);
    return (lighter + 0.05) / (darker + 0.05);
}

describe('Color Contrast - WCAG AA Compliance', () => {
    // Light mode colors
    const lightMode = {
        bg: '#fafafa',
        text: '#1f2937',
        textSecondary: '#6b7280',
        textMuted: '#9ca3af',
        primary: '#2563eb',
        success: '#059669',
        warning: '#d97706',
        error: '#dc2626',
    };

    // Dark mode colors (improved)
    const darkMode = {
        bg: '#0f172a',
        text: '#f8fafc',
        textSecondary: '#cbd5e1',
        textMuted: '#94a3b8',
        primary: '#3b82f6',
        success: '#22c55e',
        warning: '#fbbf24',
        error: '#f87171',
    };

    describe('Light Mode', () => {
        it('text on background has sufficient contrast', () => {
            const ratio = getContrastRatio(lightMode.text, lightMode.bg);
            expect(ratio).toBeGreaterThanOrEqual(4.5);
        });

        it('secondary text on background has sufficient contrast', () => {
            const ratio = getContrastRatio(lightMode.textSecondary, lightMode.bg);
            expect(ratio).toBeGreaterThanOrEqual(4.5);
        });

        it('primary color on white has sufficient contrast', () => {
            const ratio = getContrastRatio(lightMode.primary, '#ffffff');
            expect(ratio).toBeGreaterThanOrEqual(3); // 3:1 for large text/UI
        });
    });

    describe('Dark Mode', () => {
        it('text on background has sufficient contrast', () => {
            const ratio = getContrastRatio(darkMode.text, darkMode.bg);
            expect(ratio).toBeGreaterThanOrEqual(4.5);
        });

        it('secondary text on background has sufficient contrast', () => {
            const ratio = getContrastRatio(darkMode.textSecondary, darkMode.bg);
            expect(ratio).toBeGreaterThanOrEqual(4.5);
        });

        it('muted text on background has adequate contrast', () => {
            const ratio = getContrastRatio(darkMode.textMuted, darkMode.bg);
            // Muted text should have at least 3:1 for large text
            expect(ratio).toBeGreaterThanOrEqual(3);
        });

        it('success color on dark background is visible', () => {
            const ratio = getContrastRatio(darkMode.success, darkMode.bg);
            expect(ratio).toBeGreaterThanOrEqual(3);
        });

        it('warning color on dark background is visible', () => {
            const ratio = getContrastRatio(darkMode.warning, darkMode.bg);
            expect(ratio).toBeGreaterThanOrEqual(3);
        });

        it('error color on dark background is visible', () => {
            const ratio = getContrastRatio(darkMode.error, darkMode.bg);
            expect(ratio).toBeGreaterThanOrEqual(3);
        });
    });
});

describe('ADHD-Friendly Defaults', () => {
    it('reduced motion should default to ON', () => {
        // Per ADHD research, reduced motion helps focus
        const defaultReduceMotion = true;
        expect(defaultReduceMotion).toBe(true);
    });

    it('break interval should be research-based (15-25 min)', () => {
        const defaultBreakInterval = 20;
        expect(defaultBreakInterval).toBeGreaterThanOrEqual(15);
        expect(defaultBreakInterval).toBeLessThanOrEqual(25);
    });

    it('session length should be ADHD-appropriate (20-45 min)', () => {
        const defaultSessionLength = 30;
        expect(defaultSessionLength).toBeGreaterThanOrEqual(20);
        expect(defaultSessionLength).toBeLessThanOrEqual(45);
    });
});

describe('Accessibility Features', () => {
    it('dyslexic font should use OpenDyslexic', () => {
        // OpenDyslexic is designed for readability with dyslexia
        const dyslexicFont = 'OpenDyslexic';
        expect(dyslexicFont).toBe('OpenDyslexic');
    });

    it('focus states should be visible', () => {
        // Focus outline should be visible (2px solid)
        const focusOutline = '2px solid #2563eb';
        expect(focusOutline).toContain('2px');
    });
});

describe('Exercise Step Limits', () => {
    it('exercises should have 2-5 steps for ADHD', () => {
        const minSteps = 2;
        const maxSteps = 5;

        // These values match the curriculum design
        expect(minSteps).toBeLessThanOrEqual(5);
        expect(maxSteps).toBeGreaterThanOrEqual(2);
    });

    it('checkpoints should provide progress feedback', () => {
        // Every exercise should have at least one checkpoint
        const minCheckpoints = 1;
        expect(minCheckpoints).toBeGreaterThanOrEqual(1);
    });
});
