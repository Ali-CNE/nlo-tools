import numpy as np

# =========================================================
# BASIC UTILITIES
# =========================================================

def beta_of_direction(beta, n):
    """
    Contract tensor along direction n:
    β(n) = β_ijk n_i n_j n_k
    """
    return np.einsum('ijk,i,j,k', beta, n, n, n)


# =========================================================
# STATIC β TENSOR PHYSICS (MANUAL / KLEINMAN-ASSUMED)
# =========================================================

def beta_vector_static(beta):
    """
    Static hyperpolarizability vector:

    β_i = Σ_j (β_ijj + β_jij + β_jji)
    """
    vec = np.zeros(3)

    for i in range(3):
        s = 0.0
        for j in range(3):
            s += beta[i, j, j]
            s += beta[j, i, j]
            s += beta[j, j, i]
        vec[i] = s

    return vec


def beta_total_static(beta):
    return np.linalg.norm(beta_vector_static(beta))


# =========================================================
# DYNAMIC GAUSSIAN DATA (IMPORTANT: NO RECONSTRUCTION)
# =========================================================

def beta_vector_dynamic(beta):
    """
    Dynamic Gaussian β vector

    βi = Σj (βijj + βjij + βjji)
    """

    vec = np.zeros(3)

    for i in range(3):

        s = 0.0

        for j in range(3):

            s += beta[i, j, j]
            s += beta[j, i, j]
            s += beta[j, j, i]

        vec[i] = s

    return vec


def beta_total_dynamic(beta):

    return np.linalg.norm(
        beta_vector_dynamic(beta)
    )


# =========================================================
# SURFACE / VISUALIZATION (COMMON FOR BOTH)
# =========================================================

def compute_surface(beta, n_theta=60, n_phi=120):

    theta = np.linspace(0, np.pi, n_theta)
    phi = np.linspace(0, 2*np.pi, n_phi)

    theta, phi = np.meshgrid(theta, phi)

    nx = np.sin(theta) * np.cos(phi)
    ny = np.sin(theta) * np.sin(phi)
    nz = np.cos(theta)

    n = np.stack([nx, ny, nz], axis=-1)

    beta_n = np.einsum('ijk,...i,...j,...k', beta, n, n, n)

    return nx, ny, nz, beta_n


def compute_planes(beta):

    phi = np.linspace(0, 2*np.pi, 360)
    theta = np.linspace(0, np.pi, 180)

    # XY
    n_xy = np.stack([np.cos(phi), np.sin(phi), np.zeros_like(phi)], axis=-1)
    beta_xy = np.einsum('ijk,ni,nj,nk->n', beta, n_xy, n_xy, n_xy)

    # XZ
    n_xz = np.stack([np.sin(theta), np.zeros_like(theta), np.cos(theta)], axis=-1)
    beta_xz = np.einsum('ijk,ni,nj,nk->n', beta, n_xz, n_xz, n_xz)

    # YZ
    n_yz = np.stack([np.zeros_like(theta), np.sin(theta), np.cos(theta)], axis=-1)
    beta_yz = np.einsum('ijk,ni,nj,nk->n', beta, n_yz, n_yz, n_yz)

    return {
        "xy": {"angle": phi, "beta": beta_xy},
        "xz": {"angle": theta, "beta": beta_xz},
        "yz": {"angle": theta, "beta": beta_yz},
    }


# =========================================================
# BACKWARD COMPATIBILITY WRAPPERS (OPTIONAL SAFETY)
# =========================================================

def beta_vector(beta):
    """
    Default = static behavior.
    """
    return beta_vector_static(beta)


def beta_total(beta):
    return beta_total_static(beta)