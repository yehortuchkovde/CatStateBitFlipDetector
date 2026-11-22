"""Cat-qubit models: the nominal single-mode model and the two-mode memory + buffer model.

Conventions (hbar = 1, rotating frame of the memory, kappa_2 = 1 by default):

* nominal single-mode model: no Hamiltonian apart from optional Kerr and detuning, and the
  jump operators
      L_buffer    = sqrt(kappa_2) (a^2 - alpha^2)       the monitored "buffer" channel
      L_loss      = sqrt(kappa_1 (1 + n_th)) a
      L_thermal   = sqrt(kappa_1 n_th) a^dagger
      L_dephasing = sqrt(kappa_phi) a^dagger a
  alpha is real and positive, alpha^2 = nbar.

* two-mode model: memory a and buffer b with
      H = g_2 (a^2 b^dagger + a^dagger^2 b) - eps_d (b + b^dagger) - (K/2) a^dagger^2 a^2
      L_buffer = i sqrt(kappa_b) b                       the monitored channel (the phase makes
                                                         it ~ sqrt(kappa_2)(a^2 - alpha^2) after elimination)
  plus the same memory loss, thermal and dephasing channels. With eps_d = g_2 nbar the
  steady state is the cat with |alpha|^2 = nbar and, when kappa_b >> g_2, adiabatic
  elimination of the buffer gives the single-mode model with kappa_2 = 4 g_2^2 / kappa_b.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np

import dynamiqs as dq


@dataclass(frozen=True)
class SingleModeParams:
    """Parameters of the nominal single-mode model (rates in units of kappa_2).

    The defaults are the nominal device of the challenge (see CHALLENGE.md, device sheet).
    """

    nbar: float = 2.5
    kappa2: float = 1.0
    kappa1: float = 0.02
    nth: float = 0.1
    kappa_phi: float = 0.02
    kerr: float = 0.0
    detuning: float = 0.0
    N: int = 24

    @property
    def alpha(self) -> float:
        return float(np.sqrt(self.nbar))

    def to_dict(self) -> dict:
        d = asdict(self)
        d["model"] = "single_mode"
        return d


@dataclass(frozen=True)
class TwoModeParams:
    """Parameters of the two-mode memory + buffer model.

    `kappa2` is the *target* two-photon rate: it fixes g_2 = sqrt(kappa2 * kappa_b) / 2 so
    that 4 g_2^2 / kappa_b = kappa2. The buffer drive eps_d = g_2 * nbar sets the cat size.
    """

    nbar: float = 2.5
    kappa2: float = 1.0
    kappa_b: float = 16.0
    kappa1: float = 0.02
    nth: float = 0.1
    kappa_phi: float = 0.02
    kerr: float = 0.0
    Na: int = 24
    Nb: int = 6

    @property
    def g2(self) -> float:
        return float(np.sqrt(self.kappa2 * self.kappa_b) / 2)

    @property
    def eps_d(self) -> float:
        return self.g2 * self.nbar

    @property
    def alpha(self) -> float:
        return float(np.sqrt(self.nbar))

    def to_dict(self) -> dict:
        d = asdict(self)
        d["model"] = "two_mode"
        d["g2"] = self.g2
        d["eps_d"] = self.eps_d
        return d


@dataclass
class Model:
    """A ready-to-simulate model: Hamiltonian, jump operators and a few helpers."""

    H: dq.QArray
    jump_ops: list
    channels: tuple
    a: dq.QArray
    psi0: dq.QArray
    params: SingleModeParams | TwoModeParams
    x_negative_projector: np.ndarray
    b: dq.QArray | None = None

    @property
    def dim(self) -> int:
        return self.H.shape[-1]

    @property
    def buffer_index(self) -> int:
        return self.channels.index("buffer")

    @property
    def L_buffer(self) -> dq.QArray:
        return self.jump_ops[self.buffer_index]

    def to_dict(self) -> dict:
        return self.params.to_dict()


def memory_x_negative_projector(N: int) -> np.ndarray:
    """Projector onto x < 0 for the quadrature x = (a + a^dagger)/2, in the Fock basis.

    This models an ideal homodyne readout of the memory followed by a threshold at x = 0:
    outcome "-alpha" when x < 0. For a coherent state |alpha> with real alpha the error
    probability is Phi(-2 alpha), about 0.2 % for nbar = 2 and 0.08 % for nbar = 2.5.
    """
    a = np.diag(np.sqrt(np.arange(1, N)), 1)
    x = (a + a.T) / 2
    w, v = np.linalg.eigh(x)
    vneg = v[:, w < 0]
    return vneg @ vneg.conj().T


def _nonzero(ops_and_names):
    ops, names = [], []
    for op, name, rate in ops_and_names:
        if rate > 0:
            ops.append(op)
            names.append(name)
    return ops, tuple(names)


def single_mode(p: SingleModeParams) -> Model:
    """Build the nominal single-mode model."""
    a = dq.destroy(p.N)
    ad = a.dag()
    I = dq.eye(p.N)
    H = p.detuning * (ad @ a) - 0.5 * p.kerr * (ad @ ad @ a @ a)
    L_buffer = np.sqrt(p.kappa2) * (a @ a - p.nbar * I)
    ops, names = _nonzero(
        [
            (L_buffer, "buffer", p.kappa2),
            (np.sqrt(p.kappa1 * (1 + p.nth)) * a, "loss", p.kappa1),
            (np.sqrt(p.kappa1 * p.nth) * ad, "thermal", p.kappa1 * p.nth),
            (np.sqrt(p.kappa_phi) * (ad @ a), "dephasing", p.kappa_phi),
        ]
    )
    psi0 = dq.coherent(p.N, p.alpha)
    return Model(H, ops, names, a, psi0, p, memory_x_negative_projector(p.N))


def two_mode(p: TwoModeParams) -> Model:
    """Build the two-mode memory + buffer model."""
    a = dq.tensor(dq.destroy(p.Na), dq.eye(p.Nb))
    b = dq.tensor(dq.eye(p.Na), dq.destroy(p.Nb))
    ad, bd = a.dag(), b.dag()
    H = p.g2 * (a @ a @ bd + ad @ ad @ b) - p.eps_d * (b + bd) - 0.5 * p.kerr * (ad @ ad @ a @ a)
    ops, names = _nonzero(
        [
            (1j * np.sqrt(p.kappa_b) * b, "buffer", p.kappa_b),  # phase chosen so that i sqrt(kappa_b) b ~ sqrt(kappa_2)(a^2 - alpha^2)
            (np.sqrt(p.kappa1 * (1 + p.nth)) * a, "loss", p.kappa1),
            (np.sqrt(p.kappa1 * p.nth) * ad, "thermal", p.kappa1 * p.nth),
            (np.sqrt(p.kappa_phi) * (ad @ a), "dephasing", p.kappa_phi),
        ]
    )
    psi0 = dq.tensor(dq.coherent(p.Na, p.alpha), dq.basis(p.Nb, 0))
    proj = np.kron(memory_x_negative_projector(p.Na), np.eye(p.Nb))
    return Model(H, ops, names, a, psi0, p, proj, b=b)


def nominal_model(**overrides) -> Model:
    """The nominal device of the challenge (single mode), for example `nominal_model(nbar=3.0)`.

    Unless `N` is given, the Fock cutoff is the one of the datasets at that cat size
    (`protocol.fock_cutoff`: 24 up to nbar = 2.5, 28 above).
    """
    from .protocol import fock_cutoff

    overrides.setdefault("N", fock_cutoff(overrides.get("nbar", SingleModeParams.nbar)))
    return single_mode(SingleModeParams(**overrides))


def build(params) -> Model:
    if isinstance(params, SingleModeParams):
        return single_mode(params)
    if isinstance(params, TwoModeParams):
        return two_mode(params)
    raise TypeError(f"unknown parameter type {type(params)}")


def params_from_dict(d: dict):
    d = dict(d)
    kind = d.pop("model")
    if kind == "single_mode":
        return SingleModeParams(**d)
    if kind == "two_mode":
        d.pop("g2", None)
        d.pop("eps_d", None)
        return TwoModeParams(**d)
    raise ValueError(f"unknown model kind {kind}")
