import random
import time
from math  import inf
from csp import CSP, dom_j_up, num_legal_values, backtracking_search, unordered_domain_values
from csp import lcv, min_conflicts_value

vars = []      #list of variables
doms = {}        #map of domain -> tuple of possible values
constrs = {}    #map of val,val -> relation, k

weights = {}        #for dom_wdeg_heuristic
neighbs = {}

confl_set = {}
count = 0       #constraints checked

def constraint(A, a, B, b):
    """Check whether A=a, B=b satisfies the constraint between vars A and B."""
    global count
    count += 1
    relation, k = constrs[(A,B)]           #checks relation and if is not ok
    if relation == ">" and abs(a-b) > k:
        return True
    elif relation == "=" and abs(a-b) == k:
        return True

    return False    #constraint not satisfied or something went wrong

def min_conflicts(my_rlfap, max_steps=10000):
    """Solve a my_rlfap by stochastic Hill Climbing on the number of conflicts."""
    """Returns a tuple (solution, number of conflicts-constraint violations)"""
    """If not solved returns None, length of contraint-violating vars"""
    # Generate a complete assignment for all variables (probably with conflicts)
    my_rlfap.current = current = {}
    for var in my_rlfap.variables:
        val = min_conflicts_value(my_rlfap, var, current)
        my_rlfap.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = my_rlfap.conflicted_vars(current)
        if not conflicted:
            return current, 0
        var = random.choice(conflicted)
        val = min_conflicts_value(my_rlfap, var, current)
        my_rlfap.assign(var, val, current)

    return None, len(conflicted)    #UNSAT and number of contraint-violating vars

def revise(my_rlfap, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in my_rlfap.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        # if all(not my_rlfap.constraints(Xi, x, Xj, y) for y in my_rlfap.curr_domains[Xj]):
        conflict = True
        for y in my_rlfap.curr_domains[Xj]:
            if my_rlfap.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            my_rlfap.prune(Xi, x, removals)
            revised = True
    if not my_rlfap.curr_domains[Xi]: # if dom(X) emptied
        weights[(Xi, Xj)] += 1
        weights[(Xj, Xi)] += 1
    return revised, checks

def ac3(my_rlfap, queue=None, removals=None, arc_heuristic=dom_j_up):
    """Propagate constraints by enforcing Arc Consistency for the current state."""
    if queue is None:
        queue = { (Xi, Xk) for Xi in my_rlfap.variables for Xk in my_rlfap.neighbors[Xi] }
    my_rlfap.support_pruning()
    queue = arc_heuristic(my_rlfap, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(my_rlfap, Xi, Xj, removals, checks)
        if revised:
            if not my_rlfap.curr_domains[Xi]:
                return False, checks  # my_rlfap is inconsistent
            for Xk in my_rlfap.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # my_rlfap is satisfiable


def mac(my_rlfap, var, value, assignment, removals, propagate=ac3):
    """Maintain arc consistency."""
    return propagate(my_rlfap, { (X, var) for X in my_rlfap.neighbors[var] }, removals)

def forward_checking(my_rlfap, var, value, assignment, removals, running_cbj=False, new_confls=[]):
    """Prune neighbor values inconsistent with var=value."""
    my_rlfap.support_pruning()

    for B in my_rlfap.neighbors[var]:
        if B in assignment:
            continue
        for b in my_rlfap.curr_domains[B][:]:
            if not my_rlfap.constraints(var, value, B, b):
                my_rlfap.prune(B, b, removals)

                if running_cbj:
                    new_confls.append(B) # Remember prunes caused by var
                    confl_set[B].add(var) # var caused a prune in B's domain

        if not my_rlfap.curr_domains[B]:
            confl_set[B].add(var)    # domain wipe out for B, because of some value of var
            weights[(var, B)] += 1
            weights[(B, var)] += 1
            return False
    return True



"""Conflict-directed backjumping with forward checking."""
def fc_cbj(my_rlfap, select_var, select_val, inference):

    def backjump(assignment, my_rlfap):
        if len(assignment) == len(my_rlfap.variables):
            return assignment, None
        
        var = select_var(assignment, my_rlfap)
        for value in select_val(var, assignment, my_rlfap):
            new_confls = []
            if my_rlfap.nconflicts(var,value,assignment) == 0:
                my_rlfap.assign(var, value,assignment)
                removals = my_rlfap.suppose(var, value)

                if inference(my_rlfap, var, value, assignment, removals, True, new_confls):
                    result, confls = backjump(assignment, my_rlfap)
                    if result is not None:      #if a solution to my_rlfap is found
                        return result, None
            
                    if var not in confls:
                        my_rlfap.restore(removals)         # restore any changes caused by assignment var
                        my_rlfap.unassign(var, assignment) # unassign var value from assignment
                        for v in new_confls:
                            confl_set[v] -= set([var])
                        return None, confls    # Haven't jumped to the target var yet
                    else:
                        confl_set[var] = confl_set[var].union(confls).copy()  #update jump_var's conflict set
            my_rlfap.restore(removals)
            my_rlfap.unassign(var, assignment)
            for v in new_confls:
                confl_set[v] -= set([var])

        return None, set(confl_set[var] - set([var])) # Current var failed, jump back

    return backjump({}, my_rlfap)



def dom_wdeg_heuristic(assignment, my_rlfap):
    min_ratio = inf
    bestVar = 0

    for var in my_rlfap.variables:
        sum = 1
        if var in assignment:
            continue    
        
        for var2 in neighbs[var]:
            sum += weights[(var, var2)]

        #calculates the (domain size / weighted degree) ratio for var
        ratio = num_legal_values(my_rlfap, var, assignment) /sum       #sum != 0
        if min_ratio > ratio:
            bestVar = var
            min_ratio = ratio
    
    return bestVar

def read_lines(path, name):
        
    temp_vars = []
    with open(path + 'var' + name + '.txt', 'r') as file:
        num_vars = int(file.readline().strip()) # read first line
        for line in file: # read rest of lines
           temp_vars.append([int(x) for x in line.split()])

    temp_doms = []
    with open(path + 'dom' + name + '.txt', 'r') as file:
        # Read the first line to get the number of domains
        num_domains = int(file.readline().strip())

        for line in file: # read rest of lines
            temp_doms.append([int(x) for x in line.split()[2:]])
    
    for var in temp_vars:
        vars.append(var[0])
        doms[var[0]] = temp_doms[var[1]]
        neighbs[var[0]] = []     #initialize


    with open(path + 'ctr' + name + '.txt', 'r') as file:
        # Read the first line to get the number of constraints
        num_constraints = int(file.readline().strip())

        # Read each constraint
        for _ in range(num_constraints):
            constraint_line = file.readline().strip().split()
            variable_1 = int(constraint_line[0])
            variable_2 = int(constraint_line[1])
            relation = constraint_line[2]
            k = int(constraint_line[3])
            constrs[(variable_1, variable_2)] = (relation, k)       # eg constraints[0,1] = (>, 34)
            constrs[(variable_2, variable_1)] = (relation, k)
            weights[(variable_2, variable_1)] = 1
            weights[(variable_1, variable_2)] = 1
            neighbs[variable_1].append(variable_2)
            neighbs[variable_2].append(variable_1)


def main():
    instances = ["2-f24","2-f25","3-f10","3-f11","6-w2","7-w1-f4",
               "7-w1-f5","8-f10","8-f11","11","14-f27","14-f28"]

    print("Instances:")
    for i, ins in enumerate(instances):
        print(ins, end="\n" if i == len(instances) - 1 else ", ")
    inst = input("Give the name of the instance: ")
    if inst not in instances:
        exit("Invalid instance: ")

    read_lines("rlfap/",inst)
    my_rlfap = CSP(vars,doms,neighbs,constraint)
    for var in my_rlfap.variables:
        confl_set[var] = set()      #initializes each conflict set


    method = input("Give the algorithm(FC/MAC/FC-CBJ/Min-Conflicts): ")

    start = time.time()
    if method == "FC":
        sol = backtracking_search(my_rlfap, select_unassigned_variable=dom_wdeg_heuristic, 
                                    order_domain_values=unordered_domain_values, inference=forward_checking)
                                    #   order_domain_values=my_rlfap.lcv, inference=forward_checking)
    elif method == "MAC":
        sol = backtracking_search(my_rlfap, select_unassigned_variable=dom_wdeg_heuristic, 
                                        order_domain_values=unordered_domain_values, inference=mac)
                                    # order_domain_values=my_rlfap.lcv, inference=mac)
    elif method == "FC-CBJ":
        sol = fc_cbj(my_rlfap, select_var=dom_wdeg_heuristic, 
                        select_val=unordered_domain_values, inference=forward_checking)
                    # select_val=lcv, inference=forward_checking)
    elif method == "Min-Conflicts":
        sol = min_conflicts(my_rlfap)
    else:
        exit("Invalid algorithm")

    end = time.time()

    print("\n")
    if method == "FC" or method == "MAC":
        if(sol == False or sol == None):
            print("UNSAT")
        else:
            print(sol)
    else:
        if(sol[0] == None):
            print("UNSAT")
            if(method == "Min-Conflicts"):
                print(f"Constraints violated: {sol[1]} ")
        else:
            print(sol)

    print("\n")
    print(f"Assignments: {my_rlfap.nassigns}")
    print(f"Constraint checks: {count}")
    print(f"Time: {end - start:.3f} seconds")


if __name__ == "__main__":
    main()