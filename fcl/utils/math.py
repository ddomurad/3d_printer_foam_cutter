def vec_mul(v, k):
    return v[0]*k, v[1]*k


def vec_sub(*vs):
    ov = [vs[0][0], vs[0][1]]
    for v in vs[1:]:
        ov[0] -= v[0]
        ov[1] -= v[1]

    return ov[0], ov[1]


def vec_add(*vs):
    ov = [0, 0]
    for v in vs:
        ov[0] += v[0]
        ov[1] += v[1]

    return ov[0], ov[1]


def vec_len(v):
    return (v[0]**2 + v[1]**2)**0.5


def vec_normalize(v):
    length = vec_len(v)
    return v[0]/length, v[1]/length


def vec_normal(v):
    return -v[1], v[0]


def vec_dot(v1, v2):
    return v1[0]*v2[0] + v1[1]*v2[1]


def vec_cmp(v1, v2, digits):
    return round(v1[0], digits) == round(v2[0], digits) and round(v1[1], digits) == round(v2[1], digits)
