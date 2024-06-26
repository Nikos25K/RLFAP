# Radio Link Frequency Assignment Problem (RLFAP)
The Radio Link Frequency Assignment Problem is a Constraint Satisfaction Problem (CSP). <br>
Extensive description of the problem can be found [here](https://miat.inrae.fr/schiex/rlfap.shtml)

## Search Methods:
- **Backtracking with Forward Checking (FC)**
- **Backtracking with Maintaining Arc Consistency (MAC)**
- **Forward Checking with Conflict directed BackJumping hybrid (FC-CBJ)**
- **Min Conflicts**

## Heuristic used:
**dom/wdeg**
The dom/wdeg heuristic is a conflict-directed variable ordering heuristic. <br>
This heuristic aims to first explore the most "promising" branches of the search space. <br>
Given an assignment and a CSP instance, it computes and returns the variable with the smallest ratio of domain size to weighted degree.
The heuristic it is used in all of the above methods because of its efficiency. <br>
It takes some seconds only for searching, while without it, it would take a big amount of time for the search to be completed due to the difficulty of the instances.

## Experimental results:
In the following tables, we see wether the instatce was able to be solved with the constraints used (SAT) or not (UNSAT). <br>
The instances were given an amount of 6 minutes to be solved. If the time exceeded 6 minutes, then the instance was stopped executing.

### Method: Forward Checking (FC)
| Instance  | Result | Constraint Checks | Assignments | Time    |
|-----------|--------|-------------------|-------------|---------|
| 2-f24     | SAT    | 22384             | 254         | 0.11    |
| 2-f25     | UNSAT  | 37282795          | 198551      | 74.19   |
| 3-f10     | SAT    | 777626            | 4304        | 1.9     |
| 3-f11     | UNSAT  | 38962375          | 210370      | 85.1    |
| 6-w2      | UNSAT  | 46258             | 250         | 0.1     |
| 7-w1-f4   | SAT    | 106877            | 2308        | 0.48    |
| 7-w1-f5   | -      | -                 | -           | > 360   |
| 8-f10     | -      | -                 | -           | > 360   |
| 8-f11     | UNSAT  | 86488684          | 638778      | 359     |
| 11        | SAT    | 2829739           | 13855       | 17.6    |
| 14-f27    | SAT    | 5052782           | 99915       | 63      |
| 14-f28    | UNSAT  | 19178933          | 318864      | 137     |

### Method: Maintaining Arc Consistency (MAC with AC3)
| Instance  | Result | Constraint Checks | Assignments | Time    |
|-----------|--------|-------------------|-------------|---------|
| 2-f24     | SAT    | 165964            | 228         | 0.2     |
| 2-f25     | UNSAT  | 100095447         | 52330       | 202     |
| 3-f10     | SAT    | 1269090           | 852         | 2.4     |
| 3-f11     | UNSAT  | 25501996          | 8292        | 44.2    |
| 6-w2      | UNSAT  | 93186             | 44          | 0.15    |
| 7-w1-f4   | SAT    | 277559            | 442         | 0.4     |
| 7-w1-f5   | UNSAT  | 50379349          | 12847       | 49.6    |
| 8-f10     | SAT    | 30407876          | 14149       | 77.08   |
| 8-f11     | UNSAT  | 4608720           | 1979        | 11.3    |
| 11        | SAT    | 9261742           | 4560        | 27.2    |
| 14-f27    | SAT    | 4337430           | 12389       | 28.06   |
| 14-f28    | UNSAT  | 8185280           | 8874        | 35.8    |


### Method: FC-CBJ hybrid
| Instance  | Result | Constraint Checks | Assignments | Time    |
|-----------|--------|-------------------|-------------|---------|
| 2-f24     | SAT    | 19914             | 254         | 0.1     |
| 2-f25     | UNSAT  | 583322            | 3375        | 1.3     |
| 3-f10     | SAT    | 762665            | 4266        | 2       |
| 3-f11     | UNSAT  | 34414469          | 181868      | 86.7    |
| 6-w2      | UNSAT  | 46258             | 250         | 0.1     |
| 7-w1-f4   | SAT    | 88208             | 1565        | 0.48    |
| 7-w1-f5   | -      | -                 | -           | > 360   |
| 8-f10     | SAT    | 20042566          | 131430      | 71.2    |
| 8-f11     | UNSAT  | 1058127           | 7897        | 6.6     |
| 11        | SAT    | 2688859           | 13204       | 14.9    |
| 14-f27    | SAT    | 589281            | 11859       | 7.7     |
| 14-f28    | -      | -                 | -           | > 360   |

### Method: Min Conflicts with maximum steps = 10000
| Instance  | Result | Constraint Checks | Assignments | Time  | Constraints Violated |
|-----------|--------|-------------------|-------------|-------|----------------------|
| 2-f24     | UNSAT  | 29165690          | 10200       | 29.7  | 10                   |
| 2-f24     | UNSAT  | 30878474          | 10200       | 32.1  | 10                   |
| 2-f25     | UNSAT  | 29746975          | 10200       | 31.05 | 9                    |
| 2-f25     | UNSAT  | 29849722          | 10200       | 30.04 | 16                   |
| 3-f10     | UNSAT  | 60906232          | 10400       | 65.8  | 24                   |
| 3-f10     | UNSAT  | 60805943          | 10400       | 63.3  | 18                   |
| 3-f11     | UNSAT  | 61601678          | 10400       | 70.76 | 36                   |
| 3-f11     | UNSAT  | 61612504          | 10400       | 70.04 | 42                   |
| 6-w2      | UNSAT  | 16553561          | 10200       | 21.08 | 50                   |
| 6-w2      | UNSAT  | 16693293          | 10200       | 21.13 | 64                   |
| 7-w1-f4   | UNSAT  | 15076619          | 10400       | 23.67 | 65                   |
| 7-w1-f4   | UNSAT  | 15080342          | 10400       | 23.48 | 67                   |
| 7-w1-f5   | UNSAT  | 14653684          | 10400       | 21.24 | 42                   |
| 7-w1-f5   | UNSAT  | 14642987          | 10400       | 21.02 | 47                   |
| 8-f10     | UNSAT  | 80012919          | 10680       | 91.2  | 67                   |
| 8-f10     | UNSAT  | 80013024          | 10680       | 91.3  | 69                   |
| 8-f11     | UNSAT  | 79907908          | 10680       | 95.83 | 84                   |
| 8-f11     | UNSAT  | 79910004          | 10680       | 95.87 | 83                   |
| 11        | UNSAT  | 94281780          | 10680       | 111.9 | 4                    |
| 11        | UNSAT  | 94240498          | 10680       | 109.9 | 7                    |
| 14-f27    | UNSAT  | 94761382          | 10916       | 119.7 | 104                  |
| 14-f27    | UNSAT  | 94768427          | 10916       | 124.7 | 119                  |
| 14-f28    | UNSAT  | 94640989          | 10916       | 116.04| 190                  |
| 14-f28    | UNSAT  | 94641274          | 10916       | 117.2 | 182                  |

### References:
The search.py, csp.py and utils.py are used from [https://github.com/aimacode/aima-python](https://github.com/aimacode/aima-python) <br>
F. Boussemart, F. Hemery, C. Lecoutre and L. Sais. Boosting Systematic Search by
Weighting Constraints. Proc. of ECAI 2004, pages 146–150, 2004 [https://frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0146.pdf](https://frontiersinai.com/ecai/ecai2004/ecai04/pdf/p0146.pdf)
