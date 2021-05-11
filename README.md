#### Primary Objectives

- Implement a library capable of modelling the basic movement of the rover for a list of valid input commands.
- Implement wrapping across edges of the grid (since planets aren’t flat!) - disregard issues with polar coordinates.
- Implement obstacle detection before each movement step - on encountering an obstacle at its next destination the rover should halt at the last valid location & report its current position and location of the obstacle.

#### Secondary Objectives

 - Suggest and implement a revised control scheme to reduce the storage requirements for input commands
 - The rover is expected to have intermittent power issues which means that storing state & commands in memory only is unreliable. Assuming that execution of a movement instruction is not instantaneous, implement a solution to ensure that the rover can resume the navigation process after a power outage (you may assume that persistent disk storage with atomicity for individual reads/writes is available).


#### Solution

The main method initializes the planet's co-ordinates programmatically by asking the user to input some x and y limit.
An instance of `Rover` is initialized and a list of obstacle-occupied co-ordinates generately randomly (within the confines of the planet's axis.)
The program then asks the user to initialize the rover's starting position.  `Rover.isvalid` is called to check that the input provided is acceptable.
We then iterate over a list of commands i.e. R, L, F, B, and call `Rover.navigate` to move the rover to a new position, based on the rover's current position and operation to be performed.  Depending on the nature of the operation (a 90 degree left/right rotation or forwards/backwards movement), `Rover.navigate` will call either `Rover.move` and `Rover.rotate`. The new position is calculated here and both functions handle 'edge wrapping'.  `Rover.navigate` checks the newly calculated position against the obstacle-occupied co-ordinates.  In the case of a collision, the original position of the rover is returned.  Otherwise, the new position is returned and we move onto the next operation. 

To handle objective (4), the program opens a handle to file commands.txt.  This file contains the list of 'operations' to be performed by the rover.  The program reads the operations in one at a time to avoid retaining the whole list in-memory.
To handle objective (5), the program opens a handle to file results.txt.  For every operation we perform, the new position is persisted to disk.  This way, we have a log of the Rover's journey.  Alternatively, we could write to some other in-memory table and persist at EOD to avoid numerous writes.  We should also maintain some index which would point to the next operation in commands.txt.

I've implemented a solution both in python (code/python/rover.py) and in q (code/q/rover.q).  I realise rover.q requires a kdb+ license to run, so I've provided an example of the output rover.q produces (code/q/example0.txt).
An example of the output produced by the python version is also provided (code/python/example0.txt).  The programs behave quite similarly.

To run rover.py: `python code/python/rover.py`

There are some obvious improvements.  For example, I didn't get round to writing unit tests.
Further, the program assumes that 'Rover/' lives in the user's home directory.
