# Why Your Code Isn’t Pythonic (And How to Fix It)

https://www.youtube.com/watch?v=bsU7AFjh4m8

"import this" at terminal to get python philosophy


Remove the unnecessary FitnessTracker class
- Has no instance variables.
- We don't need multiple instance of fitnessTracker.
- Delete self from function params, de-indent the methods.


Replace open and close files with context manager.
- Change to with open(...) as f:


Add type annotations.

Ask for forgiveness instead of asking for permission.

Use dataclasses for structured date.




0:18 What does Pythonic mean?
2:08 Before
3:13 Step 1 – Prefer Functions Over Classes
4:32 Step 2 – Use Context Managers
6:42 Step 3 – Add Type Annotations
10:46 Step 4 – Favor EAFP Over LBYL
12:06 Step 5 – Use Dataclasses for Structured Data
17:09 Step 6 – Centralize File Paths and Use
19:19 Step 7: Rely on Python's strengths
23:10 Step 8 – Add Logging Instead of Print
24:10 Step 9 – Add a Main Function
25:56 Final Thoughts