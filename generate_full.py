import os

BASE_DIR = r"d:\godrej3\smart-loan"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Exception
exception_java = """package com.smartloan.exception;
public class InvalidLoanException extends Exception {
    public InvalidLoanException(String message) { super(message); }
}
"""
write_file("src/com/smartloan/exception/InvalidLoanException.java", exception_java)

# Thread example
thread_java = """package com.smartloan.engine;
public class SimulationEngine implements Runnable {
    private final Object lock = new Object();
    private boolean ready = false;
    @Override
    public void run() {
        synchronized(lock) {
            try {
                while(!ready) { lock.wait(1000); break; }
            } catch (InterruptedException e) { Thread.currentThread().interrupt(); }
        }
    }
}
"""
write_file("src/com/smartloan/engine/SimulationEngine.java", thread_java)

# DAO expansion
user_dao = """package com.smartloan.dao;
import com.smartloan.model.User;
import com.smartloan.util.DatabaseUtil;
import java.sql.*;
import java.util.*;
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
                return u;
            }
        } catch (Exception e) { e.printStackTrace(); }
        return null;
    }
}
"""
write_file("src/com/smartloan/dao/UserDAO.java", user_dao)

# Dashboard Servlet Update
dashboard_servlet = """package com.smartloan.web;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;

public class DashboardServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) {
            response.sendRedirect("login.jsp");
            return;
        }
        request.setAttribute("totalDebt", 100000.00); // Mocked for now due to DB limit
        request.getRequestDispatcher("/dashboard.jsp").forward(request, response);
    }
}
"""
write_file("src/com/smartloan/web/DashboardServlet.java", dashboard_servlet)

# login.jsp
login_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head><title>Login</title>
<style>
    body { font-family: Arial; background-color: #0b1f38; color: white; text-align: center; padding-top: 50px; }
    form { background-color: white; color: #0b1f38; padding: 20px; width: 300px; margin: auto; border-radius: 8px; }
    input { margin-bottom: 10px; width: 90%; padding: 8px; }
    button { background-color: #008080; color: white; border: none; padding: 10px; width: 100%; cursor: pointer; }
</style>
</head>
<body>
    <h2>Smart Loan Login</h2>
    <form action="login" method="post">
        <input type="text" name="username" placeholder="Username" required><br>
        <input type="password" name="password" placeholder="Password" required><br>
        <button type="submit">Login</button>
    </form>
</body>
</html>
"""
write_file("WebContent/login.jsp", login_jsp)

# dashboard.jsp
dashboard_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>
<head><title>Dashboard</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; }
    .header { background-color: #0b1f38; color: white; padding: 15px; text-align: center; }
    .card { background-color: white; border-top: 4px solid #008080; padding: 20px; width: 300px; margin: 20px auto; text-align: center; box-shadow: 0px 0px 10px #ccc; }
</style>
</head>
<body>
    <div class="header">
        <h1>Dashboard</h1>
        <a href="logout" style="color: #008080;">Logout</a>
    </div>
    <div class="card">
        <h3>Total Debt</h3>
        <h2>₹${totalDebt}</h2>
    </div>
</body>
</html>
"""
write_file("WebContent/dashboard.jsp", dashboard_jsp)

web_xml = """<?xml version="1.0" encoding="UTF-8"?>
<web-app xmlns="https://jakarta.ee/xml/ns/jakartaee"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="https://jakarta.ee/xml/ns/jakartaee https://jakarta.ee/xml/ns/jakartaee/web-app_6_0.xsd"
         version="6.0">
    <display-name>Smart Loan</display-name>
    <welcome-file-list>
        <welcome-file>login.jsp</welcome-file>
    </welcome-file-list>
    
    <servlet>
        <servlet-name>DashboardServlet</servlet-name>
        <servlet-class>com.smartloan.web.DashboardServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>DashboardServlet</servlet-name>
        <url-pattern>/dashboard</url-pattern>
    </servlet-mapping>
    
    <servlet>
        <servlet-name>LoginServlet</servlet-name>
        <servlet-class>com.smartloan.web.LoginServlet</servlet-class>
    </servlet>
    <servlet-mapping>
        <servlet-name>LoginServlet</servlet-name>
        <url-pattern>/login</url-pattern>
    </servlet-mapping>
</web-app>
"""
write_file("WebContent/WEB-INF/web.xml", web_xml)

print("Java files generated for phase 2.")
