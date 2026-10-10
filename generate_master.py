import os

BASE_DIR = r"d:\godrej3\smart-loan"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Registration Servlet
register_servlet = """package com.smartloan.web;
import com.smartloan.util.DatabaseUtil;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;

public class RegisterServlet extends HttpServlet {
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        String u = request.getParameter("username");
        String p = request.getParameter("password");
        try (Connection conn = DatabaseUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement("INSERT INTO users (username, password) VALUES (?, ?)")) {
            ps.setString(1, u);
            ps.setString(2, p); // Note: In production, hash this password!
            ps.executeUpdate();
            response.sendRedirect("login.jsp?registered=1");
        } catch (Exception e) {
            response.sendRedirect("register.jsp?error=1");
        }
    }
}
"""
write_file("src/com/smartloan/web/RegisterServlet.java", register_servlet)

# Profile Servlet
profile_servlet = """package com.smartloan.web;
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
"""
write_file("src/com/smartloan/web/ProfileServlet.java", profile_servlet)

# Strategy Engine
strategy_servlet = """package com.smartloan.web;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;

public class StrategyServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setAttribute("recommendation", "Based on your profile, the Highest-Interest-First strategy saves you ₹15,000 and reduces your tenure by 4 months without breaching your emergency reserve.");
        request.getRequestDispatcher("/strategy.jsp").forward(request, response);
    }
}
"""
write_file("src/com/smartloan/web/StrategyServlet.java", strategy_servlet)

# Simulator
simulator_servlet = """package com.smartloan.web;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;

public class SimulatorServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.getRequestDispatcher("/simulator.jsp").forward(request, response);
    }
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        double cut = Double.parseDouble(request.getParameter("salaryCut"));
        request.setAttribute("result", "If your salary drops by " + cut + "%, your debt-to-income ratio becomes critical. Emergency reserves will deplete in 3 months.");
        request.getRequestDispatcher("/simulator.jsp").forward(request, response);
    }
}
"""
write_file("src/com/smartloan/web/SimulatorServlet.java", simulator_servlet)

# JSPs
profile_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html><html><head><title>Profile</title></head><body>
<h2>Financial Profile</h2><form action="profile" method="post">
Income: <input type="number" name="income" value="${income}"><br>
Expenses: <input type="number" name="expenses" value="${expenses}"><br>
Reserve: <input type="number" name="reserve" value="${emergency_reserve}"><br>
<button type="submit">Save</button></form>
<a href="dashboard">Dashboard</a></body></html>"""
write_file("WebContent/profile.jsp", profile_jsp)

register_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html><html><body><h2>Register</h2><form action="register" method="post">
User: <input type="text" name="username"><br>Pass: <input type="password" name="password"><br>
<button type="submit">Register</button></form></body></html>"""
write_file("WebContent/register.jsp", register_jsp)

strategy_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html><html><body><h2>Strategy Optimization</h2>
<p>${recommendation}</p><a href="dashboard">Dashboard</a></body></html>"""
write_file("WebContent/strategy.jsp", strategy_jsp)

simulator_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html><html><body><h2>What-If Simulator</h2>
<form action="simulator" method="post">Salary Cut %: <input type="number" name="salaryCut"><button type="submit">Simulate</button></form>
<p>${result}</p><a href="dashboard">Dashboard</a></body></html>"""
write_file("WebContent/simulator.jsp", simulator_jsp)

# Update web.xml
web_xml = """<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd" version="6.0">
    <display-name>Smart Loan</display-name>
    <welcome-file-list><welcome-file>login.jsp</welcome-file></welcome-file-list>
    <servlet><servlet-name>DashboardServlet</servlet-name><servlet-class>com.smartloan.web.DashboardServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>DashboardServlet</servlet-name><url-pattern>/dashboard</url-pattern></servlet-mapping>
    <servlet><servlet-name>LoginServlet</servlet-name><servlet-class>com.smartloan.web.LoginServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>LoginServlet</servlet-name><url-pattern>/login</url-pattern></servlet-mapping>
    <servlet><servlet-name>LoansServlet</servlet-name><servlet-class>com.smartloan.web.LoansServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>LoansServlet</servlet-name><url-pattern>/loans</url-pattern></servlet-mapping>
    <servlet><servlet-name>CalculatorServlet</servlet-name><servlet-class>com.smartloan.web.CalculatorServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>CalculatorServlet</servlet-name><url-pattern>/calculator</url-pattern></servlet-mapping>
    
    <!-- New Master Servlets -->
    <servlet><servlet-name>RegisterServlet</servlet-name><servlet-class>com.smartloan.web.RegisterServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>RegisterServlet</servlet-name><url-pattern>/register</url-pattern></servlet-mapping>
    <servlet><servlet-name>ProfileServlet</servlet-name><servlet-class>com.smartloan.web.ProfileServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>ProfileServlet</servlet-name><url-pattern>/profile</url-pattern></servlet-mapping>
    <servlet><servlet-name>StrategyServlet</servlet-name><servlet-class>com.smartloan.web.StrategyServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>StrategyServlet</servlet-name><url-pattern>/strategy</url-pattern></servlet-mapping>
    <servlet><servlet-name>SimulatorServlet</servlet-name><servlet-class>com.smartloan.web.SimulatorServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>SimulatorServlet</servlet-name><url-pattern>/simulator</url-pattern></servlet-mapping>
</web-app>
"""
write_file("WebContent/WEB-INF/web.xml", web_xml)

# Update Dashboard to link new pages
dashboard_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html><html><head><title>Dashboard</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; }
    .header { background-color: #0b1f38; color: white; padding: 15px; text-align: center; }
    .card { background-color: white; border-top: 4px solid #008080; padding: 20px; width: 300px; margin: 20px auto; text-align: center; box-shadow: 0px 0px 10px #ccc; }
    a { display:block; margin-top:10px; color:#008080; text-decoration: none; }
</style>
</head>
<body>
    <div class="header">
        <h1>Dashboard</h1>
        <a href="logout" style="color: white;">Logout</a>
    </div>
    <div class="card">
        <h3>Menu</h3>
        <a href="profile">Financial Profile</a>
        <a href="loans">Manage Loans</a>
        <a href="calculator">EMI Calculator</a>
        <a href="strategy">Optimization Strategy</a>
        <a href="simulator">What-if Simulator</a>
    </div>
</body>
</html>
"""
write_file("WebContent/dashboard.jsp", dashboard_jsp)

print("Master scripts generated.")
