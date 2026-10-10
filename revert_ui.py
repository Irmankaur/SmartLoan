import os
import shutil

BASE_DIR = r"d:\godrej3\smart-loan"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Remove newly introduced directories if they exist
for folder in ["WebContent/css", "WebContent/js", "WebContent/includes"]:
    target = os.path.join(BASE_DIR, folder)
    if os.path.exists(target):
        shutil.rmtree(target)

# 1. dashboard.jsp
dashboard_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<head>
    <title>Financial Intelligence Dashboard | Smart Loan</title>
    <style>
        :root { --navy: #0b1f38; --teal: #008080; --light-bg: #f4f7f6; --card-bg: #ffffff; --text-dark: #2c3e50; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--light-bg); color: var(--text-dark); margin: 0; padding: 0; }
        .navbar { background-color: var(--navy); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { margin: 0; font-size: 20px; }
        .navbar a { color: #d1ecf1; text-decoration: none; margin-left: 15px; font-weight: 500; }
        .container { max-width: 1100px; margin: 25px auto; padding: 0 20px; }
        .card { background: var(--card-bg); border-radius: 8px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section-header { border-bottom: 2px solid #eef2f5; padding-bottom: 12px; margin-bottom: 20px; color: var(--navy); }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .kpi-card { background: white; padding: 20px; border-radius: 8px; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.05); border-top: 4px solid var(--teal); }
        .kpi-card .num { font-size: 22px; font-weight: bold; color: var(--navy); margin: 8px 0; }
        .kpi-card .label { font-size: 13px; color: #6c757d; font-weight: 500; }
        .nav-card { background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; transition: transform 0.2s, box-shadow 0.2s; text-decoration: none; color: inherit; display: block; }
        .nav-card:hover { transform: translateY(-3px); box-shadow: 0 6px 15px rgba(0,0,0,0.08); border-color: var(--teal); }
        .nav-card h4 { margin: 0 0 8px 0; color: var(--navy); font-size: 17px; }
        .nav-card p { margin: 0; font-size: 13px; color: #666; line-height: 1.4; }
        .badge { display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
        .badge-green { background: #e8f5e9; color: #2e7d32; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>Smart Loan Intelligence</h1>
        <div>
            <span>Welcome, <b>${user.username}</b></span>
            <a href="profile">Profile</a>
            <a href="logout">Logout</a>
        </div>
    </div>

    <div class="container">
        <!-- Live KPI Overview -->
        <div class="grid-4" style="margin-bottom: 25px;">
            <div class="kpi-card">
                <div class="label">Total Active Debt</div>
                <div class="num">₹<fmt:formatNumber value="${totalDebt}" pattern="#,##0.00"/></div>
            </div>
            <div class="kpi-card">
                <div class="label">Monthly Total EMI</div>
                <div class="num">₹<fmt:formatNumber value="${totalEMI}" pattern="#,##0.00"/></div>
            </div>
            <div class="kpi-card">
                <div class="label">Available Monthly Surplus</div>
                <div class="num" style="color:var(--teal);">₹<fmt:formatNumber value="${freeCashFlow}" pattern="#,##0.00"/></div>
            </div>
            <div class="kpi-card">
                <div class="label">Risk Stress Score</div>
                <div class="num" style="color:#2e7d32;">${risk.score}/100</div>
            </div>
        </div>

        <!-- Intelligence Modules Navigation Grid -->
        <div class="card">
            <h3 class="section-header">Financial Intelligence & Decision Modules</h3>
            <div class="grid-2">
                <a href="prepayment" class="nav-card">
                    <h4>🎯 Prepayment Optimizer</h4>
                    <p>Discover which specific loan to prepay with your surplus money, how much interest you will save, and why that loan is mathematically prioritized.</p>
                </a>
                <a href="strategy" class="nav-card">
                    <h4>📊 Strategy Comparison</h4>
                    <p>Compare Debt Avalanche (highest interest), Debt Snowball (smallest balance), and Balanced strategies side-by-side with real metrics.</p>
                </a>
                <a href="risk" class="nav-card">
                    <h4>🛡️ Financial Risk Assessment</h4>
                    <p>Examine your EMI burden, emergency liquidity buffer, and debt-to-income ratio with transparent explanations and protective recommendations.</p>
                </a>
                <a href="simulator" class="nav-card">
                    <h4>⚡ What-If Life Event Simulator</h4>
                    <p>Simulate the impact of salary cuts, interest rate hikes, or sudden emergency expenses on your cash flow and loan affordability.</p>
                </a>
                <a href="loans" class="nav-card">
                    <h4>📝 Manage Loans & Amortization</h4>
                    <p>View, create, and inspect month-by-month reducing-balance amortization schedules for all your home, auto, and personal debts.</p>
                </a>
                <a href="profile" class="nav-card">
                    <h4>👤 Financial Profile & Budget</h4>
                    <p>Keep your monthly income, living expenses, and emergency reserve floor updated to ensure accurate decision intelligence.</p>
                </a>
            </div>
        </div>
    </div>
</body>
</html>
"""
write_file("WebContent/dashboard.jsp", dashboard_jsp)

# 2. prepayment.jsp
prepayment_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<head>
    <title>Intelligent Prepayment Optimizer | Smart Loan</title>
    <style>
        :root { --navy: #0b1f38; --teal: #008080; --light-bg: #f4f7f6; --card-bg: #ffffff; --text-dark: #2c3e50; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--light-bg); color: var(--text-dark); margin: 0; padding: 0; }
        .navbar { background-color: var(--navy); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .navbar h1 { margin: 0; font-size: 20px; letter-spacing: 0.5px; }
        .navbar a { color: #d1ecf1; text-decoration: none; margin-left: 15px; font-weight: 500; }
        .navbar a:hover { color: #ffffff; }
        .container { max-width: 1100px; margin: 25px auto; padding: 0 20px; }
        .card { background: var(--card-bg); border-radius: 8px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section-header { border-bottom: 2px solid #eef2f5; padding-bottom: 12px; margin-bottom: 20px; color: var(--navy); }
        .info-pill { display: inline-block; padding: 4px 12px; background: #e0f2f1; color: #004d40; border-radius: 20px; font-size: 13px; font-weight: 600; margin-bottom: 10px; }
        .recommendation-banner { background: #e8f5e9; border-left: 5px solid #2e7d32; padding: 20px; border-radius: 4px; margin-bottom: 20px; }
        .recommendation-banner h3 { margin-top: 0; color: #1b5e20; }
        .form-inline { display: flex; gap: 15px; align-items: center; margin: 15px 0; }
        .form-inline input { padding: 10px 15px; border: 1px solid #ced4da; border-radius: 5px; font-size: 15px; width: 250px; }
        .btn { background: var(--teal); color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        .btn:hover { background: #006666; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .stat-box { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; padding: 15px; text-align: center; }
        .stat-box .num { font-size: 22px; font-weight: bold; color: var(--teal); margin: 5px 0; }
        .stat-box .label { font-size: 13px; color: #6c757d; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #eef2f5; font-size: 14px; }
        th { background: #f8f9fa; color: var(--navy); font-weight: 600; }
        .badge-rec { background: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; }
        .guide-box { background: #fff8e1; border-left: 4px solid #fbc02d; padding: 15px; border-radius: 4px; font-size: 14px; line-height: 1.5; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>Smart Loan Intelligence</h1>
        <div>
            <a href="dashboard">Dashboard</a>
            <a href="loans">My Loans</a>
            <a href="strategy">Strategies</a>
            <a href="risk">Risk Analysis</a>
            <a href="simulator">What-If Simulator</a>
            <a href="logout">Logout</a>
        </div>
    </div>

    <div class="container">
        <!-- Explanatory Header -->
        <div class="card">
            <span class="info-pill">Core Intelligence Module</span>
            <h2 class="section-header">Intelligent Prepayment Optimizer</h2>
            <div class="grid-3">
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">What it does</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Analyzes your entire loan portfolio and exact cash flow to tell you exactly <b>which loan to prepay</b> and how much extra money to put toward it.</p>
                </div>
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">How it works</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Uses reducing-balance mathematical amortization to simulate extra repayments against every loan, comparing interest saved vs liquidity preserved.</p>
                </div>
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">Why it matters</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Prepaying the wrong loan can waste thousands in compounding interest or leave you cash-poor during an unexpected financial emergency.</p>
                </div>
            </div>
        </div>

        <!-- Input Section -->
        <div class="card">
            <h3 style="margin-top:0; color:var(--navy);">Enter Your Available Monthly Surplus</h3>
            <p style="font-size:14px; color:#666;">We calculated your estimated monthly free cash flow as <b>₹<fmt:formatNumber value="${plan.safeSurplus}" pattern="#,##0.00"/></b> from your financial profile. You can customize the amount below:</p>
            <form action="prepayment" method="post" class="form-inline">
                <input type="number" name="surplus" value="${surplusInput}" step="100" min="0" required placeholder="Extra Monthly Amount (₹)">
                <button type="submit" class="btn">Calculate Best Allocation</button>
            </form>
        </div>

        <!-- Decision Explanation Banner -->
        <c:if test="${not empty plan.recommendedLoan}">
            <div class="recommendation-banner">
                <h3>Recommended Action: Allocate ₹<fmt:formatNumber value="${plan.proposedAmount}" pattern="#,##0.00"/> to '${plan.recommendedLoan.loanType} (ID: ${plan.recommendedLoan.id})'</h3>
                <div class="grid-3" style="margin: 15px 0;">
                    <div class="stat-box" style="background:white;">
                        <div class="label">Projected Interest Saved</div>
                        <div class="num">₹<fmt:formatNumber value="${plan.interestSavings}" pattern="#,##0.00"/></div>
                    </div>
                    <div class="stat-box" style="background:white;">
                        <div class="label">Tenure Shortened By</div>
                        <div class="num">${plan.tenureMonthsSaved} Months</div>
                    </div>
                    <div class="stat-box" style="background:white;">
                        <div class="label">Emergency Reserve Preserved</div>
                        <div class="num">₹<fmt:formatNumber value="${plan.emergencyReserveRetained}" pattern="#,##0.00"/></div>
                    </div>
                </div>
                <h4 style="margin: 15px 0 5px 0; color:#1b5e20;">Detailed Explanation & Rationale:</h4>
                <p style="font-size:14px; line-height:1.6; color:#2e7d32; white-space: pre-line; margin:0;">${plan.whyThisLoan}</p>
            </div>
        </c:if>

        <!-- Strategy Comparison Table -->
        <div class="card">
            <h3 class="section-header">Strategy Comparison for Your Portfolio</h3>
            <table>
                <thead>
                    <tr>
                        <th>Strategy</th>
                        <th>Target Loan</th>
                        <th>Total Interest Saved</th>
                        <th>Time Saved</th>
                        <th>Pros</th>
                        <th>Cons</th>
                    </tr>
                </thead>
                <tbody>
                    <c:forEach var="strat" items="${plan.strategyComparisons}">
                        <tr style="${strat.recommended ? 'background-color: #f1f8e9; font-weight: 500;' : ''}">
                            <td>
                                ${strat.strategyName}
                                <c:if test="${strat.recommended}"><span class="badge-rec">Best Choice</span></c:if>
                            </td>
                            <td>${strat.targetLoanName}</td>
                            <td style="color:#008080; font-weight:bold;">₹<fmt:formatNumber value="${strat.interestSaved}" pattern="#,##0.00"/></td>
                            <td>${strat.monthsSaved} Months</td>
                            <td><span style="color:#2e7d32; font-size:13px;">${strat.pros}</span></td>
                            <td><span style="color:#c62828; font-size:13px;">${strat.cons}</span></td>
                        </tr>
                    </c:forEach>
                </tbody>
            </table>

            <div class="guide-box">
                <b>Decision Rule Behind Recommendations:</b>
                We default to prioritizing the <i>Debt Avalanche</i> strategy (highest interest rate first) because compounding interest mathematically eats the most wealth. However, if your emergency fund covers less than 3 months of essential expenses, we advise splitting surplus 50/50 between liquidity building and debt payoff.
            </div>
        </div>
    </div>
</body>
</html>
"""
write_file("WebContent/prepayment.jsp", prepayment_jsp)

# 3. strategy.jsp
strategy_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<head>
    <title>Repayment Strategy Optimization | Smart Loan</title>
    <style>
        :root { --navy: #0b1f38; --teal: #008080; --light-bg: #f4f7f6; --card-bg: #ffffff; --text-dark: #2c3e50; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--light-bg); color: var(--text-dark); margin: 0; padding: 0; }
        .navbar { background-color: var(--navy); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { margin: 0; font-size: 20px; }
        .navbar a { color: #d1ecf1; text-decoration: none; margin-left: 15px; font-weight: 500; }
        .container { max-width: 1100px; margin: 25px auto; padding: 0 20px; }
        .card { background: var(--card-bg); border-radius: 8px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section-header { border-bottom: 2px solid #eef2f5; padding-bottom: 12px; margin-bottom: 20px; color: var(--navy); }
        .info-pill { display: inline-block; padding: 4px 12px; background: #e0f2f1; color: #004d40; border-radius: 20px; font-size: 13px; font-weight: 600; margin-bottom: 10px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #eef2f5; font-size: 14px; }
        th { background: #f8f9fa; color: var(--navy); font-weight: 600; }
        .badge-rec { background: #28a745; color: white; padding: 3px 8px; border-radius: 12px; font-size: 11px; }
        .box { padding: 15px; border-radius: 6px; margin-bottom: 15px; font-size: 14px; line-height: 1.5; }
        .box-green { background: #e8f5e9; border-left: 4px solid #2e7d32; color: #1b5e20; }
        .box-blue { background: #e3f2fd; border-left: 4px solid #1976d2; color: #0d47a1; }
        .box-yellow { background: #fffde7; border-left: 4px solid #fbc02d; color: #f57f17; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>Smart Loan Intelligence</h1>
        <div>
            <a href="dashboard">Dashboard</a>
            <a href="loans">My Loans</a>
            <a href="prepayment">Prepayment Optimizer</a>
            <a href="risk">Risk Analysis</a>
            <a href="simulator">What-If Simulator</a>
            <a href="logout">Logout</a>
        </div>
    </div>

    <div class="container">
        <div class="card">
            <span class="info-pill">Strategy Comparison Engine</span>
            <h2 class="section-header">Repayment Strategy Optimization</h2>
            <div class="grid-3">
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">What it does</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Compares four fundamental repayment methods side-by-side using your real loan numbers.</p>
                </div>
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">How it works</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Runs iterative amortization calculations against baseline contract EMIs to rank strategies by total interest savings and risk resilience.</p>
                </div>
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">Why it matters</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Choosing between Avalanche (math-first) and Snowball (mindset-first) determines how fast you become debt-free and how much wealth you retain.</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h3 class="section-header">Strategy Breakdown & Detailed Trade-offs</h3>
            
            <div class="box box-green">
                <h4 style="margin:0 0 5px 0;">1. Debt Avalanche (Recommended for Lowest Cost)</h4>
                Directs all available extra surplus toward the loan with the highest annual interest rate.
                <br><b>Why it wins:</b> Mathematically minimizes compounding interest charges across all loans.
            </div>

            <div class="box box-blue">
                <h4 style="margin:0 0 5px 0;">2. Debt Snowball (Recommended for Psychological Momentum)</h4>
                Directs extra surplus toward the loan with the smallest outstanding principal balance regardless of rate.
                <br><b>Trade-off:</b> Clears individual accounts faster to free up mental space and individual monthly EMIs, but incurs more total interest overall.
            </div>

            <div class="box box-yellow">
                <h4 style="margin:0 0 5px 0;">3. Balanced Strategy (Liquidity Preserving)</h4>
                Allocates 50% of surplus to debt reduction and 50% into liquid emergency savings.
                <br><b>Trade-off:</b> Slower debt payoff, but guards against sudden income shocks or medical emergencies.
            </div>
        </div>

        <div class="card">
            <h3 class="section-header">Calculated Comparison for Your Profile</h3>
            <table>
                <thead>
                    <tr>
                        <th>Strategy</th>
                        <th>Target Loan</th>
                        <th>Interest Saved</th>
                        <th>Tenure Reduction</th>
                        <th>Recommendation Status</th>
                    </tr>
                </thead>
                <tbody>
                    <c:forEach var="strat" items="${plan.strategyComparisons}">
                        <tr style="${strat.recommended ? 'background-color: #f1f8e9; font-weight: bold;' : ''}">
                            <td>${strat.strategyName}</td>
                            <td>${strat.targetLoanName}</td>
                            <td style="color:#008080;">₹<fmt:formatNumber value="${strat.interestSaved}" pattern="#,##0.00"/></td>
                            <td>${strat.monthsSaved} Months</td>
                            <td>
                                <c:if test="${strat.recommended}"><span class="badge-rec">Optimal</span></c:if>
                                <c:if test="${!strat.recommended}">Alternative Option</c:if>
                            </td>
                        </tr>
                    </c:forEach>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""
write_file("WebContent/strategy.jsp", strategy_jsp)

# 4. risk.jsp
risk_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<head>
    <title>Financial Risk Assessment | Smart Loan</title>
    <style>
        :root { --navy: #0b1f38; --teal: #008080; --light-bg: #f4f7f6; --card-bg: #ffffff; --text-dark: #2c3e50; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--light-bg); color: var(--text-dark); margin: 0; padding: 0; }
        .navbar { background-color: var(--navy); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { margin: 0; font-size: 20px; }
        .navbar a { color: #d1ecf1; text-decoration: none; margin-left: 15px; font-weight: 500; }
        .container { max-width: 1100px; margin: 25px auto; padding: 0 20px; }
        .card { background: var(--card-bg); border-radius: 8px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section-header { border-bottom: 2px solid #eef2f5; padding-bottom: 12px; margin-bottom: 20px; color: var(--navy); }
        .info-pill { display: inline-block; padding: 4px 12px; background: #e0f2f1; color: #004d40; border-radius: 20px; font-size: 13px; font-weight: 600; margin-bottom: 10px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .score-box { text-align: center; padding: 25px; border-radius: 8px; background: #f8f9fa; border: 1px solid #e9ecef; }
        .score-num { font-size: 48px; font-weight: bold; color: var(--teal); margin: 10px 0; }
        .risk-badge { display: inline-block; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 14px; }
        .badge-low { background: #e8f5e9; color: #2e7d32; }
        .badge-mod { background: #fff3e0; color: #ef6c00; }
        .badge-high { background: #ffebee; color: #c62828; }
        .factor-card { padding: 15px; border-radius: 6px; margin-bottom: 12px; font-size: 14px; }
        .factor-pos { background: #e8f5e9; border-left: 4px solid #43a047; }
        .factor-neg { background: #ffebee; border-left: 4px solid #e53935; }
        .rec-box { background: #e0f2f1; border-left: 4px solid #00897b; padding: 15px; border-radius: 4px; font-size: 14px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>Smart Loan Intelligence</h1>
        <div>
            <a href="dashboard">Dashboard</a>
            <a href="loans">My Loans</a>
            <a href="prepayment">Prepayment Optimizer</a>
            <a href="strategy">Strategies</a>
            <a href="simulator">What-If Simulator</a>
            <a href="logout">Logout</a>
        </div>
    </div>

    <div class="container">
        <div class="card">
            <span class="info-pill">Transparent Financial Stress Engine</span>
            <h2 class="section-header">Financial Risk Assessment</h2>
            <div class="grid-3">
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">What it does</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Measures your vulnerability to debt distress based on your EMI burden, cash flow surplus, and emergency liquidity buffer.</p>
                </div>
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">How it works</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Applies documented banking benchmarks (e.g. EMI-to-income < 35%, 3-6 months reserve) to assign an explainable 0-100 score.</p>
                </div>
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">Why it matters</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Identifies structural vulnerabilities before they trigger missed payments, penalties, or credit score damage.</p>
                </div>
            </div>
        </div>

        <div class="grid-2">
            <!-- Score Card -->
            <div class="card">
                <h3 class="section-header">Your Financial Stress Score</h3>
                <div class="score-box">
                    <div class="score-num">${risk.score}<span style="font-size:20px; color:#888;">/100</span></div>
                    <div class="risk-badge ${risk.score >= 75 ? 'badge-low' : (risk.score >= 50 ? 'badge-mod' : 'badge-high')}">
                        ${risk.category}
                    </div>
                    <p style="font-size:14px; color:#555; margin-top:15px; line-height:1.5;">${risk.plainEnglishSummary}</p>
                </div>

                <div style="margin-top:20px;">
                    <h4 style="color:var(--navy); margin-bottom:10px;">Key Financial Metrics</h4>
                    <table style="width:100%; font-size:13px;">
                        <tr><td><b>Monthly Take-Home Income:</b></td><td>₹<fmt:formatNumber value="${user.income}" pattern="#,##0.00"/></td></tr>
                        <tr><td><b>Total Monthly EMIs:</b></td><td>₹<fmt:formatNumber value="${user.income * (risk.emiToIncomeRatio / 100.0)}" pattern="#,##0.00"/> (<fmt:formatNumber value="${risk.emiToIncomeRatio}" pattern="#0.0"/>%)</td></tr>
                        <tr><td><b>Essential Living Expenses:</b></td><td>₹<fmt:formatNumber value="${user.expenses}" pattern="#,##0.00"/></td></tr>
                        <tr><td><b>Emergency Reserve:</b></td><td>₹<fmt:formatNumber value="${user.emergencyReserve}" pattern="#,##0.00"/> (<fmt:formatNumber value="${risk.reserveCoverageMonths}" pattern="#0.0"/> Months)</td></tr>
                        <tr><td><b>Free Monthly Cash Flow:</b></td><td>₹<fmt:formatNumber value="${risk.freeCashFlow}" pattern="#,##0.00"/></td></tr>
                    </table>
                </div>
            </div>

            <!-- Contributing Factors -->
            <div class="card">
                <h3 class="section-header">Contributing Factors & Actions</h3>
                
                <h4 style="color:#2e7d32; margin:10px 0 5px 0;">Protective Strengths:</h4>
                <c:forEach var="pos" items="${risk.protectiveFactors}">
                    <div class="factor-card factor-pos">${pos}</div>
                </c:forEach>

                <h4 style="color:#c62828; margin:15px 0 5px 0;">Risk Vulnerabilities:</h4>
                <c:forEach var="neg" items="${risk.riskFactors}">
                    <div class="factor-card factor-neg">${neg}</div>
                </c:forEach>

                <h4 style="color:var(--teal); margin:15px 0 5px 0;">Action Plan to Reduce Risk:</h4>
                <c:forEach var="rec" items="${risk.recommendations}">
                    <div class="rec-box">${rec}</div>
                </c:forEach>
            </div>
        </div>
    </div>
</body>
</html>
"""
write_file("WebContent/risk.jsp", risk_jsp)

# 5. simulator.jsp
simulator_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<%@ taglib uri="http://java.sun.com/jsp/jstl/fmt" prefix="fmt" %>
<!DOCTYPE html>
<html>
<head>
    <title>What-If Life Event Simulator | Smart Loan</title>
    <style>
        :root { --navy: #0b1f38; --teal: #008080; --light-bg: #f4f7f6; --card-bg: #ffffff; --text-dark: #2c3e50; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: var(--light-bg); color: var(--text-dark); margin: 0; padding: 0; }
        .navbar { background-color: var(--navy); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { margin: 0; font-size: 20px; }
        .navbar a { color: #d1ecf1; text-decoration: none; margin-left: 15px; font-weight: 500; }
        .container { max-width: 1100px; margin: 25px auto; padding: 0 20px; }
        .card { background: var(--card-bg); border-radius: 8px; padding: 25px; margin-bottom: 25px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
        .section-header { border-bottom: 2px solid #eef2f5; padding-bottom: 12px; margin-bottom: 20px; color: var(--navy); }
        .info-pill { display: inline-block; padding: 4px 12px; background: #e0f2f1; color: #004d40; border-radius: 20px; font-size: 13px; font-weight: 600; margin-bottom: 10px; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; }
        .form-group { margin-bottom: 15px; }
        .form-group label { display: block; font-size: 14px; font-weight: 600; margin-bottom: 5px; color: var(--navy); }
        .form-group input { width: 100%; padding: 10px; border: 1px solid #ced4da; border-radius: 5px; font-size: 14px; box-sizing: border-box; }
        .btn { background: var(--teal); color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold; cursor: pointer; width: 100%; font-size: 15px; }
        .btn:hover { background: #006666; }
        .result-box { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 6px; padding: 20px; font-size: 14px; line-height: 1.6; }
        .stat-badge { font-size: 18px; font-weight: bold; color: var(--teal); }
        .alert-box { background: #ffebee; border-left: 4px solid #c62828; padding: 15px; border-radius: 4px; color: #b71c1c; margin-top: 15px; }
        .success-box { background: #e8f5e9; border-left: 4px solid #2e7d32; padding: 15px; border-radius: 4px; color: #1b5e20; margin-top: 15px; }
    </style>
</head>
<body>
    <div class="navbar">
        <h1>Smart Loan Intelligence</h1>
        <div>
            <a href="dashboard">Dashboard</a>
            <a href="loans">My Loans</a>
            <a href="prepayment">Prepayment Optimizer</a>
            <a href="strategy">Strategies</a>
            <a href="risk">Risk Analysis</a>
            <a href="logout">Logout</a>
        </div>
    </div>

    <div class="container">
        <div class="card">
            <span class="info-pill">Scenario Stress Testing</span>
            <h2 class="section-header">What-If Life Event Simulator</h2>
            <div class="grid-3">
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">What it does</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Allows you to stress-test hypothetical life disruptions (salary reduction, interest rate spikes, medical costs) before they happen.</p>
                </div>
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">How it works</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Recalculates your debt-to-income ratio, monthly cash shortfall, and emergency reserve depletion rate under customized stress parameters.</p>
                </div>
                <div>
                    <h4 style="color:var(--navy); margin-bottom:5px;">Why it matters</h4>
                    <p style="font-size:13px; color:#555; margin:0;">Simulations are strictly temporary and never touch your actual saved loans. They empower you to prepare defensive emergency buffers.</p>
                </div>
            </div>
        </div>

        <div class="grid-2">
            <!-- Scenario Inputs -->
            <div class="card">
                <h3 class="section-header">Configure Hypothetical Shock</h3>
                <form action="simulator" method="post">
                    <div class="form-group">
                        <label>Salary Reduction Percentage (%)</label>
                        <input type="number" name="salaryCut" value="${salaryCut}" step="5" min="0" max="100">
                    </div>
                    <div class="form-group">
                        <label>Interest Rate Hike Across Loans (%)</label>
                        <input type="number" name="rateHike" value="${rateHike}" step="0.25" min="0" max="15">
                    </div>
                    <div class="form-group">
                        <label>One-Time Emergency Expense (₹)</label>
                        <input type="number" name="emergencyExpense" value="${emergencyExpense}" step="1000" min="0">
                    </div>
                    <button type="submit" class="btn">Run Stress Simulation</button>
                </form>
            </div>

            <!-- Simulation Outcomes -->
            <div class="card">
                <h3 class="section-header">Simulated Financial Impact</h3>
                <div class="result-box">
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <span>Simulated Monthly Income:</span>
                        <span class="stat-badge">₹<fmt:formatNumber value="${sim.simulatedIncome}" pattern="#,##0.00"/></span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <span>Simulated Total EMI Burden:</span>
                        <span class="stat-badge">₹<fmt:formatNumber value="${sim.simulatedTotalEMI}" pattern="#,##0.00"/></span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <span>Revised Net Monthly Cash Flow:</span>
                        <span class="stat-badge" style="${sim.simulatedCashFlow < 0 ? 'color:#c62828;' : 'color:#2e7d32;'}">
                            ₹<fmt:formatNumber value="${sim.simulatedCashFlow}" pattern="#,##0.00"/>
                        </span>
                    </div>
                    <hr style="border:0; border-top:1px solid #ddd; margin:15px 0;">
                    
                    <h4 style="margin:0 0 5px 0; color:var(--navy);">Analysis & Breakdown:</h4>
                    <p style="margin:0; font-size:13px; line-height:1.5; white-space: pre-line;">${sim.narrativeAnalysis}</p>

                    <c:if test="${sim.simulatedCashFlow < 0}">
                        <div class="alert-box">
                            <b>${sim.actionRecommendation}</b>
                        </div>
                    </c:if>
                    <c:if test="${sim.simulatedCashFlow >= 0}">
                        <div class="success-box">
                            <b>${sim.actionRecommendation}</b>
                        </div>
                    </c:if>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""
write_file("WebContent/simulator.jsp", simulator_jsp)

# 6. loans.jsp
loans_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head><title>My Loans</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; margin: 0; padding: 0; }
    .header { background-color: #0b1f38; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
    .header a { color: #008080; text-decoration: none; font-weight: bold; }
    table { width: 85%; margin: 25px auto; border-collapse: collapse; background: white; box-shadow: 0px 2px 8px rgba(0,0,0,0.06); }
    th, td { padding: 12px; border: 1px solid #ddd; text-align: center; }
    th { background-color: #008080; color: white; }
    form { width: 350px; margin: 25px auto; padding: 25px; background: white; border-radius: 8px; box-shadow: 0px 2px 8px rgba(0,0,0,0.06); }
    input { width: 92%; margin-bottom: 12px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
    button { background-color: #0b1f38; color: white; padding: 10px; width: 100%; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
    button:hover { background-color: #008080; }
</style>
</head>
<body>
    <div class="header">
        <h1>Manage Loans</h1>
        <a href="dashboard" style="color: #ffffff; background: #008080; padding: 8px 15px; border-radius: 4px;">Back to Dashboard</a>
    </div>
    
    <form action="loans" method="post">
        <h3 style="margin-top: 0; color: #0b1f38;">Add New Loan Facility</h3>
        <input type="text" name="loanType" placeholder="Loan Category (e.g. Home, Auto, Education)" required>
        <input type="number" name="principal" placeholder="Principal Amount (₹)" step="0.01" required>
        <input type="number" name="interestRate" placeholder="Interest Rate (%)" step="0.01" required>
        <input type="number" name="tenureMonths" placeholder="Tenure (Months)" required>
        <button type="submit">Add Loan</button>
    </form>

    <table>
        <tr><th>ID</th><th>Category</th><th>Principal</th><th>Rate</th><th>Months</th><th>Action</th></tr>
        <c:forEach var="loan" items="${loans}">
            <tr>
                <td>${loan.id}</td>
                <td><b>${loan.loanType}</b></td>
                <td>₹${loan.principal}</td>
                <td>${loan.interestRate}%</td>
                <td>${loan.tenureMonths}</td>
                <td><a href="amortization?loanId=${loan.id}" style="color: #008080; font-weight: bold;">Schedule →</a></td>
            </tr>
        </c:forEach>
    </table>
</body>
</html>
"""
write_file("WebContent/loans.jsp", loans_jsp)

# 7. profile.jsp
profile_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head><title>Financial Profile</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; margin: 0; padding: 0; }
    .header { background-color: #0b1f38; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
    form { width: 350px; margin: 30px auto; padding: 25px; background: white; border-radius: 8px; box-shadow: 0px 2px 8px rgba(0,0,0,0.06); }
    input { width: 92%; margin-bottom: 14px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
    button { background-color: #008080; color: white; padding: 10px; width: 100%; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
    label { display: block; margin-bottom: 5px; font-weight: bold; font-size: 13px; }
</style>
</head>
<body>
    <div class="header">
        <h1>Financial Profile</h1>
        <a href="dashboard" style="color: white; text-decoration: none;">Dashboard</a>
    </div>
    <form action="profile" method="post">
        <h3 style="margin-top: 0; color: #0b1f38;">Update Profile</h3>
        <label>Monthly Net Income (₹):</label>
        <input type="number" name="income" value="${income}" step="0.01" required>
        <label>Essential Monthly Expenses (₹):</label>
        <input type="number" name="expenses" value="${expenses}" step="0.01" required>
        <label>Emergency Reserve Target (₹):</label>
        <input type="number" name="reserve" value="${emergency_reserve}" step="0.01" required>
        <button type="submit">Save Profile</button>
    </form>
</body>
</html>
"""
write_file("WebContent/profile.jsp", profile_jsp)

# 8. calculator.jsp
calculator_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head><title>EMI Calculator</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; text-align: center; margin: 0; padding: 0; }
    .header { background-color: #0b1f38; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
    form { width: 350px; margin: 30px auto; padding: 25px; background: white; border-radius: 8px; box-shadow: 0px 2px 8px rgba(0,0,0,0.06); text-align: left; }
    input { width: 92%; margin-bottom: 14px; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
    button { background-color: #008080; color: white; padding: 10px; width: 100%; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
    .result { margin: 20px auto; width: 350px; padding: 15px; background: white; border-radius: 8px; font-size: 1.2em; font-weight: bold; color: #008080; box-shadow: 0px 2px 8px rgba(0,0,0,0.06); }
</style>
</head>
<body>
    <div class="header">
        <h1>EMI Calculator</h1>
        <a href="dashboard" style="color: white; text-decoration: none;">Dashboard</a>
    </div>
    
    <form action="calculator" method="post">
        <h3 style="margin-top: 0; color: #0b1f38;">Calculate Loan EMI</h3>
        <input type="number" name="principal" placeholder="Principal Amount (₹)" step="0.01" required>
        <input type="number" name="interestRate" placeholder="Interest Rate (%)" step="0.01" required>
        <input type="number" name="tenureMonths" placeholder="Tenure (Months)" required>
        <button type="submit">Calculate EMI</button>
    </form>
    
    <c:if test="${not empty emiResult}">
        <div class="result">Monthly EMI: ₹${emiResult}</div>
    </c:if>
    <c:if test="${not empty error}">
        <div class="result" style="color:red;">Error: ${error}</div>
    </c:if>
</body>
</html>
"""
write_file("WebContent/calculator.jsp", calculator_jsp)

# 9. amortization.jsp
amortization_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head><title>Amortization Schedule</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; margin: 0; padding: 0; }
    .header { background-color: #0b1f38; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
    table { width: 90%; margin: 25px auto; border-collapse: collapse; background: white; box-shadow: 0px 2px 8px rgba(0,0,0,0.06); }
    th, td { padding: 10px; border: 1px solid #ccc; text-align: center; }
    th { background-color: #008080; color: white; }
</style>
</head>
<body>
    <div class="header">
        <h1>Amortization Schedule for ${loan.loanType} (ID: ${loan.id})</h1>
        <a href="loans" style="color: white; text-decoration: none;">Back to Loans</a>
    </div>

    <c:if test="${not empty schedule}">
        <table>
            <tr><th>Month</th><th>EMI</th><th>Interest</th><th>Principal Paid</th><th>Remaining Balance</th></tr>
            <c:forEach var="row" items="${schedule}">
                <tr>
                    <td>${row.month}</td><td>₹${row.emi}</td><td>₹${row.interest}</td>
                    <td>₹${row.principal}</td><td>₹${row.balance}</td>
                </tr>
            </c:forEach>
        </table>
    </c:if>
    <c:if test="${empty schedule}">
        <p align="center" style="margin-top: 30px;">Please select a valid loan from the Manage Loans page.</p>
    </c:if>
</body>
</html>
"""
write_file("WebContent/amortization.jsp", amortization_jsp)

# 10. login.jsp
login_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head><title>Login</title>
<style>
    body { font-family: Arial; background-color: #0b1f38; color: white; text-align: center; padding-top: 50px; }
    form { background-color: white; color: #0b1f38; padding: 25px; width: 320px; margin: auto; border-radius: 8px; box-shadow: 0px 4px 12px rgba(0,0,0,0.15); }
    input { margin-bottom: 12px; width: 90%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
    button { background-color: #008080; color: white; border: none; padding: 10px; width: 100%; cursor: pointer; border-radius: 4px; font-weight: bold; }
    button:hover { background-color: #006666; }
</style>
</head>
<body>
    <h2>Smart Loan Login</h2>
    <form action="login" method="post">
        <c:if test="${param.error == '1'}">
            <p style="color:red; font-size: 13px;">Invalid credentials. (Hint: use admin/admin)</p>
        </c:if>
        <c:if test="${param.registered == '1'}">
            <p style="color:green; font-size: 13px;">Registered successfully! Please login.</p>
        </c:if>
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="register.jsp" style="color:#008080;">Register here</a></p>
</body>
</html>
"""
write_file("WebContent/login.jsp", login_jsp)

# 11. register.jsp
register_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head><title>Register</title>
<style>
    body { font-family: Arial; background-color: #0b1f38; color: white; text-align: center; padding-top: 50px; }
    form { background-color: white; color: #0b1f38; padding: 25px; width: 320px; margin: auto; border-radius: 8px; box-shadow: 0px 4px 12px rgba(0,0,0,0.15); }
    input { margin-bottom: 12px; width: 90%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
    button { background-color: #008080; color: white; border: none; padding: 10px; width: 100%; cursor: pointer; border-radius: 4px; font-weight: bold; }
</style>
</head>
<body>
    <h2>Register Account</h2>
    <form action="register" method="post">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="login.jsp" style="color:#008080;">Login here</a></p>
</body>
</html>
"""
write_file("WebContent/register.jsp", register_jsp)

print("All previous working UI files successfully restored.")
