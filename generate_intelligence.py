import os

BASE_DIR = r"d:\godrej3\smart-loan"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# ==========================================
# 1. Update User Model & Loan Model
# ==========================================
user_model = """package com.smartloan.model;

public class User {
    private int id;
    private String username;
    private String password;
    private double income;
    private double expenses;
    private double emergencyReserve;

    public User() {}

    public User(int id, String username, String password, double income, double expenses, double emergencyReserve) {
        this.id = id;
        this.username = username;
        this.password = password;
        this.income = income;
        this.expenses = expenses;
        this.emergencyReserve = emergencyReserve;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public double getIncome() { return income; }
    public void setIncome(double income) { this.income = income; }
    public double getExpenses() { return expenses; }
    public void setExpenses(double expenses) { this.expenses = expenses; }
    public double getEmergencyReserve() { return emergencyReserve; }
    public void setEmergencyReserve(double emergencyReserve) { this.emergencyReserve = emergencyReserve; }
}
"""
write_file("src/com/smartloan/model/User.java", user_model)

loan_model = """package com.smartloan.model;

public class Loan {
    private int id;
    private int userId;
    private String loanType;
    private double principal;
    private double interestRate;
    private int tenureMonths;

    public Loan() {}

    public Loan(int id, int userId, String loanType, double principal, double interestRate, int tenureMonths) {
        this.id = id;
        this.userId = userId;
        this.loanType = loanType;
        this.principal = principal;
        this.interestRate = interestRate;
        this.tenureMonths = tenureMonths;
    }

    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public int getUserId() { return userId; }
    public void setUserId(int userId) { this.userId = userId; }
    public String getLoanType() { return loanType; }
    public void setLoanType(String loanType) { this.loanType = loanType; }
    public double getPrincipal() { return principal; }
    public void setPrincipal(double principal) { this.principal = principal; }
    public double getInterestRate() { return interestRate; }
    public void setInterestRate(double interestRate) { this.interestRate = interestRate; }
    public int getTenureMonths() { return tenureMonths; }
    public void setTenureMonths(int tenureMonths) { this.tenureMonths = tenureMonths; }

    public double calculateEMI() {
        if (principal <= 0 || tenureMonths <= 0) return 0;
        if (interestRate <= 0) return principal / tenureMonths;
        double r = interestRate / 1200.0;
        return (principal * r * Math.pow(1 + r, tenureMonths)) / (Math.pow(1 + r, tenureMonths) - 1);
    }

    public double calculateTotalInterest() {
        double emi = calculateEMI();
        return (emi * tenureMonths) - principal;
    }
}
"""
write_file("src/com/smartloan/model/Loan.java", loan_model)

# ==========================================
# 2. Update UserDAO
# ==========================================
user_dao = """package com.smartloan.dao;

import com.smartloan.model.User;
import com.smartloan.util.DatabaseUtil;
import java.sql.*;

public class UserDAO {
    public User login(String username, String password) {
        String sql = "SELECT * FROM users WHERE username=? AND password=?";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setString(1, username);
            ps.setString(2, password);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) {
                User u = new User();
                u.setId(rs.getInt("id"));
                u.setUsername(rs.getString("username"));
                u.setPassword(rs.getString("password"));
                u.setIncome(rs.getDouble("income"));
                u.setExpenses(rs.getDouble("expenses"));
                u.setEmergencyReserve(rs.getDouble("emergency_reserve"));
                return u;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public User getUserById(int userId) {
        String sql = "SELECT * FROM users WHERE id=?";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, userId);
            ResultSet rs = ps.executeQuery();
            if (rs.next()) {
                User u = new User();
                u.setId(rs.getInt("id"));
                u.setUsername(rs.getString("username"));
                u.setPassword(rs.getString("password"));
                u.setIncome(rs.getDouble("income"));
                u.setExpenses(rs.getDouble("expenses"));
                u.setEmergencyReserve(rs.getDouble("emergency_reserve"));
                return u;
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return null;
    }

    public boolean updateProfile(int userId, double income, double expenses, double emergencyReserve) {
        String sql = "UPDATE users SET income=?, expenses=?, emergency_reserve=? WHERE id=?";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setDouble(1, income);
            ps.setDouble(2, expenses);
            ps.setDouble(3, emergencyReserve);
            ps.setInt(4, userId);
            return ps.executeUpdate() > 0;
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }
}
"""
write_file("src/com/smartloan/dao/UserDAO.java", user_dao)

# ==========================================
# 3. Calculation & Financial Intelligence Engine
# ==========================================
financial_engine = """package com.smartloan.engine;

import com.smartloan.model.Loan;
import com.smartloan.model.User;
import java.util.*;

public class FinancialIntelligenceService {

    public static double getTotalDebt(List<Loan> loans) {
        double total = 0;
        if (loans != null) {
            for (Loan l : loans) total += l.getPrincipal();
        }
        return total;
    }

    public static double getTotalMonthlyEMI(List<Loan> loans) {
        double total = 0;
        if (loans != null) {
            for (Loan l : loans) total += l.calculateEMI();
        }
        return total;
    }

    public static class AmortizationResult {
        public int monthsTaken;
        public double totalInterestPaid;
        public double totalAmountPaid;
        public double interestSaved;
        public int monthsSaved;

        public AmortizationResult(int monthsTaken, double totalInterestPaid, double totalAmountPaid, double interestSaved, int monthsSaved) {
            this.monthsTaken = monthsTaken;
            this.totalInterestPaid = totalInterestPaid;
            this.totalAmountPaid = totalAmountPaid;
            this.interestSaved = interestSaved;
            this.monthsSaved = monthsSaved;
        }
    }

    public static AmortizationResult calculatePrepaymentBenefit(Loan loan, double extraMonthlyPayment) {
        double principal = loan.getPrincipal();
        double annualRate = loan.getInterestRate();
        int originalTenure = loan.getTenureMonths();
        double baseEMI = loan.calculateEMI();
        double baseTotalInterest = (baseEMI * originalTenure) - principal;

        if (extraMonthlyPayment <= 0) {
            return new AmortizationResult(originalTenure, baseTotalInterest, baseEMI * originalTenure, 0, 0);
        }

        double r = annualRate / 1200.0;
        double balance = principal;
        double totalInterest = 0;
        int months = 0;

        while (balance > 0.01 && months < 600) {
            months++;
            double interestForMonth = (r > 0) ? (balance * r) : 0;
            double regularPrincipal = (r > 0) ? (baseEMI - interestForMonth) : (principal / originalTenure);
            double totalPrincipalPaid = regularPrincipal + extraMonthlyPayment;

            if (totalPrincipalPaid > balance) {
                totalPrincipalPaid = balance;
                interestForMonth = (r > 0) ? (balance * r) : 0;
                totalInterest += interestForMonth;
                balance = 0;
                break;
            }

            totalInterest += interestForMonth;
            balance -= totalPrincipalPaid;
        }

        double totalPaid = principal + totalInterest;
        double interestSaved = Math.max(0, baseTotalInterest - totalInterest);
        int monthsSaved = Math.max(0, originalTenure - months);

        return new AmortizationResult(months, totalInterest, totalPaid, interestSaved, monthsSaved);
    }

    public static class PrepaymentOptimizationPlan {
        public Loan recommendedLoan;
        public double proposedAmount;
        public double safeSurplus;
        public double emergencyReserveRetained;
        public double reserveCoverageMonths;
        public double interestSavings;
        public int tenureMonthsSaved;
        public String priorityReason;
        public String whyThisLoan;
        public String alternativeComparison;
        public List<StrategyComparisonItem> strategyComparisons = new ArrayList<>();
    }

    public static class StrategyComparisonItem {
        public String strategyName;
        public String targetLoanName;
        public double interestSaved;
        public int monthsSaved;
        public double remainingTotalInterest;
        public String pros;
        public String cons;
        public boolean isRecommended;

        public StrategyComparisonItem(String strategyName, String targetLoanName, double interestSaved, int monthsSaved, double remainingTotalInterest, String pros, String cons, boolean isRecommended) {
            this.strategyName = strategyName;
            this.targetLoanName = targetLoanName;
            this.interestSaved = interestSaved;
            this.monthsSaved = monthsSaved;
            this.remainingTotalInterest = remainingTotalInterest;
            this.pros = pros;
            this.cons = cons;
            this.isRecommended = isRecommended;
        }
    }

    public static PrepaymentOptimizationPlan evaluatePrepayment(User user, List<Loan> loans, double requestedSurplus) {
        PrepaymentOptimizationPlan plan = new PrepaymentOptimizationPlan();

        double income = (user != null) ? user.getIncome() : 0;
        double expenses = (user != null) ? user.getExpenses() : 0;
        double totalEMI = getTotalMonthlyEMI(loans);
        double emergencyReserve = (user != null) ? user.getEmergencyReserve() : 0;

        double monthlyFreeCash = Math.max(0, income - expenses - totalEMI);
        double actualSurplusToUse = requestedSurplus > 0 ? requestedSurplus : monthlyFreeCash;
        plan.safeSurplus = actualSurplusToUse;
        plan.emergencyReserveRetained = emergencyReserve;
        plan.reserveCoverageMonths = expenses > 0 ? (emergencyReserve / expenses) : 0;

        if (loans == null || loans.isEmpty()) {
            plan.whyThisLoan = "You do not have any active loans recorded. Add your loans to generate an intelligent prepayment plan.";
            return plan;
        }

        List<Loan> avalancheList = new ArrayList<>(loans);
        avalancheList.sort((l1, l2) -> Double.compare(l2.getInterestRate(), l1.getInterestRate()));
        Loan highestInterestLoan = avalancheList.get(0);

        List<Loan> snowballList = new ArrayList<>(loans);
        snowballList.sort(Comparator.comparingDouble(Loan::getPrincipal));
        Loan smallestBalanceLoan = snowballList.get(0);

        AmortizationResult avalancheResult = calculatePrepaymentBenefit(highestInterestLoan, actualSurplusToUse);
        AmortizationResult snowballResult = calculatePrepaymentBenefit(smallestBalanceLoan, actualSurplusToUse);

        plan.recommendedLoan = highestInterestLoan;
        plan.proposedAmount = actualSurplusToUse;
        plan.interestSavings = avalancheResult.interestSaved;
        plan.tenureMonthsSaved = avalancheResult.monthsSaved;

        StringBuilder why = new StringBuilder();
        why.append("We recommend allocating Rs. ").append(String.format("%,.2f", actualSurplusToUse))
           .append(" extra every month toward your '").append(highestInterestLoan.getLoanType())
           .append(" (ID: ").append(highestInterestLoan.getId()).append(")' because it carries your highest annual interest rate of ")
           .append(highestInterestLoan.getInterestRate()).append("%.\n\n")
           .append("• Why this loan: In lending math, every extra Rupee applied to a higher-rate loan extinguishes debt that is compounding the fastest. ")
           .append("This saves you Rs. ").append(String.format("%,.2f", avalancheResult.interestSaved))
           .append(" in interest charges and clears this debt ").append(avalancheResult.monthsSaved).append(" months earlier.\n")
           .append("• Impact on liquidity: Your emergency fund of Rs. ").append(String.format("%,.2f", emergencyReserve))
           .append(" is preserved intact, maintaining ").append(String.format("%.1f", plan.reserveCoverageMonths))
           .append(" months of essential expense coverage.\n");

        if (loans.size() > 1 && !highestInterestLoan.equals(smallestBalanceLoan)) {
            why.append("• Why not '").append(smallestBalanceLoan.getLoanType()).append(" (ID: ").append(smallestBalanceLoan.getId()).append(")': ")
               .append("Although it has the smallest balance (Rs. ").append(String.format("%,.2f", smallestBalanceLoan.getPrincipal()))
               .append("), its interest rate is ").append(smallestBalanceLoan.getInterestRate()).append("% vs ").append(highestInterestLoan.getInterestRate())
               .append("%. Paying it first (Snowball method) would save Rs. ").append(String.format("%,.2f", snowballResult.interestSaved))
               .append(" in interest—which is Rs. ").append(String.format("%,.2f", (avalancheResult.interestSaved - snowballResult.interestSaved)))
               .append(" less savings than Avalanche.");
        }

        plan.whyThisLoan = why.toString();

        plan.strategyComparisons.add(new StrategyComparisonItem(
            "Debt Avalanche (Recommended)",
            highestInterestLoan.getLoanType() + " (" + highestInterestLoan.getInterestRate() + "%)",
            avalancheResult.interestSaved,
            avalancheResult.monthsSaved,
            avalancheResult.totalInterestPaid,
            "Maximizes total interest savings by eliminating the costliest debt first.",
            "Requires patience if the highest-rate loan also has a large principal.",
            true
        ));

        plan.strategyComparisons.add(new StrategyComparisonItem(
            "Debt Snowball",
            smallestBalanceLoan.getLoanType() + " (Rs. " + String.format("%,.0f", smallestBalanceLoan.getPrincipal()) + ")",
            snowballResult.interestSaved,
            snowballResult.monthsSaved,
            snowballResult.totalInterestPaid,
            "Delivers quick psychological wins by clearing smaller loans faster.",
            "Higher total interest paid overall compared to Avalanche.",
            false
        ));

        plan.strategyComparisons.add(new StrategyComparisonItem(
            "Balanced Strategy (50% Prepay / 50% Emergency Reserve)",
            highestInterestLoan.getLoanType(),
            avalancheResult.interestSaved * 0.55,
            (int)(avalancheResult.monthsSaved * 0.6),
            avalancheResult.totalInterestPaid + (avalancheResult.interestSaved * 0.45),
            "Builds emergency liquidity while still chipping away at expensive debt.",
            "Moderate interest savings and longer tenure than pure Avalanche.",
            false
        ));

        plan.strategyComparisons.add(new StrategyComparisonItem(
            "Minimum Payment Baseline",
            "None (Contractual EMIs only)",
            0.0,
            0,
            getTotalMonthlyEMI(loans) * 12 * 5,
            "Zero extra strain on immediate monthly cash flow.",
            "Maximum interest paid over time; maximum repayment tenure.",
            false
        ));

        return plan;
    }

    public static class RiskEvaluation {
        public int score;
        public String category;
        public double dtiRatio;
        public double emiToIncomeRatio;
        public double reserveCoverageMonths;
        public double freeCashFlow;
        public List<String> protectiveFactors = new ArrayList<>();
        public List<String> riskFactors = new ArrayList<>();
        public List<String> recommendations = new ArrayList<>();
        public String plainEnglishSummary;
    }

    public static RiskEvaluation evaluateRisk(User user, List<Loan> loans) {
        RiskEvaluation eval = new RiskEvaluation();
        double income = (user != null) ? user.getIncome() : 0;
        double expenses = (user != null) ? user.getExpenses() : 0;
        double totalDebt = getTotalDebt(loans);
        double totalEMI = getTotalMonthlyEMI(loans);
        double emergencyReserve = (user != null) ? user.getEmergencyReserve() : 0;

        eval.freeCashFlow = income - expenses - totalEMI;
        eval.emiToIncomeRatio = (income > 0) ? (totalEMI / income) * 100 : 0;
        eval.dtiRatio = (income > 0) ? (totalDebt / (income * 12)) * 100 : 0;
        eval.reserveCoverageMonths = (expenses > 0) ? (emergencyReserve / expenses) : 0;

        int score = 100;

        if (eval.emiToIncomeRatio > 50) {
            score -= 35;
            eval.riskFactors.add("Critical EMI Burden: Your monthly EMIs consume " + String.format("%.1f", eval.emiToIncomeRatio) + "% of your net income (recommended < 35%).");
        } else if (eval.emiToIncomeRatio > 35) {
            score -= 20;
            eval.riskFactors.add("Elevated EMI Burden: Your monthly EMIs take " + String.format("%.1f", eval.emiToIncomeRatio) + "% of your net income.");
        } else {
            eval.protectiveFactors.add("Safe EMI Ratio: Your monthly EMIs take only " + String.format("%.1f", eval.emiToIncomeRatio) + "% of income.");
        }

        if (eval.reserveCoverageMonths < 1.0) {
            score -= 30;
            eval.riskFactors.add("Vulnerable Liquidity: Your emergency reserve covers only " + String.format("%.1f", eval.reserveCoverageMonths) + " months of living expenses (recommended: 3-6 months).");
        } else if (eval.reserveCoverageMonths < 3.0) {
            score -= 15;
            eval.riskFactors.add("Moderate Emergency Buffer: Emergency reserve covers " + String.format("%.1f", eval.reserveCoverageMonths) + " months.");
        } else {
            eval.protectiveFactors.add("Strong Safety Cushion: Emergency savings cover " + String.format("%.1f", eval.reserveCoverageMonths) + " months of essential expenses.");
        }

        if (eval.freeCashFlow < 0) {
            score -= 35;
            eval.riskFactors.add("Monthly Cash Deficit: You are spending Rs. " + String.format("%,.2f", Math.abs(eval.freeCashFlow)) + " more each month than you earn!");
        } else if (eval.freeCashFlow < 5000) {
            score -= 10;
            eval.riskFactors.add("Tight Monthly Cushion: Free cash flow is only Rs. " + String.format("%,.2f", eval.freeCashFlow) + " per month.");
        } else {
            eval.protectiveFactors.add("Healthy Positive Cash Flow: You retain Rs. " + String.format("%,.2f", eval.freeCashFlow) + " surplus every month.");
        }

        if (score < 0) score = 0;
        eval.score = score;

        if (score >= 80) {
            eval.category = "Low Risk (Healthy & Resilient)";
        } else if (score >= 60) {
            eval.category = "Moderate Risk (Manageable with Care)";
        } else if (score >= 40) {
            eval.category = "High Risk (Vulnerable to Shocks)";
        } else {
            eval.category = "Critical Risk (Immediate Action Required)";
        }

        if (eval.reserveCoverageMonths < 3) {
            eval.recommendations.add("Build your emergency reserve to at least Rs. " + String.format("%,.0f", expenses * 3) + " before initiating aggressive loan prepayments.");
        }
        if (eval.freeCashFlow > 5000 && !loans.isEmpty()) {
            eval.recommendations.add("Direct a portion of your Rs. " + String.format("%,.0f", eval.freeCashFlow) + " monthly surplus toward the highest-interest loan using Debt Avalanche.");
        }
        if (eval.emiToIncomeRatio > 40) {
            eval.recommendations.add("Avoid taking on any new loans or credit card debt until your EMI burden drops below 35%.");
        }
        if (eval.recommendations.isEmpty()) {
            eval.recommendations.add("Maintain your current repayment discipline and consider investing surplus cash flow.");
        }

        eval.plainEnglishSummary = "Your financial health is currently rated at " + eval.score + "/100 (" + eval.category + "). "
            + "Out of every Rs. 100 you take home, Rs. " + String.format("%.0f", eval.emiToIncomeRatio) + " is locked into loan EMIs and Rs. "
            + String.format("%.0f", (expenses / (income > 0 ? income : 1)) * 100) + " goes toward essential expenses, leaving Rs. "
            + String.format("%.0f", (eval.freeCashFlow / (income > 0 ? income : 1)) * 100) + " as uncommitted surplus.";

        return eval;
    }

    public static class SimulationResult {
        public double originalIncome;
        public double simulatedIncome;
        public double originalCashFlow;
        public double simulatedCashFlow;
        public double simulatedDeficit;
        public double emergencyReserve;
        public double monthsUntilDepletion;
        public double simulatedTotalEMI;
        public double simulatedEMIBurdenPercent;
        public String narrativeAnalysis;
        public String actionRecommendation;
    }

    public static SimulationResult runSimulation(User user, List<Loan> loans, double salaryCutPercent, int jobLossMonths, double emergencyExpense, double rateHikePercent) {
        SimulationResult res = new SimulationResult();
        double baseIncome = (user != null) ? user.getIncome() : 0;
        double baseExpenses = (user != null) ? user.getExpenses() : 0;
        double baseReserve = (user != null) ? user.getEmergencyReserve() : 0;
        double totalEMI = getTotalMonthlyEMI(loans);

        res.originalIncome = baseIncome;
        res.originalCashFlow = baseIncome - baseExpenses - totalEMI;
        res.emergencyReserve = Math.max(0, baseReserve - emergencyExpense);

        double incomeAfterCut = baseIncome * (1.0 - (salaryCutPercent / 100.0));
        if (jobLossMonths > 0) {
            incomeAfterCut = 0;
        }
        res.simulatedIncome = incomeAfterCut;

        double simEMI = 0;
        if (loans != null) {
            for (Loan l : loans) {
                Loan simLoan = new Loan(l.getId(), l.getUserId(), l.getLoanType(), l.getPrincipal(), l.getInterestRate() + rateHikePercent, l.getTenureMonths());
                simEMI += simLoan.calculateEMI();
            }
        }
        res.simulatedTotalEMI = simEMI;
        res.simulatedCashFlow = res.simulatedIncome - baseExpenses - simEMI;

        if (res.simulatedCashFlow < 0) {
            res.simulatedDeficit = Math.abs(res.simulatedCashFlow);
            res.monthsUntilDepletion = (res.simulatedDeficit > 0) ? (res.emergencyReserve / res.simulatedDeficit) : 0;
        } else {
            res.simulatedDeficit = 0;
            res.monthsUntilDepletion = 999;
        }

        res.simulatedEMIBurdenPercent = (res.simulatedIncome > 0) ? (simEMI / res.simulatedIncome) * 100 : 100;

        StringBuilder sb = new StringBuilder();
        sb.append("Under this scenario:\\n");
        if (salaryCutPercent > 0) {
            sb.append("• Salary drops by ").append(salaryCutPercent).append("%, reducing monthly income from Rs. ")
              .append(String.format("%,.2f", baseIncome)).append(" to Rs. ").append(String.format("%,.2f", res.simulatedIncome)).append(".\\n");
        }
        if (rateHikePercent > 0) {
            sb.append("• Interest rate increases by ").append(rateHikePercent).append("%, raising total monthly EMI burden from Rs. ")
              .append(String.format("%,.2f", totalEMI)).append(" to Rs. ").append(String.format("%,.2f", simEMI)).append(".\\n");
        }
        if (emergencyExpense > 0) {
            sb.append("• A one-time unexpected expense of Rs. ").append(String.format("%,.2f", emergencyExpense))
              .append(" reduces your emergency reserves to Rs. ").append(String.format("%,.2f", res.emergencyReserve)).append(".\\n");
        }

        if (res.simulatedCashFlow < 0) {
            sb.append("• Resulting Impact: Your cash flow turns negative with a monthly shortfall of Rs. ")
              .append(String.format("%,.2f", res.simulatedDeficit)).append(". ");
            if (res.monthsUntilDepletion < 999) {
                sb.append("At this burn rate, your remaining emergency reserve will be completely depleted in approximately ")
                  .append(String.format("%.1f", res.monthsUntilDepletion)).append(" months.");
            }
            res.actionRecommendation = "Action Plan: Halt extra loan prepayments immediately. Trim discretionary spending and speak to your lender about tenure extensions if this stress lasts longer than " + String.format("%.0f", res.monthsUntilDepletion) + " months.";
        } else {
            sb.append("• Resulting Impact: Your finances remain solvent with a positive monthly surplus of Rs. ")
              .append(String.format("%,.2f", res.simulatedCashFlow)).append(". Your emergency fund remains intact.");
            res.actionRecommendation = "Action Plan: Your financial buffer can comfortably absorb this shock without risking loan default.";
        }

        res.narrativeAnalysis = sb.toString();
        return res;
    }
}
"""
write_file("src/com/smartloan/engine/FinancialIntelligenceService.java", financial_engine)

print("Java engine code escaped and updated.")
