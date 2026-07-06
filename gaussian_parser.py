import numpy as np
import re

def _to_float(x):
    return float(x.replace("D", "E"))

def extract_gaussian_components(text):
    """
    Extract (label -> value) from Gaussian output
    using first numeric column (au)
    """

    pattern = re.compile(
        r'^\s*([a-z]{3})\s+([-\d.]+D[+-]\d+|[-\d.]+)',
        re.IGNORECASE
    )

    components = {}

    for line in text.splitlines():
        match = pattern.match(line)
        if not match:
            continue

        key = match.group(1).lower()
        value = _to_float(match.group(2))

        components[key] = value

    return components

def build_beta_tensor(components):
    """
    Returns beta[i,j,k] in canonical form (3,3,3)
    """

    beta_x = np.zeros((3,3))
    beta_y = np.zeros((3,3))
    beta_z = np.zeros((3,3))

    # -------------------------
    # mapping helpers
    # -------------------------
    def set_sym(mat_list, i, j, k, val):
        mat_list[i][j, k] = val
        mat_list[j][i, k] = val
        mat_list[k][i, j] = val

    # -------------------------
    # direct assignments
    # -------------------------

    # xxx
    beta_x[0,0] = components.get("xxx", 0.0)

    # xxy symmetry
    val = components.get("xxy", 0.0)
    beta_x[0,1] = val
    beta_x[1,0] = val
    beta_y[0,0] = val

    # yxy
    val = components.get("yxy", 0.0)
    beta_y[0,1] = val
    beta_x[1,1] = val
    beta_y[1,0] = val

    # yyy
    beta_y[1,1] = components.get("yyy", 0.0)

    # xxz
    val = components.get("xxz", 0.0)
    beta_x[0,2] = val
    beta_x[2,0] = val
    beta_z[0,0] = val

    # yxz (fully symmetric group)
    val = components.get("yxz", 0.0)
    beta_y[0,2] = val
    beta_x[1,2] = val
    beta_x[2,1] = val
    beta_y[2,0] = val
    beta_z[0,1] = val
    beta_z[1,0] = val

    # yyz
    val = components.get("yyz", 0.0)
    beta_y[1,2] = val
    beta_y[2,1] = val
    beta_z[1,1] = val

    # zxz
    val = components.get("zxz", 0.0)
    beta_z[0,2] = val
    beta_x[2,2] = val
    beta_z[2,0] = val

    # zyz
    val = components.get("zyz", 0.0)
    beta_z[1,2] = val
    beta_y[2,2] = val
    beta_z[2,1] = val

    # zzz
    beta_z[2,2] = components.get("zzz", 0.0)

    # -------------------------
    # stack into canonical tensor
    # -------------------------
    beta = np.zeros((3,3,3))
    beta[0] = beta_x
    beta[1] = beta_y
    beta[2] = beta_z

    return beta

def parse_gaussian_static_beta(text):
    """
    Full pipeline:
    Gaussian text → components → tensor (3,3,3)
    """

    components = extract_gaussian_components(text)
    beta = build_beta_tensor(components)

    return beta
