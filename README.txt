----------------
Fish simulation
----------------

Fish of different Speeds and Sizes swim around on the screen as their default behaviour.

Swimming reduces Fish's Hunger bar (depends on Speed). Current Hunger level is represented by a circle around a Fish which changes color accordingly (green - full, yellow - starts getting hungry, red - more hungry, black - preying).

If Hunger level falls below certain value, Fish starts to prey - finds nearest smaller target and starts following it When Fish catches up with its Followning target, it eats it, making her hunger and size go up (depends on eaten Fish's size).

User can interact with Fish by making them follow the mouse cursor (when left mouse button is pressed) or throwing them Food (right mouse button). When Fish follow User's cursor, they cannot eat each other. Thrown Food is treated as any other targets to eat (Fish will chose it if its the closest target).
