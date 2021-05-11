## Challenge

You are responsible for building software to control the movement and behavior of an interplanetary rover. Since you won’t be able to fix your code    once it is deployed onboard, you should ensure that your program will function as intended with suitable tests.

To simplify navigation, the planet has been divided into a two-dimensional cartesian grid. The rover’s position (consisting of its location and compass orientation) is represented as a 3-tuple of x & y coordinates together with one of the 4 cardinal compass points (N,E,S,W). An example position could be (0, 0, E) which would indicate the rover is in the bottom-left of the grid & facing East. Increases to the X & Y values correspond to movement in the East & North directions respectively.

Navigation is achieved by a simple string of commands represented by single letters (“F”, “B”, “L”, “R”):

  - “F” or “B” indicate movement forwards/backwards. Movement is only in discrete grid point intervals, and the rover’s orientation should be unchanged afterwards.

  - “L” and “R” indicate rotation on the spot of 90 degrees left/right, i.e. without a change in grid position


Assume that the dimensions of the grid & the rover’s initial landing position within it are known ahead of time and can be loaded into the rover at startup.

An initial survey of obstacles in the grid has already been conducted, and is available as a separate pre-loaded list of 2-tuples, each giving a point on the grid that should be treated as impassable.

## Primary Objectives

- Implement a library capable of modelling the basic movement of the rover for a list of valid input commands.
- Implement wrapping across edges of the grid (since planets aren’t flat!) - disregard issues with polar coordinates.
- Implement obstacle detection before each movement step - on encountering an obstacle at its next destination the rover should halt at the last valid location & report its current position and location of the obstacle.

## Secondary Objectives

- Suggest and implement a revised control scheme to reduce the storage requirements for input commands
- The rover is expected to have intermittent power issues which means that storing state & commands in memory only is unreliable. Assuming that execution of a movement instruction is not instantaneous, implement a solution to ensure that the rover can resume the navigation process after a power outage (you may assume that persistent disk storage with atomicity for individual reads/writes is available).
