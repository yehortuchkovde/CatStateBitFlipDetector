"""Bit-flip and phase-flip rates from the Liouvillian spectrum.

For a model with Liouvillian L, the slowest non-zero eigenvalues give the decay rates of the
logical observables: the eigenvector carrying <a> (i.e. Z_L) decays at the bit-flip rate
Gamma_Z, the eigenvector carrying the photon-number parity (X_L) decays at the phase-flip
rate Gamma_X. A flip is named after the axis along which the state flips: a bit flip
exchanges the eigenstates of Z_L (the two coherent states), a phase flip those of X_L (the two
cat states). Conventions:

    <Z_L>(t) ~ exp(-Gamma_Z t)      P(read "-alpha" at t | prepared "+alpha") = (1 - exp(-Gamma_Z t)) / 2
    <X_L>(t) ~ exp(-Gamma_X t)      Gamma_X ~ 2 kappa_1 [(1 + 2 n_th) nbar + n_th] (loss and thermal
                                    excitation flip the parity; dephasing does not)

so that the *probability* of a bit flip per unit time is Gamma_Z / 2.
"""

from __future__ import annotations

import numpy as np
import scipy.linalg
import scipy.sparse
import scipy.sparse.linalg

from .models import Model


def liouvillian_matrix(model: Model, sparse: bool = False):
    """Liouvillian as a (dim^2, dim^2) matrix acting on column-stacked density matrices."""
    H = np.asarray(model.H.to_jax())
    dim = H.shape[0]
    I = np.eye(dim)
    kron = scipy.sparse.kron if sparse else np.kron
    conv = (lambda m: scipy.sparse.csr_matrix(m)) if sparse else (lambda m: np.asarray(m))
    # vec(A rho B) = (B^T kron A) vec(rho) for column stacking
    L = conv(kron(I, -1j * H) + kron(1j * H.T, I))
    for op in model.jump_ops:
        C = np.asarray(op.to_jax())
        CdC = C.conj().T @ C
        L = L + conv(kron(C.conj(), C) - 0.5 * kron(I, CdC) - 0.5 * kron(CdC.T, I))
    return L


def spectrum(model: Model, n_eig: int = 8, sparse: bool | None = None) -> dict:
    """Slowest eigenvalues of the Liouvillian with the bit-flip and phase-flip rates.

    Returns dict with `eigenvalues` (sorted by decreasing real part), `gamma_z` (the bit-flip
    rate), `gamma_x` (the phase-flip rate),
    and the diagnostics used to identify them (`a_weight`, `parity_weight` per eigenvector).
    """
    dim = model.dim
    if sparse is None:
        sparse = dim > 36
    a = np.asarray(model.a.to_jax())
    n_op = np.asarray((model.a.dag() @ model.a).to_jax())
    parity = scipy.linalg.expm(1j * np.pi * n_op)
    if sparse:
        L = liouvillian_matrix(model, sparse=True)
        vals, vecs = scipy.sparse.linalg.eigs(L, k=n_eig, sigma=1e-9, which="LM")
    else:
        L = liouvillian_matrix(model)
        vals, vecs = scipy.linalg.eig(L)
    order = np.argsort(-vals.real)[:n_eig]
    vals, vecs = vals[order], vecs[:, order]
    a_w, p_w = [], []
    for k in range(len(vals)):
        rho = vecs[:, k].reshape(dim, dim, order="F")
        norm = np.abs(rho).sum() + 1e-300
        a_w.append(abs(np.trace(a @ rho)) / norm)
        p_w.append(abs(np.trace(parity @ rho)) / norm)
    a_w, p_w = np.array(a_w), np.array(p_w)
    nonzero = np.abs(vals.real) > 1e-9
    k_bit = int(np.argmax(np.where(nonzero, a_w, -1)))  # the mode that carries <a>, hence Z_L
    k_phase = int(np.argmax(np.where(nonzero, p_w, -1)))  # the mode that carries the parity X_L
    return {
        "eigenvalues": vals,
        "gamma_z": float(-vals[k_bit].real),
        "gamma_x": float(-vals[k_phase].real),
        "a_weight": a_w,
        "parity_weight": p_w,
    }


def flip_probability(gamma_z: float, T: float) -> float:
    """Probability of reading "-alpha" after a time T, starting from "+alpha", for the
    bit-flip rate `gamma_z`."""
    return 0.5 * (1.0 - np.exp(-gamma_z * T))
