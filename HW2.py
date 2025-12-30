from abc import ABC, abstractmethod
from typing import List, Tuple, Any

# 1. Abstract State class
class State(ABC):
    @abstractmethod
    def __eq__(self, other):
        pass
    
    @abstractmethod
    def __hash__(self):
        pass
    
    @abstractmethod
    def __str__(self):
        pass

# 2. Abstract Problem class
class Problem(ABC):
    def __init__(self, initial_state: State, goal_state: State = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    @abstractmethod
    def goal_test(self, state: State) -> bool:
        """Return True if state is a goal state"""
        pass
    
    @abstractmethod
    def successor(self, state: State) -> List[Tuple[Any, State]]:
        """
        Return a list of (action, new_state) pairs reachable from the current state
        """
        pass
    
    @abstractmethod
    def result(self, state: State, action: Any) -> State:
        """Return the new state after applying action to the given state"""
        pass

# 3. Tower of Hanoi State class
class HanoiState(State):
    def __init__(self, pegs: List[List[int]]):
        self.pegs = pegs  # Each peg is a list of disks, largest disk = largest number
    
    def __eq__(self, other):
        return self.pegs == other.pegs
    
    def __hash__(self):
        return hash(tuple(tuple(peg) for peg in self.pegs))
    
    def __str__(self):
        return str(self.pegs)

# 4. Tower of Hanoi Problem class
class TowerOfHanoi(Problem):
    def __init__(self, num_disks: int):
        initial_pegs = [list(range(num_disks, 0, -1)), [], []]  # All disks on peg 0
        goal_pegs = [[], [], list(range(num_disks, 0, -1))]     # All disks on peg 2
        super().__init__(HanoiState(initial_pegs), HanoiState(goal_pegs))
        self.num_disks = num_disks
    
    def goal_test(self, state: HanoiState) -> bool:
        return state.pegs == self.goal_state.pegs
    
    def successor(self, state: HanoiState) -> List[Tuple[str, HanoiState]]:
        successors = []
        for i, peg_from in enumerate(state.pegs):
            if not peg_from:
                continue
            disk = peg_from[-1]
            for j, peg_to in enumerate(state.pegs):
                if i == j:
                    continue
                if not peg_to or peg_to[-1] > disk:
                    # Legal move
                    new_pegs = [peg.copy() for peg in state.pegs]
                    new_pegs[j].append(new_pegs[i].pop())
                    action = f"Move disk {disk} from peg {i} to peg {j}"
                    successors.append((action, HanoiState(new_pegs)))
        return successors
    
    def result(self, state: HanoiState, action: str) -> HanoiState:
        # Apply action in format: "Move disk X from peg A to peg B"
        parts = action.split()
        disk = int(parts[2])
        from_peg = int(parts[5])
        to_peg = int(parts[8])
        new_pegs = [peg.copy() for peg in state.pegs]
        new_pegs[to_peg].append(new_pegs[from_peg].pop())
        return HanoiState(new_pegs)

# Example usage:
if __name__ == "__main__":
    problem = TowerOfHanoi(3)
    print("Initial state:", problem.initial_state)
    print("Goal state:", problem.goal_state)
    
    successors = problem.successor(problem.initial_state)
    for action, state in successors:
        print(action, state)
