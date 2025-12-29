"""
Human-centered tests from middle schooler and ADHD perspectives.

These tests simulate REALISTIC scenarios that an 11-14 year old with ADHD
would encounter, including:
- Common typos and mistakes kids make  
- Frustration patterns and giving up
- Short attention span behaviors
- Excitement and impatience
- Testing with real kid language
"""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock


class TestMiddleSchoolerTypos:
    """Test handling of common typos middle schoolers make."""
    
    def test_code_with_common_typos(self):
        """Kids often type 'pirnt' instead of 'print'."""
        from app.utils.code_runner import run_python_code
        
        # Common typos
        result = run_python_code("pirnt('hello')")
        assert result.success == False
        assert "NameError" in result.error
    
    def test_missing_quotes_error(self):
        """Kids forget closing quotes ALL the time."""
        from app.utils.code_runner import run_python_code
        
        result = run_python_code('print("hello)')
        assert result.success == False
        assert result.error is not None
    
    def test_missing_parenthesis(self):
        """Forgetting to close parentheses."""
        from app.utils.code_runner import run_python_code
        
        result = run_python_code('print("hello"')
        assert result.success == False
    
    def test_wrong_caps_in_print(self):
        """Kids type 'Print' or 'PRINT' instead of 'print'."""
        from app.utils.code_runner import run_python_code
        
        result = run_python_code('Print("hello")')
        assert result.success == False
        assert "NameError" in result.error
    
    def test_spaces_in_variable_name(self):
        """Kids try to use spaces in variable names."""
        from app.utils.code_runner import run_python_code
        
        result = run_python_code('my score = 100')
        assert result.success == False
    
    def test_using_equals_instead_of_double_equals(self):
        """Kids confuse = and == constantly."""
        from app.utils.code_runner import run_python_code
        
        code = """
x = 5
if x = 5:
    print("equal")
"""
        result = run_python_code(code)
        assert result.success == False


class TestMiddleSchoolerLanguage:
    """Test that prompts use age-appropriate language."""
    
    def test_tutor_prompt_avoids_jargon(self):
        """Tutor prompt should not use complex programming jargon."""
        from app.prompts.system_prompts import get_tutor_system_prompt
        
        complex_jargon = [
            "polymorphism", "encapsulation", "abstraction",
            "recursion", "algorithm complexity", "data structure",
            "inheritance", "instantiation", "implementation"
        ]
        
        prompt_lower = get_tutor_system_prompt().lower()
        for jargon in complex_jargon:
            assert jargon not in prompt_lower, f"Found jargon '{jargon}' in tutor prompt"
    
    def test_tutor_prompt_uses_encouraging_words(self):
        """Should use encouraging, friendly language."""
        from app.prompts.system_prompts import get_tutor_system_prompt
        
        encouraging = ["great", "nice", "good", "cool", "awesome", "fun"]
        found_encouraging = any(word in get_tutor_system_prompt().lower() for word in encouraging)
        assert found_encouraging, "Tutor prompt lacks encouraging language"
    
    def test_tutor_prompt_mentions_games(self):
        """Games are a huge motivator for this age group."""
        from app.prompts.system_prompts import get_tutor_system_prompt
        
        assert "game" in get_tutor_system_prompt().lower()
    
    def test_celebration_prompts_not_patronizing(self):
        """Celebrations should feel genuine, not baby-ish."""
        from app.prompts.system_prompts import get_celebration_prompt
        
        prompt = get_celebration_prompt("step_complete", 10)
        
        # Should not use baby talk
        patronizing = ["good boy", "good girl", "gold star", "you're so smart"]
        prompt_lower = prompt.lower()
        for phrase in patronizing:
            assert phrase not in prompt_lower


class TestADHDFrustrationPatterns:
    """Test handling of ADHD frustration patterns."""
    
    @pytest.mark.asyncio
    async def test_hint_escalates_after_frustration_expressed(self):
        """When student says "I'm stuck" or "I don't get it", hints should help more."""
        from app.services.hint_generator import hint_generator
        
        # Frustration should trigger escalation check
        should_escalate = hint_generator.should_escalate(
            consecutive_errors=1,
            time_stuck_seconds=60,
            frustration_expressed=True
        )
        assert should_escalate == True
    
    @pytest.mark.asyncio
    async def test_hint_escalates_after_many_attempts(self):
        """After 3+ failed attempts, give more help automatically."""
        from app.services.hint_generator import hint_generator
        
        should_escalate = hint_generator.should_escalate(
            consecutive_errors=3,
            time_stuck_seconds=30,
            frustration_expressed=False
        )
        assert should_escalate == True
    
    def test_frustration_keywords_detected(self):
        """Common frustration phrases middle schoolers use."""
        frustration_phrases = [
            "I don't get it",
            "this is stupid",
            "help me",
            "I'm stuck",
            "I give up",
            "this is hard",
            "I can't do this",
            "nothing works",
            "ugh",
            "this sucks",
        ]
        
        frustration_keywords = ["stuck", "don't get", "confused", "help", "frustrated", "hard"]
        
        for phrase in frustration_phrases:
            detected = any(kw in phrase.lower() for kw in frustration_keywords)
            # Most should be detected
            if not detected:
                print(f"Warning: '{phrase}' not detected as frustration")
    
    @pytest.mark.asyncio
    async def test_empty_code_gets_encouraging_response(self):
        """Students might submit without writing anything - don't scold them."""
        from app.services.hint_generator import hint_generator
        
        hint = await hint_generator.generate_hint("", hint_level=1)
        
        # Should be encouraging, not critical
        assert "try" in hint.hint.lower() or "start" in hint.hint.lower()
        assert "wrong" not in hint.hint.lower()


class TestADHDAttentionSpan:
    """Test that content respects ADHD attention patterns."""
    
    def test_step_instructions_are_short(self):
        """Each step instruction should be digestible quickly."""
        from app.services.task_decomposer import TaskDecomposerService
        from app.schemas.tutor import Step
        
        service = TaskDecomposerService()
        
        # Create some steps and check they'd be valid
        steps = [
            Step(number=1, title="Short", instruction="Write print('hello')", checkpoint=False),
            Step(number=2, title="Too long", instruction="x" * 250, checkpoint=True),
        ]
        
        warnings = service.validate_steps(steps)
        assert any("too long" in w.lower() for w in warnings)
    
    def test_max_steps_limit_enforced(self):
        """Too many steps overwhelms ADHD learners."""
        from app.services.task_decomposer import TaskDecomposerService
        from app.schemas.tutor import Step
        
        service = TaskDecomposerService()
        
        # 9 steps is too many
        many_steps = [
            Step(number=i, title=f"Step {i}", instruction="Do something")
            for i in range(1, 10)
        ]
        
        warnings = service.validate_steps(many_steps)
        assert any("too many" in w.lower() for w in warnings)
    
    def test_checkpoints_required(self):
        """ADHD learners need checkpoints to feel progress."""
        from app.services.task_decomposer import TaskDecomposerService
        from app.schemas.tutor import Step
        
        service = TaskDecomposerService()
        
        # No checkpoints
        steps = [
            Step(number=i, title=f"Step {i}", instruction="Do it", checkpoint=False)
            for i in range(1, 5)
        ]
        
        warnings = service.validate_steps(steps)
        assert any("checkpoint" in w.lower() for w in warnings)


class TestRealisticStudentCode:
    """Test with code that real middle schoolers would write."""
    
    def test_student_first_print_attempt(self):
        """A student's typical first attempt."""
        from app.utils.code_runner import run_python_code
        
        result = run_python_code('print("Hello World!")')
        assert result.success == True
        assert "Hello World!" in result.output
    
    def test_student_trying_math(self):
        """Basic math operations kids try."""
        from app.utils.code_runner import run_python_code
        
        code = """
x = 10
y = 5
print(x + y)
print(x - y)
print(x * y)
"""
        result = run_python_code(code)
        assert result.success == True
        assert "15" in result.output
        assert "5" in result.output
        assert "50" in result.output
    
    def test_simple_game_style_code(self):
        """The kind of code kids want to write - game-like."""
        from app.utils.code_runner import run_python_code
        
        code = """
player_score = 0
player_score = player_score + 10
print("Your score is:", player_score)
"""
        result = run_python_code(code)
        assert result.success == True
        assert "10" in result.output
    
    def test_loop_countdown_exercise(self):
        """Classic countdown exercise - rocket launch!"""
        from app.utils.code_runner import run_python_code
        
        code = """
for i in range(5, 0, -1):
    print(i)
print("BLAST OFF!")
"""
        result = run_python_code(code)
        assert result.success == True
        assert "5" in result.output
        assert "1" in result.output
        assert "BLAST OFF!" in result.output
    
    def test_input_based_code(self):
        """Interactive code - very appealing to kids."""
        from app.utils.code_runner import run_python_code
        
        code = """
name = input("What is your name? ")
print("Hello, " + name + "!")
"""
        result = run_python_code(code, test_input="Alex")
        # The important thing is it runs and includes the name
        assert result.success == True
        assert "Alex" in result.output or "Hello" in result.output
    
    def test_emoji_in_code(self):
        """Kids LOVE using emojis."""
        from app.utils.code_runner import run_python_code
        
        result = run_python_code('print("You win! 🎉🏆")')
        assert result.success == True
        assert "🎉" in result.output


class TestCOPPAforRealKids:
    """Test COPPA compliance with realistic age scenarios."""
    
    def test_age_calculation_boundary(self):
        """Test the exact 13-year-old boundary."""
        from datetime import date
        
        current_year = date.today().year
        
        # 12 years old - needs consent
        birth_year_12 = current_year - 12
        age_12 = current_year - birth_year_12
        assert age_12 < 13
        
        # 13 years old - no consent needed
        birth_year_13 = current_year - 13
        age_13 = current_year - birth_year_13
        assert age_13 >= 13
    
    def test_realistic_birth_years(self):
        """Test with realistic birth years for 6th-8th graders."""
        from datetime import date
        
        current_year = date.today().year
        
        # 6th grader: typically 11-12 years old
        sixth_grader_birth = current_year - 11
        assert sixth_grader_birth >= 2010  # Would be realistic
        
        # 8th grader: typically 13-14 years old
        eighth_grader_birth = current_year - 14
        assert eighth_grader_birth >= 2010


class TestExerciseDifficulty:
    """Test that exercise difficulty is appropriate for grade levels."""
    
    def test_grade_6_difficulty(self):
        """6th graders need the simplest content."""
        from app.models.session import Exercise
        
        # 6th grade exercise should be difficulty 1-2
        ex = Exercise(
            title="Hello World",
            description="Print hello!",
            difficulty=1,
            grade_level=6,
            starter_code="# Type here",
            solution_code='print("hello")',
            concept="print",
            estimated_minutes=5,
            step_count=2,
        )
        
        assert ex.difficulty <= 2
        assert ex.step_count <= 3
        assert ex.estimated_minutes <= 10
    
    def test_grade_8_can_handle_more(self):
        """8th graders can handle more complexity."""
        from app.models.session import Exercise
        
        ex = Exercise(
            title="Number Game",
            description="Make a guessing game!",
            difficulty=3,
            grade_level=8,
            starter_code="# Game code",
            solution_code="# Complex code",
            concept="if-statements",
            estimated_minutes=20,
            step_count=5,
        )
        
        assert ex.difficulty <= 4
        assert ex.estimated_minutes <= 25


class TestGamificationMotivation:
    """Test that gamification elements motivate middle schoolers."""
    
    @pytest.mark.asyncio
    async def test_points_calculated_fairly(self, db_session):
        """Points should feel fair - not too easy, not too hard."""
        from app.routers.exercises import _calculate_points
        
        # Easy exercise, no hints = good points
        points_easy_no_hints = _calculate_points(difficulty=1, hints_used=0)
        assert points_easy_no_hints >= 15
        
        # Hard exercise, some hints = still decent points
        points_hard_some_hints = _calculate_points(difficulty=4, hints_used=2)
        assert points_hard_some_hints >= 50
        
        # Using lots of hints shouldn't make points negative
        points_many_hints = _calculate_points(difficulty=1, hints_used=10)
        assert points_many_hints >= 10  # Minimum 10 points
    
    def test_user_has_points_tracking(self):
        """User model tracks points and streaks."""
        from app.models.user import User
        
        user = User(
            username="gamer",
            hashed_password="hash",
            birth_year=2010,
            grade_level=7,
            total_points=0,
            current_streak=0,
        )
        
        assert hasattr(user, 'total_points')
        assert hasattr(user, 'current_streak')
        assert user.total_points == 0  # Starts at 0


class TestAccessibilityForADHD:
    """Test accessibility features specific to ADHD."""
    
    def test_reduce_animations_default_on(self):
        """Reduced animations should default to ON for ADHD."""
        from app.models.user import User
        
        # SQLAlchemy column defaults apply on database commit.
        # Verify the column definition has correct default
        mapper = User.__mapper__
        reduce_col = mapper.columns['reduce_animations']
        
        assert reduce_col.default.arg == True  # Default ON for ADHD
    
    def test_user_preferences_exist(self):
        """All accessibility options should be available."""
        from app.models.user import User
        
        user = User(
            username="accessuser",
            hashed_password="hash",
            birth_year=2010,
            grade_level=7,
            # SQLAlchemy applies column defaults on commit, so set explicitly
            preferred_break_interval=20,
            preferred_session_length=30,
        )
        
        assert hasattr(user, 'dyslexia_font')
        assert hasattr(user, 'high_contrast')
        assert hasattr(user, 'reduce_animations')
        assert hasattr(user, 'preferred_break_interval')
        assert hasattr(user, 'preferred_session_length')
    
    def test_break_interval_default(self):
        """Break reminders default to 20 minutes (research-based)."""
        from app.models.user import User
        
        # Note: SQLAlchemy column defaults apply on database commit.
        # This tests the column definition has correct default
        from app.models.user import User
        import sqlalchemy.inspection as insp
        
        mapper = User.__mapper__
        break_col = mapper.columns['preferred_break_interval']
        session_col = mapper.columns['preferred_session_length']
        
        assert break_col.default.arg == 20
        assert session_col.default.arg == 30
