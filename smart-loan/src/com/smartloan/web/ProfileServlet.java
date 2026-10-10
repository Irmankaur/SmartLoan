package com.smartloan.web;
import com.smartloan.model.User;
import com.smartloan.util.DatabaseUtil;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class ProfileServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) { response.sendRedirect("login.jsp"); return; }
        User u = (User) session.getAttribute("user");
        
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT income, expenses, emergency_reserve FROM users WHERE id=?")) {
            ps.setInt(1, u.getId());
            ResultSet rs = ps.executeQuery();
            if(rs.next()) {
                request.setAttribute("income", rs.getDouble("income"));
                request.setAttribute("expenses", rs.getDouble("expenses"));
                request.setAttribute("emergency_reserve", rs.getDouble("emergency_reserve"));
            }
        } catch (Exception e) {}
        
        request.getRequestDispatcher("/profile.jsp").forward(request, response);
    }
    
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        User u = (User) session.getAttribute("user");
        double inc = Double.parseDouble(request.getParameter("income"));
        double exp = Double.parseDouble(request.getParameter("expenses"));
        double res = Double.parseDouble(request.getParameter("reserve"));
        
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement("UPDATE users SET income=?, expenses=?, emergency_reserve=? WHERE id=?")) {
            ps.setDouble(1, inc);
            ps.setDouble(2, exp);
            ps.setDouble(3, res);
            ps.setInt(4, u.getId());
            ps.executeUpdate();
        } catch (Exception e) {}
        response.sendRedirect("profile");
    }
}
