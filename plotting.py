import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 12,
    "axes.titlesize": 12,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.titlesize": 15,
    "savefig.dpi": 600
})


def plot_surface(nx, ny, nz, beta_n):

    radius = np.abs(beta_n)

    norm = radius / radius.max()

    cmap = plt.cm.RdBu_r

    colors = cmap(
        (beta_n - beta_n.min()) /
        (np.ptp(beta_n) + 1e-12)
    )

    fig = plt.figure(figsize=(9, 9))
    ax = fig.add_subplot(111, projection="3d")

    ax.plot_surface(
        norm * nx,
        norm * ny,
        norm * nz,
        facecolors=colors,
        linewidth=0,
        alpha=0.85
    )

    mappable = plt.cm.ScalarMappable(
        cmap=cmap,
        norm=plt.Normalize(
            vmin=beta_n.min(),
            vmax=beta_n.max()
        )
    )

    fig.colorbar(
        mappable,
        ax=ax,
        shrink=0.6,
        pad=0.05,
        aspect=18
    )

    ax.tick_params(axis='x', pad=1)
    ax.tick_params(axis='y', pad=2)
    ax.tick_params(axis='z', pad=6)

    ax.set_xlabel("X (a.u.)", labelpad=2)
    ax.set_ylabel("Y (a.u.)", labelpad=4)
    ax.set_zlabel("Z (a.u.)", labelpad=8)

    ax.set_box_aspect([1, 1, 1])

    plt.tight_layout(pad=2.0)

    return fig

def plot_polar_planes(planes):

    fig, axes = plt.subplots(
        1,
        3,
        figsize=(16, 5),
        subplot_kw={"projection": "polar"}
    )

    names = ["xy", "xz", "yz"]

    titles = [
        "XY plane (θ = π/2)",
        "XZ plane (φ = 0)",
        "YZ plane (φ = π/2)"
    ]

    for ax, name, title in zip(axes, names, titles):

        beta = planes[name]["beta"]
        angle = planes[name]["angle"]

        radius = np.abs(beta)

        # Prevent division by zero
        if radius.max() > 0:
            radius = radius / radius.max()

        colors = [
            "red" if b >= 0 else "blue"
            for b in beta
        ]

        ax.scatter(
            angle,
            radius,
            c=colors,
            s=5
        )

        ax.plot(
            angle,
            radius,
            "k-",
            lw=0.5
        )

        ax.set_ylim(0, 1.1)
        ax.set_title(title)

    plt.tight_layout(pad=2.0)

    return fig

def plot_signed_curves(planes):

    fig, axes = plt.subplots(
        1, 3,
        figsize=(16, 5)
    )

    colors = ["b", "r", "g"]

    names = ["xy", "xz", "yz"]

    titles = [
    "XY plane (θ = π/2)",
    "XZ plane (φ = 0)",
    "YZ plane (φ = π/2)"
]

    xlabels = [
        "φ (rad)",
        "θ (rad)",
        "θ (rad)"
    ]

    ylabels = [
        r"β(φ) (a.u.)",
        r"β(θ) (a.u.)",
        r"β(θ) (a.u.)"
    ]

    for ax, name, color, title, xl, yl in zip(
        axes, names, colors, titles, xlabels, ylabels
    ):

        ax.plot(
            planes[name]["angle"],
            planes[name]["beta"],
            color
        )

        ax.axhline(
            0,
            color="k",
            ls="--",
            lw=0.5
        )

        ax.set_title(title, fontsize=14)

        ax.set_xlabel(xl, fontsize=12)
        ax.set_ylabel(yl, fontsize=12)

        ax.tick_params(labelsize=11)
        ax.grid(True, alpha=0.3)

    plt.tight_layout(pad=2.0)
    return fig