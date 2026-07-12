import io
import streamlit as st

from tensor_parser import parse_tensor
from gaussian_parser import parse_gaussian_static_beta
from gaussian_dynamic_parser import parse_gaussian_dynamic_beta
from orca_parser import parse_orca_beta
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

    st.title("⚛️ ATANLO: Nonlinear Optical (NLO) Tensor Analyzer")
    st.markdown(
        """
        <p style="font-size: 18px; color: #666666; margin-top: -15px;">
        ATANLO is a <strong>free, open-access online tool</strong> to analyze first hyperpolarizability tensor, 
        developed by <b><a href="https://ustc.ac.bd/fm-fatema-nusrat/" target="_blank" style="color: #0066cc; text-decoration: underline;">Fatema Nusrat</a></b> and 
        <b><a href="https://www.imi-bd.com/people" target="_blank" style="color: #0066cc; text-decoration: underline;">Ali Hossain</a></b> at the 
        <a href="https://www.imi-bd.com" target="_blank" style="color: #0066cc; text-decoration: underline;">Institute of Materials Informatics</a>.<br>
        For inquiries or further correspondence, you are welcome to reach out via email at <a href="mailto:ali.hossain@imi-bd.com" style="color: #0066cc; text-decoration: underline;">ali.hossain@imi-bd.com</a>.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown(
        """
        ### Welcome

        Welcome to the ATANLO: Nonlinear Optical (NLO) Tensor Analyzer. This tool provides interactive analysis and visualization of **first hyperpolarizability (β) tensors** obtained from quantum chemistry calculations.

        It supports:

        - Manual β tensor input
        - Gaussian static output parsing
        - Gaussian frequency-dependent (dynamic) output parsing
        - ORCA output parsing
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
        ### Scientific Capabilities
        <ul style="list-style-type: none; padding-left: 0; margin-bottom: 25px;">
        <li style="margin-bottom: 8px;">⚡ <strong>Tensor Reconstruction:</strong> Seamless parsing from leading quantum chemical suites (Gaussian, ORCA, etc.)</li>
        <li style="margin-bottom: 8px;">📊 <strong>Vector Analysis:</strong> Exact contraction of &beta;-vector and total scalar hyperpolarizability (&beta;<sub>total</sub>)</li>
        <li style="margin-bottom: 8px;">🔄 <strong>Isotropic Averaging:</strong> Comprehensive Hyper-Rayleigh Scattering (HRS) cross-section mapping</li>
        <li style="margin-bottom: 8px;">🔷 <strong>Subspace Projection:</strong> Rigorous direct J=1 (dipolar) and J=3 (octupolar) irreducible decomposition</li>
        <li style="margin-bottom: 8px;">🌐 <strong>Spatial Mapping:</strong> 3D molecular orientation response surfaces and dynamic polar plane curves</li>
        </ul>

        <hr style="border: 0; height: 1px; background: #e0e0e0; margin: 20px 0;">

        ### 📂 Supported Formats
        <ul style="padding-left: 20px; margin-bottom: 25px;">
        <li style="margin-bottom: 6px;">Manual custom tensor coordinates</li>
        <li style="margin-bottom: 6px;">Gaussian static NLO output dataset</li>
        <li style="margin-bottom: 6px;">Gaussian dynamic &beta;(-&omega;; &omega;, 0) output dataset</li>
        <li style="margin-bottom: 6px;">ORCA output dataset</li>
        </ul>

        <hr style="border: 0; height: 1px; background: #e0e0e0; margin: 20px 0;">

        ### 📋 Recommended Workflow
        <ol style="padding-left: 20px; margin-bottom: 25px;">
        <li style="margin-bottom: 6px;">Select the target parser dataset type</li>
        <li style="margin-bottom: 6px;">Paste the raw text block or output data</li>
        <li style="margin-bottom: 6px;">Execute calculations by clicking <strong>Analyze</strong> button</li>
        <li style="margin-bottom: 6px;">Review derived physical macroscopic invariants</li>
        <li style="margin-bottom: 6px;">Visualize tensor properties</li>
        </</ol>

        <hr style="border: 0; height: 1px; background: #e0e0e0; margin: 20px 0;">

        ### Developed For
        <p style="font-style: italic; color: #444444; margin-top: 10px;">
        Computational chemistry &bull; Molecular Physics &bull; Condensed Matter Physics &bull; Materials science
        </p>
        """,
        unsafe_allow_html=True
)

    st.info("Use the sidebar to start analysis.")
    
# ==========================================================
# ANALYZER PAGE
# ==========================================================
if page == "🔬 Analyzer":

    st.title("⚛️ ATANLO: Nonlinear Optical (NLO) Tensor Analyzer")
    st.markdown(
        '<p style="font-size: 20px; color: #666666; margin-top: -15px;">'
        'Interactive visualization of β tensors'
        '</p>',
        unsafe_allow_html=True
    )

    input_mode = st.radio(
        "Select input method",
        (
            "Manual Tensor",
            "Gaussian Static Dataset",
            "Gaussian Dynamic Dataset",
            "ORCA Dataset",
        ),
        horizontal=True,
    )

    input_text = st.text_area(
        "Paste input data here",
        height=300,
    )

    if st.button("Analyze"):

        try:

            if input_mode == "Manual Tensor":
                beta = parse_tensor(input_text)

            elif input_mode == "Gaussian Static Dataset":
                beta = parse_gaussian_static_beta(input_text)

            elif input_mode == "Gaussian Dynamic Dataset":
                beta = parse_gaussian_dynamic_beta(input_text)

            elif input_mode == "ORCA Dataset":
                beta = parse_orca_beta(input_text)

            st.session_state.beta = beta
            st.success("Analysis completed successfully")

        except Exception as e:
            st.error(f"Parsing failed: {e}")

    # =====================================================
    # OUTPUT
    # =====================================================
    if st.session_state.beta is not None:

        beta = st.session_state.beta

        st.header("Calculated Hyperpolarizability (au)")

        if input_mode == "Gaussian Dataset Dynamic":
            beta_vec = beta_vector_dynamic(beta)
            beta_tot = beta_total_dynamic(beta)
        else:
            beta_vec = beta_vector(beta)
            beta_tot = beta_total(beta)

        #Compute HRS quantities
        hrs = compute_hrs_quantities(beta)

        c1, c2, c3, c4 = st.columns(4)

#        c1.metric(r"$\beta_{\text{x}}$", f"{beta_vec[0]:.3f}")
#        c2.metric(r"$\beta_{\text{y}}$", f"{beta_vec[1]:.3f}")
#        c3.metric(r"$\beta_{\text{z}}$", f"{beta_vec[2]:.3f}")
#        c4.metric(r"$\beta_{\text{total}}$", f"{beta_tot:.3f}")

        with c1:
            st.markdown(r"### $\beta_{\text{x}}$")
            st.metric(label="x-component", value=f"{beta_vec[0]:.3f}")

        with c2:
            st.markdown(r"### $\beta_{\text{y}}$")
            st.metric(label="y-component", value=f"{beta_vec[1]:.3f}")

        with c3:
            st.markdown(r"### $\beta_{\text{z}}$")
            st.metric(label="z-component", value=f"{beta_vec[2]:.3f}")

        with c4:
            st.markdown(r"### $\beta_{\text{total}}$")
            st.metric(label="Total", value=f"{beta_tot:.3f}")
            

        st.divider()
        st.header("Hyper-Rayleigh Scattering")

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(r"### $\beta_{\text{HRS}}$")
            st.metric(label="Total HRS Response", value=f"{hrs['beta_HRS']:.4f}")

        with c2:
            st.markdown(r"### $DR$")
            st.metric(label="Depolarization Ratio", value=f"{hrs['DR']:.4f}")

        with c3:
            st.markdown(r"### $\rho$")
            st.metric(label="Nonlinear Anisotropy", value=f"{hrs['rho']:.4f}")

        st.divider()

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(r"### $\langle \beta_{ZZZ}^2 \rangle$")
            st.metric(label="Co-polarized Average", value=f"{hrs['beta_ZZZ2']:.4f}")

        with c2:
            st.markdown(r"### $\langle \beta_{XZZ}^2 \rangle$")
            st.metric(label="Cross-polarized Average", value=f"{hrs['beta_XZZ2']:.4f}")

        st.divider()
        st.header("Exact Dipolar and Octupolar Decomposition") 

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(r"### $|\beta_{J=1}|$")
            st.metric(label="Dipolar Invariant", value=f"{hrs['beta_J1']:.4f}")

        with c2:
            st.markdown(r"### $|\beta_{J=3}|$")
            st.metric(label="Octupolar Invariant", value=f"{hrs['beta_J3']:.4f}")

        st.subheader("Dipolar / Octupolar Contribution")

        st.progress(float(hrs["phi_dipolar"]))

        c1, c2 = st.columns(2)

        c1.metric(
            "Irreducible J=1 Fraction : Dipolar (Squared Weight %)",
            f"{100*hrs['phi_dipolar']:.2f}"
        )

        c2.metric(
            "Irreducible J=3 Fraction : Octupolar (Squared Weight %)",
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

    st.title("⚛️ ATANLO: Nonlinear Optical (NLO) Tensor Analyzer")
    st.markdown(
        '<p style="font-size: 20px; color: #666666; margin-top: -15px;">'
        'About This Tool'
        '</p>',
        unsafe_allow_html=True
    )


#    st.title("About This Tool")
    st.markdown("---")

    st.markdown(
        """
        **ATANLO** (*Analysis of Tensor Attributes for Non-Linear Optics*) is an interactive, open-access 
        informatics platform designed to automate the post-processing, spatial visualization, and 
        rotational invariant analysis of microscopic first hyperpolarizability tensors.
        """
    )

    st.markdown(
        """
        This application implements tensor reconstruction and visualization 
        of nonlinear optical (NLO) response properties directly from quantum chemistry outputs.

        ### 🧠 Core Methodology
        <ul style="list-style-type: none; padding-left: 0; margin-bottom: 25px;">
            <li style="margin-bottom: 10px;">📐 <strong>Tensor Symmetrization:</strong> Accounts for field permutations where &beta;<sub>ijk</sub> = &beta;<sub>jik</sub></li>
            <li style="margin-bottom: 10px;">🎯 <strong>Directional Contraction:</strong> Projects spatial vectors using &beta;(n) = &beta;<sub>ijk</sub> n<sub>i</sub> n<sub>j</sub> n<sub>k</sub></li>
            <li style="margin-bottom: 10px;">🌐 <strong>Rotational Mapping:</strong> Generates dynamic response surfaces on a unit sphere</li>
        </ul>

        <hr style="border: 0; height: 1px; background: #e0e0e0; margin: 20px 0;">

        ### 🎓 Application Scope
        <p style="margin-bottom: 10px;">Designed to accelerate research and enhance teaching in:</p>
        <ul style="padding-left: 20px; margin-bottom: 25px;">
            <li style="margin-bottom: 6px;">Computational Chemistry</li>
            <li style="margin-bottom: 6px;">Molecular Physics</li>
            <li style="margin-bottom: 6px;">Materials Modeling</li>
        </ul>
        """,
        unsafe_allow_html=True
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