"""Helper functions for defining forms."""

from typing import Union
import numpy as np
from numpy import ndarray
from skfem.element import DiscreteField


FieldOrArray = Union[DiscreteField, ndarray]


def grad(u: DiscreteField):
    """Gradient."""
    return u.grad


def div(u: DiscreteField):
    """Divergence."""
    if u.div is not None:
        return u.div
    elif u.grad is not None:
        try:
            return np.einsum('ii...', u.grad)
        except ValueError:  # one-dimensional u?
            return u.grad[0]
    raise NotImplementedError


def curl(u: DiscreteField):
    """Curl."""
    if u.curl is not None:
        return u.curl
    raise NotImplementedError


def d(u: DiscreteField):
    """Gradient, divergence or curl."""
    if u.grad is not None:
        return u.grad
    elif u.div is not None:
        return u.div
    elif u.curl is not None:
        return u.curl
    raise NotImplementedError


def sym_grad(u: DiscreteField):
    """Symmetric gradient."""
    return .5 * (u.grad + transpose(u.grad))


def dd(u):
    return u.hess


def ddd(u):
    return u.hod[0]


def dddd(u):
    return u.hod[1]


def dot(u: FieldOrArray, v: FieldOrArray):
    """Dot product."""
    return np.einsum('i...,i...', u, v)


def ddot(u: FieldOrArray, v: FieldOrArray):
    """Double dot product."""
    return np.einsum('ij...,ij...', u, v)


def dddot(u: FieldOrArray, v: FieldOrArray):
    """Triple dot product."""
    return np.einsum('ijk...,ijk...', u, v)


def prod(u: FieldOrArray, v: FieldOrArray, w: FieldOrArray = None):
    """Tensor product."""
    if w is None:
        return np.einsum('i...,j...->ij...', u, v)
    return np.einsum('i...,j...,k...->ijk...', u, v, w)


def trace(T):
    """Trace of matrix."""
    return np.einsum('ii...', T)


def transpose(T):
    """Transpose of matrix."""
    return np.einsum('ij...->ji...', T)


def eye(w, n):
    """Create diagonal matrix with w on diagonal."""
    return np.array([[w if i == j else 0. * w for i in range(n)]
                     for j in range(n)])
