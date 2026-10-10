import os

BASE_DIR = r"d:\godrej3\smart-loan"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# LoanDAO
loan_dao = """package com.smartloan.dao;
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
"""
write_file("src/com/smartloan/dao/LoanDAO.java", loan_dao)

# LoansServlet
loans_servlet = """package com.smartloan.web;
import com.smartloan.dao.LoanDAO;
import com.smartloan.model.Loan;
import com.smartloan.model.User;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.util.List;

public class LoansServlet extends HttpServlet {
    private LoanDAO loanDAO = new LoanDAO();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect("login.jsp");
            return;
        }
        User u = (User) session.getAttribute("user");
        List<Loan> loans = loanDAO.getLoansByUser(u.getId());
        request.setAttribute("loans", loans);
        request.getRequestDispatcher("/loans.jsp").forward(request, response);
    }

    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect("login.jsp");
            return;
        }
        User u = (User) session.getAttribute("user");
        
        Loan loan = new Loan();
        loan.setUserId(u.getId());
        loan.setLoanType(request.getParameter("loanType"));
        loan.setPrincipal(Double.parseDouble(request.getParameter("principal")));
        loan.setInterestRate(Double.parseDouble(request.getParameter("interestRate")));
        loan.setTenureMonths(Integer.parseInt(request.getParameter("tenureMonths")));
        
        loanDAO.addLoan(loan);
        response.sendRedirect("loans");
    }
}
"""
write_file("src/com/smartloan/web/LoansServlet.java", loans_servlet)

# CalculatorServlet
calc_servlet = """package com.smartloan.web;
import com.smartloan.engine.LoanCalculator;
import com.smartloan.model.Loan;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;

public class CalculatorServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        try {
            Loan loan = new Loan();
            loan.setPrincipal(Double.parseDouble(request.getParameter("principal")));
            loan.setInterestRate(Double.parseDouble(request.getParameter("interestRate")));
            loan.setTenureMonths(Integer.parseInt(request.getParameter("tenureMonths")));
            
            double emi = LoanCalculator.calculateEMI(loan);
            request.setAttribute("emiResult", String.format("%.2f", emi));
        } catch (Exception e) {
            request.setAttribute("error", e.getMessage());
        }
        request.getRequestDispatcher("/calculator.jsp").forward(request, response);
    }
    
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.getRequestDispatcher("/calculator.jsp").forward(request, response);
    }
}
"""
write_file("src/com/smartloan/web/CalculatorServlet.java", calc_servlet)

# JSPs
loans_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html>
<html>
<head><title>My Loans</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; }
    .header { background-color: #0b1f38; color: white; padding: 15px; text-align: center; }
    table { width: 80%; margin: 20px auto; border-collapse: collapse; }
    th, td { padding: 10px; border: 1px solid #ccc; text-align: center; }
    th { background-color: #008080; color: white; }
    form { width: 300px; margin: 20px auto; padding: 20px; background: white; box-shadow: 0px 0px 5px #ccc; }
    input { width: 90%; margin-bottom: 10px; padding: 5px; }
    button { background-color: #0b1f38; color: white; padding: 8px; width: 100%; border: none; }
</style>
</head>
<body>
    <div class="header">
        <h1>Manage Loans</h1>
        <a href="dashboard" style="color: #008080;">Back to Dashboard</a>
    </div>
    
    <form action="loans" method="post">
        <h3>Add New Loan</h3>
        <input type="text" name="loanType" placeholder="Loan Type (e.g. Home, Auto)" required>
        <input type="number" name="principal" placeholder="Principal Amount" step="0.01" required>
        <input type="number" name="interestRate" placeholder="Interest Rate (%)" step="0.01" required>
        <input type="number" name="tenureMonths" placeholder="Tenure (Months)" required>
        <button type="submit">Add Loan</button>
    </form>

    <table>
        <tr><th>ID</th><th>Type</th><th>Principal</th><th>Rate</th><th>Months</th></tr>
        <c:forEach var="loan" items="${loans}">
            <tr>
                <td>${loan.id}</td>
                <td>${loan.loanType}</td>
                <td>${loan.principal}</td>
                <td>${loan.interestRate}%</td>
                <td>${loan.tenureMonths}</td>
            </tr>
        </c:forEach>
    </table>
</body>
</html>
"""
write_file("WebContent/loans.jsp", loans_jsp)

calc_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head><title>EMI Calculator</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; text-align: center; }
    .header { background-color: #0b1f38; color: white; padding: 15px; }
    form { width: 300px; margin: 20px auto; padding: 20px; background: white; box-shadow: 0px 0px 5px #ccc; }
    input { width: 90%; margin-bottom: 10px; padding: 5px; }
    button { background-color: #008080; color: white; padding: 8px; width: 100%; border: none; }
    .result { margin-top: 20px; font-size: 1.2em; font-weight: bold; color: #008080; }
</style>
</head>
<body>
    <div class="header">
        <h1>EMI Calculator</h1>
        <a href="dashboard" style="color: #008080;">Dashboard</a>
    </div>
    
    <form action="calculator" method="post">
        <input type="number" name="principal" placeholder="Principal Amount" step="0.01" required>
        <input type="number" name="interestRate" placeholder="Interest Rate (%)" step="0.01" required>
        <input type="number" name="tenureMonths" placeholder="Tenure (Months)" required>
        <button type="submit">Calculate EMI</button>
    </form>
    
    <c:if test="${not empty emiResult}">
        <div class="result">Your Monthly EMI: ₹${emiResult}</div>
    </c:if>
    <c:if test="${not empty error}">
        <div class="result" style="color:red;">Error: ${error}</div>
    </c:if>
</body>
</html>
"""
write_file("WebContent/calculator.jsp", calc_jsp)

# Update web.xml to include new servlets
web_xml = """<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd"
         version="6.0">
    <display-name>Smart Loan</display-name>
    <welcome-file-list>
        <welcome-file>login.jsp</welcome-file>
    </welcome-file-list>
    
    <servlet><servlet-name>DashboardServlet</servlet-name><servlet-class>com.smartloan.web.DashboardServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>DashboardServlet</servlet-name><url-pattern>/dashboard</url-pattern></servlet-mapping>
    
    <servlet><servlet-name>LoginServlet</servlet-name><servlet-class>com.smartloan.web.LoginServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>LoginServlet</servlet-name><url-pattern>/login</url-pattern></servlet-mapping>

    <servlet><servlet-name>LoansServlet</servlet-name><servlet-class>com.smartloan.web.LoansServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>LoansServlet</servlet-name><url-pattern>/loans</url-pattern></servlet-mapping>

    <servlet><servlet-name>CalculatorServlet</servlet-name><servlet-class>com.smartloan.web.CalculatorServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>CalculatorServlet</servlet-name><url-pattern>/calculator</url-pattern></servlet-mapping>
</web-app>
"""
write_file("WebContent/WEB-INF/web.xml", web_xml)

print("Java files generated for full functionality.")
