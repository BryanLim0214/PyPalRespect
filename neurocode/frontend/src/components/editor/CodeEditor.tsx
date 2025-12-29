/**
 * CodeEditor component using CodeMirror 6.
 * Professional Python code editor with syntax highlighting.
 */
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';
import { useThemeStore } from '../../stores';

interface CodeEditorProps {
    value: string;
    onChange: (value: string) => void;
    placeholder?: string;
    readOnly?: boolean;
    height?: string;
}

export function CodeEditor({
    value,
    onChange,
    placeholder = '# Write your Python code here',
    readOnly = false,
    height = '300px',
}: CodeEditorProps) {
    const { themeMode } = useThemeStore();

    return (
        <div className="rounded-lg overflow-hidden border border-[var(--color-border)]">
            <CodeMirror
                value={value}
                height={height}
                extensions={[python()]}
                theme={themeMode === 'dark' ? oneDark : undefined}
                onChange={(val) => onChange(val)}
                placeholder={placeholder}
                readOnly={readOnly}
                basicSetup={{
                    lineNumbers: true,
                    highlightActiveLineGutter: true,
                    highlightSpecialChars: true,
                    history: true,
                    foldGutter: false,
                    drawSelection: true,
                    dropCursor: true,
                    allowMultipleSelections: false,
                    indentOnInput: true,
                    syntaxHighlighting: true,
                    bracketMatching: true,
                    closeBrackets: true,
                    autocompletion: true,
                    rectangularSelection: false,
                    crosshairCursor: false,
                    highlightActiveLine: true,
                    highlightSelectionMatches: true,
                    closeBracketsKeymap: true,
                    defaultKeymap: true,
                    searchKeymap: true,
                    historyKeymap: true,
                    foldKeymap: false,
                    completionKeymap: true,
                    lintKeymap: true,
                    tabSize: 4,
                }}
                style={{
                    fontSize: '15px',
                    fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
                }}
            />
        </div>
    );
}
