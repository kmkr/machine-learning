import helper

def partial_mapped_crossover(P1, P2):
    cross_a, cross_b = helper.get_crossover_points(len(P1))

    child_1 = child_from(P1, P2, cross_a, cross_b)
    child_2 = child_from(P2, P1, cross_a, cross_b)

    return child_1, child_2

def child_from(P1, P2, cross_a, cross_b):
    child = [None]*len(P1)

    child[cross_a:cross_b] = P1[cross_a:cross_b]

    for x in range(cross_a, cross_b):
        p2_index = cross_a

        index = x
        p2_segment_val = P2[index]
        while p2_index >= cross_a and p2_index < cross_b:
            p1_segment_val = P1[index]
            p2_index = P2.index(p1_segment_val)
            index = p2_index
            if p1_segment_val == p2_segment_val:
                break

        if not p2_segment_val in child:
            child[p2_index] = p2_segment_val

    for i, item in enumerate(child):
        if item is None:
            child[i] = P2[i]

    return child
