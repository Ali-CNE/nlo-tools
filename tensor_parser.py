import numpy as np

def parse_tensor(text):
    """
    Expects 9 rows × 3 columns:
    xxx xxy xxz
    ...
    """

    rows = []
    for line in text.strip().splitlines():
        parts = line.split()
        if len(parts) != 3:
            continue
        rows.append([float(x) for x in parts])

    if len(rows) != 9:
        raise ValueError("Expected 9 rows of tensor components")

    # reshape into 3 matrices (x,y,z)
    beta = np.zeros((3,3,3))

    # simple mapping: row blocks
    beta[0,:,:] = np.array(rows[0:3])
    beta[1,:,:] = np.array(rows[3:6])
    beta[2,:,:] = np.array(rows[6:9])

    return beta