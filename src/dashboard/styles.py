"""Global CSS — injected once by app.py, applies to every page."""

GLOBAL_CSS = """
<style>
/* ================================================================
   PlantMind x GotzeEngine  |  Dashboard Stylesheet
   ================================================================ */

/* --- Strip default Streamlit chrome --- */
#MainMenu, footer { visibility: hidden !important; }
header { visibility: hidden !important; height: 0 !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stStatusWidget"] { display: none !important; }

/* --- App base --- */
.stApp { background: #07070f !important; }
.main .block-container {
    padding: 0.5rem 2rem 3rem 2rem !important;
    max-width: 100% !important;
}

/* --- Animated gradient bar at very top --- */
.pm-topbar {
    height: 3px;
    background: linear-gradient(90deg, #4C78A8, #00CC88, #FF4B4B, #4C78A8);
    background-size: 300% 100%;
    animation: pm-gradient 8s linear infinite;
    margin: -0.5rem -2rem 0 -2rem;
}
@keyframes pm-gradient {
    0%   { background-position: 0% 50%; }
    100% { background-position: 300% 50%; }
}

/* --- Sidebar --- */
section[data-testid="stSidebar"] {
    background: #08081a !important;
    border-right: 1px solid #14142a !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.5) !important;
}
section[data-testid="stSidebar"] > div {
    padding: 1rem 0.9rem 2rem !important;
}
section[data-testid="stSidebar"] hr {
    border-color: #14142a !important;
    margin: 10px 0 !important;
}

/* --- Segmented control (top nav) --- */
[data-testid="stSegmentedControl"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 1px solid #14142a !important;
    border-radius: 0 !important;
    padding: 0 !important;
    gap: 0 !important;
    width: auto !important;
    margin-bottom: 1.5rem !important;
}
[data-testid="stSegmentedControl"] > div {
    background: transparent !important;
    border: none !important;
    border-radius: 0 !important;
    gap: 0 !important;
    padding: 0 !important;
}
[data-testid="stSegmentedControl"] button,
[data-testid="stSegmentedControl"] label {
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    border-radius: 0 !important;
    padding: 10px 26px !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #33335a !important;
    transition: color 0.15s, border-color 0.15s !important;
    margin-bottom: -1px !important;
    white-space: nowrap !important;
}
[data-testid="stSegmentedControl"] button:hover,
[data-testid="stSegmentedControl"] label:hover {
    color: #6666aa !important;
    background: rgba(76,120,168,0.05) !important;
}
[data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stSegmentedControl"] label[aria-checked="true"] {
    color: #4C78A8 !important;
    border-bottom-color: #4C78A8 !important;
    background: transparent !important;
}

/* --- st.tabs() internal tabs --- */
[data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #14142a !important;
    gap: 0 !important;
    padding: 0 !important;
}
button[data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    border-radius: 0 !important;
    padding: 10px 20px !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #33335a !important;
    transition: all 0.15s !important;
    margin-bottom: -1px !important;
}
button[data-baseweb="tab"]:hover {
    color: #6666aa !important;
    background: rgba(76,120,168,0.04) !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #4C78A8 !important;
    border-bottom-color: #4C78A8 !important;
    background: transparent !important;
}
[data-testid="stTabPanel"] { padding-top: 1.5rem !important; }
[data-testid="stTabs"] { margin-bottom: 0 !important; }

/* --- Metrics --- */
[data-testid="metric-container"] {
    background: #0d0d1e !important;
    border: 1px solid #14142a !important;
    border-radius: 12px !important;
    padding: 18px 20px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="metric-container"]:hover {
    border-color: #28285a !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3) !important;
}
[data-testid="stMetricLabel"] > div {
    color: #44446a !important;
    font-size: 0.67rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
[data-testid="stMetricValue"] > div {
    color: #fff !important;
    font-size: 2rem !important;
    font-weight: 900 !important;
    letter-spacing: -0.03em !important;
}
[data-testid="stMetricDelta"] > div { font-size: 0.72rem !important; }

/* --- Plotly charts --- */
[data-testid="stPlotlyChart"] > div {
    border: 1px solid #14142a !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    background: #0a0a1c !important;
}

/* --- Buttons --- */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    font-size: 0.85rem !important;
    transition: all 0.15s ease !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #1a3f80, #2455a8) !important;
    border: none !important;
    color: #fff !important;
    box-shadow: 0 2px 10px rgba(36,85,168,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #2350a0, #2f65c8) !important;
    box-shadow: 0 4px 18px rgba(36,85,168,0.5) !important;
    transform: translateY(-1px) !important;
}
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid #22224a !important;
    color: #55558a !important;
}
.stButton > button[kind="secondary"]:hover {
    border-color: #4C78A8 !important;
    color: #4C78A8 !important;
    background: rgba(76,120,168,0.08) !important;
}

/* --- Alert boxes --- */
[data-testid="stAlert"] {
    border-radius: 10px !important;
    border-left-width: 4px !important;
    font-size: 0.87rem !important;
    padding: 14px 16px !important;
}

/* --- Expander --- */
[data-testid="stExpander"] {
    border: 1px solid #14142a !important;
    border-radius: 10px !important;
    background: #0a0a1c !important;
}

/* --- Select / Input --- */
[data-testid="stSelectbox"] > div > div > div {
    background: #0d0d1e !important;
    border-color: #22224a !important;
    border-radius: 8px !important;
    color: #ccccee !important;
}
[data-testid="stTextArea"] textarea {
    background: #0d0d1e !important;
    border-color: #22224a !important;
    border-radius: 8px !important;
    color: #ccccee !important;
    font-size: 0.88rem !important;
}
[data-testid="stTextInput"] input {
    background: #0d0d1e !important;
    border-color: #22224a !important;
    border-radius: 8px !important;
    color: #ccccee !important;
}

/* --- DataFrame / table --- */
[data-testid="stDataFrame"] {
    border: 1px solid #14142a !important;
    border-radius: 10px !important;
    overflow: hidden !important;
}

/* --- Divider --- */
hr { border-color: #14142a !important; }

/* --- Scrollbar --- */
* { scrollbar-width: thin; scrollbar-color: #22224a #07070f; }
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #07070f; }
::-webkit-scrollbar-thumb { background: #22224a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #333360; }

/* --- Page links (horizontal tab nav bar) --- */
[data-testid="stPageLink"] {
    padding: 0 !important;
}
[data-testid="stPageLink"] a {
    display: block !important;
    padding: 10px 20px !important;
    border: none !important;
    border-bottom: 3px solid transparent !important;
    border-radius: 0 !important;
    background: transparent !important;
    color: #33335a !important;
    text-decoration: none !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    transition: color 0.15s, border-color 0.15s !important;
    white-space: nowrap !important;
    margin-bottom: -1px !important;
}
[data-testid="stPageLink"] a:hover {
    color: #7777bb !important;
    background: rgba(76,120,168,0.05) !important;
    text-decoration: none !important;
}
[data-testid="stPageLink"] a[aria-current="page"] {
    color: #4C78A8 !important;
    border-bottom-color: #4C78A8 !important;
    background: transparent !important;
}
[data-testid="stPageLink"] p,
[data-testid="stPageLink"] a p,
[data-testid="stPageLink"] span {
    margin: 0 !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
}

/* Nav bar wrapper */
.pm-nav-bar {
    border-bottom: 1px solid #14142a;
    margin-bottom: 1.5rem;
}
.pm-nav-bar [data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
}

/* ================================================================
   Reusable component classes
   ================================================================ */

/* --- Page header --- */
.pm-page-hdr {
    display: flex; align-items: flex-start;
    justify-content: space-between;
    padding: 1rem 0 1.25rem 0;
    border-bottom: 1px solid #14142a;
    margin-bottom: 1.5rem;
}
.pm-page-title {
    font-size: 1.65rem; font-weight: 900;
    color: #fff; letter-spacing: -0.03em; line-height: 1.1;
}
.pm-page-sub {
    font-size: 0.7rem; color: #333355;
    margin-top: 4px; letter-spacing: 0.02em;
}

/* --- Status badges --- */
.pm-badge {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 4px 10px; border-radius: 20px;
    font-size: 0.62rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase;
}
.pm-badge-crit { background: rgba(255,75,75,0.10); color: #FF4B4B; border: 1px solid rgba(255,75,75,0.2); }
.pm-badge-warn { background: rgba(255,165,0,0.09); color: #FFA500; border: 1px solid rgba(255,165,0,0.2); }
.pm-badge-ok   { background: rgba(0,204,136,0.08); color: #00CC88; border: 1px solid rgba(0,204,136,0.18); }
.pm-badge-blue { background: rgba(76,120,168,0.10); color: #4C78A8; border: 1px solid rgba(76,120,168,0.2); }

/* --- LIVE pulsing dot --- */
@keyframes pm-pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255,75,75,0.5); }
    50%       { box-shadow: 0 0 0 6px rgba(255,75,75,0); }
}
.pm-live-dot {
    display: inline-block; width: 9px; height: 9px;
    background: #FF4B4B; border-radius: 50%;
    animation: pm-pulse 1.4s infinite;
    vertical-align: middle; margin-right: 6px;
}

/* --- Sidebar brand block --- */
.sb-brand { padding: 4px 0 14px 0; }
.sb-brand-name { font-size: 1.1rem; font-weight: 900; color: #fff; letter-spacing: -0.02em; }
.sb-brand-sub  { font-size: 0.6rem; color: #4C78A8; text-transform: uppercase; letter-spacing: 0.16em; font-weight: 700; margin-top: 2px; }
.sb-section {
    font-size: 0.58rem; text-transform: uppercase; letter-spacing: 0.16em;
    color: #252545; font-weight: 800; margin: 16px 0 8px 0;
    padding-bottom: 5px; border-bottom: 1px solid #14142a;
}

/* --- Fleet plant cards --- */
.fp-card {
    background: #0d0d1e; border: 1px solid #14142a;
    border-radius: 14px; padding: 20px; margin-bottom: 4px;
    font-family: inherit;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.fp-card:hover { border-color: #28285a; box-shadow: 0 6px 28px rgba(0,0,0,0.4); }
.fp-card-crit { border-left: 3px solid #FF4B4B !important; }
.fp-card-warn { border-left: 3px solid #FFA500 !important; }
.fp-card-ok   { border-left: 3px solid #00CC88 !important; }
.fp-name { font-size: 1.05rem; font-weight: 800; color: #fff; }
.fp-loc  { font-size: 0.7rem; color: #33335a; margin-top: 2px; }
.fp-hbar-bg { background: #14142a; border-radius: 3px; height: 5px; overflow: hidden; margin: 10px 0 4px 0; }
.fp-hbar-fill { height: 100%; border-radius: 3px; }
.fp-stats { display: flex; gap: 8px; margin: 10px 0; }
.fp-stat { flex: 1; text-align: center; border-radius: 8px; padding: 8px 4px; }
.fp-stat-v { font-size: 1.3rem; font-weight: 900; line-height: 1; }
.fp-stat-l { font-size: 0.58rem; text-transform: uppercase; letter-spacing: 0.08em; margin-top: 3px; }
.fp-footer { display: flex; justify-content: space-between; padding-top: 10px; border-top: 1px solid #14142a; }

/* --- Recommendation card (GotzeEngine) --- */
.rec-card {
    background: linear-gradient(160deg, #0a1628 0%, #0d1520 100%);
    border: 1.5px solid #1e3a6a; border-radius: 14px; padding: 28px;
}
.rec-label { font-size: 0.62rem; color: #4C78A8; text-transform: uppercase; letter-spacing: 0.16em; font-weight: 800; }
.rec-action { font-size: 1.9rem; font-weight: 900; color: #4C78A8; letter-spacing: -0.02em; margin: 8px 0 2px 0; }
.rec-iis { font-size: 3.8rem; font-weight: 900; color: #fff; letter-spacing: -0.04em; line-height: 1; }
.rec-narrative { font-size: 0.8rem; color: #44446a; margin-top: 12px; line-height: 1.6; }

/* --- What-if panels --- */
.wif-bad {
    background: linear-gradient(160deg, #190808 0%, #0f0404 100%);
    border: 1.5px solid rgba(255,75,75,0.3); border-radius: 12px; padding: 22px;
}
.wif-good {
    background: linear-gradient(160deg, #081608 0%, #050e05 100%);
    border: 1.5px solid rgba(0,204,136,0.22); border-radius: 12px; padding: 22px;
}
.wif-title { font-size: 0.65rem; font-weight: 800; letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 14px; }
.wif-total { font-size: 2rem; font-weight: 900; margin: 10px 0; line-height: 1; }
.wif-row { font-size: 0.8rem; color: #505070; padding: 6px 0; border-bottom: 1px solid #1a1a28; }
.wif-row b { color: #c0c0e0; float: right; }

/* --- Cascade chain --- */
.cas-primary { background: rgba(255,75,75,0.07); border-left: 3px solid #FF4B4B; border-radius: 0 8px 8px 0; padding: 12px 16px; margin: 6px 0; }
.cas-node-1  { background: rgba(255,140,0,0.05); border-left: 3px solid #FFA500; border-radius: 0 8px 8px 0; padding: 12px 16px 12px 28px; margin: 4px 0; }
.cas-node-2  { background: rgba(200,50,50,0.04); border-left: 3px solid #cc3333; border-radius: 0 8px 8px 0; padding: 12px 16px 12px 44px; margin: 4px 0; }
.cas-asset { font-weight: 800; font-size: 0.9rem; }
.cas-reason { font-size: 0.75rem; color: #505070; margin-top: 3px; }

/* --- Signal anomaly pills --- */
.sig-pill {
    display: inline-block;
    background: rgba(255,75,75,0.12); color: #FF4B4B;
    border: 1px solid rgba(255,75,75,0.22);
    border-radius: 20px; padding: 4px 12px;
    font-size: 0.72rem; font-weight: 700; margin: 3px 3px;
}

/* --- RL outcome logger --- */
.rl-card {
    background: #0d0d1e; border: 1px solid #14142a;
    border-radius: 12px; padding: 22px; margin-bottom: 12px;
}
.rl-card-title { font-size: 0.72rem; font-weight: 800; color: #4C78A8; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 12px; }

/* --- KPI block (custom HTML alternative to st.metric) --- */
.kpi-block {
    background: #0d0d1e; border: 1px solid #14142a;
    border-radius: 12px; padding: 18px 16px; text-align: center;
}
.kpi-val { font-size: 2rem; font-weight: 900; line-height: 1.1; }
.kpi-lbl { font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.12em; color: #44446a; margin-top: 5px; }
.kpi-sub { font-size: 0.72rem; margin-top: 6px; }

</style>
"""
