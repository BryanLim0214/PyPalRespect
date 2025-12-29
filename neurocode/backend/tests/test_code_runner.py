"""
Tests for safe code execution.
"""
import pytest
from app.utils.code_runner import (
    run_python_code, 
    run_with_tests,
    CodeValidator,
    CodeExecutionResult,
)


class TestCodeValidator:
    """Tests for CodeValidator."""
    
    def test_validate_empty_code(self):
        """Test validation of empty code."""
        is_valid, error = CodeValidator.validate("")
        assert is_valid == False
        assert "No code" in error
    
    def test_validate_valid_code(self):
        """Test validation of valid code."""
        is_valid, error = CodeValidator.validate('print("hello")')
        assert is_valid == True
        assert error is None
    
    def test_validate_syntax_error(self):
        """Test syntax error detection."""
        is_valid, error = CodeValidator.validate('print("hello')
        assert is_valid == False
        assert "Syntax error" in error
    
    def test_validate_blocks_os_import(self):
        """Test that os import is blocked."""
        is_valid, error = CodeValidator.validate("import os")
        assert is_valid == False
        assert "not allowed" in error.lower()
    
    def test_validate_blocks_subprocess(self):
        """Test that subprocess is blocked."""
        is_valid, error = CodeValidator.validate("import subprocess")
        assert is_valid == False
        assert "not allowed" in error.lower()
    
    def test_validate_blocks_open_function(self):
        """Test that open() is blocked."""
        is_valid, error = CodeValidator.validate('open("file.txt")')
        assert is_valid == False
        assert "not allowed" in error.lower()
    
    def test_validate_blocks_from_import(self):
        """Test that blocked module from imports are caught."""
        is_valid, error = CodeValidator.validate("from os import path")
        assert is_valid == False
        assert "not allowed" in error.lower()
    
    def test_validate_blocks_dunder_methods(self):
        """Test that __builtins__ access is blocked."""
        is_valid, error = CodeValidator.validate("x.__builtins__")
        assert is_valid == False
        assert "not allowed" in error.lower()
    
    def test_validate_allows_safe_code(self):
        """Test that safe operations are allowed."""
        safe_code = """
x = 5
y = 10
print(x + y)
for i in range(5):
    print(i)
"""
        is_valid, error = CodeValidator.validate(safe_code)
        assert is_valid == True
    
    def test_validate_code_too_long(self):
        """Test that very long code is rejected."""
        long_code = "x = 1\n" * 5000
        is_valid, error = CodeValidator.validate(long_code)
        assert is_valid == False
        assert "too long" in error.lower()


class TestRunPythonCode:
    """Tests for run_python_code function."""
    
    def test_run_simple_print(self):
        """Test running simple print statement."""
        result = run_python_code('print("Hello, World!")')
        
        assert result.success == True
        assert "Hello, World!" in result.output
        assert result.error is None
    
    def test_run_with_variables(self):
        """Test running code with variables."""
        code = """
x = 5
y = 3
print(x + y)
"""
        result = run_python_code(code)
        
        assert result.success == True
        assert "8" in result.output
    
    def test_run_with_loop(self):
        """Test running code with loops."""
        code = """
for i in range(3):
    print(i)
"""
        result = run_python_code(code)
        
        assert result.success == True
        assert "0" in result.output
        assert "1" in result.output
        assert "2" in result.output
    
    def test_run_with_error(self):
        """Test running code that has a runtime error."""
        result = run_python_code("x = 1 / 0")
        
        assert result.success == False
        assert "ZeroDivisionError" in result.error
    
    def test_run_with_name_error(self):
        """Test running code with undefined variable."""
        result = run_python_code("print(undefined_variable)")
        
        assert result.success == False
        assert "NameError" in result.error
    
    def test_run_blocked_code(self):
        """Test that blocked code is rejected."""
        result = run_python_code("import os")
        
        assert result.success == False
        assert "not allowed" in result.error.lower()
    
    def test_run_with_input(self):
        """Test running code that expects input."""
        code = """
name = input("Enter name: ")
print("Hello, " + name)
"""
        result = run_python_code(code, test_input="Alice")
        
        assert result.success == True
        assert "Alice" in result.output
    
    def test_execution_time_recorded(self):
        """Test that execution time is recorded."""
        result = run_python_code('print("test")')
        
        assert result.execution_time_ms >= 0
    
    def test_output_truncation(self):
        """Test that long output is truncated."""
        code = """
for i in range(10000):
    print("x" * 100)
"""
        result = run_python_code(code)
        
        assert "truncated" in result.output.lower()


class TestRunWithTests:
    """Tests for run_with_tests function."""
    
    def test_passing_tests(self):
        """Test code that passes all tests."""
        code = 'print("Hello")'
        test_cases = [
            {"input": "", "expected_output": "Hello"}
        ]
        
        result = run_with_tests(code, test_cases)
        
        assert result.success == True
        assert result.test_results is not None
        assert result.test_results[0]["passed"] == True
    
    def test_failing_tests(self):
        """Test code that fails tests."""
        code = 'print("Wrong")'
        test_cases = [
            {"input": "", "expected_output": "Hello"}
        ]
        
        result = run_with_tests(code, test_cases)
        
        assert result.success == False
        assert result.test_results[0]["passed"] == False
    
    def test_multiple_test_cases(self):
        """Test running multiple test cases."""
        code = """
x = int(input())
print(x * 2)
"""
        test_cases = [
            {"input": "5", "expected_output": "10"},
            {"input": "3", "expected_output": "6"},
            {"input": "0", "expected_output": "0"},
        ]
        
        result = run_with_tests(code, test_cases)
        
        assert result.success == True
        assert len(result.test_results) == 3
        assert all(t["passed"] for t in result.test_results)
    
    def test_partial_pass(self):
        """Test when some tests pass and some fail."""
        code = 'print("5")'  # Always prints 5
        test_cases = [
            {"input": "", "expected_output": "5"},  # Pass
            {"input": "", "expected_output": "10"},  # Fail
        ]
        
        result = run_with_tests(code, test_cases)
        
        assert result.success == False
        assert result.test_results[0]["passed"] == True
        assert result.test_results[1]["passed"] == False


class TestEdgeCases:
    """Edge case tests for code runner."""
    
    def test_empty_output(self):
        """Test code with no output."""
        result = run_python_code("x = 5")
        
        assert result.success == True
        assert result.output == ""
    
    def test_whitespace_only_code(self):
        """Test whitespace-only code."""
        result = run_python_code("   \n\t\n   ")
        
        assert result.success == False
    
    def test_unicode_in_code(self):
        """Test code with unicode characters."""
        result = run_python_code('print("Hello 🎉")')
        
        assert result.success == True
        assert "🎉" in result.output
    
    def test_multiline_strings(self):
        """Test code with multiline strings."""
        code = '''
message = """
Hello
World
"""
print(message)
'''
        result = run_python_code(code)
        
        assert result.success == True
        assert "Hello" in result.output
    
    def test_list_operations(self):
        """Test list operations work correctly."""
        code = """
my_list = [1, 2, 3]
my_list.append(4)
print(sum(my_list))
"""
        result = run_python_code(code)
        
        assert result.success == True
        assert "10" in result.output
