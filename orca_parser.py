import re
import numpy as np


def parse_orca_beta(text):
    """
    Parse the ORCA raw Cartesian hyperpolarizability tensor.

    Input example

    ( x x x ):  -122.105309
    ( x x y ):   112.953365
    ...

    Returns
    -------
    beta : ndarray (3,3,3)

    beta[i,j,k]
    """

    beta = np.zeros((3, 3, 3))

    axis = {
        "x": 0,
        "y": 1,
        "z": 2,
    }

    pattern = re.compile(
        r"\(\s*([xyz])\s+([xyz])\s+([xyz])\s*\)\s*:\s*([-+0-9EeDd\.]+)",
        re.IGNORECASE,
    )

    for line in text.splitlines():

        m = pattern.search(line)

        if not m:
            continue

        i = axis[m.group(1).lower()]
        j = axis[m.group(2).lower()]
        k = axis[m.group(3).lower()]

        value = float(
            m.group(4).replace("D", "E")
        )

        beta[i, j, k] = value

    if np.allclose(beta, 0):
        raise ValueError(
            "No ORCA tensor found."
        )

    return beta