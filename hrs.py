"""
======================================================================
hrs.py

Hyper-Rayleigh Scattering (HRS) Analysis Module

Implements Multiwfn-style Hyper-Rayleigh Scattering analysis for the
first hyperpolarizability tensor βijk.

Designed for the NLO Tensor Analyzer.
======================================================================
"""

import numpy as np

# ======================================================================
# Cartesian indices
# ======================================================================
X = 0
Y = 1
Z = 2
AXES = ("x", "y", "z")

# ======================================================================
# Tensor validation
# ======================================================================
def validate_beta(beta):
    """Validate beta tensor."""
    if not isinstance(beta, (list, tuple, np.ndarray)):
        raise ValueError("beta must be a list, tuple, or numpy array of three matrices.")

    if len(beta) != 3:
        raise ValueError("beta must contain exactly three matrices.")

    mats = []
    for i in range(3):
        arr = np.asarray(beta[i], dtype=float)
        if arr.shape != (3, 3):
            raise ValueError("Each beta matrix must have shape (3,3).")
        mats.append(arr)
    return mats

# ======================================================================
# Convert to full tensor
# ======================================================================
def tensor3(beta):
    """Convert parser output into a full 3×3×3 tensor."""
    mats = validate_beta(beta)
    tensor = np.zeros((3, 3, 3))
    for i in range(3):
        tensor[i, :, :] = mats[i]
    return tensor

# ======================================================================
# Distinct index generators
# ======================================================================
def unequal_pairs():
    pairs = []
    for i in range(3):
        for j in range(3):
            if i != j:
                pairs.append((i, j))
    return pairs

def unequal_triplets():
    triplets = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if len({i, j, k}) == 3:
                    triplets.append((i, j, k))
    return triplets

PAIRS = unequal_pairs()
TRIPLETS = unequal_triplets()

# ======================================================================
# Tensor norms and invariants
# ======================================================================
def frobenius_norm(beta):
    B = tensor3(beta)
    return np.sqrt(np.sum(B ** 2))

def beta_vector(beta):
    B = tensor3(beta)
    vec = np.zeros(3)
    for i in range(3):
        s = 0.0
        for j in range(3):
            s += B[i, j, j]
            s += B[j, i, j]
            s += B[j, j, i]
        vec[i] = s
    return vec

def beta_vector_norm(beta):
    return np.linalg.norm(beta_vector(beta))

def beta_ZZZ2(beta):
    B = tensor3(beta)
    value = 0.0

    for i in range(3):
        value += (1.0 / 7.0) * B[i, i, i] ** 2

    for i, j in PAIRS:
        value += (4.0 / 35.0) * B[i, i, j] ** 2
        value += (2.0 / 35.0) * B[i, i, i] * B[i, j, j]
        value += (4.0 / 35.0) * B[i, i, i] * B[i, i, j]
        value += (4.0 / 35.0) * B[i, i, i] * B[j, j, i]
        value += (1.0 / 35.0) * B[j, j, i] ** 2

    for i, j, k in TRIPLETS:
        value += (4.0 / 105.0) * B[i, i, j] * B[j, k, i]
        value += (1.0 / 105.0) * B[j, k, i] ** 2
        value += (4.0 / 105.0) * B[i, i, j] * B[i, i, k]
        value += (2.0 / 105.0) * B[i, i, j] ** 2
        value += (4.0 / 105.0) * B[i, j, k] * B[j, k, i]

    return value

def beta_XZZ2(beta):
    B = tensor3(beta)
    value = 0.0

    for i, j in PAIRS:
        value += (1.0 / 35.0) * B[i, i, i] ** 2
        value += (4.0 / 105.0) * B[i, i, i] * B[i, j, j]
        value += (-2.0 / 35.0) * B[i, i, i] * B[j, j, i]
        value += (8.0 / 105.0) * B[i, i, j] ** 2
        value += (3.0 / 35.0) * B[i, j, j] ** 2
        value += (-2.0 / 35.0) * B[i, i, j] * B[j, i, i]

    for i, j, k in TRIPLETS:
        value += (1.0 / 35.0) * B[i, j, j] * B[i, k, k]
        value += (-2.0 / 105.0) * B[i, i, i] * B[j, j, k]
        value += (-2.0 / 105.0) * B[i, i, j] * B[j, k, i]
        value += (2.0 / 35.0) * B[i, i, j] ** 2
        value += (-2.0 / 105.0) * B[i, j, k] * B[j, k, i]

    return value

# ==========================================================
# Comprehensive Public Wrapper for Streamlit
# ==========================================================
def compute_hrs_quantities(beta):
    """
    Compute Multiwfn-style Hyper-Rayleigh Scattering (HRS) quantities.
    """
    # 1. Calculate underlying base rotational averages
    b_zzz2 = beta_ZZZ2(beta)
    b_xzz2 = beta_XZZ2(beta)

    # 2. Total HRS hyperpolarizability
    b_hrs = np.sqrt(max(0.0, b_zzz2 + b_xzz2))

    # 3. Depolarization Ratio
    if b_zzz2 > 1e-14:
        dr = b_xzz2 / b_zzz2
    else:
        dr = np.nan

    # 4. Nonlinear anisotropy parameter
    denom = b_zzz2 + 2.0 * b_xzz2
    if abs(denom) > 1e-14:
        rho = (b_zzz2 - b_xzz2) / denom
    else:
        rho = np.nan

    return {
        "beta_ZZZ2": b_zzz2,
        "beta_XZZ2": b_xzz2,
        "beta_HRS": b_hrs,
        "DR": dr,
        "rho": rho,
    }

# ==========================================================
# Self-test Execution Block
# ==========================================================
if __name__ == "__main__":
    beta_x = np.array([
        [76.1135,  -6.17042, -130.296],
        [-3.58976, 107.758,   100.735],
        [-110.547, 74.4836,  -506.650]
    ])

    beta_y = np.array([
        [-3.58976, 107.758, 100.735],
        [91.4138, -123.232, 23.0796],
        [78.9942, 72.0804, 347.781]
    ])

    beta_z = np.array([
        [-110.547, 74.4836, -506.650],
        [78.9942, 72.0804, 347.781],
        [-495.894, 330.497, -1195.450]
    ])

    beta_input = [beta_x, beta_y, beta_z]
    results = compute_hrs_quantities(beta_input)

    print("\n========== HRS Analysis ==========\n")
    print(f"<βZZZ²>            : {results['beta_ZZZ2']:.6f}")
    print(f"<βXZZ²>            : {results['beta_XZZ2']:.6f}")
    print("-------------------------------------------")
    print(f"βHRS               : {results['beta_HRS']:.6f}")
    print(f"Depolarization DR  : {results['DR']:.6f}")
    print(f"ρ                  : {results['rho']:.6f}")
    print("-------------------------------------------")
    print("\n===========================================\n")