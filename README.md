# Smart Fitness Session Analyzer

**Student name:** Sebastian Skrøvseth Haugen
**Student number:** 409883

## What this project does

This program simulates a fitness centre that receives heart-rate and other sensor
readings from wearable devices during training sessions. It takes a stream of raw
observations (timestamp, heart rate, skin response, temperature, activity level,
signal quality), checks whether each reading is trustworthy, and groups the good
readings into a session for one participant.

Once a session is built, the program:

- calculates summary statistics (average, min, max) for heart rate and the other
  measurements,
- compares those numbers against the participant's personal reference values,
- classifies the session as **resting**, **moderate activity**, **high activity**,
  **recovering**, or **insufficient data**,
- checks whether heart rate and activity level drop off near the end of the
  session (a sign of recovery), and
- prints a readable console report explaining how many observations were used
  and why the session was classified the way it was.

## Class design

| Class | Responsibility |
|---|---|
| `Participant` | Stores a participant's identity and personal reference measurements (resting heart rate, max heart rate, etc.). The reference values are kept as a protected attribute and only reachable through a property/methods, so they can't be overwritten with bad data by accident. |
| `Observation` | Represents one single measurement window from the wearable device. Knows how to validate itself (missing fields, out-of-range values, bad signal quality) and reports whether it is usable. |
| `Session` | Composed of one `Participant` object and a list of `Observation` objects. This is the clearest example of composition in the project — a session *has* a participant and *has* observations, rather than being one of them. Session is responsible for filtering out invalid observations and handing off usable data to the analyzer. |
| `SessionAnalyzer` (base class) | Defines the general steps needed to analyze a session: compute summaries, compare to reference values, classify, and check for recovery. |
| `RecoveryAwareAnalyzer` (subclass of `SessionAnalyzer`) | Overrides the classification step to add recovery detection (checking whether the tail end of a session shows declining heart rate/activity). This is where inheritance and method overriding are used meaningfully — the base analyzer knows how to classify activity level, and the subclass adds the extra recovery-specific logic on top instead of duplicating the whole class. |
| `ReportGenerator` | Takes the structured result dictionary produced by the analyzer and turns it into a readable console report. Kept separate from the analysis logic so that presentation and calculation don't get mixed together. |

### Where the requirements are demonstrated

- **Composition:** `Session` contains a `Participant` and a list of `Observation` objects.
- **Encapsulation:** `Participant`'s reference values are stored as `_reference_values` (protected) and only accessed/updated through a property and setter methods, which validate the new values before accepting them.
- **Inheritance & overriding:** `RecoveryAwareAnalyzer` inherits from `SessionAnalyzer` and overrides the classification method to add recovery detection.
- **Class/static method:** `Observation.from_raw_dict()` is a class method that builds an `Observation` from the raw dictionary produced by the data generator, keeping that conversion logic in one place. `Observation.is_within_human_range()` is a static method used to sanity-check a heart rate or temperature value without needing an instance.
- **Standalone functions:** `validate_observation()`, `compute_summary_stats()`, `classify_intensity()`, `detect_recovery()`, and `format_console_report()` are written as plain functions rather than methods, since they do a single calculation/validation/presentation job that doesn't need to belong to a class.

## Assumptions and classification rules

- An observation is considered **invalid** if any required field is missing, heart
  rate is outside a realistic human range, signal quality is below a set
  threshold (e.g. `0.5`), or activity level / skin response fall outside `0–1`.
- A session needs a minimum number of valid observations (e.g. `3`) before it can
  be classified; otherwise it is reported as **insufficient data**.
- **Resting**: average heart rate close to the participant's resting reference
  and low activity level throughout.
- **Moderate / high activity**: average heart rate and activity level exceed the
  resting reference by set margins, with high activity representing the larger
  gap.
- **Recovering**: heart rate and activity level are elevated earlier in the
  session but show a clear downward trend in the final portion.
- Exact thresholds and margins are defined as constants near the top of
  `main.py` so they're easy to find and adjust.

## Project structure

```
your-repository/
├── README.md
├── main.py            # entry point, ties everything together and prints the report
├── sample_data.py      # example participants/sessions built using the data generator
├── tests.py             # test scenarios (see below)
└── requirements.txt    # empty — standard library only
```

## Installation and running instructions

This project only uses the Python standard library — no installation needed
beyond Python itself.

```bash
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY
python3 main.py
```

If your system uses `python` instead of `python3`, run `python main.py` instead.

To run the test scenarios:

```bash
python3 tests.py
```

## Example output

```
=== Fitness Session Report ===
Participant: Alex (ref. resting HR: 62 bpm)
Observations received: 10 | Usable: 9 | Rejected: 1 (bad signal quality)

Average heart rate: 134.2 bpm
Average activity level: 0.71
Heart rate vs reference: +72.2 bpm above resting

Classification: HIGH ACTIVITY
Recovery detected: No

Reasoning: Average heart rate and activity level are well above the
participant's resting reference throughout the session, with no
downward trend near the end.
```

## Test scenarios

`tests.py` covers the five required scenarios:

1. Resting session
2. Moderate activity session
3. High activity session
4. Activity followed by recovery
5. Poor-quality / invalid sensor data (mix of missing fields, bad signal
   quality, out-of-range values)

## Known limitations

- Thresholds for classification (e.g. what counts as "high" activity) are
  fixed constants rather than personalized per participant beyond the
  resting/max heart rate reference.
- Recovery detection only looks at the trend in the final segment of a
  session; it does not model heart-rate-recovery time in seconds.
- The program works entirely on simulated data from `data_generator.py` and
  does not connect to a real wearable device or database.