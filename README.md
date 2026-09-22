# Smart Fitness Session Analyzer

## What this project does

This program simulates a fitness centre that receives heart-rate and other sensor readings from wearable devices during training sessions. It takes a stream of raw observations (timestamp, heart rate, skin response, temperature, activity level, signal quality), checks whether each reading is trustworthy, and groups the good
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

Will finish readme when the project is finished