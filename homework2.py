class State:
    def __init__(self, towers):
        self.towers = towers

    def __eq__(self, other):
        return self.towers == other.towers


class Problem:
    def __init__(self, start_state, goal_state):
        self.start_state = start_state
        self.goal_state = goal_state

    def goal_test(self, state):
        return state == self.goal_state

    def successor(self, state):
        pass


class TowerOfHanoi(Problem):
    def __init__(self, disks):
        start_state = State([list(range(disks, 0, -1)), [], []])
        goal_state = State([[], [], list(range(disks, 0, -1))])
        self.start_state = start_state
        self.goal_state = goal_state
        self.disks = disks

    def successor(self, state):
        states = []
        for i in range(3):
            if not state.towers[i]:
                continue
            disk = state.towers[i][-1]
            for j in range(3):
                if i != j:
                    if not state.towers[j] or state.towers[j][-1] > disk:
                        new_towers = [tower[:] for tower in state.towers]
                        new_towers[j].append(new_towers[i].pop())
                        states.append(State(new_towers))
        return states
