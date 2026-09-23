"""Sample data used by main.py and tests.py.

Provides generator-based sample sessions (via data_generator.py, with fixed
seeds for reproducibility) plus a few hand-built raw observation dictionaries
for testing validation edge cases directly, independent of randomness.
"""

from data_generator import generate_fitness_data


def get_sample_scenario(scenario, seed=1, number_of_windows=12):
    """Return (profile, observations) for one scenario, with a fixed seed
    so the same call always produces the same data.
    """
    return generate_fitness_data(
        participant_id="P001",
        scenario=scenario,
        seed=seed,
        number_of_windows=number_of_windows,
    )


# Hand-built raw observations for validation edge-case tests.

VALID_OBSERVATION = {
    "timestamp": 0,
    "heart_rate": 90,
    "skin_response": 1.8,
    "temperature": 32.0,
    "activity_level": 0.30,
    "signal_quality": 0.90,
}

MISSING_HEART_RATE = {
    "timestamp": 1,
    "heart_rate": None,
    "skin_response": 1.8,
    "temperature": 32.0,
    "activity_level": 0.30,
    "signal_quality": 0.90,
}

IMPOSSIBLE_HEART_RATE = {
    "timestamp": 2,
    "heart_rate": 265,
    "skin_response": 1.8,
    "temperature": 32.0,
    "activity_level": 0.30,
    "signal_quality": 0.90,
}

NEGATIVE_ACTIVITY_LEVEL = {
    "timestamp": 3,
    "heart_rate": 90,
    "skin_response": 1.8,
    "temperature": 32.0,
    "activity_level": -0.20,
    "signal_quality": 0.90,
}

LOW_SIGNAL_QUALITY = {
    "timestamp": 4,
    "heart_rate": 90,
    "skin_response": 1.8,
    "temperature": 32.0,
    "activity_level": 0.30,
    "signal_quality": 0.40,
}