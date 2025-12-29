"""
Tests to verify exercise test cases work correctly.

These tests ensure that:
1. Solution code passes test cases
2. Incorrect code FAILS test cases (i.e., tests are meaningful)
"""
import pytest
import json
from app.utils.code_runner import run_with_tests, run_python_code
from app.data.curriculum import get_all_exercises


class TestSolutionCodePassesTestCases:
    """Verify each exercise's solution code passes its test cases."""
    
    def test_hello_coder_solution_passes(self):
        """Hello Coder solution should pass."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Hello Coder")
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Hello Coder failed: {result.test_results}"
    
    def test_math_magic_solution_passes(self):
        """Math Magic solution should pass."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Math Magic")
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Math Magic failed: {result.test_results}"
    
    def test_build_your_profile_solution_passes(self):
        """Build Your Profile solution should pass."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Build Your Profile")
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Build Your Profile failed: {result.test_results}"
    
    def test_high_score_tracker_solution_passes(self):
        """High Score Tracker solution should pass."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "High Score Tracker")
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"High Score Tracker failed: {result.test_results}"
    
    def test_grade_checker_solution_passes(self):
        """Grade Checker solution should pass."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Grade Checker")
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Grade Checker failed: {result.test_results}"
    
    def test_rocket_countdown_solution_passes(self):
        """Rocket Countdown solution should pass."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Rocket Countdown")
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Rocket Countdown failed: {result.test_results}"
    
    def test_shopping_cart_solution_passes(self):
        """Shopping Cart solution should pass."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Shopping Cart")
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Shopping Cart failed: {result.test_results}"
    
    def test_build_a_calculator_solution_passes(self):
        """Build a Calculator solution should pass."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Build a Calculator")
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests(ex["solution_code"], test_cases)
        assert result.success, f"Build a Calculator failed: {result.test_results}"


class TestIncorrectCodeFails:
    """Verify that incorrect code FAILS the test cases."""
    
    def test_hello_coder_wrong_output_fails(self):
        """Wrong output should fail Hello Coder."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Hello Coder")
        test_cases = json.loads(ex["test_cases"])
        
        # Incorrect code
        bad_code = 'print("Hi there!")'
        result = run_with_tests(bad_code, test_cases)
        assert not result.success, "Bad code should NOT pass Hello Coder"
    
    def test_math_magic_wrong_calculation_fails(self):
        """Wrong calculation should fail Math Magic."""
        exercises = get_all_exercises()
        ex = next(e for e in exercises if e["title"] == "Math Magic")
        test_cases = json.loads(ex["test_cases"])
        
        # Wrong numbers
        bad_code = 'print("Total score:", 100)'
        result = run_with_tests(bad_code, test_cases)
        assert not result.success, "Wrong calc should NOT pass Math Magic"
    
    def test_empty_code_fails(self):
        """Empty code should fail any exercise with test cases."""
        exercises = get_all_exercises()
        ex = exercises[0]  # Hello Coder
        test_cases = json.loads(ex["test_cases"])
        
        result = run_with_tests("", test_cases)
        assert not result.success, "Empty code should NOT pass"
    
    def test_syntax_error_fails(self):
        """Syntax errors should fail."""
        exercises = get_all_exercises()
        ex = exercises[0]  # Hello Coder
        test_cases = json.loads(ex["test_cases"])
        
        bad_code = 'print("Hello'  # Missing closing quote
        result = run_with_tests(bad_code, test_cases)
        assert not result.success, "Syntax errors should NOT pass"
