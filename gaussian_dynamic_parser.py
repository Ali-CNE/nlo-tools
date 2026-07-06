import numpy as np


def parse_gaussian_dynamic_beta(text):
    """
    Parse Gaussian dynamic first hyperpolarizability
    Beta(-w;w,0)

    Returns
    -------
    beta : ndarray (3,3,3)

    beta[0] = βx matrix
    beta[1] = βy matrix
    beta[2] = βz matrix
    """

    labels = [
        "xxx", "yxx", "yyx", "zxx", "zyx", "zzx",
        "xxy", "yxy", "yyy", "zxy", "zyy", "zzy",
        "xxz", "yxz", "yyz", "zxz", "zyz", "zzz"
    ]

    values = {}

    for line in text.splitlines():

        cols = line.split()

        if len(cols) < 2:
            continue

        label = cols[0].lower()

        if label not in labels:
            continue

        values[label] = float(
            cols[1].replace("D", "E").replace("d", "e")
        )

    missing = [x for x in labels if x not in values]

    if missing:
        raise ValueError(
            "Missing dynamic β components:\n"
            + ", ".join(missing)
        )

    # ---------------------------------------------------------
    # Construct βx, βy, βz matrices
    # ---------------------------------------------------------

    beta_x = np.array([
        [values["xxx"], values["xxy"], values["xxz"]],
        [values["yxx"], values["yxy"], values["yxz"]],
        [values["zxx"], values["zxy"], values["zxz"]],
    ])

    beta_y = np.array([
        [values["yxx"], values["yxy"], values["yxz"]],
        [values["yyx"], values["yyy"], values["yyz"]],
        [values["zyx"], values["zyy"], values["zyz"]],
    ])

    beta_z = np.array([
        [values["zxx"], values["zxy"], values["zxz"]],
        [values["zyx"], values["zyy"], values["zyz"]],
        [values["zzx"], values["zzy"], values["zzz"]],
    ])

    beta = np.array(
        [beta_x, beta_y, beta_z],
        dtype=float
    )

    return beta