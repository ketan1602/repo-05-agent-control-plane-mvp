import pytest

from cost import (
    Assumptions,
    MissingAssumptionError,
    PlatformCosts,
    run_cost_event,
    summarize,
)


def _assumptions() -> Assumptions:
    return Assumptions(
        token_price_per_1k=0.002,
        approval_minutes=30,
        reviewer_rate_per_hour=60,
        remediation_per_violation=500,
        cost_center="CC-100",
        platform=PlatformCosts(0.01, 0.02, 0.03),
    )


def test_approval_cost_is_minutes_at_hourly_rate():
    assert _assumptions().approval_cost == pytest.approx(30.0)


def test_clean_run_costs_model_tokens_plus_platform_only():
    event = run_cost_event(
        run_id="r1", agent_id="a", workflow="w", tokens=1000,
        successful=True, escalated=False, violated=False, assumptions=_assumptions(),
    )
    assert event.model == pytest.approx(0.002)
    assert event.human_review == 0.0
    assert event.remediation == 0.0
    assert event.cost == pytest.approx(0.002 + 0.01 + 0.02 + 0.03)


def test_escalated_and_violated_run_adds_review_and_remediation():
    event = run_cost_event(
        run_id="r2", agent_id="a", workflow="w", tokens=0,
        successful=False, escalated=True, violated=True, assumptions=_assumptions(),
    )
    assert event.human_review == pytest.approx(30.0)
    assert event.remediation == pytest.approx(500.0)
    assert event.cost == pytest.approx(0.06 + 30.0 + 500.0)


def test_summarize_counts_runs_and_successes():
    events = [
        run_cost_event(run_id=str(i), agent_id="a", workflow="w", tokens=1000,
                       successful=i % 2 == 0, escalated=False, violated=False,
                       assumptions=_assumptions())
        for i in range(4)
    ]
    econ = summarize(events)
    assert econ.runs == 4
    assert econ.successes == 2
    assert econ.cost_per_success == pytest.approx(econ.total_cost / 2)


def test_summarize_with_no_successes_is_infinite_per_success():
    assert summarize([]).cost_per_success == float("inf")


def test_assumptions_require_every_env_value(monkeypatch):
    monkeypatch.setenv("COST_CENTER", "CC-1")
    for name in ("LLM_COST_PER_1K_TOKENS", "HUMAN_APPROVAL_MINUTES",
                 "HUMAN_REVIEW_RATE_PER_HOUR", "VIOLATION_REMEDIATION_COST_USD",
                 "PLATFORM_RUNTIME_COST_PER_RUN", "PLATFORM_OBSERVABILITY_COST_PER_RUN",
                 "PLATFORM_CONTROL_COST_PER_RUN"):
        monkeypatch.setenv(name, "1")
    monkeypatch.delenv("LLM_COST_PER_1K_TOKENS")
    with pytest.raises(MissingAssumptionError, match="LLM_COST_PER_1K_TOKENS"):
        Assumptions.from_env()


def test_assumptions_reject_negative_values(monkeypatch):
    monkeypatch.setenv("COST_CENTER", "CC-1")
    monkeypatch.setenv("LLM_COST_PER_1K_TOKENS", "-1")
    with pytest.raises(MissingAssumptionError, match="must not be negative"):
        Assumptions.from_env()
