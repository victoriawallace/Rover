import os
from random import randint as rndm

class Rover(object):
  """
  Set-up the axis we will be working with i.e. xmax * ymax
  Generate random set of co-ordinates which will be occupied by objects
  """
  def __init__(self,xmax,ymax):
    self.xmax = xmax
    self.ymax = ymax
    self.obstacles = self.getobstacles()

  """
  By default, let's say these obstacles cannot occupy more than 25% of the planet's area.
  I could do something smarter here to ensure/return only distinct co-ordinates.
  """
  def getobstacles(self):
    n = self.xmax * self.ymax // 4
    return [(rndm(0,self.xmax - 1),rndm(0,self.ymax -1)) for i in range(n)]

  # check x,y are valid co-ordinates, c represents a valid cardinal direction and x,y is not occupied by an obstacle.
  def isvalid(self,x,y,c):
    return x <= self.xmax and y <= self.ymax and c in self.compass.keys() and not (x,y) in self.obstacles

  """
  Method that controls the movement of the Rover.
  Checks the operation is allowed i.e. 'L','R','F' or 'B'.  If not, the current position is returned.
  If it is valid, navigate() will calculate the rover's new position based on the arguments provided.
  If the new position coincides with an obstacle, the original position is returned.
  Otherwise, the newly calculated position is returned.
  """
  def navigate(self,pos,op):
    # if op not in key action
    if not op in self.action.keys():
      print("Invalid operation {}.  Ignoring.".format(op))
      return pos

    # calculate new position
    func,m = self.action[op]
    newpos = func(self,pos,m)
    if newpos[:2] in self.obstacles:
      print("Operaton: {op} unsuccessful (there's something in my way at {newpos}!).  Assuming position at {pos}".format(op=op,newpos=newpos,pos=pos))
      return pos

    # return new position
    print("Operation {op} successful.  Rover's current position is {pos}".format(op=op,pos=newpos))
    return newpos

  """
  Calculates rover's next cardial position
  Called when op = 'L' or 'R'.  pos = current position (x,y,c), m = -1 (left) or 1 (right)
  Performing mod 4 acts as a 'wrapper' as we iterate over the compass points.
  """
  def rotate(self,pos,m):
    x,y,c = pos
    cps = list(self.compass.keys())
    k = m + cps.index(c)
    c = cps[k%4]
    return (x,y,c)
 
  """
  Calculates rover's next co-ordinate
  Called when op = 'F' or 'B'.  pos = current position (x,y,c), m= -1 (backwards) or 1 (forwards)
  """
  def move(self,pos,m):
    x,y,c = pos
    """
    self.compass[c] will return a multiplier based on rover's cardial position
    'F' -> advance 1 step in c direction, 'B' -> advance -1 step in c direction
    if, say, we are facing 'W' and want to advance +1 step, we will want to multiply the 'm' multiplier by -1.
    """
    n = self.compass[c] 
    """
    performing 'mod' acts as a 'wrapper' as we iterate over the planet's coordinates, ensuring we don't 'fall over the edge'. :)
    """
    if c in 'EW':
      k = n*m + x
      x = k%self.xmax
    if c in 'NS':
      k = n*m + y
      y = k%self.ymax
    return (x,y,c)

  # establish valid operations and map each to an appropriate function and integer (represents direction of rotation/movement)
  action = {
    'L':(rotate,-1),
    'R':(rotate,1),
    'B':(move,-1),
    'F':(move,1)
  }

  # establish valid compass points and map each to an appropriate multiplier
  compass = {
    'N': 1,
    'E': 1,
    'S': -1,
    'W': -1
  }

def main():
  
  commands_path = os.path.join(os.environ['HOME'],'Rover/code/python/commands.txt')
  results_path = os.path.join(os.environ['HOME'],'Rover/code/python/results.txt')

  """
  Set-up planet co-ordinates based on user input and initialize rover.
  """
  
  print("Initialize planet co-ordinates")
  xmax = abs(int(input("Length in x-direction: ")))
  ymax = abs(int(input("Length in y-direction: ")))
  rover = Rover(xmax,ymax)

  """
  Initialize rover's starting position based on user's input e.g. (0,0,'E').
  Ensure the co-ordinates/cardial direction provided are valid before proceeding.
  """

  valid = False
  while not valid:
    print("Initialize rover's position")
    x = int(input("Enter x co-ordinate: "))
    y = int(input("Enter y co-ordinate: "))
    c = input("Enter cardinal direction (N, E, S, W): ")
    if rover.isvalid(x,y,c):
      valid = True
      pos = (x,y,c)
    else:
      print("Invalid co-ordinates {},{},{}.  Try again.".format(x,y,c)) 
 
  """
  Open handle to text file containing a list of commands ('L','R','F','B') to navigate the rover.
  Iterate over each character in text file.
  Provide the rover's current position 'pos' and next operation 'op' as read from file.
  rover.navigate() calculates rover's new position.
  """

  cmds = open(commands_path,'r')
  incomplete = True
 
  while incomplete:
    op = cmds.read(1)
    if not op:
      incomplete = False
      break
    pos = rover.navigate(pos,op)
    with open(results_path,'a') as f:
      f.write(str(pos))
      f.write('\n')

if __name__ == "__main__":
  main()  
