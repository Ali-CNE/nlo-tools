from tensor_parser import load_tensor

from analysis import compute_surface
from analysis import compute_planes

from plotting import plot_surface
from plotting import plot_polar_planes
from plotting import plot_signed_curves


def main():

    print("Loading tensor...")

    beta = load_tensor("tensor.txt")

    print("Tensor shape:", beta.shape)

    print("Computing surface...")
    nx, ny, nz, beta_n = compute_surface(beta)

    print("Computing planes...")
    planes = compute_planes(beta)

    print("Plotting surface...")
    plot_surface(nx, ny, nz, beta_n)

    print("Plotting polar planes...")
    plot_polar_planes(planes)

    print("Plotting signed curves...")
    plot_signed_curves(planes)

    print("Done.")

if __name__ == "__main__":
    main()

