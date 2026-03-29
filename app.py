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
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# ------------------------ STYLES -------------------------
# =========================================================
st.markdown(
    """
    <style>
    :root {
        --bg: #0b1220;
        --panel: #111827;
        --panel-2: #0f172a;
        --text: #e5e7eb;
        --muted: #94a3b8;
        --line: rgba(255,255,255,0.08);
        --card-bg: #f8fafc;
        --card-text: #124076;
        --card-sub: #5f6b7a;
        --blue-bg: #eaf3ff;
        --blue-border: #3b82f6;
        --green-bg: #ecfdf5;
        --green-border: #10b981;
        --amber-bg: #fff7ed;
        --amber-border: #f59e0b;
        --danger-bg: #fff1f2;
        --danger-border: #ef4444;
        --dark-text: #17212b;
    }

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    .app-subtitle {
        color: var(--muted);
        font-size: 0.98rem;
        margin-top: -0.15rem;
        margin-bottom: 1rem;
    }

    .page-section {
        margin-top: 0.65rem;
        margin-bottom: 0.45rem;
    }

    .panel {
        background: rgba(255,255,255,0.04);
        border: 1px solid var(--line);
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 12px;
    }

    .metric-box {
        background: var(--card-bg);
        border: 1px solid #dbe2ea;
        border-radius: 18px;
        padding: 16px 12px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.06);
        min-height: 88px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }

    .metric-box.warn {
        background: #fff7ed;
        border-color: #fdba74;
    }

    .metric-box.info {
        background: #eff6ff;
        border-color: #93c5fd;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 700;
        color: var(--card-text);
        line-height: 1.1;
    }

    .metric-label {
        font-size: 14px;
        color: var(--card-sub);
        margin-top: 6px;
    }

    .guide-box {
        background: var(--blue-bg);
        border-left: 4px solid var(--blue-border);
        padding: 11px 13px;
        border-radius: 10px;
        color: var(--dark-text);
        margin-bottom: 10px;
    }
    .guide-box * {
        color: var(--dark-text) !important;
    }

    .good-box {
        background: var(--green-bg);
        border-left: 4px solid var(--green-border);
        padding: 11px 13px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: var(--dark-text);
    }
    .good-box * {
        color: var(--dark-text) !important;
    }

    .warn-box {
        background: var(--amber-bg);
        border-left: 4px solid var(--amber-border);
        padding: 11px 13px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: var(--dark-text);
    }
    .warn-box * {
        color: var(--dark-text) !important;
    }

    .danger-box {
        background: var(--danger-bg);
        border-left: 4px solid var(--danger-border);
        padding: 11px 13px;
        border-radius: 10px;
        margin-bottom: 10px;
        color: var(--dark-text);
    }
    .danger-box * {
        color: var(--dark-text) !important;
    }

    .tiny {
        color: var(--muted);
        font-size: 0.9rem;
    }

    .chart-help {
        background: rgba(255,255,255,0.04);
        border: 1px solid var(--line);
        padding: 10px 12px;
        border-radius: 10px;
        margin-bottom: 12px;
        color: #dbe4ee;
    }

    .priority-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid var(--line);
        border-radius: 14px;
        padding: 12px 13px;
        min-height: 86px;
    }

    .priority-title {
        color: #cbd5e1;
        font-size: 0.87rem;
        margin-bottom: 6px;
    }

    .priority-value {
        font-size: 1.35rem;
        font-weight: 700;
        color: white;
        line-height: 1.1;
    }

    .priority-note {
        color: var(--muted);
        font-size: 0.85rem;
        margin-top: 6px;
    }

    .step-box {
        background: rgba(255,255,255,0.035);
        border: 1px dashed rgba(255,255,255,0.10);
        border-radius: 12px;
        padding: 12px 13px;
        margin-bottom: 10px;
    }

    .step-title {
        color: #f8fafc;
        font-weight: 700;
        margin-bottom: 6px;
    }

    .page-divider {
        height: 1px;
        background: var(--line);
        margin: 0.8rem 0 1rem 0;
    }

    .compact-box {
        padding-top: 8px !important;
        padding-bottom: 8px !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stExpander"] {
        border-radius: 12px !important;
        overflow: hidden;
        margin-bottom: 10px;
    }

    .stButton button {
        border-radius: 10px;
    }

    .stDownloadButton button {
        border-radius: 10px;
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
    }
    local_vars = {col: df[col] for col in df.columns}
    local_vars.update(allowed_funcs)
    return eval(formula, {"__builtins__": {}}, local_vars)

def recommend_actions(df: pd.DataFrame):
    prof = build_profile(df)
    recommendations = []

    if prof["likely_dates"]:
        recommendations.append(f"Parse likely date columns: {', '.join(prof['likely_dates'][:3])}")

    total_missing = int(prof["missing_count"].sum())
    if total_missing > 0:
        recommendations.append(f"Review missing values before scaling or charting ({total_missing} missing cells detected)")
    else:
        recommendations.append("No missing values detected in this file, so null handling may not be needed")

    if prof["duplicates"] > 0:
        recommendations.append(f"Check duplicate rows before exporting ({prof['duplicates']} duplicates detected)")

    if prof["cat_cols"]:
        recommendations.append("Standardize text categories to fix whitespace, casing, or label inconsistencies")

    if prof["numeric_cols"]:
        recommendations.append("Review outliers before scaling numeric columns")

    return recommendations

def download_excel(df, logframe, violations):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="cleaned_data")
        logframe.to_excel(writer, index=False, sheet_name="transformation_log")
        if not violations.empty:
            violations.to_excel(writer, index=False, sheet_name="validation_violations")
    buffer.seek(0)
    return buffer.getvalue()

def style_metric_box(label, value, level="normal"):
    extra = ""
    if level == "warn":
        extra = " warn"
    elif level == "info":
        extra = " info"
    return f"""
        <div class="metric-box{extra}">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{label}</div>
        </div>
    """

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

# =========================================================
# ----------------------- SIDEBAR -------------------------
# =========================================================
with st.sidebar:
    st.title("🧪 Mini Data Prep Studio")
    st.caption("Clean, validate, visualize, and export tabular data.")

    page = st.radio(
        "Navigate",
        ["Upload & Overview", "Cleaning Studio", "Visualization Builder", "Export & Report"],
    )

    st.markdown('<div class="page-divider"></div>', unsafe_allow_html=True)

    if st.button("Reset session", use_container_width=True):
        reset_session()
        st.rerun()

    if dataset_ready():
        wdf = st.session_state.working_df
        st.markdown(
            f"""
            <div class="panel compact-box">
            <div><b>Loaded file:</b> {st.session_state.loaded_filename}</div>
            <div><b>Working shape:</b> {wdf.shape[0]} rows × {wdf.shape[1]} cols</div>
            <div><b>Steps logged:</b> {len(st.session_state.transformation_log)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Undo last step", use_container_width=True):
            undo_last_step()
            st.rerun()

# =========================================================
# ------------------ PAGE A: OVERVIEW ---------------------
# =========================================================
if page == "Upload & Overview":
    st.title("Upload & Overview")
    st.markdown(
        '<div class="app-subtitle">Start by loading a CSV, Excel, or JSON file. This page helps the user understand what is in the dataset before making any changes.</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload a dataset", type=["csv", "xlsx", "json"])

    if uploaded_file is not None:
        ext = uploaded_file.name.split(".")[-1].lower()
        try:
            df = load_data(uploaded_file, ext)
            st.session_state.original_df = safe_copy(df)
            st.session_state.working_df = safe_copy(df)
            st.session_state.history = []
            st.session_state.transformation_log = []
            st.session_state.validation_results = pd.DataFrame()
            st.session_state.loaded_filename = uploaded_file.name
            st.success("Dataset loaded successfully.")
        except Exception as e:
            st.error(f"Could not load file: {e}")
            st.stop()

    if not dataset_ready():
        st.markdown(
            """
            <div class="guide-box">
            <b>What this app is for</b><br>
            This tool is designed as a guided workflow rather than a dashboard gallery:
            upload → inspect → clean → visualize → export.
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.info("Upload a file to unlock profiling, cleaning tools, charts, and export options.")
        st.stop()

    df = st.session_state.working_df
    prof = build_profile(df)
    total_missing = int(df.isna().sum().sum())

    m1, m2, m3, m4, m5 = st.columns(5)
    with m1:
        st.markdown(style_metric_box("Rows", df.shape[0]), unsafe_allow_html=True)
    with m2:
        st.markdown(style_metric_box("Columns", df.shape[1]), unsafe_allow_html=True)
    with m3:
        st.markdown(style_metric_box("Missing Cells", total_missing, "warn" if total_missing > 0 else "normal"), unsafe_allow_html=True)
    with m4:
        st.markdown(style_metric_box("Duplicates", prof["duplicates"], "warn" if prof["duplicates"] > 0 else "normal"), unsafe_allow_html=True)
    with m5:
        st.markdown(style_metric_box("Numeric Columns", len(prof["numeric_cols"]), "info"), unsafe_allow_html=True)

    recs = recommend_actions(df)
    if recs:
        st.markdown("### Recommended next actions")
        rec_text = "<br>".join([f"• {x}" for x in recs])
        st.markdown(f"<div class='good-box'>{rec_text}</div>", unsafe_allow_html=True)

    notes = []
    if prof["duplicates"] > 0:
        notes.append("Duplicate rows are present, so this file is good for demonstrating duplicate removal.")
    if total_missing == 0:
        notes.append("No missing values were detected, so this file is weaker for demonstrating null-handling features.")
    if len(prof["dt_cols"]) == 0 and not prof["likely_dates"]:
        notes.append("No parsed or likely datetime columns were detected yet.")
    elif prof["likely_dates"] and len(prof["dt_cols"]) == 0:
        notes.append(f"Some columns may represent dates or times but are not parsed yet: {', '.join(prof['likely_dates'][:3])}.")
    if notes:
        st.markdown("### Quick interpretation")
        st.markdown(
            "<div class='guide-box'>" + "<br>".join([f"• {x}" for x in notes]) + "</div>",
            unsafe_allow_html=True,
        )

    st.markdown("### Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Columns and Inferred Types")
        dtype_frame = pd.DataFrame({
            "column": df.columns,
            "dtype": df.dtypes.astype(str).values,
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean() * 100).round(2).values,
        })
        st.dataframe(dtype_frame, use_container_width=True)

    with col2:
        st.markdown("### Missing Values by Column")
        miss_frame = pd.DataFrame({
            "column": df.columns,
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean() * 100).round(2).values,
        }).sort_values(["missing_count", "missing_pct"], ascending=False)
        st.dataframe(miss_frame, use_container_width=True)

    st.markdown("### Summary Statistics")
    t1, t2 = st.tabs(["Numeric", "Categorical"])
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

# =========================================================
# ---------------- PAGE B: CLEANING STUDIO ----------------
# =========================================================
elif page == "Cleaning Studio":
    st.title("Cleaning Studio")
    st.markdown(
        '<div class="app-subtitle">Use this page like a step-by-step workshop: first review the biggest issues, then clean the data, then check the log below.</div>',
        unsafe_allow_html=True
    )

    if not dataset_ready():
        st.warning("Upload a dataset first.")
        st.stop()

    df = st.session_state.working_df
    prof = build_profile(df)
    total_missing = int(df.isna().sum().sum())
    primary_issue = get_primary_issue(prof)

    # top metrics
    a, b, c, d = st.columns(4)
    with a:
        st.markdown(style_metric_box("Rows", df.shape[0]), unsafe_allow_html=True)
    with b:
        st.markdown(style_metric_box("Columns", df.shape[1]), unsafe_allow_html=True)
    with c:
        st.markdown(style_metric_box("Missing Cells", total_missing, "warn" if total_missing > 0 else "normal"), unsafe_allow_html=True)
    with d:
        st.markdown(style_metric_box("Duplicates", prof["duplicates"], "warn" if prof["duplicates"] > 0 else "normal"), unsafe_allow_html=True)

    # step-by-step guidance
    st.markdown("### What to do first")
    if primary_issue == "duplicates":
        st.markdown(
            f"""
            <div class="danger-box">
            <b>Start with duplicates</b><br>
            This dataset currently contains <b>{prof["duplicates"]}</b> duplicate rows. Remove or review them first, because duplicates can distort charts, summaries, and exported results.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif primary_issue == "missing":
        st.markdown(
            f"""
            <div class="warn-box">
            <b>Start with missing values</b><br>
            This dataset contains <b>{total_missing}</b> missing cells. Handle missing values before scaling, validation, or chart building.
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif primary_issue == "dates":
        st.markdown(
            f"""
            <div class="warn-box">
            <b>Start with date parsing</b><br>
            Likely date/time columns were detected: <b>{", ".join(prof["likely_dates"][:3])}</b>. Converting them early makes time-based charts and time logic easier later.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="guide-box">
            <b>Start with category standardization</b><br>
            No major duplicates or missing values were detected first, so a good next step is checking categorical columns for label consistency.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # priority diagnostics
    st.markdown("### Priority diagnostics")
    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown(
            f"""
            <div class="priority-card">
                <div class="priority-title">Duplicates</div>
                <div class="priority-value">{prof["duplicates"]}</div>
                <div class="priority-note">Review this first if above zero.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p2:
        st.markdown(
            f"""
            <div class="priority-card">
                <div class="priority-title">Missing cells</div>
                <div class="priority-value">{total_missing}</div>
                <div class="priority-note">Handle before scaling or charts.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p3:
        st.markdown(
            f"""
            <div class="priority-card">
                <div class="priority-title">Likely date columns</div>
                <div class="priority-value">{len(prof["likely_dates"])}</div>
                <div class="priority-note">{", ".join(prof["likely_dates"][:2]) if prof["likely_dates"] else "None detected"}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with p4:
        st.markdown(
            f"""
            <div class="priority-card">
                <div class="priority-title">Categorical columns</div>
                <div class="priority-value">{len(prof["cat_cols"])}</div>
                <div class="priority-note">Useful for standardization and mapping.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Suggested workflow")
    wf1, wf2, wf3 = st.columns(3)
    with wf1:
        st.markdown(
            """
            <div class="step-box">
                <div class="step-title">Step 1 — Clean big issues</div>
                Review duplicates, missing values, and type problems first.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with wf2:
        st.markdown(
            """
            <div class="step-box">
                <div class="step-title">Step 2 — Prepare variables</div>
                Standardize categories, handle outliers, and scale only if needed.
            </div>
            """,
            unsafe_allow_html=True,
        )
    with wf3:
        st.markdown(
            """
            <div class="step-box">
                <div class="step-title">Step 3 — Validate and export</div>
                Run validation rules, then review the transformation log below.
            </div>
            """,
            unsafe_allow_html=True,
        )

    # expander defaults based on detected issues
    exp_missing = primary_issue == "missing"
    exp_dups = primary_issue == "duplicates"
    exp_types = primary_issue == "dates"

    with st.expander("1) Missing Values", expanded=exp_missing):
        st.markdown(
            """
            <div class="chart-help">
            Use this section when the dataset contains null values. Choose one action, apply it, then check how the row or column count changes.
            </div>
            """,
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
            key="mv_action_v4"
        )
        mv_cols = st.multiselect("Select columns", df.columns.tolist(), key="mv_cols_v4")
        mv_threshold = st.slider("Missing % threshold", 0, 100, 40, key="mv_thresh_v4")
        mv_constant = st.text_input("Constant fill value", key="mv_const_v4")

        if st.button("Apply missing-value action", key="mv_apply_v4"):
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

    with st.expander("2) Duplicates", expanded=exp_dups):
        st.markdown(
            """
            <div class="chart-help">
            Use this section to detect and remove repeated rows. Start with full-row duplicates, then optionally test duplicates by selected key columns.
            </div>
            """,
            unsafe_allow_html=True,
        )

        dup_cols = st.multiselect("Subset columns for duplicate check", df.columns.tolist(), key="dup_cols_v4")
        keep_opt = st.selectbox("Keep", ["first", "last"], key="dup_keep_v4")

        dup_mask = df.duplicated(subset=dup_cols if dup_cols else None, keep=False)
        dup_table = df[dup_mask]
        st.write(f"Duplicate rows found: **{len(dup_table)}**")

        if not dup_table.empty:
            st.dataframe(dup_table.head(100), use_container_width=True)

        if st.button("Remove duplicates", key="dup_apply_v4"):
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

    with st.expander("3) Data Types & Parsing", expanded=exp_types):
        st.markdown(
            """
            <div class="chart-help">
            Convert columns when the detected type is not useful yet. Typical example: text dates that should become datetime.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if prof["likely_dates"]:
            st.markdown(
                "<div class='warn-box'><b>Likely date columns detected:</b> "
                + ", ".join(prof["likely_dates"]) +
                "</div>",
                unsafe_allow_html=True,
            )

        dtype_col = st.selectbox("Column to convert", df.columns.tolist(), key="dtype_col_v4")
        dtype_target = st.selectbox("Target type", ["numeric", "categorical", "datetime"], key="dtype_target_v4")
        datetime_format = st.text_input("Datetime format (optional)", placeholder="%d-%m-%Y", key="dtype_format_v4")
        clean_num = st.checkbox("Clean dirty numeric strings first", value=True, key="dtype_clean_num_v4")

        if st.button("Apply type conversion", key="dtype_apply_v4"):
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

    with st.expander("4) Categorical Data Tools", expanded=(primary_issue == "categories")):
        st.markdown(
            """
            <div class="chart-help">
            Use this section to make category labels cleaner and more consistent before grouping or charting.
            </div>
            """,
            unsafe_allow_html=True,
        )

        cat_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

        if not cat_cols:
            st.info("No categorical columns found.")
        else:
            std_cols = st.multiselect("Columns to standardize", cat_cols, key="std_cols_v4")
            std_action = st.selectbox("Standardization action", ["None", "Trim whitespace", "Lowercase", "Title Case"], key="std_action_v4")

            map_col = st.selectbox("Column for mapping", [""] + cat_cols, key="map_col_v4")
            mapping_json = st.text_area("Mapping dictionary as JSON", value='{"old": "new"}', key="mapping_json_v4")
            set_other = st.checkbox("Set unmatched values to 'Other'", key="map_set_other_v4")

            rare_col = st.selectbox("Column for rare-category grouping", [""] + cat_cols, key="rare_col_v4")
            rare_threshold = st.number_input("Minimum frequency to keep", min_value=1, value=10, step=1, key="rare_thresh_v4")

            ohe_cols = st.multiselect("One-hot encode columns", cat_cols, key="ohe_cols_v4")

            if std_cols and std_action != "None":
                preview_col = std_cols[0]
                preview_df = pd.DataFrame({
                    "before": df[preview_col].astype(str).head(8),
                    "after_preview": apply_case_standardization(df[preview_col].head(8), std_action).astype(str)
                })
                st.markdown("**Preview of standardization effect**")
                st.dataframe(preview_df, use_container_width=True)

            if st.button("Apply categorical tools", key="cat_apply_v4"):
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

    with st.expander("5) Numeric Cleaning / Outliers", expanded=False):
        st.markdown(
            """
            <div class="chart-help">
            Detect unusually large or small values, then decide whether to keep them, cap them, or remove the affected rows.
            </div>
            """,
            unsafe_allow_html=True,
        )

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        if not num_cols:
            st.info("No numeric columns available.")
        else:
            out_col = st.selectbox("Numeric column", num_cols, key="out_col_v4")
            detect_method = st.selectbox("Detection method", ["IQR", "Z-score"], key="out_method_v4")
            out_action = st.selectbox("Action", ["Do nothing", "Cap / winsorize", "Remove outlier rows"], key="out_action_v4")
            low_q = st.slider("Lower quantile for capping", 0.0, 0.2, 0.01, 0.01, key="low_q_v4")
            high_q = st.slider("Upper quantile for capping", 0.8, 1.0, 0.99, 0.01, key="high_q_v4")
            z_thr = st.number_input("Z-score threshold", min_value=1.0, value=3.0, step=0.5, key="z_thr_v4")

            if detect_method == "IQR":
                mask, low, high = get_outlier_mask_iqr(df[out_col])
                st.info(f"Detected outliers: {int(mask.sum())}" + (f" | Bounds: {low:.2f} to {high:.2f}" if low is not None else ""))
            else:
                mask = get_outlier_mask_zscore(df[out_col], threshold=z_thr)
                st.info(f"Detected outliers: {int(mask.sum())}")

            if st.button("Apply numeric cleaning", key="out_apply_v4"):
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

    with st.expander("6) Normalization / Scaling", expanded=False):
        st.markdown(
            """
            <div class="chart-help">
            Scale numeric columns only when it helps comparison or modeling. Raw values are often easier to explain in final presentation charts.
            </div>
            """,
            unsafe_allow_html=True,
        )

        num_cols = df.select_dtypes(include=np.number).columns.tolist()
        scale_cols = st.multiselect("Numeric columns to scale", num_cols, key="scale_cols_v4")
        scale_method = st.selectbox("Scaling method", ["Min-Max", "Z-score"], key="scale_method_v4")

        if scale_cols:
            st.markdown("**Before scaling**")
            st.dataframe(df[scale_cols].describe().T[["mean", "std", "min", "max"]], use_container_width=True)

        if st.button("Apply scaling", key="scale_apply_v4"):
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

    with st.expander("7) Column Operations", expanded=False):
        st.markdown(
            """
            <div class="chart-help">
            Use this section to rename columns, drop columns, create derived variables, or bin numeric values into groups.
            </div>
            """,
            unsafe_allow_html=True,
        )

        rename_col = st.selectbox("Column to rename", [""] + df.columns.tolist(), key="rename_col_v4")
        rename_new = st.text_input("New name", key="rename_new_v4")

        drop_cols = st.multiselect("Columns to drop", df.columns.tolist(), key="drop_cols_v4")

        new_formula_col = st.text_input("New formula column name", key="new_formula_col_v4")
        formula = st.text_input("Formula", placeholder="average_monthly_hours / number_project", key="formula_v4")

        bin_col = st.selectbox("Numeric column to bin", [""] + df.select_dtypes(include=np.number).columns.tolist(), key="bin_col_v4")
        bin_method = st.selectbox("Binning method", ["equal-width", "quantile"], key="bin_method_v4")
        bin_count = st.number_input("Number of bins", min_value=2, max_value=20, value=4, step=1, key="bin_count_v4")
        bin_new_col = st.text_input("Binned column name", value="binned_feature", key="bin_new_col_v4")

        if st.button("Apply column operations", key="col_apply_v4"):
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

    with st.expander("8) Data Validation Rules", expanded=False):
        st.markdown(
            """
            <div class="chart-help">
            Validation rules help you find rows that break expected conditions, such as invalid ranges, unexpected categories, or missing required values.
            </div>
            """,
            unsafe_allow_html=True,
        )

        rule_type = st.selectbox("Validation rule", ["Numeric range check", "Allowed categories list", "Non-null constraint"], key="rule_type_v4")
        rule_col = st.selectbox("Column", df.columns.tolist(), key="rule_col_v4")
        min_val = st.number_input("Minimum value", value=0.0, key="rule_min_v4")
        max_val = st.number_input("Maximum value", value=100.0, key="rule_max_v4")
        allowed = st.text_input("Allowed categories (comma separated)", key="rule_allowed_v4")

        if st.button("Run validation", key="rule_apply_v4"):
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
            st.markdown("**Violations table**")
            st.dataframe(st.session_state.validation_results, use_container_width=True)

    st.markdown("### Transformation Log")
    logs = log_df()
    if logs.empty:
        st.info("No transformations yet. Apply one cleaning step and it will be recorded here.")
    else:
        st.dataframe(logs, use_container_width=True)

# =========================================================
# ----------------- PAGE C: VISUALIZATION -----------------
# =========================================================
elif page == "Visualization Builder":
    st.title("Visualization Builder")
    st.markdown(
        '<div class="app-subtitle">Build one chart at a time from the transformed data. First choose the chart type, then fill only the controls that matter for that chart.</div>',
        unsafe_allow_html=True
    )

    if not dataset_ready():
        st.warning("Upload a dataset first.")
        st.stop()

    df = st.session_state.working_df.copy()
    all_cols = df.columns.tolist()
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
    dt_cols = df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns.tolist()

    st.markdown(
        """
        <div class="guide-box">
        Step 1: optionally apply filters.<br>
        Step 2: choose a chart type.<br>
        Step 3: fill the fields shown for that chart only.<br>
        Step 4: review the filtered preview table at the bottom.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Filters")
    f1, f2, f3 = st.columns(3)

    with f1:
        filter_cat_col = st.selectbox("Category filter", ["None"] + cat_cols, key="viz_f_cat_v4")
        if filter_cat_col != "None":
            options = sorted(df[filter_cat_col].dropna().astype(str).unique().tolist())
            selected = st.multiselect("Values", options, default=options[:min(len(options), 5)], key="viz_f_cat_values_v4")
            if selected:
                df = df[df[filter_cat_col].astype(str).isin(selected)]

    with f2:
        filter_num_col = st.selectbox("Numeric range filter", ["None"] + num_cols, key="viz_f_num_v4")
        if filter_num_col != "None" and not df.empty:
            lo = float(df[filter_num_col].min())
            hi = float(df[filter_num_col].max())
            if lo == hi:
                st.info("Selected numeric filter column has only one value.")
            else:
                rng = st.slider("Range", lo, hi, (lo, hi), key="viz_f_num_rng_v4")
                df = df[(df[filter_num_col] >= rng[0]) & (df[filter_num_col] <= rng[1])]

    with f3:
        top_n = st.number_input("Top N for bar chart", min_value=3, max_value=50, value=10, step=1, key="viz_topn_v4")

    st.markdown("### Chart Builder")
    fig, ax = plt.subplots(figsize=(11, 5.8))
    plot_type = st.selectbox(
        "Plot type",
        ["Histogram", "Box Plot", "Scatter Plot", "Line Chart", "Bar Chart", "Correlation Heatmap"],
        key="plot_type_v4"
    )

    try:
        if plot_type == "Histogram":
            st.markdown("<div class='chart-help'>Best for understanding the distribution of one numeric variable.</div>", unsafe_allow_html=True)
            x_col = st.selectbox("Numeric X column", num_cols, key="hist_x_v4")
            bins = st.slider("Bins", 5, 60, 25, key="hist_bins_v4")
            ax.hist(df[x_col].dropna(), bins=bins)
            ax.set_title(f"Distribution of {x_col}")
            ax.set_xlabel(x_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)
            st.caption(f"This histogram shows how values of {x_col} are distributed after the current filters.")

        elif plot_type == "Box Plot":
            st.markdown("<div class='chart-help'>Best for comparing median, spread, and possible outliers across categories.</div>", unsafe_allow_html=True)
            bp_y = st.selectbox("Numeric Y column", num_cols, key="box_y_v4")
            bp_x = st.selectbox("Optional category grouping", ["None"] + cat_cols, key="box_x_v4")

            if bp_x == "None":
                ax.boxplot(df[bp_y].dropna())
                ax.set_title(f"Box Plot of {bp_y}")
                ax.set_ylabel(bp_y)
            else:
                grouped = [grp[bp_y].dropna().values for _, grp in df.groupby(bp_x)]
                labels = [str(x) for x in df.groupby(bp_x).groups.keys()]
                ax.boxplot(grouped, tick_labels=labels)
                plt.xticks(rotation=45, ha="right")
                ax.set_title(f"{bp_y} by {bp_x}")
                ax.set_xlabel(bp_x)
                ax.set_ylabel(bp_y)
            st.pyplot(fig)
            st.caption("Use this to compare spread, median, and possible outliers across groups.")

        elif plot_type == "Scatter Plot":
            st.markdown("<div class='chart-help'>Best for exploring the relationship between two numeric variables.</div>", unsafe_allow_html=True)
            sc_x = st.selectbox("Numeric X column", num_cols, key="sc_x_v4")
            sc_y = st.selectbox("Numeric Y column", num_cols, key="sc_y_v4")
            sc_group = st.selectbox("Optional color group", ["None"] + cat_cols, key="sc_group_v4")

            if sc_group == "None":
                ax.scatter(df[sc_x], df[sc_y], alpha=0.35, s=28)
            else:
                groups = list(df.groupby(sc_group))
                if len(groups) > 8:
                    st.warning("This grouping has many categories, so the scatter plot may become crowded.")
                for name, group in groups:
                    ax.scatter(group[sc_x], group[sc_y], label=str(name), alpha=0.35, s=28)
                ax.legend()
            ax.set_title(f"{sc_y} vs {sc_x}")
            ax.set_xlabel(sc_x)
            ax.set_ylabel(sc_y)
            st.pyplot(fig)
            st.caption("Scatter plots work best when overlap is not too heavy and when groups are limited.")

        elif plot_type == "Line Chart":
            st.markdown("<div class='chart-help'>Best for trends over time. Monthly or yearly aggregation is often easier to read than daily lines.</div>", unsafe_allow_html=True)
            usable_time = dt_cols + [c for c in all_cols if c not in dt_cols and ("date" in c.lower() or "time" in c.lower())]
            if not usable_time:
                st.info("No time-like columns are available for a line chart.")
            else:
                line_x = st.selectbox("Time column", usable_time, key="line_x_v4")
                line_y = st.selectbox("Numeric Y column", num_cols, key="line_y_v4")
                line_group = st.selectbox("Optional group", ["None"] + cat_cols, key="line_group_v4")
                line_agg = st.selectbox("Aggregation", ["mean", "sum", "count", "median"], key="line_agg_v4")
                time_grain = st.selectbox("Time granularity", ["Month", "Year", "Week", "Day"], index=0, key="line_grain_v4")

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
                st.pyplot(fig)
                st.caption("For sparse dates, monthly or yearly aggregation usually produces a more readable chart than daily lines.")

        elif plot_type == "Bar Chart":
            st.markdown("<div class='chart-help'>Best for comparing categories by count or aggregated numeric value.</div>", unsafe_allow_html=True)
            if not cat_cols:
                st.info("No categorical columns available for a bar chart.")
            else:
                bar_x = st.selectbox("Category X column", cat_cols, key="bar_x_v4")
                bar_mode = st.selectbox("Bar mode", ["Count", "Aggregate numeric value"], key="bar_mode_v4")
                orientation = st.selectbox("Orientation", ["Vertical", "Horizontal"], key="bar_orient_v4")

                if bar_mode == "Count":
                    series = df[bar_x].astype(str).value_counts().head(int(top_n))
                    labels = series.index.astype(str)
                    values = series.values
                    y_label = "Count"
                    title = f"Top {int(top_n)} categories in {bar_x}"
                else:
                    bar_y = st.selectbox("Numeric Y column", num_cols, key="bar_y_v4")
                    bar_agg = st.selectbox("Aggregation", ["sum", "mean", "median"], key="bar_agg_v4")
                    grouped = df.groupby(bar_x)[bar_y].agg(bar_agg).sort_values(ascending=False).head(int(top_n))
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
                st.pyplot(fig)
                st.caption("Horizontal bars are often easier to read when category names are long.")

        elif plot_type == "Correlation Heatmap":
            st.markdown("<div class='chart-help'>Best for showing which numeric variables move together most strongly.</div>", unsafe_allow_html=True)
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
                ax.set_title("Correlation Matrix")
                fig.colorbar(im)
                st.pyplot(fig)
                st.caption("Use the heatmap to inspect which numeric variables move together most strongly.")

    except Exception as e:
        st.error(f"Could not build chart: {e}")

    st.markdown("### Filtered Data Preview")
    st.dataframe(df.head(50), use_container_width=True)

# =========================================================
# ---------------- PAGE D: EXPORT / REPORT ----------------
# =========================================================
elif page == "Export & Report":
    st.title("Export & Report")
    st.markdown(
        '<div class="app-subtitle">Review the final data, inspect the transformation log, then download the cleaned dataset, recipe, and report.</div>',
        unsafe_allow_html=True
    )

    if not dataset_ready():
        st.warning("Upload a dataset first.")
        st.stop()

    df = st.session_state.working_df
    logs = log_df()
    violations = st.session_state.validation_results

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(style_metric_box("Final Rows", df.shape[0]), unsafe_allow_html=True)
    with c2:
        st.markdown(style_metric_box("Final Columns", df.shape[1]), unsafe_allow_html=True)
    with c3:
        st.markdown(style_metric_box("Logged Steps", len(st.session_state.transformation_log), "info"), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="guide-box">
        Final check: confirm the dataset preview looks correct, skim the transformation log, then choose the export format you need.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### Final Dataset Preview")
    st.dataframe(df.head(30), use_container_width=True)

    st.markdown("### Transformation Log")
    if logs.empty:
        st.info("No transformation steps recorded yet.")
    else:
        st.dataframe(logs, use_container_width=True)

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

    left, right = st.columns(2)
    with left:
        st.download_button("Download cleaned dataset (CSV)", csv_bytes, "cleaned_dataset.csv", "text/csv", use_container_width=True)
        st.download_button("Download recipe (JSON)", recipe_bytes, "transformation_recipe.json", "application/json", use_container_width=True)
    with right:
        st.download_button("Download cleaned dataset (Excel)", excel_bytes, "cleaned_dataset.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
        st.download_button("Download transformation report (JSON)", report_bytes, "transformation_report.json", "application/json", use_container_width=True)

    if not violations.empty:
        st.markdown("### Validation Violations")
        st.dataframe(violations, use_container_width=True)
        st.download_button(
            "Download violations table (CSV)",
            violations.to_csv(index=False).encode("utf-8"),
            "validation_violations.csv",
            "text/csv",
            use_container_width=True,
        )
