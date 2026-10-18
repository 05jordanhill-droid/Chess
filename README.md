# Overview

The game that I programmed is Chess. Due to time contrainsts it stills has a few bugs in it, but the overall functioning is there. Some features I implemented was making it impossible to do illegal moves (except in the case of bugs). I have an inidicator for whose turn it is. When someone has no possible moves left or if their King has been captured, text will display the other player as having won. This is a two-player game.

My purpose for writing this program was to help me improve my skills in game organization in programming and familiarizing myself with how the arcade module works and how I can use it to bring a program to visuals.

[Chess Game Demo Video](https://youtu.be/18qKHvlMZYM)

# Development Environment

The primary tool that I used to help build this software was VSCode.
I used the assistance of ChatGPT to help understand some of the deeper syntaxing of Python as I had to readjust to the lack of specificity compared to C#.

I used Python for the language of this project. Libraries included Arcade, Copy, Math, Annotation, TYPE_CHECKING, and Protocol. Arcade was used to visualize the game. Copy was used in implementing hypothetical moves by making a deep copy of the board. Math was used very lightly, utilizing its absolute value function. Annotation and TYPE_CHECKING were used for deal with some issues with importing custom classes. Protocol was used for a small custom protocol class.

# Useful Websites

* [Python Arcade Tutorial](https://api.arcade.academy/en/stable/tutorials/platform_tutorial/index.html)
* [ChatGPT - Python/Arcade Questions](https://chatgpt.com/share/6ad4260a-1b3c-83e8-a3c3-78b89282f2d3)

# Future Work

* Fixing the remaining bugs
* Implementing best move function
* Implementing Player vs Robot mode