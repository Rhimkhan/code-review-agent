import pytest

def test_github_tools_import():
    from src.tools.github_tools import get_pr_files, get_pr_diff
    assert callable(get_pr_files)
    assert callable(get_pr_diff)

def test_evaluation_pipeline_import():
    from src.evaluation.pipeline import EvaluationPipeline
    pipeline = EvaluationPipeline()
    assert pipeline is not None

def test_ground_truth_samples():
    from src.evaluation.ground_truth import GROUND_TRUTH_SAMPLES
    assert len(GROUND_TRUTH_SAMPLES) > 0
    assert "code" in GROUND_TRUTH_SAMPLES[0]
    assert "expected_findings" in GROUND_TRUTH_SAMPLES[0]
