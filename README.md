# Smart Fitness Session Analyzer

**Student name:** Sebastian Skrøvseth Haugen
**Student number:** 409883

## What this project does

This is a program that pretends to be a fitness centre getting data from wearable devices during training sessions. It takes in a bunch of raw readings (heart rate, skin response, temperature, activity level, signal quality, that kind of thing), checks whether each reading actually makes sense, and groups the good ones into a session for one participant. Made for the first assignmnet in the course ACIT4420 Problem-Solving with Scripting.

Once it has a session, it works out the average, min and max for heart rate and activity level, compares those against the participant's own baseline, and figures out whether the session counts as resting, moderate activity, high activity, recovering, or just insufficient data if too much of it got rejected. It also checks if heart rate and activity dropped off near the end, which is basically how it decides someone is recovering. At the end it prints a normal readable report explaining what it found and why.

## Class design

I created four classes different classes for this assignment.

`Observation` is one single reading. It knows how to build itself from the raw dictionary the generator spits out, and it knows how to check whether it's actually valid (missing values, impossible heart rate, bad signal quality and stuff like that).

`Participant` holds the person's id and their baseline numbers (resting heart rate, skin response, temperature). I kept the baseline values behind a protected attribute called `_reference` so they can't just get overwritten by accident, you have to go through a property or the `update_reference` method which checks the value first.

`Session` is just a participant plus a list of observations. This is the composition part of the assignment, a session isn't a type of participant or a type of observation, it just contains both, so composition made more sense than inheritance here.

`SessionAnalyzer` takes a session and does the actual analysis, the summaries, the comparison to baseline, the classification, and the recovery check. It hands back everything as one dictionary.

I decided not to force any inheritance into the design since nothing here is really an "is a" relationship, so instead of making something extend something else just to tick a box, I went with the assignment's other option which is to explain why composition made more sense. Session having a Participant and a list of Observations is that example.

For the class method and static method requirement, `Observation.from_dict()` and `Participant.from_profile()` are both classmethods that build the object straight from a generator dictionary, and `Observation.is_within_range()` is a staticmethod since it doesn't need any instance data at all, it's just a reusable range check I use for a few different fields.

The standalone functions are `compute_summary_stats()`, `classify_intensity()`, `detect_recovery()`, `build_reasoning()` and `format_console_report()`. None of these needed to be methods on a class, they each just do one job (a calculation, a classification, or printing something readable to the console).

## Assumptions and classification rules

An observation gets rejected if heart rate or skin response is missing, heart rate is outside 30 to 220 bpm, activity level or signal quality is outside 0 to 1, or signal quality drops below 0.6.

A session needs at least 3 usable observations before it even attempts a classification, otherwise it just reports insufficient data.

Resting means the average heart rate is close to baseline (within about 10 bpm) and activity level stays low.

Moderate activity is a bigger gap from baseline but still under a certain threshold, high activity is anything above that.

Recovering overrides whatever classification it would've gotten if the second half of the session clearly shows heart rate and activity dropping compared to the first half.

All the actual numbers for these thresholds live near the top of `main.py` so they're easy to find and tweak if needed.

## Project structure

```
your-repository/
├── README.md
├── data_generator.py   (the one given by the instructor, untouched)
├── main.py              (all the classes plus the demo that runs everything)
├── sample_data.py       (sample sessions and some hand made test data)
├── tests.py              (the required scenarios plus a few extra checks)
└── requirements.txt     (empty, only standard library used)
```

## Installation and running instructions

Nothing to install, it's all standard library.

```bash
git clone https://github.com/SebastianHaugen/ACIT4420-assignment1.git
cd ACIT4420-assignment1
python main.py
```

My machine just uses python or py not python3 

To run the tests:

```bash
python tests.py
```

## Example output

```
=== Fitness Session Report ===
Participant: P001
Observations received: 12 | Usable: 12 | Rejected: 0

Heart rate   - avg: 118.08 | min: 99 | max: 130
Activity lvl - avg: 0.85 | min: 0.71 | max: 0.94
Heart rate vs reference: +56.08 bpm

Classification: HIGH ACTIVITY
Recovery detected: No
Reasoning: Average heart rate was 118.08 bpm (+56.1 bpm vs reference). Values remained elevated with no clear downward trend.
```

## Test scenarios

`tests.py` covers all five required scenarios: resting, moderate activity, high activity, recovery, and poor quality or invalid data. There are also a couple of extra tests for validating individual observations and for the insufficient data case when there just isn't enough usable data.

## Known limitations

The classification thresholds (what counts as resting vs moderate vs high, and the MIN_USABLE_OBSERVATIONS = 3 cutoff) are just numbers I picked that seemed reasonable, not something derived from any real fitness science. A real system would probably tune these per participant or based on actual research.

Skin response and temperature get validated and rejected if they're bad, but they don't actually factor into the classification or recovery logic at all, only heart rate and activity level do. So a session could have completely normal skin response and temperature and it wouldn't change the result either way.

Recovery detection is pretty basic, it just splits the session in half and checks if the second half trends down compared to the first half. It doesn't look at how fast the decline happens or use the actual timestamp gaps, so a long slow decline and a short sharp one would get treated the same way.

The generator uses a fixed seed in a few places (like the demo in main.py), so running it repeatedly gives identical results. That's useful for reproducibility but means the demo never shows the natural variation you'd get from truly random data.

It's also entirely built around the simulated data from data_generator.py. There's no real device, no database, and nothing persists between runs, every time you run main.py it's starting from scratch.