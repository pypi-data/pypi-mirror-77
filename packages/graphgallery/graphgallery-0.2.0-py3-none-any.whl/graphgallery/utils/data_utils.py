import numpy as np
import scipy.sparse as sp
import tensorflow as tf

from numbers import Number
from sklearn.preprocessing import normalize, StandardScaler, RobustScaler

from graphgallery.utils.shape import repeat
from graphgallery.utils.type_check import is_list_like
from graphgallery import config

__all__ = ['sample_mask', 'normalize_adj', 'normalize_x', 'Bunch']


def sample_mask(indices, shape):
    mask = np.zeros(shape, np.bool)
    mask[indices] = True
    return mask


def normalize_x(x, norm='l1'):
    """Normalize the attribute matrix with given type.

    Parameters
    ----------
    x: Numpy array-like matrix
    norm: The specified type for the normalization.
        `l1`: l1-norm for axis 1, from `sklearn.preprocessing`.
        `l1_0`: l1-norm for axis 0, from `sklearn.preprocessing`.
        `scale`: standard scale for axis 0, `sklearn.preprocessing.scale`
        `robust_scale`, robust scale for axis 0, `sklearn.preprocessing.robust_scale`
        otherwise: not normalize, return the copy of `x`

    Returns
    ----------
        A normalized attribute matrix.
    """
    if norm not in {'l1', 'l1_0', 'scale', 'robust_scale', None}:
        raise ValueError(f'{norm} is not a supported norm.')

    if norm == 'l1':
        x_norm = normalize(x, norm='l1', axis=1)
    elif norm == 'l1_0':
        x_norm = normalize(x, norm='l1', axis=0)
    elif norm == 'scale':
        # something goes wrong with type float32
        x_norm = StandardScaler().fit(x).transform(x)
    elif norm == 'robust_scale':
        x_norm = RobustScaler().fit(x).transform(x)
    else:
        x_norm = x.copy()
    return x_norm


def normalize_adj(adj_matrics, rate=-0.5, self_loop=1.0):
    """Normalize adjacency matrix.

    >>> normalize_adj(adj, rate=-0.5) # return a normalized adjacency matrix

    # return a list of normalized adjacency matrices
    >>> normalize_adj([adj, adj], rate=[-0.5, 1.0]) 

    Parameters
    ----------
    adj_matrics: Scipy matrix or a list of them 
        Single or a list of Scipy sparse matrices.
    rate: Single or a list of float scale, optional.
        the normalize rate for `adj_matrics`.
    self_loop: float scalar, optional.
        weight of self loops for the adjacency matrix.

    Returns
    ----------
    Single or a list of Scipy sparse matrix or Numpy matrices.

    """
    def normalize(adj, r):

        # here creats a new copy of adj
        adj = adj + self_loop*sp.eye(adj.shape[0])

        if r is None:
            return adj.astype(config.floatx(), copy=False)

        degree = adj.sum(1).A1
        degree_power = np.power(degree, r)

        adj = adj.tocoo(copy=False)
        adj.data = degree_power[adj.row] * adj.data * degree_power[adj.col]
        adj = adj.tocsr(copy=False)

        return adj.astype(config.floatx(), copy=False)

    if is_list_like(adj_matrics) and not isinstance(adj_matrics[0], Number):
        size = len(adj_matrics)
        rate = repeat(rate, size)
        return [normalize(A, r) for A, r in zip(adj_matrics, rate)]
    else:
        return normalize(adj_matrics, rate)


class Bunch(dict):
    """Container object for datasets
    Dictionary-like object that exposes its keys as attributes.
    >>> b = Bunch(a=1, b=2)
    >>> b['b']
    2
    >>> b.b
    2
    >>> b.a = 3
    >>> b['a']
    3
    >>> b.c = 6
    >>> b['c']
    6
    """

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def __setattr__(self, key, value):
        self[key] = value

    def __dir__(self):
        return self.keys()

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(key)

    def __setstate__(self, state):
        # Bunch pickles generated with scikit-learn 0.16.* have an non
        # empty __dict__. This causes a surprising behaviour when
        # loading these pickles scikit-learn 0.17: reading bunch.key
        # uses __dict__ but assigning to bunch.key use __setattr__ and
        # only changes bunch['key']. More details can be found at:
        # https://github.com/scikit-learn/scikit-learn/issues/6196.
        # Overriding __setstate__ to be a noop has the effect of
        # ignoring the pickled __dict__
        pass
