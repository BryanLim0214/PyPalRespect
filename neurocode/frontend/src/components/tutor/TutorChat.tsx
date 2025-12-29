/**
 * TutorChat component for AI tutor interactions.
 */
import { useState, useRef, useEffect } from 'react';
import type { TutorResponse } from '../../types';
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
    onPointsEarned?: (points: number) => void;
}

export function TutorChat({
    sessionId,
    currentStep,
    currentCode,
    onPointsEarned,
}: TutorChatProps) {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: 'welcome',
            role: 'tutor',
            content: "Hi! I'm your coding tutor. Ask me anything about Python or your current exercise.",
            timestamp: new Date(),
        },
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
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
        <div className="card flex flex-col h-full">
            <h3 className="font-semibold text-lg mb-4">Coding Tutor</h3>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto space-y-4 mb-4 min-h-[200px] max-h-[400px]">
                {messages.map((message) => (
                    <div
                        key={message.id}
                        className={clsx(
                            'p-3 rounded-lg max-w-[85%]',
                            message.role === 'student'
                                ? 'bg-[var(--color-primary)] text-white ml-auto'
                                : 'bg-[var(--color-bg-secondary)]'
                        )}
                    >
                        <p className="whitespace-pre-wrap text-sm">{message.content}</p>
                    </div>
                ))}

                {isLoading && (
                    <div className="bg-[var(--color-bg-secondary)] p-3 rounded-lg max-w-[85%]">
                        <div className="flex items-center gap-2">
                            <div className="flex gap-1">
                                <span className="w-2 h-2 bg-[var(--color-text-muted)] rounded-full animate-bounce" />
                                <span
                                    className="w-2 h-2 bg-[var(--color-text-muted)] rounded-full animate-bounce"
                                    style={{ animationDelay: '0.1s' }}
                                />
                                <span
                                    className="w-2 h-2 bg-[var(--color-text-muted)] rounded-full animate-bounce"
                                    style={{ animationDelay: '0.2s' }}
                                />
                            </div>
                            <span className="text-sm text-[var(--color-text-secondary)]">Thinking...</span>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="flex gap-2">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Ask a question..."
                    className="input flex-1"
                    disabled={isLoading}
                />
                <button
                    onClick={handleSend}
                    disabled={isLoading || !input.trim()}
                    className="btn btn-primary"
                >
                    Send
                </button>
            </div>
        </div>
    );
}
