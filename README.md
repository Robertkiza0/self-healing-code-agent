# Self-Healing Code Agent

An experimental Python prototype demonstrating an automated software development agent loop. 

## How it works
1. **Execute:** The agent attempts to run a target Python script via a subprocess pipeline.
2. **Catch:** If a runtime exception occurs (e.g., NameError, SyntaxError), the agent captures the exact traceback error stream.
3. **Reflect & Fix:** The error context is structured into a feedback loop to generate automated software patches.
4. **Validate:** The corrected code is written back to disk and re-tested autonomously.
   i used llam3.2 on my litte I5 core 8RAM to try it
