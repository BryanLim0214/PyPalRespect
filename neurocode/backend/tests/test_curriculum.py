"""
Tests for the Python curriculum exercises.
"""
import pytest
import json


class TestCurriculumStructure:
    """Test curriculum data structure and content."""
    
    def test_curriculum_loads(self):
        """Curriculum module should load without errors."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        assert len(exercises) > 0
    
    def test_curriculum_has_exercises(self):
        """Should have at least 15 exercises in curriculum."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        assert len(exercises) >= 15, f"Expected at least 15 exercises, got {len(exercises)}"
    
    def test_all_exercises_have_required_fields(self):
        """Every exercise must have all required fields."""
        from app.data.curriculum import get_all_exercises
        
        required_fields = [
            "title", "description", "difficulty", "concept",
            "grade_level", "estimated_minutes", "step_count",
            "starter_code", "solution_code", "steps", "interest_tags"
        ]
        
        exercises = get_all_exercises()
        
        for ex in exercises:
            for field in required_fields:
                assert field in ex, f"Exercise '{ex['title']}' missing field '{field}'"
    
    def test_grade_level_distribution(self):
        """Should have exercises for grades 6, 7, and 8."""
        from app.data.curriculum import get_exercises_by_grade
        
        grade_6 = get_exercises_by_grade(6)
        grade_7 = get_exercises_by_grade(7)
        grade_8 = get_exercises_by_grade(8)
        
        assert len(grade_6) >= 4, "Should have at least 4 grade 6 exercises"
        assert len(grade_7) >= 4, "Should have at least 4 grade 7 exercises"
        assert len(grade_8) >= 3, "Should have at least 3 grade 8 exercises"
    
    def test_difficulty_matches_grade(self):
        """Difficulty should be appropriate for grade level."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            if ex["grade_level"] == 6:
                assert ex["difficulty"] <= 2, f"Grade 6 exercise '{ex['title']}' has difficulty > 2"
            elif ex["grade_level"] == 7:
                assert ex["difficulty"] <= 3, f"Grade 7 exercise '{ex['title']}' has difficulty > 3"
            elif ex["grade_level"] == 8:
                assert ex["difficulty"] <= 4, f"Grade 8 exercise '{ex['title']}' has difficulty > 4"


class TestADHDFriendlyDesign:
    """Test ADHD-specific design requirements."""
    
    def test_step_count_within_limits(self):
        """Each exercise should have 2-5 steps (ADHD friendly)."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            assert 2 <= ex["step_count"] <= 5, \
                f"Exercise '{ex['title']}' has {ex['step_count']} steps (should be 2-5)"
    
    def test_estimated_time_reasonable(self):
        """Estimated time should be 5-25 minutes (ADHD attention span)."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            assert 5 <= ex["estimated_minutes"] <= 25, \
                f"Exercise '{ex['title']}' is {ex['estimated_minutes']} min (should be 5-25)"
    
    def test_steps_are_valid_json(self):
        """Steps should be valid JSON."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            steps = json.loads(ex["steps"])
            assert isinstance(steps, list)
            assert len(steps) == ex["step_count"], \
                f"Exercise '{ex['title']}' has mismatched step_count"
    
    def test_steps_have_required_fields(self):
        """Each step should have number, title, instruction, checkpoint."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            steps = json.loads(ex["steps"])
            for step in steps:
                assert "number" in step
                assert "title" in step
                assert "instruction" in step
                assert "checkpoint" in step
    
    def test_exercises_have_checkpoints(self):
        """Each exercise should have at least one checkpoint step."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            steps = json.loads(ex["steps"])
            checkpoints = [s for s in steps if s["checkpoint"]]
            assert len(checkpoints) >= 1, \
                f"Exercise '{ex['title']}' has no checkpoints"
    
    def test_interest_tags_present(self):
        """Each exercise should have at least one interest tag."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            tags = json.loads(ex["interest_tags"])
            assert len(tags) >= 1, \
                f"Exercise '{ex['title']}' has no interest tags"


class TestSolutionCodeValidity:
    """Test that solution code is valid Python."""
    
    def test_solution_code_compiles(self):
        """Solution code should compile without syntax errors."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            try:
                compile(ex["solution_code"], f"<{ex['title']}>", "exec")
            except SyntaxError as e:
                pytest.fail(f"Exercise '{ex['title']}' solution has syntax error: {e}")
    
    def test_starter_code_compiles(self):
        """Starter code should compile without syntax errors."""
        from app.data.curriculum import get_all_exercises
        exercises = get_all_exercises()
        
        for ex in exercises:
            try:
                compile(ex["starter_code"], f"<{ex['title']}>", "exec")
            except SyntaxError as e:
                pytest.fail(f"Exercise '{ex['title']}' starter code has syntax error: {e}")


class TestConceptCoverage:
    """Test curriculum covers required concepts."""
    
    def test_covers_print(self):
        """Should have print exercises."""
        from app.data.curriculum import get_exercises_by_concept
        assert len(get_exercises_by_concept("print")) >= 1
    
    def test_covers_variables(self):
        """Should have variables exercises."""
        from app.data.curriculum import get_exercises_by_concept
        assert len(get_exercises_by_concept("variables")) >= 1
    
    def test_covers_conditionals(self):
        """Should have conditionals exercises."""
        from app.data.curriculum import get_exercises_by_concept
        conditionals = get_exercises_by_concept("conditionals")
        if_else = get_exercises_by_concept("if-else")
        assert len(conditionals) + len(if_else) >= 2
    
    def test_covers_loops(self):
        """Should have loops exercises."""
        from app.data.curriculum import get_exercises_by_concept
        assert len(get_exercises_by_concept("loops")) >= 1
    
    def test_covers_lists(self):
        """Should have lists exercises."""
        from app.data.curriculum import get_exercises_by_concept
        lists = get_exercises_by_concept("lists")
        list_methods = get_exercises_by_concept("list-methods")
        assert len(lists) + len(list_methods) >= 2
    
    def test_covers_functions(self):
        """Should have functions exercises."""
        from app.data.curriculum import get_exercises_by_concept
        assert len(get_exercises_by_concept("functions")) >= 2
