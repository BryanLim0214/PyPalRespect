"""
Comprehensive tests for ALL exercises in the curriculum.

Tests:
1. All solution code compiles and runs
2. Solution code passes test cases where available
3. Interactive exercises work with mocked input
4. Random/dynamic exercises produce valid output patterns
"""
import pytest
import json
import re
from app.utils.code_runner import run_with_tests, run_python_code
from app.data.curriculum import get_all_exercises, EXERCISES


class TestAllExerciseSolutionsRun:
    """Test that every exercise's solution code runs without error."""
    
    @pytest.mark.parametrize("exercise", EXERCISES, ids=[e["title"] for e in EXERCISES])
    def test_solution_code_runs(self, exercise):
        """Every solution should run without runtime errors."""
        # For interactive exercises, provide mock input
        test_input = None
        
        # Exercises that require user input need mock data
        if "Number Guessing" in exercise["title"]:
            test_input = "5\n5\n5\n"  # Mock guesses
        elif "Choose Your Adventure" in exercise["title"]:
            test_input = "1"
        elif "Quiz Builder" in exercise["title"]:
            test_input = "4\nblue"
        elif "Digital Journal" in exercise["title"]:
            test_input = "My test entry"
        elif "Pet Age Calculator" in exercise["title"]:
            test_input = "3"  # Dog age
        elif "Emoji Mood Checker" in exercise["title"]:
            test_input = "happy"  # Mood
        elif "Word Counter" in exercise["title"]:
            test_input = "Hello world test sentence"
        elif "Rock Paper Scissors" in exercise["title"]:
            test_input = "rock"
        elif "Simple To-Do List" in exercise["title"]:
            test_input = "Task 1\nTask 2\nTask 3\n"  # Three tasks
        
        result = run_python_code(exercise["solution_code"], test_input=test_input)
        assert result.success, f"{exercise['title']} failed: {result.error}"


class TestExercisesWithTestCases:
    """Test exercises that have defined test_cases."""
    
    def test_hello_coder(self):
        ex = next(e for e in EXERCISES if e["title"] == "Hello Coder")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_math_magic(self):
        ex = next(e for e in EXERCISES if e["title"] == "Math Magic")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_build_your_profile(self):
        ex = next(e for e in EXERCISES if e["title"] == "Build Your Profile")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_high_score_tracker(self):
        ex = next(e for e in EXERCISES if e["title"] == "High Score Tracker")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_grade_checker(self):
        ex = next(e for e in EXERCISES if e["title"] == "Grade Checker")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_rocket_countdown(self):
        ex = next(e for e in EXERCISES if e["title"] == "Rocket Countdown")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_favorite_songs_playlist(self):
        ex = next(e for e in EXERCISES if e["title"] == "Favorite Songs Playlist")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_shopping_cart(self):
        ex = next(e for e in EXERCISES if e["title"] == "Shopping Cart")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_build_a_calculator(self):
        ex = next(e for e in EXERCISES if e["title"] == "Build a Calculator")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_mad_libs_story(self):
        ex = next(e for e in EXERCISES if e["title"] == "Mad Libs Story")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Failed: {result.test_results}"
    
    def test_choose_your_adventure_choice_1(self):
        """Test Choose Your Adventure with choice 1."""
        ex = next(e for e in EXERCISES if e["title"] == "Choose Your Adventure")
        test_cases = json.loads(ex["test_cases"])
        # Test first case (choice 1)
        result = run_with_tests(ex["solution_code"], [test_cases[0]])
        assert result.success, f"Choice 1 failed: {result.test_results}"
    
    def test_choose_your_adventure_choice_2(self):
        """Test Choose Your Adventure with choice 2."""
        ex = next(e for e in EXERCISES if e["title"] == "Choose Your Adventure")
        test_cases = json.loads(ex["test_cases"])
        # Test second case (choice 2)
        result = run_with_tests(ex["solution_code"], [test_cases[1]])
        assert result.success, f"Choice 2 failed: {result.test_results}"
    
    def test_quiz_builder_correct_answers(self):
        """Test Quiz Builder with correct answers."""
        ex = next(e for e in EXERCISES if e["title"] == "Quiz Builder")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], [test_cases[0]])
        assert result.success, f"Correct answers failed: {result.test_results}"
    
    def test_quiz_builder_wrong_answers(self):
        """Test Quiz Builder with wrong answers."""
        ex = next(e for e in EXERCISES if e["title"] == "Quiz Builder")
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests(ex["solution_code"], [test_cases[1]])
        assert result.success, f"Wrong answers failed: {result.test_results}"


class TestRandomAndDynamicExercises:
    """Test exercises with random or dynamic output using pattern matching."""
    
    def test_password_maker_output_pattern(self):
        """Password Maker should output 'Your password:' followed by word+number."""
        ex = next(e for e in EXERCISES if e["title"] == "Password Maker")
        result = run_python_code(ex["solution_code"])
        
        assert result.success, f"Failed to run: {result.error}"
        assert "Your password:" in result.output
        # Check that output contains one of the words and one of the numbers
        words = ["dragon", "ninja", "robot"]
        numbers = ["123", "456", "789"]
        password_found = any(
            word in result.output and num in result.output
            for word in words for num in numbers
        )
        assert password_found, f"Invalid password pattern: {result.output}"
    
    def test_number_guessing_game_runs(self):
        """Number Guessing Game should run with mocked input."""
        ex = next(e for e in EXERCISES if e["title"] == "Number Guessing Game")
        # Mock 3 guesses
        result = run_python_code(ex["solution_code"], test_input="5\n7\n3\n")
        
        assert result.success, f"Failed to run: {result.error}"
        # Should have Higher!, Lower!, or Correct! in output
        has_game_output = (
            "Higher!" in result.output or 
            "Lower!" in result.output or 
            "Correct!" in result.output
        )
        assert has_game_output, f"No game logic output: {result.output}"
    
    def test_digital_journal_output_pattern(self):
        """Digital Journal should output 'Saved entry:' with date and entry."""
        ex = next(e for e in EXERCISES if e["title"] == "Digital Journal")
        result = run_python_code(ex["solution_code"], test_input="My test entry")
        
        assert result.success, f"Failed to run: {result.error}"
        assert "Saved entry:" in result.output
        # Date pattern like 2025-12-27
        date_pattern = r"\d{4}-\d{2}-\d{2}"
        assert re.search(date_pattern, result.output), f"No date in output: {result.output}"
        assert "My test entry" in result.output


class TestIncorrectCodeFails:
    """Verify incorrect student code correctly FAILS test cases."""
    
    def test_wrong_hello_world_fails(self):
        """Wrong Hello World should fail."""
        ex = next(e for e in EXERCISES if e["title"] == "Hello Coder")
        test_cases = json.loads(ex["test_cases"])
        bad_code = 'print("Wrong message")'
        result = run_with_tests(bad_code, test_cases)
        assert not result.success, "Wrong code should NOT pass"
    
    def test_wrong_math_fails(self):
        """Wrong math calculation should fail."""
        ex = next(e for e in EXERCISES if e["title"] == "Math Magic")
        test_cases = json.loads(ex["test_cases"])
        bad_code = 'print("Total score: 999")'
        result = run_with_tests(bad_code, test_cases)
        assert not result.success, "Wrong calc should NOT pass"
    
    def test_wrong_countdown_fails(self):
        """Wrong countdown should fail."""
        ex = next(e for e in EXERCISES if e["title"] == "Rocket Countdown")
        test_cases = json.loads(ex["test_cases"])
        bad_code = 'print("5\\n4\\n3\\n2\\n1\\nBLAST OFF!")'  # Wrong ending
        result = run_with_tests(bad_code, test_cases)
        assert not result.success, "Wrong countdown should NOT pass"
    
    def test_syntax_error_fails_any(self):
        """Syntax errors should fail any exercise."""
        ex = EXERCISES[0]  # Any exercise
        test_cases = json.loads(ex["test_cases"]) if "test_cases" in ex else [{"input": "", "expected_output": "anything"}]
        bad_code = 'print("unclosed'
        result = run_with_tests(bad_code, test_cases)
        assert not result.success, "Syntax errors should NOT pass"
    
    def test_empty_code_fails(self):
        """Empty code should fail."""
        ex = EXERCISES[0]
        test_cases = json.loads(ex["test_cases"])
        result = run_with_tests("", test_cases)
        assert not result.success, "Empty code should NOT pass"
