package com.smartloan.engine;
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
