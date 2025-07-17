import sys

def remove_redundant_clauses(clauses):
    non_redundant_clauses = clauses.copy()
    for clause1 in clauses:
        clause1_set = set(clause1.split(' v '))
        for clause2 in clauses:
            clause2_set = set(clause2.split(' v '))
            if clause1_set != clause2_set and clause1_set.issubset(clause2_set) and clause2 in non_redundant_clauses:
                non_redundant_clauses.remove(clause2)
    return non_redundant_clauses


def remove_irrelevant_clauses(clause):
    clause = set(clause.split(' v '))
    for literal in clause:
        if not literal.startswith("~"):
            negated_literal = '~' + literal
        else:
            negated_literal = literal.replace("~", "")
        if negated_literal in clause:
            return 'Clause is valid'
    return 'Clause is not valid'


def get_clauses(path):
    with open(path, 'r', encoding='utf-8') as f:
        clauses = []
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                if remove_irrelevant_clauses(line.lower()) == 'Clause is not valid':
                    clauses.append(line.lower())
    return clauses


def get_clauses_with_identifier(path):
    with open(path, 'r', encoding='utf-8') as f:
        clauses_with_identifier = []
        for line in f:
            line = line.strip()
            if not line.startswith("#"):
                clauses_with_identifier.append(line.lower())
    return clauses_with_identifier

entry = sys.argv

if 'resolution' in entry:
    path_clause = entry[2]
    clauses = get_clauses(path_clause)

    Sos = []
    goal_clause = clauses[len(clauses) - 1]
    goal_clause_set = set(goal_clause.split(' v '))
    for cnk in goal_clause_set:
        if not cnk.startswith("~"):
            cnk = '~' + cnk
        else:
            cnk = cnk.replace("~", "")
        Sos.append(cnk)

    clauses.pop(len(clauses) - 1)
    factorized_clauses = clauses.copy()
    i = 0
    for clause in clauses:
        if len(clause.split(' v ')) > len(set(clause.split(' v '))):
            clause_set = set(clause.split(' v '))
            factorized_clauses.pop(i)
            factorized_clauses.insert(i, " v ".join(clause_set))
        i += 1
    clauses = factorized_clauses

    clauses = remove_redundant_clauses(clauses)

    all_clauses = clauses.copy()

    for new_goal_clause in Sos:
        all_clauses.append(new_goal_clause)

    parents = {}

    NIL = 'searching'
    while NIL == 'searching':
        new = set()
        for new_goal_clause in Sos:
            parent1 = new_goal_clause
            new_goal_clause = set(new_goal_clause.split(' v '))
            for clause in clauses:
                parent2 = clause
                clause = set(clause.split(' v '))
                resolvents = set()
                if len(new_goal_clause) > 1:
                    for cnk in new_goal_clause:
                        original_cnk = cnk
                        if not cnk.startswith("~"):
                            cnk = '~' + cnk
                        else:
                            cnk = cnk.replace("~", "")
                        if cnk in clause:
                            clause.remove(cnk)
                            copy_goal_clause = new_goal_clause.copy()
                            copy_goal_clause.remove(original_cnk)
                            clause.update(copy_goal_clause)
                            new_clause = " v ".join(sorted(clause))
                            parents[new_clause] = (parent1, parent2)
                            resolvents.add(new_clause)
                else:
                    for cnk in new_goal_clause:
                        if not cnk.startswith("~"):
                            cnk = '~' + cnk
                        else:
                            cnk = cnk.replace("~", "")
                        if cnk == clause:
                            clause.remove(cnk)
                            clause.add('')
                            new_clause = " v ".join(sorted(clause))
                            parents[new_clause] = (parent1, parent2)
                            resolvents.add(new_clause)
                        elif cnk in clause:
                            clause.remove(cnk)
                            new_clause = " v ".join(sorted(clause))
                            parents[new_clause] = (parent1, parent2)
                            resolvents.add(new_clause)

                if '' in resolvents:
                    NIL = 'found'
                    break
                new.update(resolvents)
            if NIL == 'found':
                break
        if NIL == 'found':
            break
        if new.issubset(set(clauses)):
            NIL = 'not_found'
            break
        for new_clause in new:
            if remove_irrelevant_clauses(new_clause) == 'Clause is not valid':
                clauses.append(new_clause)
                Sos.insert(0, new_clause)

        Sos = remove_redundant_clauses(Sos)
        clauses = remove_redundant_clauses(clauses)

    if NIL == 'found':
        used_clauses = ['']
        used_initial_clauses = set()
        for used_clause in used_clauses:
            if used_clause not in all_clauses:
                parent1, parent2 = parents[used_clause]
                used_initial_clauses.add(parent1)
                used_initial_clauses.add(parent2)
                if parent1 not in all_clauses:
                    used_clauses.append(parent1)
                if parent2 not in all_clauses:
                    used_clauses.append(parent2)

        used_clauses = used_clauses[::-1]

        unique_clauses = []
        for used_clause in used_clauses:
            if used_clause not in unique_clauses:
                unique_clauses.append(used_clause)

        clause_numbers = {}
        numbering = 1
        for clause in all_clauses:
            if clause in used_initial_clauses:
                print(f"{numbering}. {clause}")
                clause_numbers[clause] = numbering
                numbering += 1
        print('===============')
        for clause in unique_clauses:
            if clause == '':
                parent1, parent2 = parents[clause]
                print(f"{numbering}. NIL ({clause_numbers[parent2]}, {clause_numbers[parent1]})")
            else:
                parent1, parent2 = parents[clause]
                print(f"{numbering}. {clause} ({clause_numbers[parent2]}, {clause_numbers[parent1]})")
                clause_numbers[clause] = numbering
                numbering += 1
        print('===============')
        print(f"[CONCLUSION]: {goal_clause} is true")
    else:
        print(f"[CONCLUSION]: {goal_clause} is unknown")

elif 'cooking' in entry:
    path_clause = entry[2]
    clauses = get_clauses(path_clause)

    path_clause_identifier = entry[3]
    clauses_with_identifier = get_clauses_with_identifier(path_clause_identifier)

    factorized_clauses = clauses.copy()
    i = 0
    for clause in clauses:
        if len(clause.split(' v ')) > len(set(clause.split(' v '))):
            clause_set = set(clause.split(' v '))
            factorized_clauses.pop(i)
            factorized_clauses.insert(i, " v ".join(clause_set))
        i += 1
    clauses = factorized_clauses

    clauses = remove_redundant_clauses(clauses)

    for clause_identifier in clauses_with_identifier:
        if '+' in clause_identifier:
            print('User’s command:', clause_identifier)
            clause_identifier = clause_identifier.replace(" +", "")

            if len(clause_identifier.split(' v ')) > len(set(clause_identifier.split(' v '))):
                clause_identifier_set = set(clause_identifier.split(' v '))
                clause_identifier = " v ".join(clause_identifier_set)

            if remove_irrelevant_clauses(clause_identifier) == 'Clause is not valid' and clause_identifier not in clauses:
                clauses.append(clause_identifier)

            clauses = remove_redundant_clauses(clauses)
            print('Added', clause_identifier)
            print()
            
        elif '-' in clause_identifier:
            print('User’s command:', clause_identifier)
            clause_identifier = clause_identifier.replace(" -", "")

            if clause_identifier in clauses:
                clauses.remove(clause_identifier)

            clauses = remove_redundant_clauses(clauses)
            print('Removed', clause_identifier)
            print()
        else:
            print('User’s command:', clause_identifier)
            clause_identifier = clause_identifier.replace(" ?", "")
            goal_clause = clause_identifier
            goal_clause_set = set(clause_identifier.split(' v '))

            Sos = []
            for cnk in goal_clause_set:
                if not cnk.startswith("~"):
                    cnk = '~' + cnk
                else:
                    cnk = cnk.replace("~", "")
                Sos.append(cnk)

            all_clauses = clauses.copy()
            original_clauses = clauses.copy()

            for new_goal_clause in Sos:
                all_clauses.append(new_goal_clause)

            parents = {}

            NIL = 'searching'
            while NIL == 'searching':
                new = set()
                for new_goal_clause in Sos:
                    parent1 = new_goal_clause
                    new_goal_clause = set(new_goal_clause.split(' v '))
                    for clause in clauses:
                        parent2 = clause
                        clause = set(clause.split(' v '))
                        resolvents = set()
                        if len(new_goal_clause) > 1:
                            for cnk in new_goal_clause:
                                original_cnk = cnk
                                if not cnk.startswith("~"):
                                    cnk = '~' + cnk
                                else:
                                    cnk = cnk.replace("~", "")
                                if cnk in clause:
                                    clause.remove(cnk)
                                    copy_goal_clause = new_goal_clause.copy()
                                    copy_goal_clause.remove(original_cnk)
                                    clause.update(copy_goal_clause)
                                    new_clause = " v ".join(sorted(clause))
                                    parents[new_clause] = (parent1, parent2)
                                    resolvents.add(new_clause)
                        else:
                            for cnk in new_goal_clause:
                                if not cnk.startswith("~"):
                                    cnk = '~' + cnk
                                else:
                                    cnk = cnk.replace("~", "")
                                if cnk == clause:
                                    clause.remove(cnk)
                                    clause.add('')
                                    new_clause = " v ".join(sorted(clause))
                                    parents[new_clause] = (parent1, parent2)
                                    resolvents.add(new_clause)
                                elif cnk in clause:
                                    clause.remove(cnk)
                                    new_clause = " v ".join(sorted(clause))
                                    parents[new_clause] = (parent1, parent2)
                                    resolvents.add(new_clause)

                        if '' in resolvents:
                            NIL = 'found'
                            break
                        new.update(resolvents)
                    if NIL == 'found':
                        break
                if NIL == 'found':
                    break
                if new.issubset(set(clauses)):
                    NIL = 'not_found'
                    break
                for new_clause in new:
                    if remove_irrelevant_clauses(new_clause) == 'Clause is not valid':
                        clauses.append(new_clause)
                        Sos.insert(0, new_clause)

                Sos = remove_redundant_clauses(Sos)
                clauses = remove_redundant_clauses(clauses)

            if NIL == 'found':
                used_clauses = ['']
                used_initial_clauses = set()
                for used_clause in used_clauses:
                    if used_clause not in all_clauses:
                        parent1, parent2 = parents[used_clause]
                        used_initial_clauses.add(parent1)
                        used_initial_clauses.add(parent2)
                        if parent1 not in all_clauses:
                            used_clauses.append(parent1)
                        if parent2 not in all_clauses:
                            used_clauses.append(parent2)

                used_clauses = used_clauses[::-1]

                unique_clauses = []
                for used_clause in used_clauses:
                    if used_clause not in unique_clauses:
                        unique_clauses.append(used_clause)

                clause_numbers = {}
                numbering = 1
                for clause in all_clauses:
                    if clause in used_initial_clauses:
                        print(f"{numbering}. {clause}")
                        clause_numbers[clause] = numbering
                        numbering += 1
                print('===============')
                for clause in unique_clauses:
                    if clause == '':
                        parent1, parent2 = parents[clause]
                        print(f"{numbering}. NIL ({clause_numbers[parent2]}, {clause_numbers[parent1]})")
                    else:
                        parent1, parent2 = parents[clause]
                        print(f"{numbering}. {clause} ({clause_numbers[parent2]}, {clause_numbers[parent1]})")
                        clause_numbers[clause] = numbering
                        numbering += 1
                print('===============')
                print(f"[CONCLUSION]: {goal_clause} is true")
                print()
            else:
                print(f"[CONCLUSION]: {goal_clause} is unknown")
                print()

            clauses = original_clauses
else:
    print('Wrong entry')
