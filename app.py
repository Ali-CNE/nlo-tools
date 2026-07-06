import io
import streamlit as st
from gaussian_parser import parse_gaussian_static_beta
from gaussian_dynamic_parser import parse_gaussian_dynamic_beta

def fig_to_png(fig):

    buf = io.BytesIO()

    fig.savefig(
        buf,
        format="png",
        dpi=600,
        bbox_inches="tight"
    )

    buf.seek(0)

    return buf

from parser import parse_tensor
from analysis import (
    compute_surface,
    compute_planes,
    beta_vector,
    beta_total,
    beta_vector_dynamic,
    beta_total_dynamic
)
from plotting import (
    plot_surface,
    plot_polar_planes,
    plot_signed_curves,
)

st.set_page_config(page_title="NLO Analyzer", layout="wide")

st.title("Nonlinear Optical (NLO) Tensor Analyzer")
st.caption("Interactive visualization of β tensors")

# =========================
# SESSION STATE
# =========================
if "beta" not in st.session_state:
    st.session_state.beta = None


# =========================
# INPUT MODE
# =========================

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

# =========================
# ANALYZE BUTTON
# =========================

if st.button("Analyze"):

    try:

        if input_mode == "β Tensor":

            beta = parse_tensor(input_text)

        elif input_mode == "Gaussian Dataset Static":

            beta = parse_gaussian_static_beta(input_text)

        elif input_mode == "Gaussian Dataset Dynamic":

            beta = parse_gaussian_dynamic_beta(input_text)

        st.session_state.beta = beta

        st.success("Analysis completed successfully")

    except Exception as e:

        st.error(f"Parsing failed: {e}")


# =========================
# OUTPUT SECTION
# =========================

if st.session_state.beta is not None:

    beta = st.session_state.beta

    # ----------------------------
    # Hyperpolarizability values
    # ----------------------------
    st.header("Calculated Hyperpolarizability")

    if input_mode == "Gaussian Dataset Dynamic":

        beta_vec = beta_vector_dynamic(beta)
        beta_tot = beta_total_dynamic(beta)

    else:

        beta_vec = beta_vector(beta)
        beta_tot = beta_total(beta)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("βx", f"{beta_vec[0]:.3f}")
    c2.metric("βy", f"{beta_vec[1]:.3f}")
    c3.metric("βz", f"{beta_vec[2]:.3f}")
    c4.metric("βtotal", f"{beta_tot:.3f}")

    # ----------------------------
    # 3D Surface
    # ----------------------------
    st.divider()
    st.header("3D Hyperpolarizability Surface")

    nx, ny, nz, beta_n = compute_surface(beta)

    fig_surface = plot_surface(nx, ny, nz, beta_n)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        st.pyplot(fig_surface, use_container_width=False)
    
    st.download_button(
        "Download Surface (PNG)",
        data=fig_to_png(fig_surface),
        file_name="beta_surface.png",
        mime="image/png",
)

    # ----------------------------
    # Polar Sections
    # ----------------------------
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

    # ----------------------------
    # Signed Curves
    # ----------------------------
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