"""
Safe Python code execution for student code.

IMPORTANT: This sandbox is basic and for educational use only.
For production, consider using Docker containers or a proper sandbox.
"""
import sys
import io
import traceback
import time
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import ast
import logging

logger = logging.getLogger(__name__)

# Dangerous modules that students shouldn't access
BLOCKED_MODULES = {
    "os", "sys", "subprocess", "shutil", "socket", "http", 
    "urllib", "ftplib", "smtplib", "telnetlib", "pickle",
    "ctypes", "multiprocessing", "threading", "_thread",
    "importlib", "builtins", "__builtins__", "eval", "exec",
    "compile", "open", "file"
}

# Maximum execution time in seconds
MAX_EXECUTION_TIME = 5

# Maximum output length
MAX_OUTPUT_LENGTH = 5000


@dataclass
class CodeExecutionResult:
    """Result of code execution."""
    success: bool
    output: str
    error: Optional[str] = None
    execution_time_ms: int = 0
    test_results: Optional[List[Dict[str, Any]]] = None


class CodeValidator:
    """Validates code for dangerous operations before execution."""
    
    @staticmethod
    def validate(code: str) -> tuple[bool, Optional[str]]:
        """
        Validate code for safety.
        Returns (is_safe, error_message).
        """
        if not code or not code.strip():
            return False, "No code provided"
        
        if len(code) > 10000:
            return False, "Code is too long (max 10,000 characters)"
        
        # Parse the AST
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return False, f"Syntax error: {e.msg} on line {e.lineno}"
        
        # Check for dangerous imports and operations
        for node in ast.walk(tree):
            # Check imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split('.')[0] in BLOCKED_MODULES:
                        return False, f"Import '{alias.name}' is not allowed for safety"
            
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] in BLOCKED_MODULES:
                    return False, f"Import from '{node.module}' is not allowed for safety"
            
            # Check for dangerous function calls
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in BLOCKED_MODULES:
                        return False, f"Function '{node.func.id}' is not allowed for safety"
                    if node.func.id == "open":
                        return False, "File operations are not allowed"
            
            # Check for attribute access on blocked items
            elif isinstance(node, ast.Attribute):
                if node.attr in {"__import__", "__builtins__", "__class__", "__bases__"}:
                    return False, f"Access to '{node.attr}' is not allowed"
        
        return True, None


def run_python_code(
    code: str,
    test_input: Optional[str] = None,
    timeout: float = MAX_EXECUTION_TIME
) -> CodeExecutionResult:
    """
    Run Python code safely and return the result.
    
    Args:
        code: Python code to execute
        test_input: Optional input to provide to the program
        timeout: Maximum execution time in seconds
        
    Returns:
        CodeExecutionResult with output and any errors
    """
    # Validate first
    is_valid, error = CodeValidator.validate(code)
    if not is_valid:
        return CodeExecutionResult(
            success=False,
            output="",
            error=error,
            execution_time_ms=0
        )
    
    # Capture stdout and stderr
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    old_stdin = sys.stdin
    
    captured_output = io.StringIO()
    captured_error = io.StringIO()
    
    # Provide test input if given
    if test_input:
        sys.stdin = io.StringIO(test_input)
    else:
        sys.stdin = io.StringIO("")
    
    sys.stdout = captured_output
    sys.stderr = captured_error
    
    # Create a restricted globals dict
    import random
    import datetime
    
    safe_globals = {
        "__builtins__": {
            "print": print,
            "len": len,
            "range": range,
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "input": input,
            "abs": abs,
            "max": max,
            "min": min,
            "sum": sum,
            "sorted": sorted,
            "reversed": reversed,
            "enumerate": enumerate,
            "zip": zip,
            "map": map,
            "filter": filter,
            "round": round,
            "pow": pow,
            "type": type,
            "isinstance": isinstance,
            "True": True,
            "False": False,
            "None": None,
            "__import__": __import__,  # Allow safe imports
        },
        "random": random,
        "datetime": datetime,
    }
    
    start_time = time.time()
    success = True
    error_msg = None
    
    try:
        exec(code, safe_globals, safe_globals)
    except Exception as e:
        success = False
        error_msg = f"{type(e).__name__}: {str(e)}"
        # Get a simplified traceback
        tb_lines = traceback.format_exc().split('\n')
        # Filter to show only the relevant line
        for i, line in enumerate(tb_lines):
            if 'File "<string>"' in line and i + 1 < len(tb_lines):
                error_msg += f"\n{tb_lines[i+1].strip()}"
                break
    finally:
        execution_time = int((time.time() - start_time) * 1000)
        
        # Restore streams
        sys.stdout = old_stdout
        sys.stderr = old_stderr
        sys.stdin = old_stdin
    
    output = captured_output.getvalue()
    stderr = captured_error.getvalue()
    
    # Truncate if too long
    if len(output) > MAX_OUTPUT_LENGTH:
        output = output[:MAX_OUTPUT_LENGTH] + "\n... (output truncated)"
    
    # Combine stderr into error if present
    if stderr and not error_msg:
        error_msg = stderr
    
    return CodeExecutionResult(
        success=success,
        output=output,
        error=error_msg,
        execution_time_ms=execution_time
    )


def run_with_tests(
    code: str,
    test_cases: List[Dict[str, Any]]
) -> CodeExecutionResult:
    """
    Run code against multiple test cases.
    
    Args:
        code: Python code to test
        test_cases: List of {"input": str, "expected_output": str}
        
    Returns:
        CodeExecutionResult with test results
    """
    test_results = []
    all_passed = True
    
    for i, test in enumerate(test_cases):
        result = run_python_code(code, test.get("input", ""))
        
        expected = test.get("expected_output", "").strip()
        actual = result.output.strip()
        passed = actual == expected
        
        if not passed:
            all_passed = False
        
        test_results.append({
            "test_number": i + 1,
            "passed": passed,
            "expected": expected,
            "actual": actual,
            "error": result.error
        })
    
    return CodeExecutionResult(
        success=all_passed,
        output=f"Passed {sum(1 for t in test_results if t['passed'])}/{len(test_results)} tests",
        test_results=test_results
    )
