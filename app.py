import streamlit as st
import csv
import os
import datetime
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

st.set_page_config(
    page_title="Smart Expense Analyzer",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323:wght@400&display=swap');

:root {
    --pink1: #ffb6c1;
    --pink2: #ff8fab;
    --pink3: #ffc8dd;
    --pink4: #ffafcc;
    --dark:  #c9184a;
    --bg:    #fff0f3;
    --white: #ffffff;
    --text:  #590d22;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    font-family: 'VT323', monospace;
    font-size: 18px;
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 1.5rem 2rem; }

[data-testid="stSidebar"] {
    background-color: #ffc8dd !important;
    border-right: 4px solid #c9184a !important;
}
[data-testid="stSidebar"] * {
    color: #590d22 !important;
    font-family: 'Press Start 2P', monospace !important;
    font-size: 9px !important;
    line-height: 2 !important;
}
[data-testid="stSidebar"] .stRadio label {
    display: block;
    padding: 6px 8px;
    border: 2px solid #c9184a;
    margin: 4px 0;
    background: #fff0f3;
    cursor: pointer;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: #ffb6c1;
}

.pixel-window {
    background: #ffc8dd;
    border: 4px solid #c9184a;
    padding: 0;
    margin-bottom: 1.5rem;
    box-shadow: 4px 4px 0px #c9184a;
}
.pixel-titlebar {
    background: #ff8fab;
    border-bottom: 4px solid #c9184a;
    padding: 6px 10px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #590d22;
}
.pixel-body {
    padding: 1rem 1.2rem;
    background: #fff0f3;
}

.metric-pixel {
    background: #fff0f3;
    border: 3px solid #c9184a;
    padding: 12px 14px;
    box-shadow: 3px 3px 0px #c9184a;
    margin-bottom: 1rem;
}
.metric-pixel .label {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: #c9184a;
    margin-bottom: 6px;
}
.metric-pixel .value {
    font-family: 'Press Start 2P', monospace;
    font-size: 16px;
    color: #590d22;
}

.pixel-header {
    background: #ffc8dd;
    border: 4px solid #c9184a;
    padding: 0;
    margin-bottom: 2rem;
    box-shadow: 6px 6px 0px #c9184a;
}
.pixel-header .titlebar {
    background: #ff8fab;
    border-bottom: 4px solid #c9184a;
    padding: 6px 12px;
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #590d22;
    display: flex;
    justify-content: space-between;
}
.pixel-header .content {
    padding: 1.5rem;
    text-align: center;
    background: #fff0f3;
}
.pixel-header h1 {
    font-family: 'Press Start 2P', monospace;
    font-size: 18px;
    color: #c9184a;
    margin: 0 0 0.5rem;
    text-shadow: 2px 2px 0px #ffb6c1;
    line-height: 1.8;
}
.pixel-header p {
    font-family: 'VT323', monospace;
    font-size: 22px;
    color: #590d22;
    margin: 0;
}

.stButton > button {
    font-family: 'Press Start 2P', monospace !important;
    font-size: 9px !important;
    background: #ff8fab !important;
    color: #590d22 !important;
    border: 3px solid #c9184a !important;
    border-radius: 0px !important;
    padding: 10px 20px !important;
    box-shadow: 3px 3px 0px #c9184a !important;
    transition: all 0.1s !important;
}
.stButton > button:hover {
    transform: translate(2px, 2px) !important;
    box-shadow: 1px 1px 0px #c9184a !important;
    background: #ffc8dd !important;
}
.stButton > button:active {
    transform: translate(3px, 3px) !important;
    box-shadow: 0px 0px 0px #c9184a !important;
}

.stSelectbox > div > div,
.stNumberInput > div > div > input {
    border: 3px solid #c9184a !important;
    border-radius: 0 !important;
    background: #fff0f3 !important;
    font-family: 'VT323', monospace !important;
    font-size: 18px !important;
    color: #590d22 !important;
    box-shadow: 2px 2px 0px #c9184a !important;
}

.stProgress > div > div > div {
    background: linear-gradient(90deg, #ff8fab, #c9184a) !important;
    border-radius: 0 !important;
}
.stProgress > div > div {
    background: #ffc8dd !important;
    border: 2px solid #c9184a !important;
    border-radius: 0 !important;
    height: 16px !important;
}

.pixel-warn {
    background: #ffe066;
    border: 3px solid #b8860b;
    box-shadow: 3px 3px 0px #b8860b;
    padding: 10px 14px;
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #5c4000;
    margin: 10px 0;
}
.pixel-danger {
    background: #ffb3b3;
    border: 3px solid #c9184a;
    box-shadow: 3px 3px 0px #c9184a;
    padding: 10px 14px;
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #590d22;
    margin: 10px 0;
}
.pixel-success {
    background: #b8f0c8;
    border: 3px solid #1a7a35;
    box-shadow: 3px 3px 0px #1a7a35;
    padding: 10px 14px;
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: #0d3b1e;
    margin: 10px 0;
}

.insight-row {
    background: #fff0f3;
    border: 2px solid #ffb6c1;
    border-left: 5px solid #c9184a;
    padding: 10px 14px;
    margin: 6px 0;
    font-family: 'VT323', monospace;
    font-size: 20px;
    color: #590d22;
    box-shadow: 2px 2px 0px #ffb6c1;
}

.sec-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 11px;
    color: #c9184a;
    border-bottom: 3px solid #ffb6c1;
    padding-bottom: 6px;
    margin: 1.5rem 0 1rem;
    display: block;
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #ffc8dd; }
::-webkit-scrollbar-thumb { background: #c9184a; }
</style>
""", unsafe_allow_html=True)

# ── CONFIG ───────────────────────────────────────────────────────
DATA_FILE   = "expenses.csv"
BUDGET_FILE = "budget.txt"
FIELDNAMES  = ["date", "category", "amount", "mood"]
CATEGORIES  = ["Food","Transport","Shopping","Entertainment",
               "Health","Education","Utilities","Investment","Other"]
MOODS       = ["Necessary","Impulsive","Investment"]
PALETTE     = ["#ff8fab","#c9184a","#ffb3c6","#ff4d6d","#ff758f",
               "#ff85a1","#fbb1bd","#ff5c8a","#a4133c","#800f2f"]

# ── HELPERS ──────────────────────────────────────────────────────
def load_expenses():
    if not os.path.exists(DATA_FILE): return []
    with open(DATA_FILE, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def save_expense(row):
    exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not exists: w.writeheader()
        w.writerow(row)

def load_budget():
    if os.path.exists(BUDGET_FILE):
        try: return float(open(BUDGET_FILE).read().strip())
        except: return None
    return None

def save_budget(v):
    open(BUDGET_FILE, "w").write(str(v))

def get_all_months(expenses):
    """Return sorted list of (year, month) tuples that have expenses"""
    months = set()
    for e in expenses:
        d = datetime.date.fromisoformat(e["date"])
        months.add((d.year, d.month))
    now = datetime.date.today()
    months.add((now.year, now.month))
    return sorted(months, reverse=True)

def filter_exp(expenses, year, month):
    return [e for e in expenses
            if datetime.date.fromisoformat(e["date"]).month == month
            and datetime.date.fromisoformat(e["date"]).year  == year]

def month_exp():
    now = datetime.date.today()
    return filter_exp(load_expenses(), now.year, now.month)

def total(exp):
    return sum(float(e["amount"]) for e in exp)

def build_pixel_calendar(year, month, expense_dates):
    """Build a cute pixel HTML calendar with expense dates encircled"""
    import calendar
    cal = calendar.monthcalendar(year, month)
    month_name = datetime.date(year, month, 1).strftime("%b %Y").upper()
    days_header = ["MO","TU","WE","TH","FR","SA","SU"]

    html = f"""
    <div style="
        background:#fff0f3;
        border:3px solid #c9184a;
        box-shadow:3px 3px 0px #c9184a;
        padding:8px;
        font-family:'Press Start 2P',monospace;
        font-size:7px;
        color:#590d22;
        margin-top:8px;
    ">
        <div style="
            background:#ff8fab;
            border-bottom:2px solid #c9184a;
            padding:4px 6px;
            text-align:center;
            font-size:7px;
            margin:-8px -8px 6px -8px;
            color:#590d22;
        ">{month_name}</div>
        <table style="width:100%;border-collapse:collapse;table-layout:fixed">
            <tr>{"".join(f'<th style="text-align:center;padding:2px;font-size:6px;color:#c9184a">{d}</th>' for d in days_header)}</tr>
    """
    for week in cal:
        html += "<tr>"
        for day in week:
            if day == 0:
                html += '<td style="padding:2px"></td>'
            else:
                is_today = (datetime.date.today() == datetime.date(year, month, day))
                has_exp  = day in expense_dates

                if has_exp and is_today:
                    # today + has expense — bold circle with dot
                    style = "background:#c9184a;color:#fff0f3;border-radius:50%;width:18px;height:18px;line-height:18px;text-align:center;margin:auto;font-size:6px;display:block;border:2px solid #590d22"
                elif has_exp:
                    # has expense — pink circle
                    style = "background:#ff8fab;color:#590d22;border-radius:50%;width:18px;height:18px;line-height:18px;text-align:center;margin:auto;font-size:6px;display:block;border:2px solid #c9184a"
                elif is_today:
                    # today only — outline circle
                    style = "background:#ffc8dd;color:#590d22;border-radius:50%;width:18px;height:18px;line-height:18px;text-align:center;margin:auto;font-size:6px;display:block;border:2px dashed #c9184a"
                else:
                    style = "text-align:center;font-size:6px;padding:2px;display:block;width:18px;height:18px;line-height:18px;margin:auto"

                html += f'<td style="padding:1px"><span style="{style}">{day}</span></td>'
        html += "</tr>"

    html += """
        </table>
        <div style="margin-top:6px;font-size:5px;color:#c9184a;line-height:1.8">
            <span style="background:#ff8fab;border-radius:50%;padding:1px 4px;border:1px solid #c9184a">8</span> expense day &nbsp;
            <span style="background:#ffc8dd;border-radius:50%;padding:1px 4px;border:1px dashed #c9184a">8</span> today
        </div>
    </div>
    """
    return html

def pink_chart():
    fig, ax = plt.subplots()
    fig.patch.set_facecolor("#fff0f3")
    ax.set_facecolor("#fff0f3")
    for sp in ax.spines.values():
        sp.set_edgecolor("#c9184a"); sp.set_linewidth(2)
    ax.tick_params(colors="#590d22")
    return fig, ax

def pixel_window(title, content_html):
    return f"""<div class="pixel-window">
        <div class="pixel-titlebar">
            <span>* * *</span><span>{title}</span><span>[x]</span>
        </div>
        <div class="pixel-body">{content_html}</div>
    </div>"""

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p style="font-family:\'Press Start 2P\',monospace;font-size:9px;color:#590d22;text-align:center;line-height:2">SMART EXPENSE<br>ANALYZER</p>', unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", [
        "DASHBOARD","LOG EXPENSE","SET BUDGET",
        "ANALYTICS","AI INSIGHTS","PREDICTION",
    ], label_visibility="collapsed")
    st.markdown("---")

    # ── MONTH SELECTOR ────────────────────────────────────────
    all_expenses = load_expenses()
    all_months   = get_all_months(all_expenses)
    month_labels = [datetime.date(y, m, 1).strftime("%B %Y") for y, m in all_months]
    sel_idx      = st.selectbox("SELECT MONTH", range(len(month_labels)),
                                 format_func=lambda i: month_labels[i],
                                 label_visibility="visible")
    sel_year, sel_month = all_months[sel_idx]
    # Store selected month in session state so pages can use it
    st.session_state["sel_year"]  = sel_year
    st.session_state["sel_month"] = sel_month

    # ── PIXEL CALENDAR ────────────────────────────────────────
    sel_expenses   = filter_exp(all_expenses, sel_year, sel_month)
    expense_days   = set(datetime.date.fromisoformat(e["date"]).day for e in sel_expenses)
    calendar_html  = build_pixel_calendar(sel_year, sel_month, expense_days)
    st.markdown(calendar_html, unsafe_allow_html=True)

    st.markdown("---")
    budget = load_budget()
    spent  = total(sel_expenses)
    if budget:
        pct = min(spent/budget, 1.0)
        st.markdown('<p style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#590d22">BUDGET</p>', unsafe_allow_html=True)
        st.progress(pct)
        st.markdown(f'<p style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:#590d22">RS{spent:.0f} / RS{budget:.0f}</p>', unsafe_allow_html=True)
        status = "!! EXCEEDED !!" if pct>=1 else ("! WARNING !" if pct>=0.8 else "ON TRACK")
        color  = "#c9184a" if pct>=1 else ("#b8860b" if pct>=0.8 else "#1a7a35")
        st.markdown(f'<p style="font-family:\'Press Start 2P\',monospace;font-size:7px;color:{color}">{status}</p>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(f'<p style="font-family:\'Press Start 2P\',monospace;font-size:6px;color:#590d22">{datetime.date.today().strftime("%d.%m.%Y")}</p>', unsafe_allow_html=True)

# ── HEADER ───────────────────────────────────────────────────────
st.markdown("""
<div class="pixel-header">
    <div class="titlebar">
        <span>* * *</span>
        <span>SMART EXPENSE ANALYZER v1.0</span>
        <span>[x]</span>
    </div>
    <div class="content">
        <h1>SMART EXPENSE<br>ANALYZER</h1>
        <p>your personal finance companion</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# DASHBOARD
# ════════════════════════════════════════════════════════════
if page == "DASHBOARD":
    sy = st.session_state.get("sel_year",  datetime.date.today().year)
    sm = st.session_state.get("sel_month", datetime.date.today().month)
    me     = filter_exp(load_expenses(), sy, sm)
    budget = load_budget()
    spent  = total(me)
    import calendar as cal_mod
    days_in = cal_mod.monthrange(sy, sm)[1]
    elapsed = min(datetime.date.today().day, days_in) if (sy == datetime.date.today().year and sm == datetime.date.today().month) else days_in
    daily  = spent / max(elapsed, 1)
    st.markdown(f'<span class="sec-title">VIEWING : {datetime.date(sy,sm,1).strftime("%B %Y").upper()}</span>', unsafe_allow_html=True)

    c1,c2,c3,c4 = st.columns(4)
    for col, lbl, val in zip(
        [c1,c2,c3,c4],
        ["TOTAL SPENT","TRANSACTIONS","DAILY AVG","BUDGET"],
        [f"RS {spent:.0f}", str(len(me)), f"RS {daily:.0f}",
         f"RS {budget:.0f}" if budget else "NOT SET"]
    ):
        with col:
            st.markdown(f'<div class="metric-pixel"><div class="label">{lbl}</div><div class="value">{val}</div></div>', unsafe_allow_html=True)

    if me:
        st.markdown('<span class="sec-title">THIS MONTH</span>', unsafe_allow_html=True)
        cat_totals = defaultdict(float)
        for e in me: cat_totals[e["category"]] += float(e["amount"])

        fig, ax = pink_chart()
        fig.set_size_inches(9,4)
        cats = list(cat_totals.keys()); vals = list(cat_totals.values())
        bars = ax.bar(cats, vals, color=PALETTE[:len(cats)], edgecolor="#590d22", linewidth=2, width=0.6)
        for b,v in zip(bars,vals):
            ax.text(b.get_x()+b.get_width()/2, b.get_height()+max(vals)*0.01,
                    f"RS{v:.0f}", ha="center", fontsize=8, color="#590d22", fontweight="bold")
        ax.set_ylabel("Amount (RS)", color="#590d22")
        ax.tick_params(axis="x", rotation=25)
        ax.set_title("CATEGORY BREAKDOWN", color="#c9184a", fontsize=11, fontweight="bold")
        ax.grid(axis="y", alpha=0.3, color="#ffb6c1")
        plt.tight_layout(); st.pyplot(fig)

        st.markdown('<span class="sec-title">RECENT EXPENSES</span>', unsafe_allow_html=True)
        import pandas as pd
        df = pd.DataFrame(me[-8:][::-1])
        df["amount"] = df["amount"].apply(lambda x: f"RS {float(x):.2f}")
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.markdown(pixel_window("NOTE.txt","<p style='font-family:VT323,monospace;font-size:20px;color:#590d22'>No expenses yet! Go to LOG EXPENSE.</p>"), unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# LOG EXPENSE
# ════════════════════════════════════════════════════════════
elif page == "LOG EXPENSE":
    st.markdown('<span class="sec-title">NEW ENTRY</span>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-row">DATE : {datetime.date.today().strftime("%d %B %Y")}  (auto)</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        category = st.selectbox("CATEGORY", CATEGORIES)
        amount   = st.number_input("AMOUNT (RS)", min_value=1.0, step=10.0, format="%.2f")
    with col2:
        mood = st.selectbox("MOOD TAG", MOODS)
        st.markdown(pixel_window("mood_guide.txt",
            "<p style='font-family:VT323,monospace;font-size:18px;color:#590d22;line-height:1.8'>NECESSARY  = bills, essentials<br>IMPULSIVE  = unplanned buying<br>INVESTMENT = growth, learning</p>"), unsafe_allow_html=True)

    if st.button("[ SAVE EXPENSE ]"):
        save_expense({"date": datetime.date.today().isoformat(),
                      "category": category, "amount": amount, "mood": mood})
        budget = load_budget(); me2 = month_exp(); spent2 = total(me2)
        st.markdown(f'<div class="pixel-success">SAVED  |  {category}  |  RS {amount:.2f}  |  {mood}</div>', unsafe_allow_html=True)
        if budget:
            pct = (spent2/budget)*100
            if pct >= 100:
                st.markdown(f'<div class="pixel-danger">!! BUDGET EXCEEDED !!  RS {spent2:.0f} / RS {budget:.0f}</div>', unsafe_allow_html=True)
            elif pct >= 80:
                st.markdown(f'<div class="pixel-warn">! WARNING  {pct:.1f}% used  RS {budget-spent2:.0f} left</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="pixel-success">ON TRACK  {pct:.1f}% used  RS {budget-spent2:.0f} left</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# SET BUDGET
# ════════════════════════════════════════════════════════════
elif page == "SET BUDGET":
    st.markdown('<span class="sec-title">BUDGET SETTINGS</span>', unsafe_allow_html=True)
    budget = load_budget()
    if budget:
        st.markdown(f'<div class="insight-row">CURRENT BUDGET : RS {budget:.2f}</div>', unsafe_allow_html=True)
    new_b = st.number_input("SET MONTHLY BUDGET (RS)", min_value=100.0, step=500.0,
                             format="%.2f", value=float(budget) if budget else 5000.0)
    if st.button("[ SAVE BUDGET ]"):
        save_budget(new_b)
        st.markdown(f'<div class="pixel-success">BUDGET SET TO RS {new_b:.2f}</div>', unsafe_allow_html=True)
    st.markdown('<span class="sec-title">ALERT SYSTEM</span>', unsafe_allow_html=True)
    st.markdown('<div class="pixel-warn">! 80% WARNING -- slow down spending</div>', unsafe_allow_html=True)
    st.markdown('<div class="pixel-danger">!! 100% EXCEEDED -- budget is gone</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# ANALYTICS
# ════════════════════════════════════════════════════════════
elif page == "ANALYTICS":
    sy = st.session_state.get("sel_year",  datetime.date.today().year)
    sm = st.session_state.get("sel_month", datetime.date.today().month)
    st.markdown(f'<span class="sec-title">ANALYTICS : {datetime.date(sy,sm,1).strftime("%B %Y").upper()}</span>', unsafe_allow_html=True)
    me = filter_exp(load_expenses(), sy, sm)
    if not me:
        st.markdown(pixel_window("ERROR.txt","<p style='font-family:VT323,monospace;font-size:20px;color:#590d22'>No data this month.</p>"), unsafe_allow_html=True)
    else:
        cat_totals  = defaultdict(float)
        mood_totals = defaultdict(float)
        for e in me:
            cat_totals[e["category"]] += float(e["amount"])
            mood_totals[e["mood"]]    += float(e["amount"])
        grand = sum(cat_totals.values())

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**DISTRIBUTION**")
            fig, ax = pink_chart(); fig.set_size_inches(5,5)
            labels = list(cat_totals.keys()); sizes = list(cat_totals.values())
            wedges, texts, autotexts = ax.pie(
                sizes, labels=labels, autopct="%1.1f%%", colors=PALETTE[:len(labels)],
                startangle=140, wedgeprops=dict(edgecolor="#590d22", linewidth=2), pctdistance=0.82)
            for t in autotexts: t.set_color("white"); t.set_fontweight("bold"); t.set_fontsize(8)
            centre = plt.Circle((0,0),0.62,fc="#fff0f3"); ax.add_patch(centre)
            ax.text(0,0,f"RS\n{grand:.0f}",ha="center",va="center",
                    fontsize=11,fontweight="bold",color="#c9184a")
            ax.set_title("EXPENSE PIE", color="#c9184a", fontsize=10, fontweight="bold")
            plt.tight_layout(); st.pyplot(fig)

        with col2:
            st.markdown("**CATEGORY BARS**")
            fig2, ax2 = pink_chart(); fig2.set_size_inches(5,5)
            cats = list(cat_totals.keys()); vals = list(cat_totals.values())
            bars = ax2.barh(cats, vals, color=PALETTE[:len(cats)], edgecolor="#590d22", linewidth=2, height=0.6)
            for b,v in zip(bars,vals):
                ax2.text(b.get_width()+grand*0.01, b.get_y()+b.get_height()/2,
                         f"RS{v:.0f}", va="center", fontsize=8, color="#590d22", fontweight="bold")
            ax2.set_xlabel("Amount (RS)", color="#590d22")
            ax2.set_title("AMOUNTS", color="#c9184a", fontsize=10, fontweight="bold")
            ax2.grid(axis="x", alpha=0.3, color="#ffb6c1")
            plt.tight_layout(); st.pyplot(fig2)

        st.markdown('<span class="sec-title">MOOD BREAKDOWN</span>', unsafe_allow_html=True)
        m1,m2,m3 = st.columns(3)
        for col, mood, color in zip([m1,m2,m3],
                                     ["Necessary","Impulsive","Investment"],
                                     ["#b8f0c8","#ffb3b3","#d4b8f0"]):
            amt = mood_totals.get(mood,0); pct = (amt/grand*100) if grand else 0
            with col:
                st.markdown(f'<div class="metric-pixel" style="background:{color}"><div class="label">{mood.upper()}</div><div class="value">RS {amt:.0f}</div><div style="font-family:VT323,monospace;font-size:18px;color:#590d22">{pct:.1f}%</div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# AI INSIGHTS
# ════════════════════════════════════════════════════════════
elif page == "AI INSIGHTS":
    sy = st.session_state.get("sel_year",  datetime.date.today().year)
    sm = st.session_state.get("sel_month", datetime.date.today().month)
    st.markdown(f'<span class="sec-title">AI INSIGHTS : {datetime.date(sy,sm,1).strftime("%B %Y").upper()}</span>', unsafe_allow_html=True)
    me = filter_exp(load_expenses(), sy, sm)
    if not me:
        st.markdown(pixel_window("ERROR.txt","<p style='font-family:VT323,monospace;font-size:20px;color:#590d22'>Log expenses first!</p>"), unsafe_allow_html=True)
    else:
        grand       = total(me)
        cat_totals  = defaultdict(float)
        mood_totals = defaultdict(float)
        for e in me:
            cat_totals[e["category"]] += float(e["amount"])
            mood_totals[e["mood"]]    += float(e["amount"])

        top_cat      = max(cat_totals, key=cat_totals.get)
        top_pct      = cat_totals[top_cat]/grand*100
        imp_pct      = mood_totals.get("Impulsive",0)/grand*100
        inv_pct      = mood_totals.get("Investment",0)/grand*100
        nec_pct      = mood_totals.get("Necessary",0)/grand*100
        today        = datetime.date.today()
        import calendar as cal_mod
        days_in_month = cal_mod.monthrange(sy, sm)[1]
        if sy == today.year and sm == today.month:
            days_elapsed = today.day
        else:
            days_elapsed = days_in_month
        daily_avg    = grand / max(days_elapsed, 1)
        days_left    = max(days_in_month - days_elapsed, 0)
        budget       = load_budget()

        insights = [
            f"{top_pct:.1f}% of expenses are on {top_cat.upper()}",
            f"IMPULSIVE spending : {imp_pct:.1f}%" + ("  >> too high!" if imp_pct>30 else "  >> ok"),
            f"NECESSARY : {nec_pct:.1f}%   INVESTMENT : {inv_pct:.1f}%",
            f"DAILY AVERAGE : RS {daily_avg:.2f}",
            f"DAYS GONE : {days_elapsed}   DAYS LEFT : {days_left}",
        ]
        if budget:
            remaining = budget-grand
            if remaining > 0 and daily_avg > 0:
                dte = remaining/daily_avg
                insights.append(f"!! BUDGET EXCEED IN ~{int(dte)} DAYS !!" if dte<days_left else f"ON TRACK  --  RS {remaining:.0f} surplus")
            elif remaining <= 0:
                insights.append(f"!! BUDGET EXCEEDED BY RS {abs(remaining):.0f} !!")
        if imp_pct > 40:
            insights.append("TIP >> try 24hr rule before buying")
        elif inv_pct > 20:
            insights.append("TIP >> great investment habit")
        else:
            insights.append("TIP >> balanced pattern, stay consistent")

        for ins in insights:
            st.markdown(f'<div class="insight-row">>> {ins}</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════
# PREDICTION
# ════════════════════════════════════════════════════════════
elif page == "PREDICTION":
    st.markdown('<span class="sec-title">SPENDING PREDICTION</span>', unsafe_allow_html=True)
    expenses = load_expenses()
    today    = datetime.date.today()
    last7    = [e for e in expenses if (today-datetime.date.fromisoformat(e["date"])).days < 7]

    if not last7:
        st.markdown(pixel_window("ERROR.txt","<p style='font-family:VT323,monospace;font-size:20px;color:#590d22'>Need 7 days of data!</p>"), unsafe_allow_html=True)
    else:
        total7    = total(last7)
        daily_avg = total7/7
        predicted = daily_avg*30
        budget    = load_budget()

        c1,c2,c3 = st.columns(3)
        for col, lbl, val in zip([c1,c2,c3],
            ["7-DAY TOTAL","DAILY AVG","PREDICTED"],
            [f"RS {total7:.0f}", f"RS {daily_avg:.0f}", f"RS {predicted:.0f}"]):
            with col:
                st.markdown(f'<div class="metric-pixel"><div class="label">{lbl}</div><div class="value">{val}</div></div>', unsafe_allow_html=True)

        if budget:
            diff = predicted-budget
            if diff > 0:
                st.markdown(f'<div class="pixel-danger">!! RS {diff:.0f} OVER BUDGET -- reduce RS {diff/30:.0f}/day</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="pixel-success">RS {abs(diff):.0f} UNDER BUDGET -- good job!</div>', unsafe_allow_html=True)

        days = list(range(1,31)); projected = [daily_avg*d for d in days]
        fig, ax = pink_chart(); fig.set_size_inches(10,5)
        ax.plot(days, projected, color="#c9184a", linewidth=3, label="Projected", zorder=3)
        ax.fill_between(days, projected, alpha=0.15, color="#ff8fab")
        ax.scatter(days[::5],[projected[i] for i in range(0,30,5)],color="#590d22",s=60,zorder=4,marker="s")
        if budget:
            ax.axhline(y=budget, color="#b8860b", linewidth=2, linestyle="--", label=f"Budget RS{budget:.0f}")
            cross = budget/daily_avg if daily_avg else 31
            if cross <= 30:
                ax.axvline(x=cross, color="#ff4d6d", linewidth=1.5, linestyle=":", label=f"Exceeds Day {int(cross)}")
        ax.set_title("MONTHLY PROJECTION", color="#c9184a", fontsize=12, fontweight="bold")
        ax.set_xlabel("Day of Month", color="#590d22")
        ax.set_ylabel("Cumulative Spend (RS)", color="#590d22")
        ax.legend(facecolor="#fff0f3", edgecolor="#c9184a")
        ax.grid(alpha=0.25, color="#ffb6c1")
        plt.tight_layout(); st.pyplot(fig)

        st.markdown(f'<div class="insight-row">>> FORMULA : RS {daily_avg:.2f} x 30 = RS {predicted:.2f} predicted monthly</div>', unsafe_allow_html=True)