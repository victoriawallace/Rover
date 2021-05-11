#!/usr/bin/env q
/ look up, i'm executable
/ requires kdb+ lic to run - https://code.kx.com/q/learn/licensing/
/ command line: q -xmax 4 -ymax 5 -cmds R R F F L F L

.rover.run:{                                                                               / main method - run rover!
  .rover.args:.Q.opt .z.x;                                                                 / parse command line args
  .rover.init[];                                                                           / initialize variables
  -1 "Obstacles at: "," "sv","sv/:string .rover.obstacles;                                 / stdout co-ordinates of obstacles
  -1 "Planet co-ordinates: ",string[.rover.xmax]," x ",string .rover.ymax;                 / stdout planet size
  -1 "Ready to move...";
  .rover.navigate/[.rover.pos;.rover.cmds];                                                / move rover by iterating over list of commands, starting at position (0;0;"E")
  -1 "Navigation complete.  Exiting.";                                                    
  exit 0;                                                                                  / Exit process
 };

.rover.init:{
  .rover.xmax:$[`xmax in key .rover.args;"I"$.rover.args[`xmax;0];10];                     / max co-ord in x direction; '10' if command line argument 'xmax' is not specified
  .rover.ymax:$[`ymax in key .rover.args;"I"$.rover.args[`ymax;0];10];                     / max co-ord in y direction; '10' if command line argument 'ymax' is not specified
  .rover.pos:(0;0;"E");                                                                    / starting position of rover
  .rover.compass:"NESW";                                                                   / possible 'compass' points (the 'z' position)
  .rover.ops:`L`R`F`B!`rot`rot`move`move;                                                  / map operations L(eft), R(ight), F(orward) and B(ack) to an appropriate function name i.e. rot(ate) if L or R, move if F or B
  .rover.cmds:$[`cmds in key .rover.args;`$.rover.args`cmds;20?key .rover.ops];            / list of operations; generate 20 operations at random if 'cmd' not specified as command line argument
  .rover.obstacles:distinct?[floor 0.25*/.rover`ymax`xmax;(cross/)til each .rover`xmax`ymax]; / generate list of random co-ordinates occupied by obstacles.  Space occupied by obstacles must not exceed 25% of the planet's area.
 };

.rover.navigate:{[pos;op]                                                                  / [rover position;operation]
  if[not op in key .rover.ops;                                                             / if 'op' is invalid e.g. 'P'...
    -1 "Invalid operation '",string[op],"'.  Ignoring.";
    :pos;                                                                                  / Ignore. Return current position.
  ];
  newpos:get(.rover .rover.ops op;pos;op);                                                 / Calculate new position
  if[newpos[0 1]in .rover.obstacles;                                                       / Check new position isn't obstructed by some obstacle
    -1 "Operation: ",string[op]," unsuccessful (there's something in my way!). Assuming position at ",","sv string pos;
    :pos;                                                                                  / If so, return original position.
  ];
  -1 "Operation: ",string[op]," successful.  Rover's current position is ",","sv string newpos;
  :newpos;                                                                                 / If the move/rotation was successful, return new position.
 };

.rover.rot:{[pos;op]@[pos;2;:;.rover.compass mod[;4]$[op=`L;neg 1;1]+.rover.compass?pos 2]}; / rotate rover 90 degrees left or right

.rover.move:{[pos;op].rover.moveme[pos;op]. $[pos[2]in"NS";(1;.rover.ymax);(0;.rover.xmax)]}; / move rover forwards or backwards 1 co-ordinate, along the x or y axis (depending on the cardinal direction the rover is facing)

.rover.moveme:{[pos;op;i;m]                                                                / move helper - adds/negates 1 to/from 'i' position based on op ("F" = 1, "B" = -1)
  n:1 1 -1 -1"NESW"?pos 2;                                                                 / multiplier applied to m - corrects direction of movement based on the cardial direction rover is facing i.e. multiplies 'm' by -1 if rover is facing 'W' or 'S'.
  :@/[pos;i;(+;mod);(n*1 -1 `F`B?op;m)]};                                                  / modulus m against new co-ordinate, to ensure we don't 'fall off the edge' of the planet :)

.rover.run[];
