def get_idxes(P1, P2, start):
    idxes = []
    cur = start
    done = False
    while not done:
        idxes.append(cur)
        p2_val = P2[cur]
        cur = P1.index(p2_val)
        if cur == start:
            done = True

    return idxes

def cycle_crossover(P1, P2):
    child_1 = [None] * len(P1)
    child_2 = [None] * len(P2)

    opposite = False
    while None in child_1:
        idx_first_none = child_1.index(None)
        idxes = get_idxes(P1, P2, idx_first_none)
        first = child_2 if opposite else child_1
        second = child_1 if opposite else child_2
        for item in idxes:
            first[item] = P1[item]
            second[item] = P2[item]

        opposite = not opposite

    return child_1, child_2
