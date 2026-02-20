"""
╔══════════════════════════════════════════════════════════════╗
║       AI-Powered Personal Finance Analyzer v1.0             ║
║       Built with Python | CSV | Matplotlib | Analytics      ║
╚══════════════════════════════════════════════════════════════╝
"""

import csv
import os
import datetime
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict

# ── CONFIG ──────────────────────────────────────────────────────
DATA_FILE   = "expenses.csv"
BUDGET_FILE = "budget.txt"
FIELDNAMES  = ["date", "category", "amount", "mood"]

CATEGORIES = [
    "Food", "Transport", "Shopping", "Entertainment",
    "Health", "Education", "Utilities", "Investment", "Other"
]

MOODS = {
    "1": "Necessary",
    "2": "Impulsive",
    "3": "Investment"
}

MOOD_EMOJI = {
    "Necessary":  "✅",
    "Impulsive":  "🔥",
    "Investment": "📈"
}

# ── HELPERS ─────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("\n" + "═"*60)
    print("   💰  AI-Powered Personal Finance Analyzer  🤖")
    print("═"*60 + "\n")

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, newline="") as f:
        return list(csv.DictReader(f))

def save_expense(row: dict):
    file_exists = os.path.exists(DATA_FILE)
    with open(DATA_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(row)

def load_budget():
    if os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE) as f:
            try:
                return float(f.read().strip())
            except ValueError:
                return None
    return None

def save_budget(amount: float):
    with open(BUDGET_FILE, "w") as f:
        f.write(str(amount))

def current_month_expenses(expenses):
    now = datetime.date.today()
    return [
        e for e in expenses
        if datetime.date.fromisoformat(e["date"]).month == now.month
        and datetime.date.fromisoformat(e["date"]).year == now.year
    ]

def total_amount(expenses):
    return sum(float(e["amount"]) for e in expenses)

# ── FEATURE 1 — LOG EXPENSE ─────────────────────────────────────
def log_expense():
    print("\n📝  NEW EXPENSE ENTRY")
    print("─"*40)

    date = datetime.date.today().isoformat()
    print(f"📅  Date (auto): {date}")

    print("\n📂  Categories:")
    for i, c in enumerate(CATEGORIES, 1):
        print(f"    {i}. {c}")
    while True:
        choice = input("\nEnter category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            category = CATEGORIES[int(choice) - 1]
            break
        print("❌  Invalid choice. Try again.")

    while True:
        amt = input("💵  Amount (₹): ").strip()
        try:
            amount = float(amt)
            if amount > 0:
                break
        except ValueError:
            pass
        print("❌  Enter a valid positive number.")

    print("\n🧠  Mood Tag:")
    for k, v in MOODS.items():
        print(f"    {k}. {MOOD_EMOJI[v]} {v}")
    while True:
        m = input("Select mood: ").strip()
        if m in MOODS:
            mood = MOODS[m]
            break
        print("❌  Invalid. Enter 1, 2, or 3.")

    row = {"date": date, "category": category, "amount": amount, "mood": mood}
    save_expense(row)
    print(f"\n✅  Expense logged! [{category} | ₹{amount:.2f} | {MOOD_EMOJI[mood]} {mood}]")

    # ── Budget check ──────────────────────────────────────────
    budget = load_budget()
    if budget:
        month_total = total_amount(current_month_expenses(load_expenses()))
        pct = (month_total / budget) * 100
        if pct >= 100:
            print(f"\n🚨  BUDGET EXCEEDED! ₹{month_total:.2f} / ₹{budget:.2f} ({pct:.1f}%)")
        elif pct >= 80:
            print(f"\n⚠️   Warning! You've used {pct:.1f}% of your budget. ₹{budget - month_total:.2f} remaining.")

    input("\nPress Enter to continue...")

# ── FEATURE 2 — SET BUDGET ──────────────────────────────────────
def set_budget():
    print("\n💼  BUDGET INTELLIGENCE SYSTEM")
    print("─"*40)
    current = load_budget()
    if current:
        print(f"Current monthly budget: ₹{current:.2f}")
    while True:
        amt = input("Set new monthly budget (₹): ").strip()
        try:
            b = float(amt)
            if b > 0:
                save_budget(b)
                print(f"✅  Budget set to ₹{b:.2f}")
                break
        except ValueError:
            pass
        print("❌  Invalid amount.")
    input("\nPress Enter to continue...")

# ── FEATURE 3 — CATEGORY ANALYTICS + CHARTS ─────────────────────
def category_analytics():
    expenses = load_expenses()
    month_exp = current_month_expenses(expenses)

    if not month_exp:
        print("\n📭  No expenses recorded this month.")
        input("\nPress Enter to continue...")
        return

    print("\n📊  CATEGORY ANALYTICS ENGINE")
    print("─"*40)

    cat_totals = defaultdict(float)
    for e in month_exp:
        cat_totals[e["category"]] += float(e["amount"])

    grand = sum(cat_totals.values())

    print(f"\n{'Category':<16} {'Amount':>10} {'Share':>8}")
    print("─"*38)
    for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1]):
        pct = (amt / grand) * 100
        bar = "█" * int(pct / 5)
        print(f"{cat:<16} ₹{amt:>8.2f}  {pct:>5.1f}%  {bar}")
    print("─"*38)
    print(f"{'TOTAL':<16} ₹{grand:>8.2f}")

    # ── Pie Chart ─────────────────────────────────────────────
    labels = list(cat_totals.keys())
    sizes  = list(cat_totals.values())
    colors = plt.cm.Set3.colors[:len(labels)]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle("💰 Monthly Expense Analysis", fontsize=16, fontweight="bold")

    axes[0].pie(sizes, labels=labels, autopct="%1.1f%%", colors=colors,
                startangle=140, wedgeprops=dict(edgecolor="white", linewidth=1.5))
    axes[0].set_title("Category Distribution (Pie Chart)")

    bars = axes[1].bar(labels, sizes, color=colors, edgecolor="white", linewidth=1.2)
    axes[1].set_title("Category-wise Spending (Bar Chart)")
    axes[1].set_ylabel("Amount (₹)")
    axes[1].set_xlabel("Category")
    axes[1].tick_params(axis="x", rotation=30)
    for bar, amt in zip(bars, sizes):
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + grand*0.005,
                     f"₹{amt:.0f}", ha="center", va="bottom", fontsize=8)

    plt.tight_layout()
    chart_path = "expense_chart.png"
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"\n📁  Chart saved as '{chart_path}'")
    input("\nPress Enter to continue...")

# ── FEATURE 4 — AI INSIGHT REPORT ───────────────────────────────
def ai_insight_report():
    expenses = load_expenses()
    month_exp = current_month_expenses(expenses)

    if not month_exp:
        print("\n📭  No data for AI analysis.")
        input("\nPress Enter to continue...")
        return

    print("\n🤖  AI INSIGHT REPORT")
    print("═"*50)

    grand = total_amount(month_exp)
    cat_totals = defaultdict(float)
    mood_totals = defaultdict(float)

    for e in month_exp:
        cat_totals[e["category"]] += float(e["amount"])
        mood_totals[e["mood"]]    += float(e["amount"])

    top_cat     = max(cat_totals, key=cat_totals.get)
    top_cat_pct = (cat_totals[top_cat] / grand) * 100
    imp_pct     = (mood_totals.get("Impulsive", 0) / grand) * 100
    inv_pct     = (mood_totals.get("Investment", 0) / grand) * 100
    nec_pct     = (mood_totals.get("Necessary", 0) / grand) * 100

    # Days elapsed this month
    today       = datetime.date.today()
    days_elapsed = today.day
    daily_avg   = grand / days_elapsed
    days_in_month = 30
    days_left   = days_in_month - days_elapsed
    budget      = load_budget()

    print(f"\n🔎  Insights for {today.strftime('%B %Y')}:\n")
    print(f"  • {top_cat_pct:.1f}% of your expenses are on {top_cat}.")
    print(f"  • Impulsive spending is {imp_pct:.1f}%.", end="")
    if imp_pct > 30:
        print("  ⚠️  Consider mindful spending!")
    else:
        print("  👍 Well controlled!")
    print(f"  • Necessary spending: {nec_pct:.1f}%  |  Investment: {inv_pct:.1f}%")
    print(f"  • Your average daily expense is ₹{daily_avg:.2f}.")
    print(f"  • Days elapsed this month: {days_elapsed}  |  Days remaining: {days_left}")

    if budget:
        remaining = budget - grand
        if remaining > 0 and daily_avg > 0:
            days_to_exceed = remaining / daily_avg
            if days_to_exceed < days_left:
                print(f"  • 🚨 You are likely to exceed your budget in ~{int(days_to_exceed)} days!")
            else:
                print(f"  • ✅ You're on track! Budget surplus: ₹{remaining:.2f}")
        elif remaining <= 0:
            print(f"  • 🚨 Budget already exceeded by ₹{abs(remaining):.2f}!")

    # Spending velocity
    if imp_pct > 40:
        print("\n  🧠 AI Tip: High impulsive spending detected. Try the 24-hour rule before buying!")
    elif inv_pct > 20:
        print("\n  🧠 AI Tip: Great investment habit! Keep allocating towards growth.")
    else:
        print("\n  🧠 AI Tip: Balanced spending pattern. Stay consistent!")

    print("\n" + "═"*50)
    input("\nPress Enter to continue...")

# ── FEATURE 5 — FUTURE SPENDING PREDICTION ──────────────────────
def spending_prediction():
    expenses = load_expenses()

    if not expenses:
        print("\n📭  No expense data available.")
        input("\nPress Enter to continue...")
        return

    print("\n📈  FUTURE SPENDING PREDICTION")
    print("─"*40)

    today = datetime.date.today()
    last_7 = [
        e for e in expenses
        if (today - datetime.date.fromisoformat(e["date"])).days < 7
    ]

    if not last_7:
        print("⚠️  No expenses in the last 7 days for prediction.")
        input("\nPress Enter to continue...")
        return

    total_7  = total_amount(last_7)
    daily_avg = total_7 / 7
    predicted_monthly = daily_avg * 30
    predicted_weekly  = daily_avg * 7

    budget = load_budget()

    print(f"\n  📅  Last 7-day total   : ₹{total_7:.2f}")
    print(f"  📊  Daily average      : ₹{daily_avg:.2f}")
    print(f"  🗓️   Predicted Weekly   : ₹{predicted_weekly:.2f}")
    print(f"\n  💡  At current rate, you may spend ₹{predicted_monthly:.2f} this month.")

    if budget:
        diff = predicted_monthly - budget
        if diff > 0:
            print(f"  🚨  This is ₹{diff:.2f} OVER your budget of ₹{budget:.2f}!")
            print(f"  💡  Reduce daily spending by ₹{diff/30:.2f} to stay within budget.")
        else:
            print(f"  ✅  This is ₹{abs(diff):.2f} UNDER your budget. Great discipline!")

    # Prediction chart
    days = list(range(1, 31))
    projected = [daily_avg * d for d in days]

    plt.figure(figsize=(10, 5))
    plt.plot(days, projected, color="#4C9BE8", linewidth=2, label="Projected Spending")
    plt.fill_between(days, projected, alpha=0.15, color="#4C9BE8")

    if budget:
        plt.axhline(y=budget, color="#E84C4C", linewidth=2,
                    linestyle="--", label=f"Budget ₹{budget:.0f}")
        cross = budget / daily_avg if daily_avg else 31
        if cross <= 30:
            plt.axvline(x=cross, color="orange", linewidth=1.5,
                        linestyle=":", label=f"Budget Hit ~Day {int(cross)}")

    plt.title("📈 Monthly Spending Projection", fontsize=14, fontweight="bold")
    plt.xlabel("Day of Month")
    plt.ylabel("Cumulative Spend (₹)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    chart_path = "prediction_chart.png"
    plt.savefig(chart_path, dpi=150, bbox_inches="tight")
    plt.show()
    print(f"\n  📁  Prediction chart saved as '{chart_path}'")
    input("\nPress Enter to continue...")

# ── FEATURE 6 — VIEW ALL EXPENSES ───────────────────────────────
def view_expenses():
    expenses = load_expenses()
    month_exp = current_month_expenses(expenses)

    print(f"\n📋  EXPENSE LOG — {datetime.date.today().strftime('%B %Y')}")
    print("─"*65)
    if not month_exp:
        print("  No expenses recorded this month.")
    else:
        print(f"  {'#':<4} {'Date':<12} {'Category':<16} {'Amount':>9}  {'Mood'}")
        print("  " + "─"*60)
        for i, e in enumerate(month_exp, 1):
            mood_icon = MOOD_EMOJI.get(e["mood"], "")
            print(f"  {i:<4} {e['date']:<12} {e['category']:<16} ₹{float(e['amount']):>8.2f}  {mood_icon} {e['mood']}")
        print("  " + "─"*60)
        print(f"  {'TOTAL':<32}  ₹{total_amount(month_exp):>8.2f}")

        budget = load_budget()
        if budget:
            pct = (total_amount(month_exp) / budget) * 100
            bar = "█" * int(pct / 5) + "░" * (20 - min(20, int(pct / 5)))
            status = "🚨 EXCEEDED" if pct >= 100 else ("⚠️  WARNING" if pct >= 80 else "✅ ON TRACK")
            print(f"\n  Budget: ₹{budget:.2f}  [{bar}] {pct:.1f}%  {status}")

    input("\nPress Enter to continue...")

# ── MAIN MENU ────────────────────────────────────────────────────
def main():
    menu = {
        "1": ("📝  Log New Expense",            log_expense),
        "2": ("💼  Set Monthly Budget",          set_budget),
        "3": ("📊  Category Analytics + Charts", category_analytics),
        "4": ("🤖  AI Insight Report",           ai_insight_report),
        "5": ("📈  Future Spending Prediction",  spending_prediction),
        "6": ("📋  View All Expenses",           view_expenses),
        "7": ("🚪  Exit",                        None),
    }

    while True:
        clear()
        banner()
        budget = load_budget()
        if budget:
            expenses = current_month_expenses(load_expenses())
            spent = total_amount(expenses)
            pct   = (spent / budget) * 100
            print(f"  Monthly Budget: ₹{budget:.2f}  |  Spent: ₹{spent:.2f}  |  {pct:.1f}% used\n")

        for k, (label, _) in menu.items():
            print(f"  {k}.  {label}")
        print()

        choice = input("  Select option: ").strip()
        if choice == "7":
            print("\n  👋  Thanks for using Finance Analyzer. Stay financially smart!\n")
            break
        elif choice in menu:
            clear()
            menu[choice][1]()
        else:
            print("  ❌  Invalid choice.")
            import time; time.sleep(1)

if __name__ == "__main__":
    main()