# Radio Link Frequency Assignment Problem (RLFAP)
The Radio Link Frequency Assignment Problem is a Constraint Satisfaction Problem (CSP)
Extensive description of the problem can be found 

## Search Methods:
Backtracking with Forward Checking (FC)
Backtracking with Maintaining Arc Consistency (MAC)
Forward Checking with Conflict directed BackJumping hybrid (FC-CBJ)
Min Conflicts

## Heuristic used:
The dom/wdeg heuristic It's a conflict-directed variable ordering heuristic. The heuristic it is used in all of the above methods because of its efficiency. It takes some seconds only for searching, while without it, it would take a big amount of time for the search to be completed due to the difficulty of the instances.

## Experimental results:

### Method: Forward Checking (FC)
