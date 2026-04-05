import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import io
from datetime import datetime

# =========================================================
# -------------------- PAGE CONFIG ------------------------
# =========================================================
st.set_page_config(
    page_title="Mini Data Prep Studio",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# ------------------------ STYLES -------------------------
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #f5f1e8;
        --panel: #fcfbf7;
        --panel-2: #ffffff;
        --text: #183a36;
        --muted: #5d6c67;
        --line: rgba(24,58,54,0.10);
        --shadow: 0 14px 34px rgba(18, 34, 32, 0.07);
        --green: #1f5c4d;
        --green-2: #2f7a68;
        --green-soft: #e5f1eb;
        --green-soft-2: #eef6f2;
        --blue-soft: #e9eff8;
        --amber-soft: #f8ead9;
        --danger-soft: #f7e5e2;
        --hero: linear-gradient(135deg, #faf7f2 0%, #eef4ef 100%);
        --dark-pill: #163732;
    }

    .stApp {
        background: var(--bg);
        color: var(--text);
    }

    .block-container {
        max-width: 1380px;
        padding-top: 1.2rem;
        padding-bottom: 3rem;
    }

    h1, h2, h3, h4 {
        color: var(--text);
        letter-spacing: -0.02em;
    }

    section[data-testid="stSidebar"] {
        display: none !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* Top area */
    .top-shell {
        background: var(--panel-2);
        border: 1px solid var(--line);
        border-radius: 24px;
        box-shadow: var(--shadow);
        padding: 18px 22px;
        margin-bottom: 14px;
    }

    .top-brand-title {
        font-size: 2rem;
        line-height: 1;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 0.3rem;
    }

    .top-brand-sub {
        color: var(--muted);
        font-size: 0.98rem;
        line-height: 1.45;
    }

    .top-status-bar {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin: 0.55rem 0 1rem 0;
    }

    .top-status-item {
        background: rgba(255,255,255,0.82);
        border: 1px solid var(--line);
        border-radius: 999px;
        padding: 8px 12px;
        color: var(--text);
        font-size: 0.9rem;
        box-shadow: var(--shadow);
    }

    /* Top radio nav */
    div[role="radiogroup"] {
        gap: 10px !important;
        flex-wrap: wrap !important;
    }

    div[role="radiogroup"] label {
        background: var(--panel-2) !important;
        border: 1px solid var(--line) !important;
        border-radius: 999px !important;
        padding: 10px 16px !important;
        color: var(--text) !important;
        font-weight: 700 !important;
        box-shadow: var(--shadow);
    }

    div[role="radiogroup"] label p {
        color: var(--text) !important;
        font-weight: 700 !important;
    }

    div[role="radiogroup"] label:has(input:checked) {
        background: var(--dark-pill) !important;
        border-color: var(--dark-pill) !important;
    }

    div[role="radiogroup"] label:has(input:checked) p {
        color: #ffffff !important;
    }

    /* Cards */
    .hero-wrap {
        background: var(--hero);
        border: 1px solid var(--line);
        border-radius: 30px;
        box-shadow: var(--shadow);
        padding: 36px 34px;
        margin-bottom: 18px;
    }

    .hero-title {
        font-size: 3.2rem;
        line-height: 0.98;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 12px;
        max-width: 760px;
    }

    .hero-sub {
        font-size: 1.05rem;
        color: var(--muted);
        line-height: 1.7;
        max-width: 780px;
        margin-bottom: 14px;
    }

    .hero-mini-row {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 14px;
    }

    .hero-mini-chip {
        background: rgba(255,255,255,0.82);
        border: 1px solid var(--line);
        border-radius: 999px;
        color: var(--text);
        font-size: 0.9rem;
        font-weight: 600;
        padding: 9px 12px;
    }

    .soft-card {
        background: rgba(255,255,255,0.9);
        border: 1px solid var(--line);
        border-radius: 26px;
        box-shadow: var(--shadow);
        padding: 20px;
        margin-bottom: 16px;
    }

    .mini-kpi-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-top: 12px;
    }

    .mini-kpi {
        background: rgba(255,255,255,0.96);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 16px;
        min-height: 94px;
    }

    .mini-kpi .label {
        color: var(--muted);
        font-size: 0.82rem;
        margin-bottom: 8px;
    }

    .mini-kpi .value {
        color: var(--text);
        font-size: 1.7rem;
        font-weight: 800;
        line-height: 1;
    }

    .mini-kpi .hint {
        color: var(--muted);
        font-size: 0.8rem;
        margin-top: 7px;
        line-height: 1.45;
    }

    .section-card {
        background: var(--panel-2);
        border: 1px solid var(--line);
        border-radius: 26px;
        box-shadow: var(--shadow);
        padding: 22px 22px 18px 22px;
        margin-bottom: 18px;
    }

    .section-title {
        font-size: 1.95rem;
        line-height: 1.08;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 6px;
    }

    .section-sub {
        color: var(--muted);
        font-size: 0.97rem;
        line-height: 1.6;
        margin-bottom: 4px;
        max-width: 920px;
    }

    .small-overline {
        display: inline-block;
        margin-bottom: 8px;
        padding: 6px 10px;
        border-radius: 999px;
        background: var(--green-soft);
        color: var(--green);
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.01em;
    }

    .kpi-card {
        background: #ffffff;
        border-radius: 24px;
        border: 1px solid var(--line);
        box-shadow: var(--shadow);
        padding: 22px 18px;
        min-height: 122px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .kpi-card.warn {
        background: var(--amber-soft);
        border-color: rgba(191,123,48,0.18);
    }

    .kpi-card.danger {
        background: var(--danger-soft);
        border-color: rgba(187,91,82,0.18);
    }

    .kpi-card.info {
        background: var(--blue-soft);
        border-color: rgba(71,111,149,0.18);
    }

    .kpi-value {
        font-size: 2.2rem;
        font-weight: 800;
        color: var(--text);
        line-height: 1;
    }

    .kpi-label {
        margin-top: 8px;
        color: var(--muted);
        font-size: 0.92rem;
    }

    .kpi-desc {
        margin-top: 10px;
        font-size: 0.8rem;
        color: var(--muted);
        line-height: 1.45;
    }

    .action-card {
        background: #ffffff;
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 16px;
        box-shadow: var(--shadow);
        min-height: 116px;
        margin-bottom: 12px;
    }

    .action-card-title {
        font-weight: 800;
        color: var(--text);
        font-size: 1rem;
        margin-bottom: 6px;
    }

    .action-card-body {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.55;
    }

    .guide-box {
        background: var(--green-soft-2);
        border: 1px solid rgba(31,92,77,0.10);
        border-left: 5px solid var(--green);
        color: var(--text);
        padding: 15px 16px;
        border-radius: 18px;
        margin-bottom: 12px;
        line-height: 1.55;
    }

    .warn-box {
        background: var(--amber-soft);
        border: 1px solid rgba(191,123,48,0.14);
        border-left: 5px solid #bf7b30;
        color: var(--text);
        padding: 15px 16px;
        border-radius: 18px;
        margin-bottom: 12px;
        line-height: 1.55;
    }

    .danger-box {
        background: var(--danger-soft);
        border: 1px solid rgba(187,91,82,0.14);
        border-left: 5px solid #bb5b52;
        color: var(--text);
        padding: 15px 16px;
        border-radius: 18px;
        margin-bottom: 12px;
        line-height: 1.55;
    }

    .workflow-step {
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 16px;
        box-shadow: var(--shadow);
        min-height: 120px;
    }

    .workflow-step .step-no {
        color: var(--green);
        font-size: 0.82rem;
        font-weight: 800;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .workflow-step .step-title {
        color: var(--text);
        font-size: 1rem;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .workflow-step .step-body {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.5;
    }

    .chart-help {
        background: #f8f6f1;
        border: 1px solid var(--line);
        padding: 12px 14px;
        border-radius: 16px;
        color: var(--muted);
        margin-bottom: 12px;
        font-size: 0.93rem;
        line-height: 1.55;
    }

    .export-card {
        background: #fff;
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 18px;
        box-shadow: var(--shadow);
        min-height: 150px;
    }

    .export-title {
        font-size: 1rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: 6px;
    }

    .export-sub {
        color: var(--muted);
        font-size: 0.9rem;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .subtle-note {
        color: var(--muted);
        font-size: 0.92rem;
        line-height: 1.5;
        margin-top: 6px;
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input,
    .stTextArea textarea {
        border-radius: 14px !important;
        border: 1px solid rgba(23,58,54,0.10) !important;
        background: #fff !important;
        color: var(--text) !important;
    }

    .stTextArea textarea {
        min-height: 120px;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #9aa6a1 !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 14px !important;
        border: 1px solid rgba(23,58,54,0.10) !important;
        min-height: 44px;
        background: #fff !important;
        color: var(--text) !important;
    }

    div[data-baseweb="select"] span {
        color: var(--text) !important;
    }

    .stCheckbox label,
    .stRadio label,
    .stNumberInput label,
    .stTextInput label,
    .stSelectbox label,
    .stMultiSelect label,
    .stTextArea label,
    .stSlider label {
        color: var(--text) !important;
        font-weight: 600 !important;
    }

    .stSlider [role="slider"] {
        background: var(--green) !important;
        border: none !important;
    }

    .stSlider span {
        color: var(--text) !important;
    }

    .stButton button,
    .stDownloadButton button {
        background: var(--green) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        min-height: 44px !important;
        font-weight: 700 !important;
        box-shadow: 0 8px 24px rgba(31,92,77,0.18);
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        background: #17493f !important;
    }

    /* File uploader */
    div[data-testid="stFileUploader"] section {
        background: #1d2029 !important;
        border-radius: 18px !important;
        border: 1px solid rgba(255,255,255,0.08) !important;
    }

    div[data-testid="stFileUploader"] small,
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] p {
        color: #f4f6f8 !important;
    }

    div[data-testid="stFileUploader"] button {
        background: #ffffff !important;
        color: var(--text) !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }

    .stTabs [data-baseweb="tab"] {
        background: #fff;
        color: var(--text) !important;
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 8px 14px;
        margin-right: 6px;
        font-weight: 700;
    }

    .stTabs [aria-selected="true"] {
        background: var(--green-soft) !important;
        color: var(--text) !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid var(--line);
    }

    div[data-testid="stExpander"] {
        border-radius: 18px !important;
        overflow: hidden;
        border: 1px solid var(--line);
        background: #fff;
        margin-bottom: 12px;
    }

    .stAlert {
        border-radius: 16px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# -------------------- SESSION STATE ----------------------
# =========================================================
def init_state():
    defaults = {
        "original_df": None,
        "working_df": None,
        "history": [],
        "transformation_log": [],
        "validation_results": pd.DataFrame(),
        "loaded_filename": None,
        "page_nav": "Upload & Overview",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# =========================================================
# ---------------------- UTILITIES ------------------------
# =========================================================
@st.cache_data(show_spinner=False)
def load_data(uploaded_file, extension: str) -> pd.DataFrame:
    if extension == "csv":
        tried = []
        for enc in ["utf-8", "utf-8-sig", "cp1252", "latin-1"]:
            try:
                uploaded_file.seek(0)
                return pd.read_csv(uploaded_file, encoding=enc)
            except Exception as e:
                tried.append(f"{enc}: {e}")
        uploaded_file.seek(0)
        raise ValueError("Could not read CSV with common encodings. Tried: " + " | ".join(tried))

    if extension == "xlsx":
        return pd.read_excel(uploaded_file)

    if extension == "json":
        return pd.read_json(uploaded_file)

    raise ValueError("Unsupported file type")

@st.cache_data(show_spinner=False)
def build_profile(df: pd.DataFrame) -> dict:
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    dt_cols = df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns.tolist()
    object_cols = df.select_dtypes(include=["object"]).columns.tolist()

    missing_count = df.isna().sum()
    missing_pct = (df.isna().mean() * 100).round(2)
    likely_dates = [c for c in object_cols if "date" in c.lower() or "time" in c.lower()]

    return {
        "shape": df.shape,
        "numeric_cols": numeric_cols,
        "cat_cols": cat_cols,
        "dt_cols": dt_cols,
        "object_cols": object_cols,
        "likely_dates": likely_dates,
        "duplicates": int(df.duplicated().sum()),
        "missing_count": missing_count,
        "missing_pct": missing_pct,
    }

def safe_copy(df):
    return df.copy(deep=True)

def dataset_ready():
    return st.session_state.working_df is not None

def reset_session():
    for k in ["original_df", "working_df", "loaded_filename"]:
        st.session_state[k] = None
    st.session_state.history = []
    st.session_state.transformation_log = []
    st.session_state.validation_results = pd.DataFrame()
    st.session_state.page_nav = "Upload & Overview"

def push_history():
    if dataset_ready():
        st.session_state.history.append(safe_copy(st.session_state.working_df))

def undo_last_step():
    if st.session_state.history:
        st.session_state.working_df = st.session_state.history.pop()
        if st.session_state.transformation_log:
            st.session_state.transformation_log.pop()

def log_step(operation: str, params: dict, affected_columns=None):
    st.session_state.transformation_log.append({
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation": operation,
        "parameters": params,
        "affected_columns": affected_columns or [],
    })

def log_df():
    if not st.session_state.transformation_log:
        return pd.DataFrame(columns=["timestamp", "operation", "parameters", "affected_columns"])
    return pd.DataFrame(st.session_state.transformation_log)

def convert_dirty_numeric(series: pd.Series) -> pd.Series:
    cleaned = (
        series.astype(str)
        .str.replace(",", "", regex=False)
        .str.replace("$", "", regex=False)
        .str.replace("€", "", regex=False)
        .str.replace("£", "", regex=False)
        .str.replace("%", "", regex=False)
        .str.replace(r"[^\d\.\-]", "", regex=True)
    )
    return pd.to_numeric(cleaned, errors="coerce")

def get_outlier_mask_iqr(series: pd.Series):
    s = pd.to_numeric(series, errors="coerce").dropna()
    if s.empty:
        return pd.Series(False, index=series.index), None, None
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    iqr = q3 - q1
    low = q1 - 1.5 * iqr
    high = q3 + 1.5 * iqr
    full_mask = (pd.to_numeric(series, errors="coerce") < low) | (pd.to_numeric(series, errors="coerce") > high)
    full_mask = full_mask.fillna(False)
    return full_mask, low, high

def get_outlier_mask_zscore(series: pd.Series, threshold=3.0):
    s = pd.to_numeric(series, errors="coerce")
    std = s.std()
    if pd.isna(std) or std == 0:
        return pd.Series(False, index=series.index)
    z = (s - s.mean()) / std
    return z.abs().fillna(0) > threshold

def minmax_scale(series: pd.Series):
    s = pd.to_numeric(series, errors="coerce")
    mn, mx = s.min(), s.max()
    if pd.isna(mn) or pd.isna(mx) or mn == mx:
        return s
    return (s - mn) / (mx - mn)

def zscore_scale(series: pd.Series):
    s = pd.to_numeric(series, errors="coerce")
    std = s.std()
    if pd.isna(std) or std == 0:
        return s
    return (s - s.mean()) / std

def try_formula(df: pd.DataFrame, formula: str):
    allowed_funcs = {
        "log": np.log,
        "sqrt": np.sqrt,
        "abs": np.abs,
        "round": np.round,
        "exp": np.exp,
        "df": df,
        "np": np,
    }
    local_vars = {col: df[col] for col in df.columns}
    local_vars.update(allowed_funcs)
    return eval(formula, {"__builtins__": {}}, local_vars)

def recommend_actions(df: pd.DataFrame):
    prof = build_profile(df)
    recommendations = []

    if prof["likely_dates"]:
        recommendations.append(("Parse time fields", f"Convert columns like {', '.join(prof['likely_dates'][:2])} so time-based charts and grouping work correctly."))

    total_missing = int(prof["missing_count"].sum())
    if total_missing > 0:
        recommendations.append(("Handle missing values", f"Review nulls before scaling or charting. This file contains {total_missing} missing cells."))
    if prof["duplicates"] > 0:
        recommendations.append(("Check duplicates", f"Remove repeated rows before export. Current duplicate count: {prof['duplicates']}."))
    if prof["cat_cols"]:
        recommendations.append(("Clean text labels", "Standardize categories to fix whitespace, casing, or inconsistent labels."))
    if prof["numeric_cols"]:
        recommendations.append(("Review numeric spread", "Inspect outliers before scaling to avoid distorted transformations."))

    if not recommendations:
        recommendations.append(("Ready to explore", "This file looks structurally clean, so you can move directly to charts or export."))
    return recommendations[:4]

def download_excel(df, logframe, violations):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="cleaned_data")
        logframe.to_excel(writer, index=False, sheet_name="transformation_log")
        if not violations.empty:
            violations.to_excel(writer, index=False, sheet_name="validation_violations")
    buffer.seek(0)
    return buffer.getvalue()

def get_primary_issue(prof: dict):
    total_missing = int(prof["missing_count"].sum())
    if prof["duplicates"] > 0:
        return "duplicates"
    if total_missing > 0:
        return "missing"
    if prof["likely_dates"]:
        return "dates"
    return "categories"

def apply_case_standardization(series: pd.Series, action: str) -> pd.Series:
    if action == "Trim whitespace":
        return series.astype(str).str.strip()
    if action == "Lowercase":
        return series.astype(str).str.strip().str.lower()
    if action == "Title Case":
        return series.astype(str).str.strip().str.title()
    return series

def kpi_card(label, value, desc="", variant="normal"):
    extra = ""
    if variant == "warn":
        extra = " warn"
    elif variant == "danger":
        extra = " danger"
    elif variant == "info":
        extra = " info"
    return f"""
    <div class="kpi-card{extra}">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-desc">{desc}</div>
    </div>
    """

def stat_chip(title, value, hint):
    return f"""
    <div class="mini-kpi">
        <div class="label">{title}</div>
        <div class="value">{value}</div>
        <div class="hint">{hint}</div>
    </div>
    """

def action_card(title, body):
    return f"""
    <div class="action-card">
        <div class="action-card-title">{title}</div>
        <div class="action-card-body">{body}</div>
    </div>
    """

# =========================================================
# ---------------------- TOP NAV BAR ----------------------
# =========================================================
st.markdown(
    """
    <div class="top-shell">
        <div class="top-brand-title">Mini Data Prep Studio</div>
        <div class="top-brand-sub">Upload, clean, visualize, and export tabular datasets in one place.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

nav_left, nav_right = st.columns([2.8, 1.2])

with nav_left:
    page = st.radio(
        "Navigation",
        ["Upload & Overview", "Cleaning Studio", "Visualization Builder", "Export & Report"],
        horizontal=True,
        key="page_nav",
        label_visibility="collapsed",
    )

with nav_right:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("Reset session", use_container_width=True):
            reset_session()
            st.rerun()
    with b2:
        if dataset_ready():
            if st.button("Undo last step", use_container_width=True):
                undo_last_step()
                st.rerun()

if dataset_ready():
    wdf = st.session_state.working_df
    st.markdown(
        f"""
        <div class="top-status-bar">
            <div class="top-status-item"><b>File:</b> {st.session_state.loaded_filename}</div>
            <div class="top-status-item"><b>Rows:</b> {wdf.shape[0]}</div>
            <div class="top-status-item"><b>Columns:</b> {wdf.shape[1]}</div>
            <div class="top-status-item"><b>Steps logged:</b> {len(st.session_state.transformation_log)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# ------------------ PAGE A: OVERVIEW ---------------------
# =========================================================
if page == "Upload & Overview":
    if dataset_ready():
        df = st.session_state.working_df
        prof = build_profile(df)
        total_missing = int(df.isna().sum().sum())
    else:
        df = None
        prof = None
        total_missing = None

    left, right = st.columns([1.55, 1], gap="large")

    with left:
        st.markdown(
            """
            <div class="hero-wrap">
                <div class="hero-title">Prepare your data with less friction.</div>
                <div class="hero-sub">
                    Start by uploading a file. The app will surface the main issues first,
                    then guide you into cleaning, chart building, and export.
                </div>
                <div class="hero-mini-row">
                    <div class="hero-mini-chip">Upload files</div>
                    <div class="hero-mini-chip">Fix issues</div>
                    <div class="hero-mini-chip">Build charts</div>
                    <div class="hero-mini-chip">Export outputs</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_file = st.file_uploader(
            "Upload a dataset",
            type=["csv", "xlsx", "json"],
            label_visibility="collapsed",
        )

        if uploaded_file is not None:
            ext = uploaded_file.name.split(".")[-1].lower()
            try:
                loaded = load_data(uploaded_file, ext)
                st.session_state.original_df = safe_copy(loaded)
                st.session_state.working_df = safe_copy(loaded)
                st.session_state.history = []
                st.session_state.transformation_log = []
                st.session_state.validation_results = pd.DataFrame()
                st.session_state.loaded_filename = uploaded_file.name
                st.success("Dataset loaded successfully.")
                df = st.session_state.working_df
                prof = build_profile(df)
                total_missing = int(df.isna().sum().sum())
            except Exception as e:
                st.error(f"Could not load file: {e}")

    with right:
        if dataset_ready():
            st.markdown(
                f"""
                <div class="soft-card">
                    <div class="small-overline">Current dataset</div>
                    <div class="section-title">At a glance</div>
                    <div class="section-sub">A quick snapshot before you move into detailed cleaning and chart building.</div>
                    <div class="mini-kpi-grid">
                        {stat_chip("Rows", st.session_state.working_df.shape[0], "Records in working copy")}
                        {stat_chip("Columns", st.session_state.working_df.shape[1], "Fields available")}
                        {stat_chip("Missing", int(st.session_state.working_df.isna().sum().sum()), "Cells requiring attention")}
                        {stat_chip("Duplicates", int(st.session_state.working_df.duplicated().sum()), "Rows to review")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="soft-card">
                    <div class="small-overline">How it works</div>
                    <div class="section-title">A simple workflow</div>
                    <div class="section-sub">
                        Upload a file, review the main indicators, clean what matters,
                        create a few visuals, then export the results.
                    </div>
                    <div class="mini-kpi-grid">
                        <div class="mini-kpi">
                            <div class="label">Supported files</div>
                            <div class="value">3</div>
                            <div class="hint">CSV, XLSX, JSON</div>
                        </div>
                        <div class="mini-kpi">
                            <div class="label">Main pages</div>
                            <div class="value">4</div>
                            <div class="hint">Overview, Cleaning, Charts, Export</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if not dataset_ready():
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">Get started</div>
                <div class="section-title">Upload a file to unlock the full workflow.</div>
                <div class="section-sub">
                    Once a dataset is loaded, you will be able to inspect KPIs, clean issues,
                    build charts, and export the results.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.markdown(kpi_card("Rows", df.shape[0], "Total observations loaded"), unsafe_allow_html=True)
    with k2:
        st.markdown(kpi_card("Columns", df.shape[1], "Fields in working dataset"), unsafe_allow_html=True)
    with k3:
        st.markdown(kpi_card("Missing cells", total_missing, "Review before analysis", "warn" if total_missing > 0 else "normal"), unsafe_allow_html=True)
    with k4:
        variant = "warn" if prof["duplicates"] > 0 else "normal"
        st.markdown(kpi_card("Duplicates", prof["duplicates"], "Rows that may distort results", variant), unsafe_allow_html=True)
    with k5:
        st.markdown(kpi_card("Numeric columns", len(prof["numeric_cols"]), "Useful for charts and scaling", "info"), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Next actions</div>
            <div class="section-title">Recommended workflow</div>
            <div class="section-sub">The app highlights a few sensible next steps based on the current file structure.</div>
        """,
        unsafe_allow_html=True,
    )

    recs = recommend_actions(df)
    c1, c2 = st.columns(2)
    if len(recs) > 0:
        with c1:
            st.markdown(action_card(recs[0][0], recs[0][1]), unsafe_allow_html=True)
    if len(recs) > 1:
        with c2:
            st.markdown(action_card(recs[1][0], recs[1][1]), unsafe_allow_html=True)
    if len(recs) > 2:
        with c1:
            st.markdown(action_card(recs[2][0], recs[2][1]), unsafe_allow_html=True)
    if len(recs) > 3:
        with c2:
            st.markdown(action_card(recs[3][0], recs[3][1]), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    notes = []
    if prof["duplicates"] > 0:
        notes.append("This dataset contains duplicate rows, so duplicate removal is worth reviewing before export.")
    if total_missing == 0:
        notes.append("No missing values were detected, so this file is ready for charting sooner.")
    if len(prof["dt_cols"]) == 0 and prof["likely_dates"]:
        notes.append(f"Time-like fields are present but not parsed yet, such as {', '.join(prof['likely_dates'][:3])}.")
    if notes:
        st.markdown(
            "<div class='guide-box'><b>Quick interpretation</b><br>" +
            "<br>".join([f"• {x}" for x in notes]) +
            "</div>",
            unsafe_allow_html=True,
        )

    prev_col, types_col = st.columns([1.35, 1], gap="large")

    with prev_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">Data preview</div>
                <div class="section-title">Inspect the first rows</div>
                <div class="section-sub">Use the preview to connect the summary above to actual columns and values.</div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(df.head(20), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with types_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">Column profile</div>
                <div class="section-title">Types and missingness</div>
                <div class="section-sub">A compact schema view keeps the page readable without one oversized table.</div>
            """,
            unsafe_allow_html=True,
        )
        dtype_frame = pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str).values,
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean() * 100).round(2).values,
        })
        st.dataframe(dtype_frame, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Statistics</div>
            <div class="section-title">Summary statistics</div>
            <div class="section-sub">Switch between numeric and categorical summaries depending on what you want to inspect.</div>
        """,
        unsafe_allow_html=True,
    )
    t1, t2 = st.tabs(["Numeric summary", "Categorical summary"])
    with t1:
        if prof["numeric_cols"]:
            st.dataframe(df[prof["numeric_cols"]].describe().T, use_container_width=True)
        else:
            st.info("No numeric columns found.")
    with t2:
        if prof["cat_cols"]:
            st.dataframe(df[prof["cat_cols"]].astype(str).describe().T, use_container_width=True)
        else:
            st.info("No categorical columns found.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ---------------- PAGE B: CLEANING STUDIO ----------------
# =========================================================
elif page == "Cleaning Studio":
    if not dataset_ready():
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">No data yet</div>
                <div class="section-title">Upload a dataset first.</div>
                <div class="section-sub">This page becomes a cleaning workspace as soon as a file is loaded.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    df = st.session_state.working_df
    prof = build_profile(df)
    total_missing = int(df.isna().sum().sum())
    primary_issue = get_primary_issue(prof)

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Cleaning workspace</div>
            <div class="section-title">Fix the biggest issues first.</div>
            <div class="section-sub">
                Start with the most obvious structural problems, then move into category cleaning,
                scaling, validation, and review.
            </div>
        """,
        unsafe_allow_html=True,
    )

    a, b, c, d = st.columns(4)
    with a:
        st.markdown(kpi_card("Rows", df.shape[0], "Working observations"), unsafe_allow_html=True)
    with b:
        st.markdown(kpi_card("Columns", df.shape[1], "Current features"), unsafe_allow_html=True)
    with c:
        st.markdown(kpi_card("Missing cells", total_missing, "Nulls to inspect", "warn" if total_missing > 0 else "normal"), unsafe_allow_html=True)
    with d:
        variant = "danger" if prof["duplicates"] > 0 else "normal"
        st.markdown(kpi_card("Duplicate rows", prof["duplicates"], "Potential distortion in summaries", variant), unsafe_allow_html=True)

    if primary_issue == "duplicates":
        st.markdown(
            f"""
            <div class="danger-box">
                <b>Start here:</b> this file contains <b>{prof["duplicates"]}</b> duplicate rows.
                Review or remove them before building charts or exporting.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif primary_issue == "missing":
        st.markdown(
            f"""
            <div class="warn-box">
                <b>Start here:</b> this file contains <b>{total_missing}</b> missing cells.
                Handle nulls before scaling or visualization.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif primary_issue == "dates":
        st.markdown(
            f"""
            <div class="warn-box">
                <b>Start here:</b> convert time-related fields such as <b>{", ".join(prof["likely_dates"][:3])}</b>
                so they become useful for trend analysis.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="guide-box">
                <b>Start here:</b> review text categories and standardize them before moving into charts and export.
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Suggested path</div>
            <div class="section-title">A simple cleaning flow</div>
            <div class="section-sub">Work top-down so each transformation stays easy to understand and explain.</div>
        """,
        unsafe_allow_html=True,
    )

    w1, w2, w3 = st.columns(3)
    with w1:
        st.markdown(
            """
            <div class="workflow-step">
                <div class="step-no">Step 1</div>
                <div class="step-title">Fix structural issues</div>
                <div class="step-body">Review duplicates, missing values, and type problems before deeper transformations.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with w2:
        st.markdown(
            """
            <div class="workflow-step">
                <div class="step-no">Step 2</div>
                <div class="step-title">Prepare variables</div>
                <div class="step-body">Clean categories, inspect outliers, and scale numeric fields only when needed.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with w3:
        st.markdown(
            """
            <div class="workflow-step">
                <div class="step-no">Step 3</div>
                <div class="step-title">Validate and review</div>
                <div class="step-body">Run rules, inspect the transformation log, and export the final outputs.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    exp_missing = primary_issue == "missing"
    exp_dups = primary_issue == "duplicates"
    exp_types = primary_issue == "dates"

    with st.expander("Missing values", expanded=exp_missing):
        st.markdown(
            '<div class="chart-help">Choose one missing-value strategy at a time so the effect of each cleaning step stays clear.</div>',
            unsafe_allow_html=True,
        )

        st.dataframe(pd.DataFrame({
            "column": df.columns,
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean() * 100).round(2).values
        }).sort_values("missing_count", ascending=False), use_container_width=True)

        mv_action = st.selectbox(
            "Choose action",
            [
                "Drop rows with missing values in selected columns",
                "Drop columns above missing threshold",
                "Fill with constant",
                "Fill with mean",
                "Fill with median",
                "Fill with mode / most frequent",
                "Forward fill",
                "Backward fill",
            ],
            key="mv_action_v8"
        )
        mv_cols = st.multiselect("Select columns", df.columns.tolist(), key="mv_cols_v8")
        mv_threshold = st.slider("Missing % threshold", 0, 100, 40, key="mv_thresh_v8")
        mv_constant = st.text_input("Constant fill value", key="mv_const_v8")

        if st.button("Apply missing-value action", key="mv_apply_v8"):
            try:
                push_history()
                new_df = safe_copy(df)
                before_shape = df.shape

                if mv_action == "Drop rows with missing values in selected columns":
                    if not mv_cols:
                        st.error("Select at least one column.")
                    else:
                        new_df = new_df.dropna(subset=mv_cols)

                elif mv_action == "Drop columns above missing threshold":
                    drop_cols = [c for c in new_df.columns if (new_df[c].isna().mean() * 100) > mv_threshold]
                    new_df = new_df.drop(columns=drop_cols)
                    mv_cols = drop_cols

                elif mv_action == "Fill with constant":
                    if not mv_cols:
                        st.error("Select at least one column.")
                    else:
                        for c in mv_cols:
                            new_df[c] = new_df[c].fillna(mv_constant)

                elif mv_action == "Fill with mean":
                    for c in mv_cols:
                        if pd.api.types.is_numeric_dtype(new_df[c]):
                            new_df[c] = new_df[c].fillna(new_df[c].mean())

                elif mv_action == "Fill with median":
                    for c in mv_cols:
                        if pd.api.types.is_numeric_dtype(new_df[c]):
                            new_df[c] = new_df[c].fillna(new_df[c].median())

                elif mv_action == "Fill with mode / most frequent":
                    for c in mv_cols:
                        mode_vals = new_df[c].mode(dropna=True)
                        if len(mode_vals) > 0:
                            new_df[c] = new_df[c].fillna(mode_vals.iloc[0])

                elif mv_action == "Forward fill":
                    if mv_cols:
                        new_df[mv_cols] = new_df[mv_cols].ffill()

                elif mv_action == "Backward fill":
                    if mv_cols:
                        new_df[mv_cols] = new_df[mv_cols].bfill()

                st.session_state.working_df = new_df
                log_step("missing_values", {
                    "action": mv_action,
                    "columns": mv_cols,
                    "threshold": mv_threshold if mv_action == "Drop columns above missing threshold" else None,
                    "constant": mv_constant if mv_action == "Fill with constant" else None,
                    "before_shape": list(before_shape),
                    "after_shape": list(new_df.shape),
                }, mv_cols)
                st.success("Missing-value action applied.")
                st.rerun()
            except Exception as e:
                st.error(f"Action failed: {e}")

    with st.expander("Duplicates", expanded=exp_dups):
        st.markdown(
            '<div class="chart-help">Leave subset columns empty to inspect full-row duplicates. Use subset columns only when you need duplicate checks by key fields.</div>',
            unsafe_allow_html=True,
        )

        dup_cols = st.multiselect("Subset columns for duplicate check", df.columns.tolist(), key="dup_cols_v8")
        keep_opt = st.selectbox("Keep", ["first", "last"], key="dup_keep_v8")

        dup_mask = df.duplicated(subset=dup_cols if dup_cols else None, keep=False)
        dup_table = df[dup_mask]
        st.write(f"Rows in duplicate groups: **{len(dup_table)}**")

        if not dup_table.empty:
            st.dataframe(dup_table.head(100), use_container_width=True)

        if st.button("Remove duplicates", key="dup_apply_v8"):
            push_history()
            before = len(df)
            new_df = df.drop_duplicates(subset=dup_cols if dup_cols else None, keep=keep_opt)
            st.session_state.working_df = new_df
            log_step("duplicates", {
                "subset_columns": dup_cols,
                "keep": keep_opt,
                "rows_removed": before - len(new_df),
            }, dup_cols)
            st.success("Duplicates removed.")
            st.rerun()

    with st.expander("Data types & parsing", expanded=exp_types):
        st.markdown(
            '<div class="chart-help">Convert fields when the detected type is not yet useful for analysis. Date-like text columns are often the first thing to fix.</div>',
            unsafe_allow_html=True,
        )

        if prof["likely_dates"]:
            st.markdown(
                "<div class='warn-box'><b>Likely time fields:</b> " + ", ".join(prof["likely_dates"]) + "</div>",
                unsafe_allow_html=True,
            )

        dtype_col = st.selectbox("Column to convert", df.columns.tolist(), key="dtype_col_v8")
        dtype_target = st.selectbox("Target type", ["numeric", "categorical", "datetime"], key="dtype_target_v8")
        datetime_format = st.text_input("Datetime format (optional)", placeholder="%d-%m-%Y", key="dtype_format_v8")
        clean_num = st.checkbox("Clean dirty numeric strings first", value=True, key="dtype_clean_num_v8")

        if st.button("Apply type conversion", key="dtype_apply_v8"):
            try:
                push_history()
                new_df = safe_copy(df)

                if dtype_target == "numeric":
                    new_df[dtype_col] = convert_dirty_numeric(new_df[dtype_col]) if clean_num else pd.to_numeric(new_df[dtype_col], errors="coerce")
                elif dtype_target == "categorical":
                    new_df[dtype_col] = new_df[dtype_col].astype("category")
                else:
                    if datetime_format.strip():
                        new_df[dtype_col] = pd.to_datetime(new_df[dtype_col], format=datetime_format, errors="coerce")
                    else:
                        new_df[dtype_col] = pd.to_datetime(new_df[dtype_col], errors="coerce", dayfirst=True)

                st.session_state.working_df = new_df
                log_step("type_conversion", {
                    "column": dtype_col,
                    "target_type": dtype_target,
                    "format": datetime_format,
                    "clean_numeric_first": clean_num,
                }, [dtype_col])
                st.success("Type conversion applied.")
                st.rerun()
            except Exception as e:
                st.error(f"Conversion failed: {e}")

    with st.expander("Categorical data tools", expanded=(primary_issue == "categories")):
        st.markdown(
            '<div class="chart-help">Standardize text labels, group rare categories, or encode fields for more consistent analysis.</div>',
            unsafe_allow_html=True,
        )

        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        if not cat_cols:
            st.info("No categorical columns found.")
        else:
            std_cols = st.multiselect("Columns to standardize", cat_cols, key="std_cols_v8")
            std_action = st.selectbox("Standardization action", ["None", "Trim whitespace", "Lowercase", "Title Case"], key="std_action_v8")

            map_col = st.selectbox("Column for mapping", [""] + cat_cols, key="map_col_v8")
            mapping_json = st.text_area("Mapping dictionary as JSON", value='{"old": "new"}', key="mapping_json_v8")
            set_other = st.checkbox("Set unmatched values to Other", key="map_set_other_v8")

            rare_col = st.selectbox("Column for rare-category grouping", [""] + cat_cols, key="rare_col_v8")
            rare_threshold = st.number_input("Minimum frequency to keep", min_value=1, value=10, step=1, key="rare_thresh_v8")

            ohe_cols = st.multiselect("One-hot encode columns", cat_cols, key="ohe_cols_v8")

            if std_cols and std_action != "None":
                preview_col = std_cols[0]
                preview_df = pd.DataFrame({
                    "before": df[preview_col].astype(str).head(8),
                    "after_preview": apply_case_standardization(df[preview_col].head(8), std_action).astype(str)
                })
                st.dataframe(preview_df, use_container_width=True)

            if st.button("Apply categorical tools", key="cat_apply_v8"):
                try:
                    push_history()
                    new_df = safe_copy(df)

                    for c in std_cols:
                        new_df[c] = apply_case_standardization(new_df[c], std_action)

                    if map_col:
                        mapping = json.loads(mapping_json)
                        if set_other:
                            new_df[map_col] = new_df[map_col].map(mapping).fillna("Other")
                        else:
                            new_df[map_col] = new_df[map_col].replace(mapping)

                    if rare_col:
                        vc = new_df[rare_col].value_counts(dropna=False)
                        keep_vals = vc[vc >= rare_threshold].index
                        new_df[rare_col] = new_df[rare_col].where(new_df[rare_col].isin(keep_vals), "Other")

                    if ohe_cols:
                        new_df = pd.get_dummies(new_df, columns=ohe_cols, drop_first=False)

                    st.session_state.working_df = new_df
                    log_step("categorical_tools", {
                        "standardize_columns": std_cols,
                        "standardize_action": std_action,
                        "mapping_column": map_col,
                        "rare_group_column": rare_col,
                        "rare_threshold": int(rare_threshold) if rare_col else None,
                        "one_hot_columns": ohe_cols,
                    }, list(set(std_cols + ([map_col] if map_col else []) + ([rare_col] if rare_col else []) + ohe_cols)))
                    st.success("Categorical operations applied.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Categorical tools failed: {e}")

    with st.expander("Numeric cleaning / outliers", expanded=False):
        st.markdown(
            '<div class="chart-help">Inspect unusually large or small values before scaling or charting.</div>',
            unsafe_allow_html=True,
        )

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not num_cols:
            st.info("No numeric columns available.")
        else:
            out_col = st.selectbox("Numeric column", num_cols, key="out_col_v8")
            detect_method = st.selectbox("Detection method", ["IQR", "Z-score"], key="out_method_v8")
            out_action = st.selectbox("Action", ["Do nothing", "Cap / winsorize", "Remove outlier rows"], key="out_action_v8")
            low_q = st.slider("Lower quantile for capping", 0.0, 0.2, 0.01, 0.01, key="low_q_v8")
            high_q = st.slider("Upper quantile for capping", 0.8, 1.0, 0.99, 0.01, key="high_q_v8")
            z_thr = st.number_input("Z-score threshold", min_value=1.0, value=3.0, step=0.5, key="z_thr_v8")

            if detect_method == "IQR":
                mask, low, high = get_outlier_mask_iqr(df[out_col])
                st.info(f"Detected outliers: {int(mask.sum())}" + (f" | Bounds: {low:.2f} to {high:.2f}" if low is not None else ""))
            else:
                mask = get_outlier_mask_zscore(df[out_col], threshold=z_thr)
                st.info(f"Detected outliers: {int(mask.sum())}")

            if st.button("Apply numeric cleaning", key="out_apply_v8"):
                push_history()
                new_df = safe_copy(df)
                series = pd.to_numeric(new_df[out_col], errors="coerce")

                if out_action == "Cap / winsorize":
                    low_val = series.quantile(low_q)
                    high_val = series.quantile(high_q)
                    new_df[out_col] = series.clip(lower=low_val, upper=high_val)
                elif out_action == "Remove outlier rows":
                    new_df = new_df.loc[~mask].copy()

                st.session_state.working_df = new_df
                log_step("numeric_cleaning", {
                    "column": out_col,
                    "method": detect_method,
                    "action": out_action,
                    "detected_outliers": int(mask.sum()),
                }, [out_col])
                st.success("Numeric cleaning applied.")
                st.rerun()

    with st.expander("Normalization / scaling", expanded=False):
        st.markdown(
            '<div class="chart-help">Normalize numeric columns only when comparable scales are important for your analysis.</div>',
            unsafe_allow_html=True,
        )

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        scale_cols = st.multiselect("Numeric columns to scale", num_cols, key="scale_cols_v8")
        scale_method = st.selectbox("Scaling method", ["Min-Max", "Z-score"], key="scale_method_v8")

        if scale_cols:
            st.dataframe(df[scale_cols].describe().T[["mean", "std", "min", "max"]], use_container_width=True)

        if st.button("Apply scaling", key="scale_apply_v8"):
            if not scale_cols:
                st.error("Select at least one numeric column.")
            else:
                push_history()
                new_df = safe_copy(df)
                for c in scale_cols:
                    new_df[c] = minmax_scale(new_df[c]) if scale_method == "Min-Max" else zscore_scale(new_df[c])

                st.session_state.working_df = new_df
                log_step("scaling", {"columns": scale_cols, "method": scale_method}, scale_cols)
                st.success("Scaling applied.")
                st.rerun()

    with st.expander("Column operations", expanded=False):
        st.markdown(
            '<div class="chart-help">Create derived fields, rename columns, or bin numeric values into groups.</div>',
            unsafe_allow_html=True,
        )

        rename_col = st.selectbox("Column to rename", [""] + df.columns.tolist(), key="rename_col_v8")
        rename_new = st.text_input("New name", key="rename_new_v8")

        drop_cols = st.multiselect("Columns to drop", df.columns.tolist(), key="drop_cols_v8")

        new_formula_col = st.text_input("New formula column name", key="new_formula_col_v8")
        formula = st.text_input("Formula", placeholder='df["average_monthly_hours"] / df["number_project"]', key="formula_v8")

        bin_col = st.selectbox("Numeric column to bin", [""] + df.select_dtypes(include=np.number).columns.tolist(), key="bin_col_v8")
        bin_method = st.selectbox("Binning method", ["equal-width", "quantile"], key="bin_method_v8")
        bin_count = st.number_input("Number of bins", min_value=2, max_value=20, value=4, step=1, key="bin_count_v8")
        bin_new_col = st.text_input("Binned column name", value="binned_feature", key="bin_new_col_v8")

        if st.button("Apply column operations", key="col_apply_v8"):
            try:
                push_history()
                new_df = safe_copy(df)

                if rename_col and rename_new.strip():
                    new_df = new_df.rename(columns={rename_col: rename_new.strip()})

                if drop_cols:
                    new_df = new_df.drop(columns=drop_cols)

                if new_formula_col.strip() and formula.strip():
                    new_df[new_formula_col.strip()] = try_formula(new_df, formula)

                if bin_col and bin_new_col.strip():
                    if bin_method == "equal-width":
                        new_df[bin_new_col.strip()] = pd.cut(new_df[bin_col], bins=int(bin_count))
                    else:
                        new_df[bin_new_col.strip()] = pd.qcut(new_df[bin_col], q=int(bin_count), duplicates="drop")

                st.session_state.working_df = new_df
                log_step("column_operations", {
                    "rename": {rename_col: rename_new} if rename_col and rename_new.strip() else None,
                    "drop_columns": drop_cols,
                    "formula_column": new_formula_col if new_formula_col.strip() else None,
                    "formula": formula if formula.strip() else None,
                    "bin_column": bin_col if bin_col else None,
                    "bin_method": bin_method if bin_col else None,
                }, drop_cols + ([rename_col] if rename_col else []) + ([bin_col] if bin_col else []))
                st.success("Column operations applied.")
                st.rerun()
            except Exception as e:
                st.error(f"Column operations failed: {e}")

    with st.expander("Data validation rules", expanded=False):
        st.markdown(
            '<div class="chart-help">Validation rules add a quality-control layer and can produce exportable violation rows.</div>',
            unsafe_allow_html=True,
        )

        rule_type = st.selectbox("Validation rule", ["Numeric range check", "Allowed categories list", "Non-null constraint"], key="rule_type_v8")
        rule_col = st.selectbox("Column", df.columns.tolist(), key="rule_col_v8")
        min_val = st.number_input("Minimum value", value=0.0, key="rule_min_v8")
        max_val = st.number_input("Maximum value", value=100.0, key="rule_max_v8")
        allowed = st.text_input("Allowed categories (comma separated)", key="rule_allowed_v8")

        if st.button("Run validation", key="rule_apply_v8"):
            violations = pd.DataFrame()

            if rule_type == "Numeric range check":
                s = pd.to_numeric(df[rule_col], errors="coerce")
                violations = df[(s < min_val) | (s > max_val) | s.isna()].copy()
                violations["violation_reason"] = f"Outside range [{min_val}, {max_val}] or invalid numeric"
            elif rule_type == "Allowed categories list":
                allowed_vals = [x.strip() for x in allowed.split(",") if x.strip()]
                violations = df[~df[rule_col].isin(allowed_vals)].copy()
                violations["violation_reason"] = f"Value not in allowed set: {allowed_vals}"
            else:
                violations = df[df[rule_col].isna()].copy()
                violations["violation_reason"] = "Null value found in non-null constrained column"

            st.session_state.validation_results = violations
            log_step("validation_rule", {
                "rule_type": rule_type,
                "column": rule_col,
                "violation_count": len(violations),
            }, [rule_col])
            st.success(f"Validation completed. Violations found: {len(violations)}")

        if not st.session_state.validation_results.empty:
            st.dataframe(st.session_state.validation_results, use_container_width=True)

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Transformation log</div>
            <div class="section-title">Recorded steps</div>
            <div class="section-sub">Each applied action is kept here so the workflow stays easy to review and export.</div>
        """,
        unsafe_allow_html=True,
    )
    logs = log_df()
    if logs.empty:
        st.info("No transformations yet. Apply one cleaning step and it will be recorded here.")
    else:
        st.dataframe(logs, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ----------------- PAGE C: VISUALIZATION -----------------
# =========================================================
elif page == "Visualization Builder":
    if not dataset_ready():
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">No data yet</div>
                <div class="section-title">Upload a dataset first.</div>
                <div class="section-sub">This page becomes active once a working dataset is available.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    df = st.session_state.working_df.copy()
    all_cols = df.columns.tolist()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    dt_cols = df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns.tolist()

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Visualization</div>
            <div class="section-title">Build charts from the current working data.</div>
            <div class="section-sub">Apply optional filters, choose a chart, then review the live chart and filtered data preview.</div>
        """,
        unsafe_allow_html=True,
    )

    top1, top2, top3, top4 = st.columns(4)
    with top1:
        st.markdown(kpi_card("Rows in working set", df.shape[0], "After current cleaning steps"), unsafe_allow_html=True)
    with top2:
        st.markdown(kpi_card("Numeric fields", len(num_cols), "Available for axes and distributions", "info"), unsafe_allow_html=True)
    with top3:
        st.markdown(kpi_card("Category fields", len(cat_cols), "Useful for grouping and bars", "info"), unsafe_allow_html=True)
    with top4:
        st.markdown(kpi_card("Logged steps", len(st.session_state.transformation_log), "Current workflow depth"), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    control_col, chart_col = st.columns([0.9, 1.1], gap="large")

    with control_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">Controls</div>
                <div class="section-title">Filters and chart settings</div>
                <div class="section-sub">Only use the fields that matter for the chart you want to build.</div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="chart-help">
                Suggested flow: apply optional filters, choose a chart type, fill the relevant controls, then review the preview table below the chart.
            </div>
            """,
            unsafe_allow_html=True,
        )

        filter_cat_col = st.selectbox("Category filter", ["None"] + cat_cols, key="viz_f_cat_v8")
        if filter_cat_col != "None":
            options = sorted(df[filter_cat_col].dropna().astype(str).unique().tolist())
            selected = st.multiselect("Values", options, default=options[:min(len(options), 5)], key="viz_f_cat_values_v8")
            if selected:
                df = df[df[filter_cat_col].astype(str).isin(selected)]

        filter_num_col = st.selectbox("Numeric range filter", ["None"] + num_cols, key="viz_f_num_v8")
        if filter_num_col != "None" and not df.empty:
            lo = float(df[filter_num_col].min())
            hi = float(df[filter_num_col].max())
            if lo == hi:
                st.info("Selected numeric filter column has only one value.")
            else:
                rng = st.slider("Range", lo, hi, (lo, hi), key="viz_f_num_rng_v8")
                df = df[(df[filter_num_col] >= rng[0]) & (df[filter_num_col] <= rng[1])]

        plot_type = st.selectbox(
            "Plot type",
            ["Histogram", "Box Plot", "Scatter Plot", "Line Chart", "Bar Chart", "Correlation Heatmap"],
            key="plot_type_v8"
        )

        fig, ax = plt.subplots(figsize=(11, 5.8))

        try:
            if plot_type == "Histogram":
                st.markdown('<div class="chart-help">Use a histogram when you want to understand the distribution of a numeric variable.</div>', unsafe_allow_html=True)
                hist_x = st.selectbox("Numeric X column", num_cols, key="hist_x_v8")
                bins = st.slider("Bins", 5, 60, 25, key="hist_bins_v8")

                ax.hist(df[hist_x].dropna(), bins=bins)
                ax.set_title(f"Distribution of {hist_x}")
                ax.set_xlabel(hist_x)
                ax.set_ylabel("Frequency")

            elif plot_type == "Box Plot":
                st.markdown('<div class="chart-help">Use a box plot to compare spread, median, and possible outliers.</div>', unsafe_allow_html=True)
                bp_y = st.selectbox("Numeric Y column", num_cols, key="box_y_v8")
                bp_x = st.selectbox("Optional category grouping", ["None"] + cat_cols, key="box_x_v8")

                if bp_x == "None":
                    ax.boxplot(df[bp_y].dropna())
                    ax.set_title(f"Box plot of {bp_y}")
                    ax.set_ylabel(bp_y)
                else:
                    grouped = [grp[bp_y].dropna().values for _, grp in df.groupby(bp_x)]
                    labels = [str(x) for x in df.groupby(bp_x).groups.keys()]
                    ax.boxplot(grouped, tick_labels=labels)
                    plt.xticks(rotation=45, ha="right")
                    ax.set_title(f"{bp_y} by {bp_x}")
                    ax.set_xlabel(bp_x)
                    ax.set_ylabel(bp_y)

            elif plot_type == "Scatter Plot":
                st.markdown('<div class="chart-help">Use a scatter plot to explore the relationship between two numeric variables.</div>', unsafe_allow_html=True)
                sc_x = st.selectbox("Numeric X column", num_cols, key="sc_x_v8")
                sc_y = st.selectbox("Numeric Y column", num_cols, key="sc_y_v8")
                sc_group = st.selectbox("Optional color group", ["None"] + cat_cols, key="sc_group_v8")

                if sc_group == "None":
                    ax.scatter(df[sc_x], df[sc_y], alpha=0.35, s=28)
                else:
                    groups = list(df.groupby(sc_group))
                    for name, group in groups:
                        ax.scatter(group[sc_x], group[sc_y], label=str(name), alpha=0.35, s=28)
                    ax.legend()

                ax.set_title(f"{sc_y} vs {sc_x}")
                ax.set_xlabel(sc_x)
                ax.set_ylabel(sc_y)

            elif plot_type == "Line Chart":
                st.markdown('<div class="chart-help">Use a line chart for trends over time. Month or year aggregation is usually easier to read than daily lines.</div>', unsafe_allow_html=True)
                usable_time = dt_cols + [c for c in all_cols if c not in dt_cols and ("date" in c.lower() or "time" in c.lower())]
                if not usable_time:
                    st.info("No time-like columns are available for a line chart.")
                else:
                    line_x = st.selectbox("Time column", usable_time, key="line_x_v8")
                    line_y = st.selectbox("Numeric Y column", num_cols, key="line_y_v8")
                    line_group = st.selectbox("Optional group", ["None"] + cat_cols, key="line_group_v8")
                    line_agg = st.selectbox("Aggregation", ["mean", "sum", "count", "median"], key="line_agg_v8")
                    time_grain = st.selectbox("Time granularity", ["Month", "Year", "Week", "Day"], index=0, key="line_grain_v8")

                    temp = df.copy()
                    temp[line_x] = pd.to_datetime(temp[line_x], errors="coerce")
                    temp = temp.dropna(subset=[line_x])

                    freq_map = {"Day": "D", "Week": "W", "Month": "ME", "Year": "YE"}
                    freq = freq_map[time_grain]

                    if line_group == "None":
                        grouped = temp.groupby(pd.Grouper(key=line_x, freq=freq))[line_y].agg(line_agg).reset_index()
                        grouped = grouped.dropna(subset=[line_y])
                        ax.plot(grouped[line_x], grouped[line_y], marker="o")
                    else:
                        grouped = temp.groupby([pd.Grouper(key=line_x, freq=freq), line_group])[line_y].agg(line_agg).reset_index()
                        grouped = grouped.dropna(subset=[line_y])
                        for name, g in grouped.groupby(line_group):
                            ax.plot(g[line_x], g[line_y], marker="o", label=str(name))
                        ax.legend()

                    ax.set_title(f"{line_agg.title()} {line_y} over {line_x} ({time_grain.lower()}ly)")
                    ax.set_xlabel(line_x)
                    ax.set_ylabel(f"{line_agg} of {line_y}")

            elif plot_type == "Bar Chart":
                st.markdown('<div class="chart-help">Use a bar chart to compare categories by count or by aggregated numeric value.</div>', unsafe_allow_html=True)
                if not cat_cols:
                    st.info("No categorical columns available for a bar chart.")
                else:
                    bar_top_n = st.number_input("Top N categories", min_value=3, max_value=50, value=10, step=1, key="viz_topn_v8")
                    bar_x = st.selectbox("Category X column", cat_cols, key="bar_x_v8")
                    bar_mode = st.selectbox("Bar mode", ["Count", "Aggregate numeric value"], key="bar_mode_v8")
                    orientation = st.selectbox("Orientation", ["Vertical", "Horizontal"], key="bar_orient_v8")

                    if bar_mode == "Count":
                        series = df[bar_x].astype(str).value_counts().head(int(bar_top_n))
                        labels = series.index.astype(str)
                        values = series.values
                        y_label = "Count"
                        title = f"Top {int(bar_top_n)} categories in {bar_x}"
                    else:
                        bar_y = st.selectbox("Numeric Y column", num_cols, key="bar_y_v8")
                        bar_agg = st.selectbox("Aggregation", ["sum", "mean", "median"], key="bar_agg_v8")
                        grouped = df.groupby(bar_x)[bar_y].agg(bar_agg).sort_values(ascending=False).head(int(bar_top_n))
                        labels = grouped.index.astype(str)
                        values = grouped.values
                        y_label = f"{bar_agg} of {bar_y}"
                        title = f"{bar_agg.title()} {bar_y} by {bar_x}"

                    if orientation == "Vertical":
                        ax.bar(labels, values)
                        plt.xticks(rotation=45, ha="right")
                        ax.set_xlabel(bar_x)
                        ax.set_ylabel(y_label)
                    else:
                        ax.barh(labels, values)
                        ax.set_ylabel(bar_x)
                        ax.set_xlabel(y_label)

                    ax.set_title(title)

            elif plot_type == "Correlation Heatmap":
                st.markdown('<div class="chart-help">Use a correlation heatmap to quickly see which numeric variables move together most strongly.</div>', unsafe_allow_html=True)
                corr_df = df[num_cols]
                if corr_df.shape[1] < 2:
                    st.info("Need at least two numeric columns.")
                else:
                    corr = corr_df.corr(numeric_only=True)
                    im = ax.imshow(corr, aspect="auto")
                    ax.set_xticks(range(len(corr.columns)))
                    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
                    ax.set_yticks(range(len(corr.columns)))
                    ax.set_yticklabels(corr.columns)
                    ax.set_title("Correlation matrix")
                    fig.colorbar(im)

        except Exception as e:
            st.error(f"Could not configure chart: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    with chart_col:
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">Live preview</div>
                <div class="section-title">Chart output</div>
                <div class="section-sub">The chart stays on the right while settings and filters remain on the left.</div>
            """,
            unsafe_allow_html=True,
        )
        try:
            st.pyplot(fig)
            if plot_type == "Histogram":
                st.markdown('<div class="subtle-note">This histogram shows how values are distributed after the active cleaning and filtering steps.</div>', unsafe_allow_html=True)
            elif plot_type == "Bar Chart":
                st.markdown('<div class="subtle-note">This chart is useful for presentation screenshots because category differences are easy to read.</div>', unsafe_allow_html=True)
            elif plot_type == "Line Chart":
                st.markdown('<div class="subtle-note">This line chart is useful for trend storytelling, especially when monthly aggregation is used.</div>', unsafe_allow_html=True)
            elif plot_type == "Scatter Plot":
                st.markdown('<div class="subtle-note">Scatter plots are best when you want to look for relationships rather than clean category comparisons.</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not build chart: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">Filtered data</div>
                <div class="section-title">Preview table</div>
                <div class="section-sub">Keep the filtered rows visible so the chart stays connected to the underlying data.</div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(df.head(50), use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# ---------------- PAGE D: EXPORT / REPORT ----------------
# =========================================================
elif page == "Export & Report":
    if not dataset_ready():
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">No data yet</div>
                <div class="section-title">Upload a dataset first.</div>
                <div class="section-sub">This page becomes a final export dashboard once a working dataset is available.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.stop()

    df = st.session_state.working_df
    logs = log_df()
    violations = st.session_state.validation_results

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Export</div>
            <div class="section-title">Package the final outputs.</div>
            <div class="section-sub">Review the final data, skim the logged steps, then download the files you need.</div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card("Final rows", df.shape[0], "Records in final working data"), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card("Final columns", df.shape[1], "Fields ready for export"), unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card("Logged steps", len(st.session_state.transformation_log), "Transformation history depth", "info"), unsafe_allow_html=True)
    with c4:
        issue_count = len(violations) if not violations.empty else 0
        st.markdown(kpi_card("Validation issues", issue_count, "Rows currently flagged", "warn" if issue_count > 0 else "normal"), unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="guide-box">
            <b>Final check:</b> confirm the preview looks correct, skim the transformation log, then export the formats you need.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Final preview</div>
            <div class="section-title">Working dataset</div>
            <div class="section-sub">A quick review before downloading helps avoid exporting the wrong version by accident.</div>
        """,
        unsafe_allow_html=True,
    )
    st.dataframe(df.head(30), use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Transformation log</div>
            <div class="section-title">Recorded workflow</div>
            <div class="section-sub">Each step remains visible here so the final output is easier to explain in a report or demo.</div>
        """,
        unsafe_allow_html=True,
    )
    if logs.empty:
        st.info("No transformation steps recorded yet.")
    else:
        st.dataframe(logs, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    recipe = {
        "exported_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_file": st.session_state.loaded_filename,
        "steps": st.session_state.transformation_log,
    }

    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source_file": st.session_state.loaded_filename,
        "final_shape": {"rows": int(df.shape[0]), "columns": int(df.shape[1])},
        "column_names": df.columns.tolist(),
        "transformations_applied": st.session_state.transformation_log,
    }

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    recipe_bytes = json.dumps(recipe, indent=2, default=str).encode("utf-8")
    report_bytes = json.dumps(report, indent=2, default=str).encode("utf-8")
    excel_bytes = download_excel(df, logs, violations)

    st.markdown(
        """
        <div class="section-card">
            <div class="small-overline">Downloads</div>
            <div class="section-title">Export files</div>
            <div class="section-sub">Download the cleaned data and the workflow documentation files.</div>
        """,
        unsafe_allow_html=True,
    )

    e1, e2 = st.columns(2, gap="large")
    with e1:
        st.markdown(
            """
            <div class="export-card">
                <div class="export-title">Data exports</div>
                <div class="export-sub">Download the cleaned dataset in practical formats for submission or reuse.</div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button("Download cleaned dataset (CSV)", csv_bytes, "cleaned_dataset.csv", "text/csv", use_container_width=True)
        st.download_button("Download cleaned dataset (Excel)", excel_bytes, "cleaned_dataset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with e2:
        st.markdown(
            """
            <div class="export-card">
                <div class="export-title">Workflow exports</div>
                <div class="export-sub">Download the recipe and the report so the transformation process stays documented.</div>
            """,
            unsafe_allow_html=True,
        )
        st.download_button("Download recipe (JSON)", recipe_bytes, "transformation_recipe.json", "application/json", use_container_width=True)
        st.download_button("Download transformation report (JSON)", report_bytes, "transformation_report.json", "application/json", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    if not violations.empty:
        st.markdown(
            """
            <div class="section-card">
                <div class="small-overline">Validation output</div>
                <div class="section-title">Violation rows</div>
                <div class="section-sub">Keep this section when your workflow needs a separate quality-control output file.</div>
            """,
            unsafe_allow_html=True,
        )
        st.dataframe(violations, use_container_width=True)
        st.download_button(
            "Download violations table (CSV)",
            violations.to_csv(index=False).encode("utf-8"),
            "validation_violations.csv",
            "text/csv",
            use_container_width=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

