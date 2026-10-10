package com.smartloan.dao;

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
