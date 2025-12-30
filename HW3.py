from abc import ABC, abstractmethod
from typing import List, Tuple, Any, Optional
import heapq
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

class Problem(ABC):
    def __init__(self, initial_state: State, goal_state: State = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
    
    @abstractmethod
    def goal_test(self, state: State) -> bool:
        pass
    
    @abstractmethod
    def successor(self, state: State) -> List[Tuple[Any, State]]:
        pass
    
    @abstractmethod
    def result(self, state: State, action: Any) -> State:
        pass
    
    def step_cost(self, state: State, action: Any, next_state: State) -> float:
        return 1  
    
    def heuristic(self, state: State) -> float:
        return 0  


class HanoiState(State):
    def __init__(self, pegs: Tuple[Tuple[int]]):
        self.pegs = pegs
    
    def __eq__(self, other):
        return self.pegs == other.pegs
    
    def __hash__(self):
        return hash(self.pegs)
    
    def __str__(self):
        return str(self.pegs)

class TowerOfHanoi(Problem):
    def __init__(self, num_disks: int):
        initial_pegs = (tuple(range(num_disks, 0, -1)), (), ())
        goal_pegs = ((), (), tuple(range(num_disks, 0, -1)))
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
                    new_pegs = [list(peg) for peg in state.pegs]
                    new_pegs[j].append(new_pegs[i].pop())
                    new_pegs_tuple = tuple(tuple(peg) for peg in new_pegs)
                    action = f"Move disk {disk} from peg {i} to peg {j}"
                    successors.append((action, HanoiState(new_pegs_tuple)))
        return successors
    
    def result(self, state: HanoiState, action: str) -> HanoiState:
        parts = action.split()
        disk = int(parts[2])
        from_peg = int(parts[5])
        to_peg = int(parts[8])
        new_pegs = [list(peg) for peg in state.pegs]
        new_pegs[to_peg].append(new_pegs[from_peg].pop())
        new_pegs_tuple = tuple(tuple(peg) for peg in new_pegs)
        return HanoiState(new_pegs_tuple)
    
    
    def heuristic(self, state: HanoiState) -> int:
        return self.num_disks - len(state.pegs[2])

class Node:
    def __init__(self, state: State, parent: Optional['Node']=None, action: Any=None, path_cost: float=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
    
    def solution(self) -> List[Any]:
        node, actions = self, []
        while node.parent is not None:
            actions.append(node.action)
            node = node.parent
        actions.reverse()
        return actions
    
    def __lt__(self, other):
        return self.path_cost < other.path_cost

def DFS(problem: Problem):
    frontier = [Node(problem.initial_state)]
    explored = set()
    while frontier:
        node = frontier.pop()
        if problem.goal_test(node.state):
            return node.solution()
        explored.add(node.state)
        for action, child_state in problem.successor(node.state):
            if child_state not in explored and all(n.state != child_state for n in frontier):
                frontier.append(Node(child_state, node, action))
    return None

def BFS(problem: Problem):
    from collections import deque
    frontier = deque([Node(problem.initial_state)])
    explored = set()
    while frontier:
        node = frontier.popleft()
        if problem.goal_test(node.state):
            return node.solution()
        explored.add(node.state)
        for action, child_state in problem.successor(node.state):
            if child_state not in explored and all(n.state != child_state for n in frontier):
                frontier.append(Node(child_state, node, action))
    return None

def IDS(problem: Problem, max_depth=50):
    def DLS(node: Node, depth: int):
        if problem.goal_test(node.state):
            return node.solution()
        if depth == 0:
            return None
        for action, child_state in problem.successor(node.state):
            child_node = Node(child_state, node, action)
            result = DLS(child_node, depth-1)
            if result is not None:
                return result
        return None
    
    for depth in range(max_depth):
        result = DLS(Node(problem.initial_state), depth)
        if result is not None:
            return result
    return None

def UCS(problem: Problem):
    frontier = []
    heapq.heappush(frontier, (0, Node(problem.initial_state)))
    explored = {}
    while frontier:
        cost, node = heapq.heappop(frontier)
        if problem.goal_test(node.state):
            return node.solution()
        if node.state in explored and explored[node.state] <= cost:
            continue
        explored[node.state] = cost
        for action, child_state in problem.successor(node.state):
            new_cost = node.path_cost + problem.step_cost(node.state, action, child_state)
            heapq.heappush(frontier, (new_cost, Node(child_state, node, action, new_cost)))
    return None

def greedy_best_first(problem: Problem):
    frontier = []
    start_node = Node(problem.initial_state)
    heapq.heappush(frontier, (problem.heuristic(start_node.state), start_node))
    explored = set()
    while frontier:
        _, node = heapq.heappop(frontier)
        if problem.goal_test(node.state):
            return node.solution()
        explored.add(node.state)
        for action, child_state in problem.successor(node.state):
            if child_state not in explored:
                heapq.heappush(frontier, (problem.heuristic(child_state), Node(child_state, node, action)))
    return None

def astar(problem: Problem):
    frontier = []
    start_node = Node(problem.initial_state)
    heapq.heappush(frontier, (start_node.path_cost + problem.heuristic(start_node.state), start_node))
    explored = {}
    while frontier:
        f, node = heapq.heappop(frontier)
        if problem.goal_test(node.state):
            return node.solution()
        if node.state in explored and explored[node.state] <= node.path_cost:
            continue
        explored[node.state] = node.path_cost
        for action, child_state in problem.successor(node.state):
            g = node.path_cost + problem.step_cost(node.state, action, child_state)
            h = problem.heuristic(child_state)
            heapq.heappush(frontier, (g+h, Node(child_state, node, action, g)))
    return None


if __name__ == "__main__":
    problem = TowerOfHanoi(3) 

    print("DFS solution:", DFS(problem))
    print("BFS solution:", BFS(problem))
    print("IDS solution:", IDS(problem))
    print("UCS solution:", UCS(problem))
    print("Greedy solution:", greedy_best_first(problem))
    print("A* solution:", astar(problem))
