#!/usr/bin/env python3
"""
Test Coverage Analysis Script for PyPal Research

This script collects and categorizes all pytest tests to generate
statistics for research documentation and the SVG coverage chart.

Usage:
    python scripts/test_coverage_analysis.py
    
Output:
    - Console summary of test counts by category
    - JSON file with detailed test statistics
"""

import subprocess
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime


# Test file to category mapping (based on actual test structure)
CATEGORY_MAPPING = {
    "Curriculum": [
        "test_curriculum.py",
        "test_all_exercises.py", 
        "test_exercise_validation.py"
    ],
    "AI/LLM Integration": [
        "test_gemini_service.py",
        "test_hint_generator.py",
        "test_task_decomposer.py",
        "test_prompts.py"
    ],
    "ADHD Features": [
        "test_human_perspective.py",
        "test_student_experience.py"
    ],
    "Edge Cases": [
        "test_edge_cases.py",
        "test_config.py"
    ],
    "Security/COPPA": [
        "test_security.py",
        "test_auth.py"
    ],
    "Code Execution": [
        "test_code_runner.py"
    ],
    "Analytics": [
        "test_analytics.py",
        "test_models.py"
    ]
}


def collect_tests():
    """Run pytest --collect-only and parse the output."""
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "--collect-only", "-q"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent / "neurocode" / "backend"
    )
    
    test_counts = defaultdict(int)
    total_tests = 0
    
    for line in result.stdout.strip().split('\n'):
        if '::' in line:
            # Extract test file name
            parts = line.split('::')
            if len(parts) >= 1:
                file_path = parts[0]
                file_name = Path(file_path).name
                test_counts[file_name] += 1
                total_tests += 1
    
    return dict(test_counts), total_tests


def categorize_tests(test_counts):
    """Group tests by category."""
    category_counts = {}
    
    for category, files in CATEGORY_MAPPING.items():
        count = sum(test_counts.get(f, 0) for f in files)
        category_counts[category] = {
            "count": count,
            "files": files,
            "file_counts": {f: test_counts.get(f, 0) for f in files}
        }
    
    return category_counts


def run_tests_with_coverage():
    """Run pytest with coverage and return pass rate."""
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/", "-v", "--tb=no"],
        capture_output=True,
        text=True,
        cwd=Path(__file__).parent.parent / "neurocode" / "backend"
    )
    
    # Parse results
    passed = result.stdout.count(" PASSED")
    failed = result.stdout.count(" FAILED")
    skipped = result.stdout.count(" SKIPPED")
    
    total = passed + failed + skipped
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    return {
        "passed": passed,
        "failed": failed,
        "skipped": skipped,
        "total": total,
        "pass_rate": round(pass_rate, 1)
    }


def generate_report():
    """Generate complete test coverage report."""
    print("=" * 60)
    print("PyPal Test Coverage Analysis")
    print("=" * 60)
    print()
    
    # Collect tests
    print("Collecting tests...")
    test_counts, total_tests = collect_tests()
    
    print(f"Found {total_tests} tests in {len(test_counts)} files")
    print()
    
    # Categorize
    category_counts = categorize_tests(test_counts)
    
    # Display by category
    print("Tests by Category:")
    print("-" * 40)
    
    for category, data in sorted(category_counts.items(), key=lambda x: -x[1]["count"]):
        print(f"{category:20} {data['count']:4} tests")
    
    print("-" * 40)
    print(f"{'TOTAL':20} {total_tests:4} tests")
    print()
    
    # Optionally run tests for pass rate
    print("Running tests for pass rate (this may take a moment)...")
    test_results = run_tests_with_coverage()
    
    print()
    print("Test Results:")
    print("-" * 40)
    print(f"Passed:    {test_results['passed']}")
    print(f"Failed:    {test_results['failed']}")
    print(f"Skipped:   {test_results['skipped']}")
    print(f"Pass Rate: {test_results['pass_rate']}%")
    print()
    
    # Save to JSON
    report = {
        "generated_at": datetime.now().isoformat(),
        "total_tests": total_tests,
        "test_files": len(test_counts),
        "file_counts": test_counts,
        "category_counts": category_counts,
        "test_results": test_results
    }
    
    output_path = Path(__file__).parent.parent / "research" / "test_coverage_data.json"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"Report saved to: {output_path}")
    print()
    
    return report


if __name__ == "__main__":
    generate_report()
