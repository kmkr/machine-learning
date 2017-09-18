from helper import get_crossover_points

def partial_mapped_crossover(P1, P2):
    cross_a, cross_b = get_crossover_points(len(P1))
    print('Cross A: ' + str(cross_a) + ' Cross B : ' + str(cross_b))

    child_1 = child_from(P1, P2, cross_a, cross_b)
    child_2 = child_from(P2, P1, cross_a, cross_b)

    return child_1, child_2

def child_from(P1, P2, cross_a, cross_b):
    print('P1: ' + ', '.join(str(e) for e in P1))
    print('P2: ' + ', '.join(str(e) for e in P2))
    child = [None]*len(P1)

    child[cross_a:cross_b] = P1[cross_a:cross_b]

    print('Child etter step 1 (segment copy):')
    print(child)

    for x in range(cross_a, cross_b):
        p2_index = cross_a

        # Start index med segment-verdien
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

        print(child)

    print('Child etter step 2:')
    print(child)

    # Kopier resterende verdier fra P2:
    for i, item in enumerate(child):
        if item is None:
            child[i] = P2[i]

    print('Child etter step 3:')
    print(child)
    print('\n')
    return child


#seq_1 = [2,4,7,1,3,6,8,9,5]
#seq_2 = [5,9,8,6,2,4,1,3,7]

#partial_mapped_crossover(seq_1, seq_2)
