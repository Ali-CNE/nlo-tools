def compute_exact_spherical_invariants(beta_input):
    """
    Computes mathematically exact J=1 (dipolar) and J=3 (octupolar)
    irreducible spherical tensor invariants directly from any 3x3x3 Cartesian tensor.
    """
    # 1. Transform parser input into a standard 3x3x3 numpy array
    B = np.zeros((3, 3, 3))
    for i in range(3):
        B[i, :, :] = beta_input[i]
        
    # 2. Build the completely symmetrized tensor (S)
    S = np.zeros((3, 3, 3))
    for i in range(3):
        for j in range(3):
            for k in range(3):
                S[i,j,k] = (B[i,j,k] + B[i,k,j] + B[j,i,k] + B[j,k,i] + B[k,i,j] + B[k,j,i]) / 6.0

    # 3. Compute the exact J=1 Vector elements
    V = np.zeros(3)
    for i in range(3):
        s = 0.0
        for j in range(3):
            s += B[i, j, j] + B[j, i, j] + B[j, j, i]
        V[i] = s / 5.0

    # 4. Compute Invariant Norms Squared
    norm_J1_sq = np.sum(V**2)
    
    # Sum of squares of the fully symmetric tensor elements
    sum_S_sq = np.sum(S**2)
    norm_J3_sq = sum_S_sq - (5.0 / 3.0) * norm_J1_sq
    
    # 5. Extract Final Exact Magnitudes
    beta_J1 = np.sqrt(max(0.0, norm_J1_sq))
    beta_J3 = np.sqrt(max(0.0, norm_J3_sq))
    
    # 6. Exact Percentage Weights
    total_sq = norm_J1_sq + norm_J3_sq
    if total_sq > 1e-14:
        phi_dipolar = norm_J1_sq / total_sq
        phi_octupolar = norm_J3_sq / total_sq
    else:
        phi_dipolar = 0.0
        phi_octupolar = 0.0
        
    return {
        "beta_J1": beta_J1,
        "beta_J3": beta_J3,
        "phi_dipolar": phi_dipolar,
        "phi_octupolar": phi_octupolar,
    }