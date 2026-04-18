/**
 * TutorChat component for AI tutor interactions.
 */
import { useState, useRef, useEffect } from 'react';
import type { TutorResponse, Step } from '../../types';
import { tutorApi } from '../../services/api';
import clsx from 'clsx';

interface Message {
    id: string;
    role: 'student' | 'tutor';
    content: string;
    timestamp: Date;
}

interface TutorChatProps {
    sessionId?: number;
    currentStep?: number;
    currentCode?: string;
    currentStepObj?: Step;
    onPointsEarned?: (points: number) => void;
}

/**
 * Format message content with basic markdown support for code blocks
 */
function FormattedMessage({ content, isStudent }: { content: string; isStudent: boolean }) {
    // Split content by code blocks (```...```)
    const parts = content.split(/(```[\s\S]*?```)/g);
    
    return (
        <div className="space-y-2">
            {parts.map((part, index) => {
                // Check if this is a code block
                if (part.startsWith('```') && part.endsWith('```')) {
                    // Extract language and code
                    const lines = part.slice(3, -3).split('\n');
                    const firstLine = lines[0].trim();
                    const hasLang = firstLine && !firstLine.includes(' ') && firstLine.length < 20;
                    const language = hasLang ? firstLine : '';
                    const code = hasLang ? lines.slice(1).join('\n') : lines.join('\n');
                    
                    return (
                        <div key={index} className="rounded-md overflow-hidden">
                            {language && (
                                <div className="bg-gray-700 dark:bg-gray-900 px-3 py-1 text-xs text-gray-300 font-mono">
                                    {language}
                                </div>
                            )}
                            <pre className={clsx(
                                "p-3 text-sm font-mono overflow-x-auto",
                                isStudent 
                                    ? "bg-blue-900/50 text-blue-100" 
                                    : "bg-gray-800 dark:bg-gray-900 text-gray-100"
                            )}>
                                <code>{code.trim()}</code>
                            </pre>
                        </div>
                    );
                }
                
                // Check for inline code (`...`)
                const inlineParts = part.split(/(`[^`]+`)/g);
                
                return (
                    <p key={index} className="whitespace-pre-wrap text-sm leading-relaxed">
                        {inlineParts.map((inlinePart, inlineIndex) => {
                            if (inlinePart.startsWith('`') && inlinePart.endsWith('`')) {
                                return (
                                    <code 
                                        key={inlineIndex}
                                        className={clsx(
                                            "px-1.5 py-0.5 rounded font-mono text-xs",
                                            isStudent
                                                ? "bg-blue-900/50 text-blue-100"
                                                : "bg-gray-200 dark:bg-gray-700 text-pink-600 dark:text-pink-400"
                                        )}
                                    >
                                        {inlinePart.slice(1, -1)}
                                    </code>
                                );
                            }
                            return <span key={inlineIndex}>{inlinePart}</span>;
                        })}
                    </p>
                );
            })}
        </div>
    );
}

export function TutorChat({
    sessionId,
    currentStep,
    currentCode,
    currentStepObj,
    onPointsEarned,
}: TutorChatProps) {
    const getWelcomeMessage = () => {
        if (currentStepObj) {
            return `Hi! I'm here to help with Step ${currentStepObj.number}: "${currentStepObj.title}". Ask me anything!`;
        }
        return "Hi! I'm your coding tutor. Ask me anything about Python or your current exercise.";
    };

    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            role: 'tutor',
            content: getWelcomeMessage(),
            timestamp: new Date(),
        },
    ]);

    // Update welcome message when step changes
    useEffect(() => {
        setMessages([{
            id: 'welcome',
            role: 'tutor',
            content: getWelcomeMessage(),
            timestamp: new Date(),
        }]);
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [currentStepObj?.number]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesContainerRef = useRef<HTMLDivElement>(null);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        // Scroll within the container, not the whole page
        if (messagesContainerRef.current) {
            messagesContainerRef.current.scrollTop = messagesContainerRef.current.scrollHeight;
        }
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: `user-${Date.now()}`,
            role: 'student',
            content: input.trim(),
            timestamp: new Date(),
        };

        setMessages((prev) => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response: TutorResponse = await tutorApi.sendMessage({
                message: userMessage.content,
                session_id: sessionId,
                current_step: currentStep,
                current_code: currentCode,
            });

            const tutorMessage: Message = {
                id: `tutor-${Date.now()}`,
                role: 'tutor',
                content: response.response,
                timestamp: new Date(),
            };

            setMessages((prev) => [...prev, tutorMessage]);

            if (response.points_earned > 0 && onPointsEarned) {
                onPointsEarned(response.points_earned);
            }
        } catch (error) {
            const errorMessage: Message = {
                id: `error-${Date.now()}`,
                role: 'tutor',
                content: 'Sorry, I had trouble responding. Please try again.',
                timestamp: new Date(),
            };
            setMessages((prev) => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    return (
        <div className="card flex flex-col border-2 border-[var(--color-border)]">
            <div className="flex items-center gap-2 mb-4 pb-3 border-b border-[var(--color-border)]">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 5a2 2 0 012-2h7a2 2 0 012 2v4a2 2 0 01-2 2H9l-3 3v-3H4a2 2 0 01-2-2V5z" />
                        <path d="M15 7v2a4 4 0 01-4 4H9.828l-1.766 1.767c.28.149.599.233.938.233h2l3 3v-3h2a2 2 0 002-2V9a2 2 0 00-2-2h-1z" />
                    </svg>
                </div>
                <div>
                    <h3 className="font-semibold text-base">Coding Tutor</h3>
                    <p className="text-xs text-[var(--color-text-muted)]">Ask me anything!</p>
                </div>
            </div>

            {/* Messages - with fixed height and scroll */}
            <div 
                ref={messagesContainerRef}
                className="flex-1 overflow-y-auto space-y-3 mb-4 min-h-[250px] max-h-[350px] pr-2 scrollbar-thin"
            >
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={clsx(
                            'p-3 rounded-xl max-w-[90%]',
                            message.role === 'student'
                                ? 'bg-[var(--color-primary)] text-white ml-auto rounded-br-md'
                                : 'bg-[var(--color-bg-secondary)] border border-[var(--color-border)] rounded-bl-md'
                        )}
                    >
                        <FormattedMessage content={message.content} isStudent={message.role === 'student'} />
                    </div>
                ))}

                {isLoading && (
                    <div className="bg-[var(--color-bg-secondary)] border border-[var(--color-border)] p-3 rounded-xl rounded-bl-md max-w-[90%]">
                        <div className="flex items-center gap-2">
                            <div className="flex gap-1">
                                <span className="w-2 h-2 bg-[var(--color-primary)] rounded-full animate-bounce" />
                                <span
                                    className="w-2 h-2 bg-[var(--color-primary)] rounded-full animate-bounce"
                                    style={{ animationDelay: '0.15s' }}
                                />
                                <span
                                    className="w-2 h-2 bg-[var(--color-primary)] rounded-full animate-bounce"
                                    style={{ animationDelay: '0.3s' }}
                                />
                            </div>
                            <span className="text-sm text-[var(--color-text-secondary)]">Thinking...</span>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="flex gap-2 pt-3 border-t border-[var(--color-border)]">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a question..."
                    className="input flex-1 text-sm"
                    disabled={isLoading}
                />
                <button
                    onClick={handleSend}
                    disabled={isLoading || !input.trim()}
                    className="btn btn-primary px-4"
                >
                    <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
                    </svg>
                </button>
            </div>
        </div>
    );
}
