import io
import streamlit as st

from tensor_parser import parse_tensor
from gaussian_parser import parse_gaussian_static_beta
from gaussian_dynamic_parser import parse_gaussian_dynamic_beta
from hrs import compute_hrs_quantities

from analysis import (
    compute_surface,
    compute_planes,
    beta_vector,
    beta_total,
    beta_vector_dynamic,
    beta_total_dynamic,
)


from plotting import (
    plot_surface,
    plot_polar_planes,
    plot_signed_curves,
)

st.set_page_config(
    page_title="NLO Tensor Analyzer",
    page_icon="⚛️",
    layout="wide",
)


def fig_to_png(fig):
    buf = io.BytesIO()
    fig.savefig(
        buf,
        format="png",
        dpi=600,
        bbox_inches="tight",
    )
    buf.seek(0)
    return buf


# =========================
# SESSION STATE
# =========================
if "beta" not in st.session_state:
    st.session_state.beta = None


# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚛️ NLO Analyzer")

page = st.sidebar.radio(
    "",
    [
        "🏠 Home",
        "🔬 Analyzer",
        "ℹ️ About",
    ],
    label_visibility="collapsed",
)

st.sidebar.markdown("---")
st.sidebar.caption("Version 1.0")
st.sidebar.caption("©Institute of Materials Informatics")

# ==========================================================
# HOME PAGE
# ==========================================================
if page == "🏠 Home":

    st.title("⚛️ Nonlinear Optical (NLO) Tensor Analyzer")
    st.markdown("---")

    st.markdown(
        """
        ### Welcome

        This tool provides interactive analysis and visualization of **first hyperpolarizability (β) tensors** obtained from quantum chemistry calculations.

        It supports:

        - Manual β tensor input
        - Gaussian static output parsing
        - Gaussian frequency-dependent (dynamic) β tensors
        - 3D tensor visualization
        - Polar and signed directional analysis

        """
    )

    st.markdown(
        """
    <div style="
    padding:20px;
    background:#E8F4FD;
    border-radius:12px;
    text-align:center;
    ">

    <h3>🚀 Ready to Analyze Your NLO Tensor?</h3>

    Select <b>Analyzer</b> from the left sidebar.

    </div>
    """,
    unsafe_allow_html=True,
)

    st.markdown(
        """

        ### Scientific capabilities

        ✔ Tensor reconstruction from Gaussian output  
        ✔ β-vector and β-total computation  
        ✔ Directional hyperpolarizability mapping  
        ✔ 3D anisotropy surface visualization  
        ✔ Polar plane decomposition  

        ---
        ### Supported formats

        - Gaussian static NLO output
        - Gaussian dynamic β(-ω; ω, 0)
        - Manual tensor entry

        ---
        ### Recommended workflow

        1. Paste Gaussian output  
        2. Click **Analyze**  
        3. Switch between Static / Dynamic datasets  
        4. Visualize tensor properties  

        ---
        ### Developed for

        Computational chemistry • Physics • Materials science  
        """
    )

    st.info("Use the sidebar to start analysis.")
    
# ==========================================================
# ANALYZER PAGE
# ==========================================================
if page == "🔬 Analyzer":

    st.title("Nonlinear Optical (NLO) Tensor Analyzer")
    st.caption("Interactive visualization of β tensors")

    input_mode = st.radio(
        "Select input method",
        (
            "β Tensor",
            "Gaussian Dataset Static",
            "Gaussian Dataset Dynamic",
        ),
        horizontal=True,
    )

    input_text = st.text_area(
        "Paste input data here",
        height=300,
    )

    if st.button("Analyze"):

        try:

            if input_mode == "β Tensor":
                beta = parse_tensor(input_text)

            elif input_mode == "Gaussian Dataset Static":
                beta = parse_gaussian_static_beta(input_text)

            else:
                beta = parse_gaussian_dynamic_beta(input_text)

            st.session_state.beta = beta
            st.success("Analysis completed successfully")

        except Exception as e:
            st.error(f"Parsing failed: {e}")

    # =====================================================
    # OUTPUT
    # =====================================================
    if st.session_state.beta is not None:

        beta = st.session_state.beta

        st.header("Calculated Hyperpolarizability")

        if input_mode == "Gaussian Dataset Dynamic":
            beta_vec = beta_vector_dynamic(beta)
            beta_tot = beta_total_dynamic(beta)
        else:
            beta_vec = beta_vector(beta)
            beta_tot = beta_total(beta)

        #Compute HRS quantities
        hrs = compute_hrs_quantities(beta)

        c1, c2, c3, c4 = st.columns(4)

        c1.metric("βx", f"{beta_vec[0]:.3f}")
        c2.metric("βy", f"{beta_vec[1]:.3f}")
        c3.metric("βz", f"{beta_vec[2]:.3f}")
        c4.metric("βtotal", f"{beta_tot:.3f}")

        st.divider()
        st.header("Hyper-Rayleigh Scattering")

        c1, c2, c3 = st.columns(3)

        c1.metric("βHRS", f"{hrs['beta_HRS']:.4f}")
        c2.metric("Depolarization Ratio", f"{hrs['DR']:.4f}")
        c3.metric("ρ", f"{hrs['rho']:.4f}")

        c1, c2 = st.columns(2)

        c1.metric("⟨βZZZ²⟩", f"{hrs['beta_ZZZ2']:.4f}")
        c2.metric("⟨βXZZ²⟩", f"{hrs['beta_XZZ2']:.4f}")

        c1, c2 = st.columns(2)

        c1.metric("|βJ=1|", f"{hrs['beta_J1']:.4f}")
        c2.metric("|βJ=3|", f"{hrs['beta_J3']:.4f}")

        st.subheader("Dipolar / Octupolar Contribution")

        st.progress(float(hrs["phi_dipolar"]))

        c1, c2 = st.columns(2)

        c1.metric(
            "Dipolar (%)",
            f"{100*hrs['phi_dipolar']:.2f}"
        )

        c2.metric(
            "Octupolar (%)",
            f"{100*hrs['phi_octupolar']:.2f}"
        )

        st.divider()
        st.header("3D Hyperpolarizability Surface")

        nx, ny, nz, beta_n = compute_surface(beta)

        fig_surface = plot_surface(nx, ny, nz, beta_n)

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.pyplot(fig_surface, use_container_width=False)

        st.download_button(
            "Download Surface (PNG)",
            data=fig_to_png(fig_surface),
            file_name="beta_surface.png",
            mime="image/png",
        )

        st.divider()
        st.header("2D Polar Sections")

        planes = compute_planes(beta)

        fig_polar = plot_polar_planes(planes)

        st.pyplot(fig_polar, use_container_width=True)

        st.download_button(
            "Download Polar Plot (PNG)",
            data=fig_to_png(fig_polar),
            file_name="beta_polar.png",
            mime="image/png",
        )

        st.divider()
        st.header("Signed Hyperpolarizability Curves")

        fig_signed = plot_signed_curves(planes)

        st.pyplot(fig_signed, use_container_width=True)

        st.download_button(
            "Download Signed Curves (PNG)",
            data=fig_to_png(fig_signed),
            file_name="beta_signed.png",
            mime="image/png",
        )


# ==========================================================
# ABOUT PAGE
# ==========================================================
if page == "ℹ️ About":

    st.title("About This Tool")
    st.markdown("---")

    st.markdown(
        """
        This application implements tensor reconstruction and visualization
        of nonlinear optical response properties from quantum chemistry outputs.

        ### Core methodology
        - Tensor symmetrization: βᵢⱼₖ = βⱼᵢₖ
        - Directional contraction: β(n) = βᵢⱼₖ nᵢ nⱼ nₖ
        - Rotational mapping on unit sphere

        ### Author scope
        Designed for research and teaching in:
        - Computational Chemistry
        - Molecular Physics
        - Materials Modeling
        """
    )

# =========================
# FOOTER
# =========================
st.divider()

st.markdown(
    """
---
**NLO Tensor Analyzer v1.0**

Developed by the **Institute of Materials Informatics**

🌐 https://www.imi-bd.com
"""
)