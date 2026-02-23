#  Smart Expense Analyzer
### AI-Powered Personal Finance Tracker | Python | CLI | Matplotlib

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Charts-orange?style=for-the-badge)
![CSV](https://img.shields.io/badge/Storage-CSV-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

---

##  About The Project

An **AI-inspired Personal Finance Analyzer** built with Python that helps users track expenses, analyze spending behavior, get intelligent budget alerts, and predict future spending trends — all from the terminal.

> Built as a portfolio project to demonstrate data analytics, logic building, and visualization skills.

---

## Features

| Feature | Description |
|--------|-------------|
|  **Expense Logger** | Auto date capture, category selection, mood tagging |
|  **Budget Intelligence** | 80% warning & 100% exceeded alerts |
|  **Category Analytics** | Pie chart + Bar chart visualization |
|  **AI Insight Report** | Spending behavior analysis & smart tips |
|  **Future Prediction** | Predicts monthly spending from 7-day average |
|  **Expense Log Viewer** | Clean tabular view with budget progress bar |

---

##  AI Insight Report Example

```
 AI Insight Report:

• 48% of your expenses are on Food.
• Impulsive spending is 35%  Consider mindful spending!
• You are likely to exceed your budget in ~5 days!
• Your average daily expense is ₹320.
• Great investment habit! Keep allocating towards growth.
```

---

## Spending Prediction Logic

```python
Daily Average  = Last 7 days total / 7
Predicted Monthly Expense = Daily Average × 30
```

---

##  Tech Stack

- **Language:** Python 3.13
- **Data Storage:** CSV
- **Visualization:** Matplotlib
- **Modules:** datetime, collections, os

---

##  Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/Shanvi0708/smart-expense-analyzer.git

# 2. Navigate to project folder
cd smart-expense-analyzer

# 3. Create virtual environment
python -m venv venv

# 4. Activate virtual environment
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# 5. Install dependencies
pip install matplotlib

# 6. Run the program
python finance_analyzer.py
```

---

##  Program Preview

```
════════════════════════════════════════════════════════════
   💰  AI-Powered Personal Finance Analyzer  🤖
════════════════════════════════════════════════════════════

  Monthly Budget: ₹5,000  |  Spent: ₹2,340  |  46.8% used

  1.  📝  Log New Expense
  2.  💼  Set Monthly Budget
  3.  📊  Category Analytics + Charts
  4.  🤖  AI Insight Report
  5.  📈  Future Spending Prediction
  6.  📋  View All Expenses
  7.  🚪  Exit
```

---

## 📂 Project Structure

```
smart-expense-analyzer/
│
├── finance_analyzer.py   # Main program
├── expenses.csv          # Auto-generated expense data
├── budget.txt            # Stores monthly budget
└── README.md             # Project documentation
```

---

##  What I Learned

- Data handling with CSV in Python
- Analytics logic — category-wise breakdown, mood analysis
- Chart generation using Matplotlib
- Predictive logic using averages
- CLI-based user experience design

---

##  Author

**Shanvi**
- GitHub: [@Shanvi0708](https://github.com/Shanvi0708)

---

> ⭐ If you found this project helpful, please give it a star!