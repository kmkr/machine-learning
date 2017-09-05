import helper

def order_crossover(P1, P2):
    cross_a, cross_b = helper.get_crossover_points(len(P1))
    print 'Cross A: ' + str(cross_a) + ' Cross B : ' + str(cross_b)

    child_1 = child_from(P1, P2, cross_a, cross_b)
    child_2 = child_from(P2, P1, cross_a, cross_b)

    return child_1, child_2

def _get_none_idxes(list, threshold_idx):
    return [i for i,x in enumerate(list) if x is None and i >= threshold_idx]

def _get_none_idx(list, start_from_idx):
    a = _get_none_idxes(list, start_from_idx)
    if a:
        return a[0]

    return _get_none_idxes(list, 0)[0]

def child_from(P1, P2, cross_a, cross_b):
    child = [None] * len(P1)

    child[cross_a:cross_b] = P1[cross_a:cross_b]

    print 'Child etter segment copy'
    print child

    for idx in range(cross_b, len(P2)):
        if not P2[idx] in child:
            none_idx = _get_none_idx(child, cross_b)
            child[none_idx] = P2[idx]

    for idx in range(0, cross_b):
        if not P2[idx] in child:
            none_idx = _get_none_idx(child, cross_b)
            child[none_idx] = P2[idx]

    print 'Child etter order copy fra P2'
    print child
    return child
