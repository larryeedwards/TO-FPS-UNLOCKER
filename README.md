A cross-platform framerate patcher for Tornado Outbreak. It allows you to target the game to a designated framerate or optionally, run at an unlocked framerate all together. Requires either a decrypted .xex file via xextool, a decrypted .elf file, or a main.dol file.

# Usage
1. Extract your .xex / .elf / .dol
2. Run `patcher.py` or download the release exe  
3. Use browse to navigate to your designated executable
4. Choose a target framerate from the dropdown.
5. Select patch file
6. Launch your newly patched executable in-game for results
# Framerate evaulation
**Note: Performance may vary on specs. On console, 60 is the max limit.**
### Performance Key
| Icon | Meaning                      |
| ---- | ---------------------------- |
| ✔️   | No issues                    |
| ⚠️   | Still playable, proceed with caution |
| ❌    | Unplayable |
## Dolphin
| Target FPS   | Compatibility | Notes                                                                                      |
| ------------ | ------------- | ------------------------------------------------------------------------------------------ |
| **30**       | ✔️            | Default framerate                                                                          |
| **60**       | ✔️            | Occasional drops to 30 FPS during heavy scenes                                             |
| **120**      | ⚠️            | Requires Enable VBI Frequency Override set to 201% to work                                 |
| **Uncapped** | ⚠️            | Max Framerate is capped to 60 FPS unless VBI Frequency Override is set to 500%             |
## RPCS3
| Target FPS   | Compatibility | Notes                                            |
| ------------ | ------------- | ------------------------------------------------ |
| **30**       | ✔️            | Default framerate                                |
| **60**       | ✔️            | Runs at a stable 60 FPS                          |
| **120**      | ❌            | The Grab Move with **R1** becomes unstable. Training Campground becomes impossible to complete, thus limiting the playability to the first two levels |
| **Uncapped** | ❌            | Cannot naturally progress through the game without completing the Training Campground level. Bypassing with a save technically makes the game playable, but restoring L.O.A.D. STARR's timer with Chain Collecting becomes unusable due to the high framerate |
## Xenia Canary
| Target FPS   | Compatibility | Notes                             |
| ------------ | ------------- | --------------------------------- |
| **30**       | ✔️            | Default framerate                 |
| **60**       | ✔️            | Maintains steady 60 FPS           |
| **120**      | ✔️            | Occasional dips to **88–120 FPS** |
| **Uncapped** | ✔️            | Drops to ~101 FPS in heavy scenes |
