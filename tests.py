"""
Tests for the Smart Fitness Session Analyzer.

Run with: python3 tests.py
"""

from main import Observation, Participant, Session, SessionAnalyzer, build_session
from sample_data import (
    get_sample_scenario,
    VALID_OBSERVATION,
    MISSING_HEART_RATE,
    IMPOSSIBLE_HEART_RATE,
    NEGATIVE_ACTIVITY_LEVEL,
    LOW_SIGNAL_QUALITY,
)


def check(condition, message):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {message}")
    if not condition:
        raise AssertionError(message)


# --- Scenario 1: resting session --------------------------------------------

def test_resting_session():
    session = build_session("resting", seed=1)
    result = SessionAnalyzer(session).analyze()
    check(result["classification"] == "resting", "Resting session classified as resting")


# --- Scenario 2: moderate activity ------------------------------------------

def test_moderate_activity_session():
    session = build_session("moderate_activity", seed=1)
    result = SessionAnalyzer(session).analyze()
    check(
        result["classification"] == "moderate activity",
        "Moderate-activity session classified as moderate activity",
    )


# --- Scenario 3: high activity -----------------------------------------------

def test_high_activity_session():
    session = build_session("high_activity", seed=1)
    result = SessionAnalyzer(session).analyze()
    check(
        result["classification"] == "high activity",
        "High-activity session classified as high activity",
    )


# --- Scenario 4: activity followed by recovery -------------------------------

def test_recovery_session():
    session = build_session("recovery", seed=1, number_of_windows=14)
    result = SessionAnalyzer(session).analyze()
    check(result["recovery_detected"] is True, "Recovery session flagged as recovery_detected")


# --- Scenario 5: poor-quality / invalid sensor data ---------------------------

def test_poor_quality_session():
    session = build_session("poor_quality", seed=1)
    result = SessionAnalyzer(session).analyze()
    check(
        result["rejected_observations"] > 0,
        "Poor-quality session rejects at least one observation",
    )


# --- Extra: validation of individual observations -----------------------------

def test_observation_validation():
    check(Observation.from_dict(VALID_OBSERVATION).is_valid()[0] is True,
          "Valid observation passes validation")
    check(Observation.from_dict(MISSING_HEART_RATE).is_valid()[0] is False,
          "Observation with missing heart rate is rejected")
    check(Observation.from_dict(IMPOSSIBLE_HEART_RATE).is_valid()[0] is False,
          "Observation with an impossible heart rate is rejected")
    check(Observation.from_dict(NEGATIVE_ACTIVITY_LEVEL).is_valid()[0] is False,
          "Observation with a negative activity level is rejected")
    check(Observation.from_dict(LOW_SIGNAL_QUALITY).is_valid()[0] is False,
          "Observation with low signal quality is rejected")


# --- Extra: not enough usable data --------------------------------------------

def test_insufficient_data():
    profile, observations = get_sample_scenario("resting", seed=1, number_of_windows=6)
    participant = Participant.from_profile(profile)
    # Keep only 2 observations - not enough for a reliable classification.
    session = Session(participant, [Observation.from_dict(o) for o in observations[:2]])
    result = SessionAnalyzer(session).analyze()
    check(
        result["classification"] == "insufficient_data",
        "Session with too few usable observations is 'insufficient_data'",
    )


def run_all():
    test_resting_session()
    test_moderate_activity_session()
    test_high_activity_session()
    test_recovery_session()
    test_poor_quality_session()
    test_observation_validation()
    test_insufficient_data()
    print("\nAll tests passed.")


if __name__ == "__main__":
    run_all()