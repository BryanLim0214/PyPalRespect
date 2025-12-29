# NeuroCode: ADHD-Focused Python Tutor for Middle Schoolers
## Complete Implementation Guide for Cursor/Windsurf IDE

**Target Audience:** Middle school students (grades 6-8, ages 11-14) with ADHD  
**Tech Stack:** FastAPI + React + TypeScript + Gemini API + PostgreSQL  
**Research Context:** RESPECT 2026 Conference Submission  

---

## TABLE OF CONTENTS

1. [Project Overview](#1-project-overview)
2. [Architecture & Tech Stack](#2-architecture--tech-stack)
3. [Project Structure](#3-project-structure)
4. [Backend Implementation](#4-backend-implementation)
5. [Frontend Implementation](#5-frontend-implementation)
6. [Gemini API Integration](#6-gemini-api-integration)
7. [ADHD-Specific Features](#7-adhd-specific-features)
8. [Database Schema](#8-database-schema)
9. [COPPA Compliance](#9-coppa-compliance)
10. [Python Curriculum](#10-python-curriculum)
11. [Research Data Collection](#11-research-data-collection)
12. [Deployment](#12-deployment)
13. [Testing Strategy](#13-testing-strategy)

---

## 1. PROJECT OVERVIEW

### 1.1 What We're Building

NeuroCode is an LLM-powered adaptive Python programming tutor specifically designed for middle school students (ages 11-14) with ADHD. It addresses the gap identified in research: **no existing tool combines AI tutoring + programming education + ADHD-specific accommodations**.

### 1.2 Core Features

- **Micro-task decomposition**: Break coding problems into tiny, manageable steps
- **Interest-based engagement**: Generate coding exercises around student interests (games, art, music)
- **Gamification with immediate rewards**: Points, badges, progress visualization
- **Simplified IDE**: Distraction-free code editor with ADHD-friendly design
- **Adaptive hints**: LLM-powered hints that adjust to frustration levels
- **Time awareness tools**: Visual timers, break reminders, session pacing
- **Progress tracking**: For both students and researchers

### 1.3 Key Constraints

- **COPPA Compliance**: Students under 13 require verifiable parental consent
- **Age-appropriate content**: All interactions must be suitable for 11-14 year olds
- **Accessibility**: Follow WCAG 2.1 AA guidelines
- **Data minimization**: Collect only what's needed for research

---

## 2. ARCHITECTURE & TECH STACK

### 2.1 Technology Choices (Verified December 2025)

```
BACKEND:
├── Python 3.11+
├── FastAPI (async, automatic OpenAPI docs)
├── SQLAlchemy 2.0 (async ORM)
├── PostgreSQL 15+ (database)
├── Alembic (migrations)
├── Pydantic 2.0 (validation)
└── google-genai (NEW Gemini SDK - NOT google-generativeai which is deprecated)

FRONTEND:
├── React 18 + TypeScript
├── Vite (build tool)
├── @uiw/react-codemirror (code editor)
├── @codemirror/lang-python (Python syntax)
├── TailwindCSS (styling)
├── Framer Motion (animations - used sparingly for ADHD)
└── React Query / TanStack Query (data fetching)

INFRASTRUCTURE:
├── Docker + Docker Compose
├── Railway / Render (hosting)
└── GitHub Actions (CI/CD)
```

### 2.2 Why These Choices?

| Technology | Reason |
|------------|--------|
| FastAPI | Async support, auto-docs, great for LLM streaming |
| google-genai | Official Google SDK (GA as of May 2025), replaces deprecated google-generativeai |
| React + Vite | Fast dev experience, modern tooling |
| CodeMirror 6 | Lightweight, customizable, good accessibility |
| PostgreSQL | Robust, good for analytics queries |
| TailwindCSS | Rapid prototyping, easy to maintain consistent styles |

---

## 3. PROJECT STRUCTURE

```
neurocode/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app entry
│   │   ├── config.py               # Settings/environment
│   │   ├── database.py             # SQLAlchemy setup
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # User/Student models
│   │   │   ├── session.py          # Learning session models
│   │   │   ├── progress.py         # Progress tracking
│   │   │   └── consent.py          # Parental consent records
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # Pydantic schemas
│   │   │   ├── tutor.py            # Tutor request/response
│   │   │   └── analytics.py        # Research data schemas
│   │   ├── routers/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # Authentication routes
│   │   │   ├── tutor.py            # LLM tutoring routes
│   │   │   ├── exercises.py        # Exercise management
│   │   │   ├── progress.py         # Progress tracking
│   │   │   └── admin.py            # Teacher/researcher dashboard
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── gemini_service.py   # Gemini API wrapper
│   │   │   ├── task_decomposer.py  # Break problems into steps
│   │   │   ├── hint_generator.py   # Adaptive hint system
│   │   │   ├── engagement.py       # Interest-based personalization
│   │   │   └── analytics.py        # Research data collection
│   │   ├── prompts/
│   │   │   ├── __init__.py
│   │   │   ├── system_prompts.py   # ADHD-aware system prompts
│   │   │   ├── decomposition.py    # Task breakdown prompts
│   │   │   └── feedback.py         # Celebration/encouragement
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── code_runner.py      # Safe Python execution
│   │       └── validators.py       # Input validation
│   ├── alembic/                    # Database migrations
│   ├── tests/
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── CodeEditor/
│   │   │   │   ├── CodeEditor.tsx
│   │   │   │   ├── OutputPanel.tsx
│   │   │   │   └── RunButton.tsx
│   │   │   ├── Tutor/
│   │   │   │   ├── TutorChat.tsx
│   │   │   │   ├── HintPanel.tsx
│   │   │   │   └── StepProgress.tsx
│   │   │   ├── Gamification/
│   │   │   │   ├── PointsDisplay.tsx
│   │   │   │   ├── BadgeCollection.tsx
│   │   │   │   └── Celebration.tsx
│   │   │   ├── ADHD/
│   │   │   │   ├── FocusTimer.tsx
│   │   │   │   ├── BreakReminder.tsx
│   │   │   │   └── ProgressBar.tsx
│   │   │   └── Layout/
│   │   │       ├── SimplifiedLayout.tsx
│   │   │       └── Navigation.tsx
│   │   ├── pages/
│   │   │   ├── Login.tsx
│   │   │   ├── Dashboard.tsx
│   │   │   ├── Exercise.tsx
│   │   │   └── Profile.tsx
│   │   ├── hooks/
│   │   │   ├── useTutor.ts
│   │   │   ├── useProgress.ts
│   │   │   └── useTimer.ts
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## 4. BACKEND IMPLEMENTATION

### 4.1 Environment Setup

```bash
# Create project directory
mkdir neurocode && cd neurocode

# Backend setup
mkdir backend && cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy[asyncio] asyncpg alembic pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] python-multipart google-genai httpx

# Create pyproject.toml
```

**pyproject.toml:**
```toml
[project]
name = "neurocode-backend"
version = "0.1.0"
description = "ADHD-focused Python tutor backend"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy[asyncio]>=2.0.25",
    "asyncpg>=0.29.0",
    "alembic>=1.13.0",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
    "python-jose[cryptography]>=3.3.0",
    "passlib[bcrypt]>=1.7.4",
    "python-multipart>=0.0.6",
    "google-genai>=1.0.0",
    "httpx>=0.26.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.23.0",
    "httpx>=0.26.0",
]
```

### 4.2 Configuration (app/config.py)

```python
"""
Application configuration with environment variable support.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # App
    APP_NAME: str = "NeuroCode"
    DEBUG: bool = False
    SECRET_KEY: str
    
    # Database
    DATABASE_URL: str
    
    # Gemini API (NEW SDK)
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.5-flash"  # Cost-effective for education
    
    # COPPA Compliance
    REQUIRE_PARENTAL_CONSENT: bool = True
    MIN_AGE_WITHOUT_CONSENT: int = 13
    
    # Session settings
    SESSION_TIMEOUT_MINUTES: int = 45  # Recommended max for ADHD
    BREAK_REMINDER_MINUTES: int = 20   # Suggest breaks
    
    # Research
    ENABLE_ANALYTICS: bool = True
    ANONYMIZE_DATA: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance."""
    return Settings()
```

### 4.3 Database Setup (app/database.py)

```python
"""
Async SQLAlchemy database configuration.
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.config import get_settings

settings = get_settings()

# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"),
    echo=settings.DEBUG,
    pool_size=5,
    max_overflow=10,
)

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


async def get_db() -> AsyncSession:
    """Dependency for getting database sessions."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
```

### 4.4 User Models (app/models/user.py)

```python
"""
User and consent models with COPPA compliance fields.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class ADHDProfile(enum.Enum):
    """ADHD presentation types for personalization."""
    PREDOMINANTLY_INATTENTIVE = "inattentive"
    PREDOMINANTLY_HYPERACTIVE = "hyperactive"
    COMBINED = "combined"
    NOT_SPECIFIED = "not_specified"


class User(Base):
    """
    Student user model.
    
    COPPA Note: For users under 13, we collect minimal PII and require
    parental consent before any data collection.
    """
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Authentication (minimal PII)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    
    # Age verification (COPPA)
    birth_year: Mapped[int] = mapped_column(Integer)  # Only year, not full DOB
    grade_level: Mapped[int] = mapped_column(Integer)  # 6, 7, or 8
    
    # Consent tracking
    has_parental_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    parent_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    
    # ADHD-specific (optional, only with consent)
    adhd_profile: Mapped[Optional[ADHDProfile]] = mapped_column(
        Enum(ADHDProfile), nullable=True, default=ADHDProfile.NOT_SPECIFIED
    )
    
    # Preferences (for personalization)
    interests: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON array
    preferred_break_interval: Mapped[int] = mapped_column(Integer, default=20)  # minutes
    preferred_session_length: Mapped[int] = mapped_column(Integer, default=30)  # minutes
    
    # Accessibility
    dyslexia_font: Mapped[bool] = mapped_column(Boolean, default=False)
    high_contrast: Mapped[bool] = mapped_column(Boolean, default=False)
    reduce_animations: Mapped[bool] = mapped_column(Boolean, default=True)  # Default ON for ADHD
    
    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_active: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Relationships
    sessions: Mapped[list["LearningSession"]] = relationship(back_populates="user")
    progress: Mapped[list["ExerciseProgress"]] = relationship(back_populates="user")


class ParentalConsent(Base):
    """
    COPPA-compliant parental consent record.
    
    This stores verification that a parent/guardian has consented to their
    child's participation in the research study and use of the platform.
    """
    __tablename__ = "parental_consents"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    
    # Parent info (minimal)
    parent_email: Mapped[str] = mapped_column(String(255))
    
    # Consent details
    consent_given: Mapped[bool] = mapped_column(Boolean, default=False)
    consent_timestamp: Mapped[datetime] = mapped_column(DateTime)
    consent_method: Mapped[str] = mapped_column(String(50))  # "email_link", "signed_form"
    consent_ip: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)
    
    # Research consent (separate from platform consent)
    research_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    data_sharing_consent: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Revocation
    revoked: Mapped[bool] = mapped_column(Boolean, default=False)
    revoked_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
```

### 4.5 Main FastAPI App (app/main.py)

```python
"""
NeuroCode FastAPI Application Entry Point.
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import engine, Base
from app.routers import auth, tutor, exercises, progress, admin

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title="NeuroCode API",
    description="ADHD-focused Python programming tutor for middle schoolers",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tutor.router, prefix="/api/tutor", tags=["Tutor"])
app.include_router(exercises.router, prefix="/api/exercises", tags=["Exercises"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.APP_NAME}
```

---

## 5. FRONTEND IMPLEMENTATION

### 5.1 Frontend Setup

```bash
cd .. # Back to neurocode root
npm create vite@latest frontend -- --template react-ts
cd frontend

# Install dependencies
npm install @uiw/react-codemirror @codemirror/lang-python @codemirror/theme-one-dark
npm install @tanstack/react-query axios framer-motion
npm install -D tailwindcss postcss autoprefixer @types/node
npx tailwindcss init -p
```

### 5.2 Vite Configuration (vite.config.ts)

```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
});
```

### 5.3 Tailwind Configuration (tailwind.config.js)

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      // ADHD-friendly color palette
      colors: {
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        },
        // Calm, low-stimulation colors
        calm: {
          bg: '#f8fafc',      // Very light gray
          surface: '#ffffff',
          border: '#e2e8f0',
          text: '#1e293b',
        },
        // Celebration colors (used sparingly)
        success: '#10b981',
        warning: '#f59e0b',
      },
      // OpenDyslexic font option
      fontFamily: {
        dyslexic: ['OpenDyslexic', 'sans-serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      // Reduced motion by default
      animation: {
        'fade-in': 'fadeIn 0.2s ease-out',
        'slide-up': 'slideUp 0.2s ease-out',
      },
    },
  },
  plugins: [],
};
```

### 5.4 Code Editor Component (src/components/CodeEditor/CodeEditor.tsx)

```tsx
/**
 * ADHD-friendly Python code editor using CodeMirror 6.
 * 
 * Design principles:
 * - Minimal visual clutter
 * - Large, readable text
 * - Clear syntax highlighting
 * - Reduced animations
 */
import React, { useCallback, useState } from 'react';
import CodeMirror from '@uiw/react-codemirror';
import { python } from '@codemirror/lang-python';
import { EditorView } from '@codemirror/view';

interface CodeEditorProps {
  initialCode?: string;
  onCodeChange?: (code: string) => void;
  onRun?: (code: string) => void;
  readOnly?: boolean;
  fontSize?: number;
  useDyslexicFont?: boolean;
}

// Custom theme optimized for ADHD/readability
const adhdFriendlyTheme = EditorView.theme({
  '&': {
    fontSize: '16px',
    backgroundColor: '#fafafa',
  },
  '.cm-content': {
    fontFamily: '"JetBrains Mono", monospace',
    lineHeight: '1.6',
    padding: '16px',
  },
  '.cm-line': {
    padding: '2px 0',
  },
  '.cm-gutters': {
    backgroundColor: '#f1f5f9',
    color: '#64748b',
    border: 'none',
    paddingRight: '8px',
  },
  '.cm-activeLineGutter': {
    backgroundColor: '#e2e8f0',
  },
  '.cm-activeLine': {
    backgroundColor: '#f1f5f9',
  },
  // High contrast cursor
  '.cm-cursor': {
    borderLeftColor: '#3b82f6',
    borderLeftWidth: '3px',
  },
  // Selection
  '.cm-selectionBackground': {
    backgroundColor: '#bfdbfe !important',
  },
});

export const CodeEditor: React.FC<CodeEditorProps> = ({
  initialCode = '# Write your Python code here\n\n',
  onCodeChange,
  onRun,
  readOnly = false,
  fontSize = 16,
  useDyslexicFont = false,
}) => {
  const [code, setCode] = useState(initialCode);

  const handleChange = useCallback(
    (value: string) => {
      setCode(value);
      onCodeChange?.(value);
    },
    [onCodeChange]
  );

  const handleRun = () => {
    onRun?.(code);
  };

  return (
    <div className="flex flex-col h-full bg-calm-surface rounded-lg border border-calm-border overflow-hidden">
      {/* Toolbar - Simple, not overwhelming */}
      <div className="flex items-center justify-between px-4 py-3 bg-calm-bg border-b border-calm-border">
        <span className="text-sm font-medium text-calm-text">Python Editor</span>
        <button
          onClick={handleRun}
          className="px-4 py-2 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium text-sm transition-colors focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2"
          aria-label="Run your code"
        >
          ▶ Run Code
        </button>
      </div>

      {/* Editor */}
      <div className="flex-1 overflow-auto">
        <CodeMirror
          value={code}
          onChange={handleChange}
          extensions={[python(), adhdFriendlyTheme]}
          readOnly={readOnly}
          basicSetup={{
            lineNumbers: true,
            highlightActiveLineGutter: true,
            highlightActiveLine: true,
            foldGutter: false, // Reduce complexity
            dropCursor: true,
            allowMultipleSelections: false, // Simpler
            indentOnInput: true,
            bracketMatching: true,
            closeBrackets: true,
            autocompletion: true,
            rectangularSelection: false,
            crosshairCursor: false,
            highlightSelectionMatches: false, // Reduce visual noise
            closeBracketsKeymap: true,
            searchKeymap: false, // Simplify
            foldKeymap: false,
            completionKeymap: true,
            lintKeymap: false,
          }}
          style={{
            fontSize: `${fontSize}px`,
            fontFamily: useDyslexicFont
              ? '"OpenDyslexic", monospace'
              : '"JetBrains Mono", monospace',
          }}
        />
      </div>
    </div>
  );
};
```

### 5.5 Tutor Chat Component (src/components/Tutor/TutorChat.tsx)

```tsx
/**
 * ADHD-friendly tutor chat interface.
 * 
 * Design principles:
 * - Clear, chunked messages
 * - Visual step indicators
 * - Encouraging tone
 * - No overwhelming walls of text
 */
import React, { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface Message {
  id: string;
  role: 'tutor' | 'student';
  content: string;
  timestamp: Date;
  isStep?: boolean;
  stepNumber?: number;
  totalSteps?: number;
}

interface TutorChatProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
  reduceAnimations?: boolean;
}

export const TutorChat: React.FC<TutorChatProps> = ({
  messages,
  onSendMessage,
  isLoading = false,
  reduceAnimations = true,
}) => {
  const [input, setInput] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: reduceAnimations ? 'auto' : 'smooth' });
  }, [messages, reduceAnimations]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  // Quick response buttons for common questions
  const quickResponses = [
    "I'm stuck",
    "Give me a hint",
    "Explain that again",
    "I did it! ✓",
  ];

  return (
    <div className="flex flex-col h-full bg-calm-surface rounded-lg border border-calm-border">
      {/* Header */}
      <div className="px-4 py-3 bg-calm-bg border-b border-calm-border">
        <h2 className="font-semibold text-calm-text">Your Coding Buddy</h2>
        <p className="text-sm text-gray-500">Ask me anything about Python!</p>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        <AnimatePresence>
          {messages.map((message) => (
            <motion.div
              key={message.id}
              initial={reduceAnimations ? false : { opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className={`flex ${message.role === 'student' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                  message.role === 'student'
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-calm-text'
                }`}
              >
                {/* Step indicator for tutor messages */}
                {message.isStep && message.stepNumber && (
                  <div className="flex items-center gap-2 mb-2 text-sm font-medium">
                    <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-primary-500 text-white text-xs">
                      {message.stepNumber}
                    </span>
                    <span className="text-gray-500">
                      Step {message.stepNumber} of {message.totalSteps}
                    </span>
                  </div>
                )}
                
                {/* Message content - using larger text for readability */}
                <p className="text-base leading-relaxed whitespace-pre-wrap">
                  {message.content}
                </p>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl px-4 py-3">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-75" />
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick response buttons */}
      <div className="px-4 py-2 border-t border-calm-border">
        <div className="flex flex-wrap gap-2">
          {quickResponses.map((response) => (
            <button
              key={response}
              onClick={() => onSendMessage(response)}
              className="px-3 py-1.5 text-sm bg-gray-100 hover:bg-gray-200 text-calm-text rounded-full transition-colors"
            >
              {response}
            </button>
          ))}
        </div>
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="p-4 border-t border-calm-border">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your question..."
            className="flex-1 px-4 py-3 text-base border border-calm-border rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="px-6 py-3 bg-primary-600 hover:bg-primary-700 disabled:bg-gray-300 text-white rounded-lg font-medium transition-colors"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};
```

### 5.6 Progress Bar Component (src/components/ADHD/ProgressBar.tsx)

```tsx
/**
 * Visual progress indicator for ADHD learners.
 * 
 * Research basis: Robertson et al. (2020) found that visual progress
 * indicators help ADHD students with task completion by providing
 * external executive function scaffolding.
 */
import React from 'react';
import { motion } from 'framer-motion';

interface ProgressBarProps {
  currentStep: number;
  totalSteps: number;
  stepLabels?: string[];
  showLabels?: boolean;
  reduceAnimations?: boolean;
}

export const ProgressBar: React.FC<ProgressBarProps> = ({
  currentStep,
  totalSteps,
  stepLabels = [],
  showLabels = true,
  reduceAnimations = true,
}) => {
  const progress = (currentStep / totalSteps) * 100;

  return (
    <div className="w-full">
      {/* Progress bar */}
      <div className="relative h-4 bg-gray-200 rounded-full overflow-hidden">
        <motion.div
          className="absolute inset-y-0 left-0 bg-gradient-to-r from-primary-500 to-primary-600 rounded-full"
          initial={{ width: 0 }}
          animate={{ width: `${progress}%` }}
          transition={{ duration: reduceAnimations ? 0 : 0.3 }}
        />
      </div>

      {/* Step indicators */}
      <div className="flex justify-between mt-2">
        {Array.from({ length: totalSteps }, (_, i) => {
          const stepNum = i + 1;
          const isCompleted = stepNum < currentStep;
          const isCurrent = stepNum === currentStep;

          return (
            <div key={stepNum} className="flex flex-col items-center">
              {/* Step circle */}
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium transition-colors ${
                  isCompleted
                    ? 'bg-success text-white'
                    : isCurrent
                    ? 'bg-primary-600 text-white ring-4 ring-primary-200'
                    : 'bg-gray-200 text-gray-500'
                }`}
              >
                {isCompleted ? '✓' : stepNum}
              </div>

              {/* Step label */}
              {showLabels && stepLabels[i] && (
                <span
                  className={`mt-1 text-xs text-center max-w-16 ${
                    isCurrent ? 'font-medium text-primary-700' : 'text-gray-500'
                  }`}
                >
                  {stepLabels[i]}
                </span>
              )}
            </div>
          );
        })}
      </div>

      {/* Encouragement message */}
      <div className="mt-4 text-center">
        <p className="text-sm text-gray-600">
          {currentStep === totalSteps
            ? '🎉 Almost done! Just one more step!'
            : `Step ${currentStep} of ${totalSteps} - You're doing great!`}
        </p>
      </div>
    </div>
  );
};
```

---

## 6. GEMINI API INTEGRATION

### 6.1 Gemini Service (app/services/gemini_service.py)

```python
"""
Gemini API integration using the NEW google-genai SDK.

IMPORTANT: This uses the new SDK (google-genai), NOT the deprecated
google-generativeai package. The old package reached end-of-life on
November 30, 2025.

Reference: https://pypi.org/project/google-genai/
"""
from google import genai
from google.genai import types
from typing import AsyncGenerator, Optional
import logging

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class GeminiService:
    """
    Service for interacting with Google's Gemini API.
    
    Uses gemini-2.5-flash for cost-effective educational interactions.
    """
    
    def __init__(self):
        """Initialize Gemini client with API key."""
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL  # "gemini-2.5-flash"
    
    async def generate_response(
        self,
        user_message: str,
        system_prompt: str,
        conversation_history: Optional[list] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        """
        Generate a response from Gemini.
        
        Args:
            user_message: The student's message
            system_prompt: System instructions for ADHD-aware tutoring
            conversation_history: Previous messages for context
            temperature: Creativity level (0.7 is good for education)
            max_tokens: Maximum response length
            
        Returns:
            The tutor's response text
        """
        # Build conversation contents
        contents = []
        
        # Add conversation history if provided
        if conversation_history:
            for msg in conversation_history:
                contents.append(
                    types.Content(
                        role=msg["role"],  # "user" or "model"
                        parts=[types.Part(text=msg["content"])]
                    )
                )
        
        # Add current user message
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            )
        )
        
        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                    # Safety settings appropriate for children
                    safety_settings=[
                        types.SafetySetting(
                            category="HARM_CATEGORY_HARASSMENT",
                            threshold="BLOCK_LOW_AND_ABOVE"
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_HATE_SPEECH",
                            threshold="BLOCK_LOW_AND_ABOVE"
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            threshold="BLOCK_LOW_AND_ABOVE"
                        ),
                        types.SafetySetting(
                            category="HARM_CATEGORY_DANGEROUS_CONTENT",
                            threshold="BLOCK_LOW_AND_ABOVE"
                        ),
                    ],
                ),
            )
            
            return response.text
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    async def generate_response_stream(
        self,
        user_message: str,
        system_prompt: str,
        conversation_history: Optional[list] = None,
    ) -> AsyncGenerator[str, None]:
        """
        Stream a response from Gemini for real-time display.
        
        Useful for longer explanations where showing text as it
        generates keeps ADHD learners engaged.
        """
        contents = []
        
        if conversation_history:
            for msg in conversation_history:
                contents.append(
                    types.Content(
                        role=msg["role"],
                        parts=[types.Part(text=msg["content"])]
                    )
                )
        
        contents.append(
            types.Content(
                role="user",
                parts=[types.Part(text=user_message)]
            )
        )
        
        try:
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.7,
                    max_output_tokens=1024,
                ),
            ):
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            logger.error(f"Gemini streaming error: {e}")
            raise


# Singleton instance
gemini_service = GeminiService()
```

### 6.2 System Prompts for ADHD Tutoring (app/prompts/system_prompts.py)

```python
"""
ADHD-aware system prompts for the Python tutor.

These prompts are based on research on ADHD learning needs:
- Micro-task decomposition (Barkley, 2021)
- Interest-based nervous system (Dodson)
- Immediate feedback (Gabay et al., 2018)
- Reduced cognitive load (Sweller)
"""

TUTOR_SYSTEM_PROMPT = """You are a friendly Python programming tutor for middle school students (ages 11-14) with ADHD. Your name is PyBuddy.

## YOUR TEACHING STYLE

1. **Break Everything Down**: Never give a full solution. Break every problem into tiny, numbered steps (max 3-5 steps at a time).

2. **Keep It Short**: Your messages should be SHORT. Maximum 2-3 sentences per response. If you need to explain more, ask if they want to continue.

3. **Be Encouraging**: Celebrate small wins! Use phrases like "Nice!" "You got it!" "Great thinking!" after correct answers.

4. **Stay Concrete**: Use simple words. Avoid jargon. When you must use a programming term, explain it immediately.

5. **One Thing at a Time**: Only ask ONE question or give ONE instruction per message.

6. **Visual When Possible**: Use simple code examples, emoji sparingly, and clear formatting.

## RESPONSE FORMAT

Always structure your responses like this:
- Start with brief acknowledgment of what they said/did
- Give ONE small next step or ONE piece of information
- End with a simple question or clear instruction

## EXAMPLE INTERACTION

Student: "I want to make a game"
PyBuddy: "Cool! Let's start with something small that can grow into a game. 🎮

First, let's make Python print a welcome message. Can you type this and press Run?

```python
print("Welcome to my game!")
```"

Student: "I did it!"
PyBuddy: "Nice work! 🎉 You just wrote your first line of code!

Now let's ask the player their name. Add this line below your first one:

```python
name = input("What is your name? ")
```"

## HANDLING FRUSTRATION

If a student says "I don't get it" or "I'm stuck" or seems frustrated:
1. Don't repeat the same explanation
2. Try a different, simpler approach
3. Break it down even further
4. Use an analogy from games, sports, or everyday life
5. Remind them it's okay to not get it right away

## HANDLING "I'M DONE" OR "I DID IT"

When they complete something:
1. Celebrate briefly (one line)
2. Ask if they want to:
   - Keep going
   - Take a break
   - Try something new

## SAFETY RULES

- Never share inappropriate content
- Keep all examples age-appropriate
- If asked about non-Python topics, gently redirect
- If they seem upset about something serious, suggest they talk to a trusted adult

## REMEMBER

You're talking to a 6th, 7th, or 8th grader. They might:
- Get distracted easily (that's okay!)
- Need things repeated (that's okay!)  
- Want to jump ahead (help them slow down)
- Get frustrated (stay patient and encouraging)

Be the coding buddy they need - patient, fun, and always ready to help!"""


def get_task_decomposition_prompt(task: str, student_interests: list[str]) -> str:
    """
    Generate a prompt for breaking a task into ADHD-friendly steps.
    
    Args:
        task: The coding task to decompose
        student_interests: Student's interests for personalization
    """
    interests_str = ", ".join(student_interests) if student_interests else "games, technology"
    
    return f"""Break down this Python coding task into small, manageable steps for a middle schooler with ADHD.

TASK: {task}

STUDENT INTERESTS: {interests_str}

RULES:
1. Maximum 5-7 steps total
2. Each step should take 1-3 minutes
3. Each step should have a clear, achievable goal
4. Include a checkpoint after every 2-3 steps where they can run their code
5. Make examples relate to their interests when possible

FORMAT your response as JSON:
{{
    "steps": [
        {{
            "number": 1,
            "title": "Short title",
            "instruction": "Clear, simple instruction",
            "code_hint": "Small code snippet if helpful",
            "checkpoint": false
        }},
        ...
    ],
    "estimated_time_minutes": 15,
    "celebration_message": "What to say when they complete it"
}}"""


def get_hint_prompt(
    current_code: str,
    error_message: str = None,
    hint_level: int = 1
) -> str:
    """
    Generate a hint prompt with escalating specificity.
    
    hint_level:
        1 = Gentle nudge (question to prompt thinking)
        2 = Direction (point to the problem area)
        3 = Specific (tell them what to fix)
        4 = Show (give the solution with explanation)
    """
    level_instructions = {
        1: "Give a GENTLE HINT as a question that helps them think about the problem. Do NOT point directly to the error.",
        2: "Point them to the GENERAL AREA of the problem (which line or concept) but don't tell them exactly what's wrong.",
        3: "Tell them SPECIFICALLY what the problem is and what they need to change, but let them write the fix.",
        4: "Show them the CORRECT CODE with a brief explanation of why it works.",
    }
    
    error_context = f"\nERROR MESSAGE: {error_message}" if error_message else ""
    
    return f"""A middle school student with ADHD needs help with their Python code.

THEIR CODE:
```python
{current_code}
```
{error_context}

HINT LEVEL: {hint_level}/4
INSTRUCTION: {level_instructions[hint_level]}

Keep your response SHORT (2-3 sentences max). Be encouraging. Remember they're 11-14 years old."""
```

---

## 7. ADHD-SPECIFIC FEATURES

### 7.1 Focus Timer Component (src/components/ADHD/FocusTimer.tsx)

```tsx
/**
 * Focus timer with break reminders for ADHD learners.
 * 
 * Research basis: Pomodoro-style structures (25 min work, 5 min break)
 * improve attention and retention for ADHD learners (Kofler et al., 2018).
 * 
 * For middle schoolers, we use shorter intervals (15-20 min).
 */
import React, { useState, useEffect, useCallback } from 'react';

interface FocusTimerProps {
  workDuration?: number; // minutes
  breakDuration?: number; // minutes
  onBreakStart?: () => void;
  onWorkResume?: () => void;
  reduceAnimations?: boolean;
}

export const FocusTimer: React.FC<FocusTimerProps> = ({
  workDuration = 20,
  breakDuration = 5,
  onBreakStart,
  onWorkResume,
  reduceAnimations = true,
}) => {
  const [timeLeft, setTimeLeft] = useState(workDuration * 60);
  const [isBreak, setIsBreak] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [showBreakPrompt, setShowBreakPrompt] = useState(false);

  // Format time as MM:SS
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  // Timer logic
  useEffect(() => {
    if (isPaused) return;

    const timer = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          if (!isBreak) {
            // Work period ended - show break prompt
            setShowBreakPrompt(true);
            onBreakStart?.();
            return breakDuration * 60;
          } else {
            // Break ended - back to work
            setIsBreak(false);
            onWorkResume?.();
            return workDuration * 60;
          }
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [isPaused, isBreak, workDuration, breakDuration, onBreakStart, onWorkResume]);

  const handleTakeBreak = () => {
    setShowBreakPrompt(false);
    setIsBreak(true);
  };

  const handleSkipBreak = () => {
    setShowBreakPrompt(false);
    setTimeLeft(workDuration * 60);
  };

  const progress = isBreak
    ? ((breakDuration * 60 - timeLeft) / (breakDuration * 60)) * 100
    : ((workDuration * 60 - timeLeft) / (workDuration * 60)) * 100;

  return (
    <div className="relative">
      {/* Timer display */}
      <div className="flex items-center gap-3 px-4 py-2 bg-calm-bg rounded-lg border border-calm-border">
        {/* Progress ring */}
        <div className="relative w-12 h-12">
          <svg className="w-12 h-12 transform -rotate-90">
            <circle
              cx="24"
              cy="24"
              r="20"
              stroke="#e2e8f0"
              strokeWidth="4"
              fill="none"
            />
            <circle
              cx="24"
              cy="24"
              r="20"
              stroke={isBreak ? '#10b981' : '#3b82f6'}
              strokeWidth="4"
              fill="none"
              strokeDasharray={`${progress * 1.256} 125.6`}
              className={reduceAnimations ? '' : 'transition-all duration-1000'}
            />
          </svg>
          <span className="absolute inset-0 flex items-center justify-center text-xs font-medium">
            {isBreak ? '☕' : '💻'}
          </span>
        </div>

        {/* Time and status */}
        <div>
          <div className="text-lg font-mono font-medium text-calm-text">
            {formatTime(timeLeft)}
          </div>
          <div className="text-xs text-gray-500">
            {isBreak ? 'Break time!' : 'Focus time'}
          </div>
        </div>

        {/* Pause button */}
        <button
          onClick={() => setIsPaused(!isPaused)}
          className="ml-auto p-2 rounded-lg hover:bg-gray-100"
          aria-label={isPaused ? 'Resume timer' : 'Pause timer'}
        >
          {isPaused ? '▶' : '⏸'}
        </button>
      </div>

      {/* Break prompt modal */}
      {showBreakPrompt && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl p-6 max-w-sm mx-4 shadow-xl">
            <div className="text-center">
              <div className="text-4xl mb-4">🎉</div>
              <h3 className="text-xl font-semibold mb-2">
                Great work! Time for a break?
              </h3>
              <p className="text-gray-600 mb-6">
                You've been coding for {workDuration} minutes. 
                A quick break helps your brain rest!
              </p>
              
              <div className="flex flex-col gap-3">
                <button
                  onClick={handleTakeBreak}
                  className="w-full py-3 bg-success text-white rounded-lg font-medium hover:bg-green-600"
                >
                  Take a {breakDuration} min break ☕
                </button>
                <button
                  onClick={handleSkipBreak}
                  className="w-full py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
                >
                  I'm in the zone, keep going!
                </button>
              </div>

              <p className="mt-4 text-sm text-gray-500">
                Tip: Stand up, stretch, or look away from the screen!
              </p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
```

### 7.2 Celebration Component (src/components/Gamification/Celebration.tsx)

```tsx
/**
 * Celebration component for task completion.
 * 
 * Research basis: Immediate rewards trigger dopamine in ADHD brains
 * (EndeavorRx studies, Kollins et al., 2020).
 * 
 * Note: We use minimal animations and allow users to dismiss quickly.
 */
import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

interface CelebrationProps {
  show: boolean;
  message?: string;
  points?: number;
  onDismiss: () => void;
  autoDismissMs?: number;
  reduceAnimations?: boolean;
}

const CELEBRATION_MESSAGES = [
  "You did it! 🎉",
  "Awesome work! ⭐",
  "Nailed it! 💪",
  "Great job! 🌟",
  "You're on fire! 🔥",
  "Code champion! 🏆",
];

export const Celebration: React.FC<CelebrationProps> = ({
  show,
  message,
  points,
  onDismiss,
  autoDismissMs = 3000,
  reduceAnimations = true,
}) => {
  const [displayMessage] = useState(
    message || CELEBRATION_MESSAGES[Math.floor(Math.random() * CELEBRATION_MESSAGES.length)]
  );

  // Auto-dismiss after delay
  useEffect(() => {
    if (show && autoDismissMs > 0) {
      const timer = setTimeout(onDismiss, autoDismissMs);
      return () => clearTimeout(timer);
    }
  }, [show, autoDismissMs, onDismiss]);

  return (
    <AnimatePresence>
      {show && (
        <motion.div
          initial={reduceAnimations ? { opacity: 0 } : { opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: reduceAnimations ? 0.1 : 0.3 }}
          className="fixed inset-0 flex items-center justify-center z-50 pointer-events-none"
        >
          <div 
            className="bg-white rounded-2xl shadow-2xl p-8 max-w-sm mx-4 text-center pointer-events-auto"
            onClick={onDismiss}
            role="alert"
            aria-live="polite"
          >
            {/* Large emoji */}
            <div className="text-6xl mb-4">🎉</div>
            
            {/* Message */}
            <h2 className="text-2xl font-bold text-calm-text mb-2">
              {displayMessage}
            </h2>

            {/* Points earned */}
            {points && points > 0 && (
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-yellow-100 text-yellow-800 rounded-full text-lg font-medium">
                <span>+{points}</span>
                <span>⭐</span>
              </div>
            )}

            {/* Dismiss hint */}
            <p className="mt-4 text-sm text-gray-500">
              Tap anywhere to continue
            </p>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
};
```

---

## 8. DATABASE SCHEMA

### 8.1 Complete Models (app/models/session.py)

```python
"""
Learning session and exercise models.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime, ForeignKey, Text, Float, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Exercise(Base):
    """
    Python exercise definition.
    """
    __tablename__ = "exercises"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # Basic info
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[int] = mapped_column(Integer)  # 1-5
    
    # Content
    starter_code: Mapped[str] = mapped_column(Text)
    solution_code: Mapped[str] = mapped_column(Text)
    test_cases: Mapped[str] = mapped_column(JSON)  # List of test cases
    
    # Categorization
    concept: Mapped[str] = mapped_column(String(50))  # "loops", "variables", etc.
    grade_level: Mapped[int] = mapped_column(Integer)  # 6, 7, or 8
    
    # ADHD-specific
    estimated_minutes: Mapped[int] = mapped_column(Integer, default=10)
    step_count: Mapped[int] = mapped_column(Integer, default=5)
    
    # Personalization tags
    interest_tags: Mapped[str] = mapped_column(JSON, default=[])  # ["games", "art", etc.]
    
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LearningSession(Base):
    """
    A single learning session (one sitting).
    
    Used for research analytics on engagement patterns.
    """
    __tablename__ = "learning_sessions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    exercise_id: Mapped[Optional[int]] = mapped_column(ForeignKey("exercises.id"), nullable=True)
    
    # Timing
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    
    # Breaks
    break_count: Mapped[int] = mapped_column(Integer, default=0)
    total_break_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    # Engagement metrics (for research)
    hint_requests: Mapped[int] = mapped_column(Integer, default=0)
    code_runs: Mapped[int] = mapped_column(Integer, default=0)
    errors_encountered: Mapped[int] = mapped_column(Integer, default=0)
    steps_completed: Mapped[int] = mapped_column(Integer, default=0)
    
    # Outcome
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    frustration_events: Mapped[int] = mapped_column(Integer, default=0)  # "I'm stuck" etc.
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="sessions")
    interactions: Mapped[list["TutorInteraction"]] = relationship(back_populates="session")


class TutorInteraction(Base):
    """
    Individual tutor-student interaction for conversation tracking.
    """
    __tablename__ = "tutor_interactions"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("learning_sessions.id"))
    
    # Message content
    role: Mapped[str] = mapped_column(String(10))  # "student" or "tutor"
    content: Mapped[str] = mapped_column(Text)
    
    # Context
    current_step: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    code_snapshot: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timing
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    response_time_ms: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Classification (for research)
    interaction_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Types: "question", "hint_request", "celebration", "frustration", "completion"
    
    # Relationships
    session: Mapped["LearningSession"] = relationship(back_populates="interactions")


class ExerciseProgress(Base):
    """
    Student progress on exercises.
    """
    __tablename__ = "exercise_progress"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    
    # Progress
    current_step: Mapped[int] = mapped_column(Integer, default=1)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Score
    points_earned: Mapped[int] = mapped_column(Integer, default=0)
    hints_used: Mapped[int] = mapped_column(Integer, default=0)
    
    # Code
    last_code: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # Timing
    first_started: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_updated: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    total_time_seconds: Mapped[int] = mapped_column(Integer, default=0)
    
    # Attempts
    attempt_count: Mapped[int] = mapped_column(Integer, default=1)
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="progress")
```

---

## 9. COPPA COMPLIANCE

### 9.1 Key Requirements for This Application

Since we're targeting middle schoolers (ages 11-14), some users will be under 13 and COPPA applies.

**Required Actions:**

1. **Age Gate**: Collect birth year (not full DOB) to determine if under 13
2. **Parental Consent**: For users under 13, obtain verifiable parental consent before collecting any personal information
3. **Privacy Policy**: Clear, child-friendly explanation of data practices
4. **Data Minimization**: Only collect what's necessary
5. **Deletion Rights**: Parents can request deletion of child's data

### 9.2 Consent Flow (app/routers/auth.py excerpt)

```python
"""
Authentication routes with COPPA-compliant consent flow.
"""
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from datetime import datetime, date

from app.schemas.auth import RegisterRequest, ConsentRequest
from app.models.user import User, ParentalConsent
from app.services.email import send_parental_consent_email

router = APIRouter()


@router.post("/register")
async def register_student(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Step 1: Student provides username and birth year.
    If under 13, triggers parental consent flow.
    """
    current_year = date.today().year
    age = current_year - request.birth_year
    
    if age < 6 or age > 18:
        raise HTTPException(400, "This platform is for students ages 6-18")
    
    # Create user record (minimal info)
    user = User(
        username=request.username,
        birth_year=request.birth_year,
        grade_level=request.grade_level,
        has_parental_consent=False,  # Not yet
    )
    
    if age < 13:
        # COPPA: Cannot proceed without parental consent
        user.parent_email = request.parent_email
        db.add(user)
        await db.commit()
        
        # Send consent request to parent
        await send_parental_consent_email(
            parent_email=request.parent_email,
            student_username=request.username,
            consent_token=generate_consent_token(user.id),
        )
        
        return {
            "status": "consent_required",
            "message": "We sent an email to your parent/guardian. They need to give permission before you can start coding!",
        }
    else:
        # 13+ can consent for themselves (with assent)
        user.has_parental_consent = True
        user.consent_date = datetime.utcnow()
        # Still set password, complete registration
        user.hashed_password = hash_password(request.password)
        db.add(user)
        await db.commit()
        
        return {
            "status": "registered",
            "user_id": user.id,
        }


@router.post("/consent/verify")
async def verify_parental_consent(
    request: ConsentRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Step 2: Parent clicks link in email to provide consent.
    """
    # Verify token
    user_id = decode_consent_token(request.token)
    if not user_id:
        raise HTTPException(400, "Invalid or expired consent link")
    
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    
    if request.consent_given:
        # Record consent
        consent = ParentalConsent(
            user_id=user.id,
            parent_email=user.parent_email,
            consent_given=True,
            consent_timestamp=datetime.utcnow(),
            consent_method="email_link",
            research_consent=request.research_consent,
            data_sharing_consent=request.data_sharing_consent,
        )
        user.has_parental_consent = True
        user.consent_date = datetime.utcnow()
        
        db.add(consent)
        await db.commit()
        
        return {"status": "consent_recorded", "message": "Thank you! Your child can now start coding."}
    else:
        # Parent denied - delete the pending account
        await db.delete(user)
        await db.commit()
        
        return {"status": "consent_denied", "message": "Account request cancelled."}
```

---

## 10. PYTHON CURRICULUM

### 10.1 Scope for MVP (Middle School Focus)

Based on research (Sun & Liu, 2025), 8th graders show the greatest benefit from Python instruction. We'll structure content for grades 6-8.

**Curriculum Map:**

```
GRADE 6 (Introduction):
├── Unit 1: First Steps (2 weeks)
│   ├── What is code?
│   ├── print() - Make Python talk
│   ├── Variables - Storing information
│   └── input() - Getting user input
├── Unit 2: Making Decisions (2 weeks)
│   ├── if statements
│   ├── if-else
│   └── Comparison operators
└── Unit 3: Repetition (2 weeks)
    ├── for loops with range()
    └── Simple patterns

GRADE 7 (Building Skills):
├── Unit 4: More Loops (2 weeks)
│   ├── while loops
│   ├── Loop control (break, continue)
│   └── Nested loops
├── Unit 5: Lists (2 weeks)
│   ├── Creating lists
│   ├── Accessing elements
│   ├── Adding/removing items
│   └── Looping through lists
└── Unit 6: Functions (2 weeks)
    ├── Defining functions
    ├── Parameters and return
    └── Reusing code

GRADE 8 (Applications):
├── Unit 7: Text Games (2 weeks)
│   ├── Putting it together
│   ├── Number guessing game
│   └── Story adventure game
├── Unit 8: Data & Files (2 weeks)
│   ├── Reading files
│   ├── Writing files
│   └── Simple data analysis
└── Unit 9: Final Project (2 weeks)
    ├── Choose your project
    └── Build and share
```

### 10.2 Sample Exercise Definition

```python
# Example exercise for database seeding

LOOP_EXERCISE_1 = {
    "title": "Countdown Rocket Launch!",
    "description": "Use a loop to count down from 10 and launch a rocket! 🚀",
    "difficulty": 1,
    "concept": "loops",
    "grade_level": 6,
    "estimated_minutes": 15,
    "step_count": 4,
    "interest_tags": ["space", "games"],
    "starter_code": '''# Let's make a rocket launch countdown!
# Your goal: Print 10, 9, 8... down to 1, then "LIFTOFF!"

''',
    "solution_code": '''for i in range(10, 0, -1):
    print(i)
print("LIFTOFF! 🚀")''',
    "test_cases": [
        {"input": "", "expected_output": "10\n9\n8\n7\n6\n5\n4\n3\n2\n1\nLIFTOFF! 🚀"}
    ],
    "steps": [
        {
            "number": 1,
            "title": "Start with 10",
            "instruction": "First, let's just print the number 10. Type: print(10)",
            "checkpoint": False
        },
        {
            "number": 2, 
            "title": "Count down manually",
            "instruction": "Now add more print statements: print(9), print(8)... all the way to print(1). Yes, it's tedious! That's why we'll learn a better way.",
            "checkpoint": True
        },
        {
            "number": 3,
            "title": "Use a loop!",
            "instruction": "Delete all those prints. Let's use a for loop instead! Type: for i in range(10, 0, -1):",
            "checkpoint": False
        },
        {
            "number": 4,
            "title": "Print inside the loop",
            "instruction": "On the next line (indented with spaces), type: print(i). Then add print(\"LIFTOFF! 🚀\") at the end (not indented).",
            "checkpoint": True
        }
    ]
}
```

---

## 11. RESEARCH DATA COLLECTION

### 11.1 Metrics for RESPECT 2026 Paper

**Quantitative Metrics:**

| Metric | How Collected | Purpose |
|--------|---------------|---------|
| Task completion rate | ExerciseProgress.completed | Primary outcome |
| Time on task | LearningSession duration | Engagement measure |
| Hint usage | LearningSession.hint_requests | Support needs |
| Error frequency | LearningSession.errors_encountered | Learning struggles |
| Break patterns | LearningSession.break_count | ADHD-specific |
| Session length | Session timestamps | Sustained attention |
| Return rate | User.last_active | Motivation |

**Qualitative Data (Separate IRB-approved process):**

- Semi-structured interviews (n=10-15)
- Think-aloud protocols during sessions
- Teacher/parent feedback surveys

### 11.2 Analytics Service (app/services/analytics.py)

```python
"""
Research analytics service for data collection.

All data is anonymized by default. Identifiable data requires
explicit research consent from parent.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models.session import LearningSession, TutorInteraction, ExerciseProgress
from app.models.user import User


class AnalyticsService:
    """Service for collecting and aggregating research metrics."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def log_session_event(
        self,
        session_id: int,
        event_type: str,
        metadata: Optional[dict] = None,
    ):
        """
        Log a session event for research analysis.
        
        Events: "hint_requested", "code_run", "error", "step_completed",
                "frustration_expressed", "break_taken", "session_completed"
        """
        session = await self.db.get(LearningSession, session_id)
        if not session:
            return
        
        # Update counters
        if event_type == "hint_requested":
            session.hint_requests += 1
        elif event_type == "code_run":
            session.code_runs += 1
        elif event_type == "error":
            session.errors_encountered += 1
        elif event_type == "step_completed":
            session.steps_completed += 1
        elif event_type == "frustration_expressed":
            session.frustration_events += 1
        elif event_type == "break_taken":
            session.break_count += 1
            if metadata and "duration_seconds" in metadata:
                session.total_break_seconds += metadata["duration_seconds"]
        elif event_type == "session_completed":
            session.completed = True
            session.ended_at = datetime.utcnow()
        
        await self.db.commit()
    
    async def get_aggregate_metrics(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> dict:
        """
        Get aggregate metrics for research reporting.
        All data is anonymized - no individual identification.
        """
        sessions = await self.db.execute(
            select(LearningSession).where(
                LearningSession.started_at >= start_date,
                LearningSession.started_at <= end_date,
            )
        )
        sessions = sessions.scalars().all()
        
        if not sessions:
            return {"error": "No data in date range"}
        
        total = len(sessions)
        completed = sum(1 for s in sessions if s.completed)
        
        return {
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat(),
            },
            "total_sessions": total,
            "completion_rate": completed / total if total > 0 else 0,
            "avg_hints_per_session": sum(s.hint_requests for s in sessions) / total,
            "avg_errors_per_session": sum(s.errors_encountered for s in sessions) / total,
            "avg_breaks_per_session": sum(s.break_count for s in sessions) / total,
            "avg_session_duration_minutes": sum(
                (s.ended_at - s.started_at).total_seconds() / 60 
                for s in sessions if s.ended_at
            ) / completed if completed > 0 else 0,
        }
```

---

## 12. DEPLOYMENT

### 12.1 Docker Compose (docker-compose.yml)

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://neurocode:${DB_PASSWORD}@db:5432/neurocode
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - SECRET_KEY=${SECRET_KEY}
    depends_on:
      - db
    volumes:
      - ./backend:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: npm run dev -- --host

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=neurocode
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=neurocode
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

### 12.2 Environment Variables (.env.example)

```bash
# Application
SECRET_KEY=your-secret-key-here-generate-with-openssl-rand-hex-32
DEBUG=true

# Database
DB_PASSWORD=your-secure-password
DATABASE_URL=postgresql://neurocode:your-secure-password@localhost:5432/neurocode

# Gemini API
GEMINI_API_KEY=your-gemini-api-key-from-aistudio-google-com
GEMINI_MODEL=gemini-2.5-flash

# COPPA
REQUIRE_PARENTAL_CONSENT=true
MIN_AGE_WITHOUT_CONSENT=13

# Research
ENABLE_ANALYTICS=true
ANONYMIZE_DATA=true
```

---

## 13. TESTING STRATEGY

### 13.1 Backend Tests (tests/test_tutor.py)

```python
"""
Tests for the tutoring service.
"""
import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_tutor_response_is_age_appropriate():
    """Verify tutor responses are appropriate for middle schoolers."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/tutor/message",
            json={
                "message": "How do I print hello world?",
                "session_id": 1,
            },
            headers={"Authorization": "Bearer test-token"},
        )
        
        assert response.status_code == 200
        data = response.json()
        
        # Check response is not too long (ADHD-friendly)
        assert len(data["response"]) < 500
        
        # Check for encouraging language
        response_lower = data["response"].lower()
        assert any(word in response_lower for word in [
            "great", "nice", "good", "let's", "try", "!"
        ])


@pytest.mark.asyncio
async def test_hint_escalation():
    """Verify hints escalate appropriately."""
    # Test that hint level 1 doesn't give the answer
    # Test that hint level 4 provides solution
    pass  # Implementation


@pytest.mark.asyncio
async def test_coppa_blocks_under_13_without_consent():
    """Verify COPPA compliance - block minors without consent."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Try to register user born in 2014 (under 13)
        response = await client.post(
            "/api/auth/register",
            json={
                "username": "youngcoder",
                "birth_year": 2014,
                "grade_level": 6,
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "consent_required"
```

---

## QUICK START COMMANDS

```bash
# 1. Clone and setup
git clone <your-repo>
cd neurocode

# 2. Create environment file
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# 3. Start with Docker
docker-compose up --build

# 4. Access the app
# Frontend: http://localhost:5173
# Backend API docs: http://localhost:8000/docs

# --- OR without Docker ---

# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -e .
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

---

## NEXT STEPS FOR CURSOR/WINDSURF

1. **Create project structure**: Use the file tree above as your guide
2. **Start with backend**: Set up FastAPI, database models, Gemini service
3. **Add authentication**: Implement COPPA-compliant registration flow
4. **Build frontend**: Start with CodeEditor and TutorChat components
5. **Add ADHD features**: Timer, progress bar, celebrations
6. **Create exercises**: Seed database with curriculum content
7. **Test thoroughly**: Focus on age-appropriateness and COPPA
8. **Deploy**: Use Railway, Render, or similar

---

**Document Version:** 1.0  
**Last Updated:** December 2025  
**Target Conference:** RESPECT 2026 (June 8-10, Chicago, IL)  
**Submission Deadlines:** Abstract Jan 30, 2026 / Full Paper Feb 6, 2026
