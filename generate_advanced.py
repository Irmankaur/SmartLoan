import os

BASE_DIR = r"d:\godrej3\smart-loan"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Calculator & Strategy
calculator = """package com.smartloan.engine;
import com.smartloan.model.Loan;
import com.smartloan.exception.InvalidLoanException;
import java.util.*;

public class LoanCalculator {
    public static double calculateEMI(Loan loan) throws InvalidLoanException {
        if(loan.getPrincipal() <= 0) throw new InvalidLoanException("Principal must be > 0");
        double p = loan.getPrincipal();
        double r = loan.getInterestRate() / 1200.0;
        int n = loan.getTenureMonths();
        if(r == 0) return p / n;
        return (p * r * Math.pow(1 + r, n)) / (Math.pow(1 + r, n) - 1);
    }

    public static List<Map<String, Double>> generateAmortizationSchedule(Loan loan) {
        List<Map<String, Double>> schedule = new ArrayList<>();
        // Logic for schedule goes here
        return schedule;
    }
}
"""
write_file("src/com/smartloan/engine/LoanCalculator.java", calculator)

strategy = """package com.smartloan.engine;
import com.smartloan.model.Loan;
import java.util.*;

public interface RepaymentStrategy {
    void sortLoans(List<Loan> loans);
}

class HighestInterestFirst implements RepaymentStrategy {
    @Override
    public void sortLoans(List<Loan> loans) {
        loans.sort((l1, l2) -> Double.compare(l2.getInterestRate(), l1.getInterestRate()));
    }
}

class SmallestBalanceFirst implements RepaymentStrategy {
    @Override
    public void sortLoans(List<Loan> loans) {
        loans.sort(Comparator.comparingDouble(Loan::getPrincipal));
    }
}
"""
write_file("src/com/smartloan/engine/RepaymentStrategy.java", strategy)

# Risk scoring
risk_score = """package com.smartloan.engine;
public class RiskAnalyzer {
    public static String assessRisk(double debt, double income) {
        if (income == 0) return "HIGH RISK";
        double ratio = debt / income;
        if(ratio > 0.5) return "HIGH RISK";
        if(ratio > 0.3) return "MEDIUM RISK";
        return "LOW RISK (Estimate)";
    }
}
"""
write_file("src/com/smartloan/engine/RiskAnalyzer.java", risk_score)

print("Java files generated for advanced features.")
