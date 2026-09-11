from __future__ import annotations

import numpy as np


def _as_square(block, name):
    arr = np.asarray(block)
    if arr.ndim != 2 or arr.shape[0] != arr.shape[1]:
        raise ValueError(f"{name} must be square")
    if not np.all(np.isfinite(arr.real)) or not np.all(np.isfinite(arr.imag)):
        raise ValueError(f"{name} must be finite")
    return arr


def assemble_coupled_generator(blocks, couplings=None):
    """Assemble a block-structured coupled generator.

    Parameters
    ----------
    blocks:
        Sequence of square subsystem generators A_i.
    couplings:
        Mapping ``(receiver, sender) -> K_ij``.  K_ij maps the state of
        subsystem ``sender`` into its contribution to d/dt of subsystem
        ``receiver``.  Coupling blocks are dynamical transformations, not
        averaging weights.

    Returns
    -------
    dict with the full generator, subsystem slices, dimensions, and a copy of
    the validated directed coupling blocks.
    """
    if len(blocks) == 0:
        raise ValueError("at least one subsystem block is required")
    clean = [_as_square(b, f"blocks[{i}]") for i, b in enumerate(blocks)]
    dtype = np.result_type(*[b.dtype for b in clean], float)
    dims = [int(b.shape[0]) for b in clean]
    starts = np.cumsum([0] + dims)
    slices = [slice(int(starts[i]), int(starts[i + 1])) for i in range(len(dims))]
    A = np.zeros((int(starts[-1]), int(starts[-1])), dtype=dtype)
    for i, block in enumerate(clean):
        A[slices[i], slices[i]] = block

    validated = {}
    for key, value in (couplings or {}).items():
        if not isinstance(key, tuple) or len(key) != 2:
            raise ValueError("coupling keys must be (receiver, sender) tuples")
        receiver, sender = int(key[0]), int(key[1])
        if receiver == sender:
            raise ValueError("internal subsystem dynamics belong in A_i, not K_ii")
        if receiver < 0 or sender < 0 or receiver >= len(dims) or sender >= len(dims):
            raise IndexError("coupling subsystem index out of range")
        K = np.asarray(value, dtype=dtype)
        expected = (dims[receiver], dims[sender])
        if K.shape != expected:
            raise ValueError(
                f"coupling {(receiver, sender)} has shape {K.shape}, expected {expected}"
            )
        if not np.all(np.isfinite(K.real)) or not np.all(np.isfinite(K.imag)):
            raise ValueError("coupling block must be finite")
        A[slices[receiver], slices[sender]] += K
        validated[(receiver, sender)] = K.copy()

    return {
        "generator": A,
        "slices": slices,
        "dimensions": tuple(dims),
        "couplings": validated,
    }


def feedback_return_operator(
    A_group,
    A_environment,
    K_group_from_environment,
    K_environment_from_group,
    s,
):
    """Return the closed feedback contribution Sigma_G(s).

    Convention
    ----------
    dx_G/dt = A_G x_G + K_GE x_E
    dx_E/dt = A_E x_E + K_EG x_G

    Then
    Sigma_G(s) = K_GE (s I - A_E)^(-1) K_EG.

    This operator contains both the outward pathway G->E and the transformed
    return pathway E->G.  It is frequency/complex-rate dependent because the
    environment's own dynamics alter the signal before it returns.
    """
    Ag = _as_square(A_group, "A_group")
    Ae = _as_square(A_environment, "A_environment")
    Kge = np.asarray(K_group_from_environment)
    Keg = np.asarray(K_environment_from_group)
    g = Ag.shape[0]
    e = Ae.shape[0]
    if Kge.shape != (g, e):
        raise ValueError("K_group_from_environment has incompatible shape")
    if Keg.shape != (e, g):
        raise ValueError("K_environment_from_group has incompatible shape")
    dtype = np.result_type(Ag, Ae, Kge, Keg, complex(s))
    M = complex(s) * np.eye(e, dtype=dtype) - np.asarray(Ae, dtype=dtype)
    X = np.linalg.solve(M, np.asarray(Keg, dtype=dtype))
    return np.asarray(Kge, dtype=dtype) @ X


def effective_group_generator(
    A_group,
    A_environment,
    K_group_from_environment,
    K_environment_from_group,
    s,
):
    """Return the frequency-dependent effective grouped generator A_G+Sigma_G(s)."""
    Ag = _as_square(A_group, "A_group")
    Sigma = feedback_return_operator(
        Ag,
        A_environment,
        K_group_from_environment,
        K_environment_from_group,
        s,
    )
    return np.asarray(Ag, dtype=Sigma.dtype) + Sigma


def closed_loop_characteristic_matrix(
    A_group,
    A_environment,
    K_group_from_environment,
    K_environment_from_group,
    s,
):
    """Return sI - A_G - Sigma_G(s) for the grouped subsystem."""
    Aeff = effective_group_generator(
        A_group,
        A_environment,
        K_group_from_environment,
        K_environment_from_group,
        s,
    )
    return complex(s) * np.eye(Aeff.shape[0], dtype=Aeff.dtype) - Aeff


def schur_determinant_identity(
    A_group,
    A_environment,
    K_group_from_environment,
    K_environment_from_group,
    s,
):
    """Evaluate the full-vs-reduced determinant identity at complex rate s.

    For invertible ``sI-A_E``:

    det(sI-A_full)
      = det(sI-A_E) det(sI-A_G-Sigma_G(s)).

    The returned residual should be numerically small.  This is a mathematical
    consistency diagnostic, not a biological claim.
    """
    Ag = _as_square(A_group, "A_group")
    Ae = _as_square(A_environment, "A_environment")
    Kge = np.asarray(K_group_from_environment)
    Keg = np.asarray(K_environment_from_group)
    full = np.block([[Ag, Kge], [Keg, Ae]])
    lhs = np.linalg.det(complex(s) * np.eye(full.shape[0]) - full)
    env_det = np.linalg.det(complex(s) * np.eye(Ae.shape[0]) - Ae)
    reduced_det = np.linalg.det(
        closed_loop_characteristic_matrix(Ag, Ae, Kge, Keg, s)
    )
    rhs = env_det * reduced_det
    scale = max(1.0, abs(lhs), abs(rhs))
    return {
        "lhs": lhs,
        "rhs": rhs,
        "absolute_residual": float(abs(lhs - rhs)),
        "relative_residual": float(abs(lhs - rhs) / scale),
    }


def coupled_spectrum(blocks, couplings=None):
    """Return uncoupled and coupled spectra without collapsing them to a scalar."""
    assembled = assemble_coupled_generator(blocks, couplings=couplings)
    uncoupled = assemble_coupled_generator(blocks, couplings=None)["generator"]
    return {
        "uncoupled_poles": np.linalg.eigvals(uncoupled),
        "coupled_poles": np.linalg.eigvals(assembled["generator"]),
        "generator": assembled["generator"],
        "slices": assembled["slices"],
        "couplings": assembled["couplings"],
    }
