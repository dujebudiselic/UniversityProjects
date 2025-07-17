import heapq
import sys

def get_state_space_description(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = []
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                data.append(line)

    initial_state = data[0]
    goal_states = data[1].split()
    transitions = {}

    for i in range(2, len(data)):
        transition = data[i].split(":")
        state = transition[0]
        transitions[state] = {}
        next_states = transition[1].split()
        next_states.sort()
        for next_state in next_states:
            next_state_name, cost = next_state.split(',')
            transitions[state][next_state_name] = float(cost)

    return initial_state, goal_states, transitions

def get_heuristic_description(path_h):
    heuristic = {}

    with open(path_h, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                state, heuristic_value = line.split(":")
                heuristic[state] = float(heuristic_value)

    return heuristic

def print_solution(found_solution, visited, parents, goal, total_cost):
    if found_solution:
        path_nodes = [goal]
        node = goal
        while True:
            node, cost = parents[node]
            if node is None:
                break
            path_nodes.append(node)
        path = " => ".join(path_nodes[::-1])
        print('[FOUND_SOLUTION]: yes')
        print('[STATES_VISITED]:', len(visited))
        print('[PATH_LENGTH]:', len(path_nodes))
        print('[TOTAL_COST]:', total_cost)
        print('[PATH]:', path)
    else:
        print('[FOUND_SOLUTION]: no')

entry = sys.argv

if '--alg' in entry:
    index_alg = entry.index('--alg')
    algorithm = entry[index_alg + 1]
    if algorithm == 'bfs':
        index_ss = entry.index('--ss')
        path_state_space_description = entry[index_ss + 1]
        initial_state, goal_states, transitions = get_state_space_description(path_state_space_description)

        open_bfs = [(initial_state, 0.0, None)]
        visited = set()
        parents = {initial_state: (None, 0.0)}
        found_solution = False
        total_cost = 0.0
        goal = ''
        
        while open_bfs:
            current_state, current_cost, parent = open_bfs.pop(0)
            
            if current_state in parents:
                prev_parent, prev_cost = parents[current_state]
                if prev_cost > current_cost:
                    parents[current_state] = (parent, current_cost)
            else:
                parents[current_state] = (parent, current_cost)

            if current_state in goal_states:
                goal = current_state
                total_cost = current_cost
                found_solution = True
                break

            visited.add(current_state)

            for neighbor, cost in transitions[current_state].items():
                if neighbor not in visited:
                    open_bfs.append((neighbor, current_cost + cost, current_state))

        print('# BFS')
        print_solution(found_solution, visited, parents, goal, total_cost)

    elif algorithm == 'ucs':
        index_ss = entry.index('--ss')
        path_state_space_description = entry[index_ss + 1]
        initial_state, goal_states, transitions = get_state_space_description(path_state_space_description)

        open_ucs = []
        visited = set()
        parents = {initial_state: (None, 0.0)}
        heapq.heappush(open_ucs, (0.0, initial_state, None))
        found_solution = False
        total_cost = 0.0
        goal = ''

        while open_ucs:
            current_cost, current_state, parent = heapq.heappop(open_ucs)

            if current_state in parents:
                prev_parent, prev_cost = parents[current_state]
                if prev_cost > current_cost:
                    parents[current_state] = (parent, current_cost)
            else:
                parents[current_state] = (parent, current_cost)

            if current_state in goal_states:
                goal = current_state
                total_cost = current_cost
                found_solution = True
                break

            visited.add(current_state)

            for neighbor, cost in transitions[current_state].items():
                if neighbor not in visited:
                    heapq.heappush(open_ucs, (current_cost + cost, neighbor, current_state))

        print('# UCS')
        print_solution(found_solution, visited, parents, goal, total_cost)
    
    elif algorithm == 'astar':
        index_ss = entry.index('--ss')
        path_state_space_description = entry[index_ss + 1]
        initial_state, goal_states, transitions = get_state_space_description(path_state_space_description)

        index_h = entry.index('--h')
        path_heuristic_description = entry[index_h + 1]
        heuristics = get_heuristic_description(path_heuristic_description)

        open_astar = []
        heapq.heappush(open_astar, (0.0, initial_state, 0.0, None))
        closed = {}
        parents = {initial_state: (None, 0.0)}
        found_solution = False
        total_cost = 0.0
        goal = ''

        while open_astar:
            estimated_total_cost, current_state, current_cost, parent = heapq.heappop(open_astar)

            if current_state in parents:
                prev_parent, prev_cost = parents[current_state]
                if prev_cost > current_cost:
                    parents[current_state] = (parent, current_cost)
            else:
                parents[current_state] = (parent, current_cost)

            if current_state in goal_states:
                goal = current_state
                total_cost = current_cost
                found_solution = True
                break

            closed[current_state] = current_cost

            for neighbor, cost in transitions[current_state].items():
                if neighbor in closed:
                    if closed[neighbor] < current_cost + cost:
                        continue
                    else:
                        del closed[neighbor]
                i = 0
                for element in open_astar:
                    if neighbor == element[1]:
                        heuristic, _state, existing_cost, parent = open_astar[i]
                        if existing_cost < current_cost + cost:
                            continue
                        else:
                            del open_astar[i]
                    i += 1
                heapq.heappush(open_astar, (current_cost + cost + heuristics[neighbor], neighbor, current_cost + cost, current_state))

        print('# A-STAR', path_heuristic_description)
        print_solution(found_solution, closed, parents, goal, total_cost)
    else:
        print('Invalid entry')



elif '--check-optimistic' in entry:
    index_ss = entry.index('--ss')
    path_state_space_description = entry[index_ss + 1]
    initial_state, goal_states, transitions = get_state_space_description(path_state_space_description)

    index_h = entry.index('--h')
    path_heuristic_description = entry[index_h + 1]
    heuristics = get_heuristic_description(path_heuristic_description)

    error_count = 0
    print('# HEURISTIC-OPTIMISTIC', path_heuristic_description)
    for state in heuristics:
        open_HO = []
        visited = set()
        heapq.heappush(open_HO, (0.0, state, None))
        total_cost = 0.0

        while open_HO:
            current_cost, current_state, parent = heapq.heappop(open_HO)
            if current_state in goal_states:
                total_cost = current_cost
                break
            visited.add(current_state)
            for neighbor, cost in transitions[current_state].items():
                if neighbor not in visited:
                    heapq.heappush(open_HO, (current_cost + cost, neighbor, current_state))

        if heuristics[state] <= total_cost:
            print(f"[CONDITION]: [OK] h({state}) <= h*: {heuristics[state]} <= {total_cost}")
        else:
            print(f"[CONDITION]: [ERR] h({state}) <= h*: {heuristics[state]} <= {total_cost}")
            error_count += 1

    if error_count == 0:
        print('[CONCLUSION]: Heuristic is optimistic.')
    else:
        print('[CONCLUSION]: Heuristic is not optimistic.')


elif '--check-consistent' in entry:
    index_ss = entry.index('--ss')
    path_state_space_description = entry[index_ss + 1]
    initial_state, goal_states, transitions = get_state_space_description(path_state_space_description)

    index_h = entry.index('--h')
    path_heuristic_description = entry[index_h + 1]
    heuristics = get_heuristic_description(path_heuristic_description)

    error_count = 0
    print('# HEURISTIC-CONSISTENT', path_heuristic_description)
    for state in heuristics:
        for next_state in transitions[state]:
            if heuristics[state] <= heuristics[next_state] + transitions[state][next_state]:
                print(f"[CONDITION]: [OK] h({state}) <= h({next_state}) + c: {heuristics[state]} <= {heuristics[next_state]} + {transitions[state][next_state]}")
            else:
                print(f"[CONDITION]: [ERR] h({state}) <= h({next_state}) + c: {heuristics[state]} <= {heuristics[next_state]} + {transitions[state][next_state]}")
                error_count += 1

    if error_count == 0:
        print('[CONCLUSION]: Heuristic is consistent.')
    else:
        print('[CONCLUSION]: Heuristic is not consistent.')
else:
    print('Invalid entry')
