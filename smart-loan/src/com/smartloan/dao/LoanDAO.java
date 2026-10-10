package com.smartloan.dao;
import com.smartloan.model.Loan;
import com.smartloan.util.DatabaseUtil;
import java.sql.*;
import java.util.*;

public class LoanDAO {
    public void addLoan(Loan loan) {
        String sql = "INSERT INTO loans (user_id, loan_type, principal, interest_rate, tenure_months) VALUES (?, ?, ?, ?, ?)";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, loan.getUserId());
            ps.setString(2, loan.getLoanType());
            ps.setDouble(3, loan.getPrincipal());
            ps.setDouble(4, loan.getInterestRate());
            ps.setInt(5, loan.getTenureMonths());
            ps.executeUpdate();
        } catch (Exception e) { e.printStackTrace(); }
    }

    public List<Loan> getLoansByUser(int userId) {
        List<Loan> loans = new ArrayList<>();
        String sql = "SELECT * FROM loans WHERE user_id = ?";
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, userId);
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                Loan l = new Loan();
                l.setId(rs.getInt("id"));
                l.setUserId(rs.getInt("user_id"));
                l.setLoanType(rs.getString("loan_type"));
                l.setPrincipal(rs.getDouble("principal"));
                l.setInterestRate(rs.getDouble("interest_rate"));
                l.setTenureMonths(rs.getInt("tenure_months"));
                loans.add(l);
            }
        } catch (Exception e) { e.printStackTrace(); }
        return loans;
    }
}
