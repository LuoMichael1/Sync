SYNC

By Michael Luo and Deeksha Tandon
====================

A rhythm game made using pygame. 

----------------------------------------------------------------------------
SYNC, the all new, hip, free to play, rhythm game.

Click the circles to the beat of the song as they pass over the valves of a trumpet. Build up your streak to get exponentially more points and beat your friends highscores!

Open up the lesson to learn about music and specifically trumpets. Afterwards, try your luck with a quiz containing 5 multiple choice questions about the topics in the lesson!

And finally, once you’re done, click exit on the menu screen to display our sources before automatically closing the game.
----------------------------------------------------------------------------

Open main.py to play!


====================
System requirements:

Processor: Intel core i5 6th Gen
Memory: 512 MB RAM
Graphics: Integrated GPU
Storage: 20MB
OS: Windows 10

Note: These are estimates, you can probably get away with less 

===================
How to play

Circles / targets will appear from the right side of the screen and your job is to click the corresponding key on your keyboard when that circle passes over the valves. The valves are the 3 circles lined up on the left side of the screen. The closer the circles are to the valves when you click, the better your score.

The controls are ASD, A corresponds to the top lane, S corresponds to the middle lane, and D controls the bottom lane. 
The bar in the top center of your screen shows the song's progress.

The number in the top right shows your score and the number in the bottom right shows your streak.
Please be aware that your score is note saved!

Also, your quiz score is automatically set to 0 until you fill out the quiz

===================
Troubleshooting

If any issues occur try:
1 try restarting the program
2 ensure that the correct versions of pygame and python are properly installed
3 try reinstalling SYNC

If nothing succeeds in resolving the issue, please contact Dtanfr#7151 on discord.

==================
How to upload your own levels

Remove the current file called level1.txt and create a new text file with the name, level1.txt.
The first line of the file should contain the name of the music file and its file path, the second line contains the speed of the circles. Set this number higher to increase the difficulty and lower it to reduce the speed of the targets. 

After You can have as many of the following lines which contain the information for spawning the targets.

10 0 1 0

The first number contains the time at which the target should be at the evaluation line and the following 3 spots tell the program which lane to spawn the circles in. So in the example above it spawns a circle in the center lane that will arrive at the evaluation line at the ten second mark. 

Note: the last line in the file will not be read correctly, you can add 0 0 0 0 to the end of your level to negate this issue. Also, please order your notes in chronological order and give enough time for the first note to reach the evaluation line.




