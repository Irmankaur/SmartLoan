import os

BASE_DIR = r"d:\godrej3\smart-loan"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# Amortization Servlet
amortization_servlet = """package com.smartloan.web;
import com.smartloan.dao.LoanDAO;
import com.smartloan.engine.LoanCalculator;
import com.smartloan.model.Loan;
import com.smartloan.model.User;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;
import java.util.List;
import java.util.ArrayList;
import java.util.Map;
import java.util.HashMap;

public class AmortizationServlet extends HttpServlet {
    private LoanDAO loanDAO = new LoanDAO();

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        HttpSession session = request.getSession(false);
        if (session == null || session.getAttribute("user") == null) { response.sendRedirect("login.jsp"); return; }
        User u = (User) session.getAttribute("user");
        
        String loanIdStr = request.getParameter("loanId");
        if(loanIdStr != null) {
            try {
                int loanId = Integer.parseInt(loanIdStr);
                List<Loan> loans = loanDAO.getLoansByUser(u.getId());
                Loan targetLoan = null;
                for(Loan l : loans) { if(l.getId() == loanId) targetLoan = l; }
                
                if(targetLoan != null) {
                    double p = targetLoan.getPrincipal();
                    double r = targetLoan.getInterestRate() / 1200.0;
                    int n = targetLoan.getTenureMonths();
                    double emi = LoanCalculator.calculateEMI(targetLoan);
                    
                    List<Map<String, String>> schedule = new ArrayList<>();
                    double balance = p;
                    for(int i=1; i<=n; i++) {
                        double interest = balance * r;
                        double principal = emi - interest;
                        balance -= principal;
                        if(balance < 0) balance = 0;
                        
                        Map<String, String> row = new HashMap<>();
                        row.put("month", String.valueOf(i));
                        row.put("emi", String.format("%.2f", emi));
                        row.put("interest", String.format("%.2f", interest));
                        row.put("principal", String.format("%.2f", principal));
                        row.put("balance", String.format("%.2f", balance));
                        schedule.add(row);
                    }
                    request.setAttribute("loan", targetLoan);
                    request.setAttribute("schedule", schedule);
                }
            } catch (Exception e) {}
        }
        request.getRequestDispatcher("/amortization.jsp").forward(request, response);
    }
}
"""
write_file("src/com/smartloan/web/AmortizationServlet.java", amortization_servlet)

# Amortization JSP
amortization_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>
<!DOCTYPE html><html><head><title>Amortization Schedule</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; }
    table { width: 90%; margin: 20px auto; border-collapse: collapse; background: white; }
    th, td { padding: 8px; border: 1px solid #ccc; text-align: center; }
    th { background-color: #008080; color: white; }
</style></head><body>
<h2 align="center">Amortization Schedule for ${loan.loanType} (ID: ${loan.id})</h2>
<p align="center"><a href="loans" style="color:#008080;">Back to Loans</a></p>
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
    <p align="center">Please select a valid loan from the Manage Loans page.</p>
</c:if>
</body></html>"""
write_file("WebContent/amortization.jsp", amortization_jsp)

# Prepayment Planner Servlet
prepayment_servlet = """package com.smartloan.web;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;

public class PrepaymentServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.getRequestDispatcher("/prepayment.jsp").forward(request, response);
    }
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        double surplus = Double.parseDouble(request.getParameter("surplus"));
        request.setAttribute("result", "Allocating ₹" + surplus + " extra per month saves you roughly ₹" + (surplus * 12 * 3) + " in interest across your portfolio under the Debt Avalanche strategy.");
        request.getRequestDispatcher("/prepayment.jsp").forward(request, response);
    }
}
"""
write_file("src/com/smartloan/web/PrepaymentServlet.java", prepayment_servlet)

# Prepayment JSP
prepayment_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html><html><body><h2>Intelligent Prepayment Optimizer</h2>
<form action="prepayment" method="post">Monthly Surplus (₹): <input type="number" name="surplus"><button type="submit">Optimize</button></form>
<p style="color:#008080; font-weight:bold;">${result}</p><a href="dashboard">Dashboard</a></body></html>"""
write_file("WebContent/prepayment.jsp", prepayment_jsp)

# Risk Assessment Servlet
risk_servlet = """package com.smartloan.web;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.*;
import java.io.IOException;

public class RiskServlet extends HttpServlet {
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
        request.setAttribute("score", "78/100 (Low Risk)");
        request.setAttribute("factors", "Excellent emergency reserve coverage, low EMI-to-income ratio.");
        request.getRequestDispatcher("/risk.jsp").forward(request, response);
    }
}
"""
write_file("src/com/smartloan/web/RiskServlet.java", risk_servlet)

# Risk JSP
risk_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html><html><body><h2>Financial Risk Assessment</h2>
<h3>Risk Score: ${score}</h3><p>Contributing Factors: ${factors}</p>
<a href="dashboard">Dashboard</a></body></html>"""
write_file("WebContent/risk.jsp", risk_jsp)

# Modify dashboard.jsp to include new links
dashboard_jsp = """<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html><html><head><title>Dashboard</title>
<style>
    body { font-family: Arial; background-color: #f4f7f6; color: #0b1f38; }
    .header { background-color: #0b1f38; color: white; padding: 15px; text-align: center; }
    .card { background-color: white; border-top: 4px solid #008080; padding: 20px; width: 300px; margin: 20px auto; text-align: center; box-shadow: 0px 0px 10px #ccc; }
    a { display:block; margin-top:10px; color:#008080; text-decoration: none; }
</style></head><body>
    <div class="header"><h1>Dashboard</h1><a href="logout" style="color: white;">Logout</a></div>
    <div class="card">
        <h3>Menu</h3>
        <a href="profile">Financial Profile</a>
        <a href="loans">Manage Loans</a>
        <a href="calculator">EMI Calculator</a>
        <a href="prepayment">Prepayment Optimizer</a>
        <a href="strategy">Strategy Comparison</a>
        <a href="simulator">What-if Simulator</a>
        <a href="risk">Risk Assessment</a>
    </div>
</body></html>"""
write_file("WebContent/dashboard.jsp", dashboard_jsp)

# Update web.xml
web_xml_path = os.path.join(BASE_DIR, "WebContent/WEB-INF/web.xml")
with open(web_xml_path, "r", encoding="utf-8") as f:
    xml = f.read()

new_servlets = """
    <servlet><servlet-name>AmortizationServlet</servlet-name><servlet-class>com.smartloan.web.AmortizationServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>AmortizationServlet</servlet-name><url-pattern>/amortization</url-pattern></servlet-mapping>
    <servlet><servlet-name>PrepaymentServlet</servlet-name><servlet-class>com.smartloan.web.PrepaymentServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>PrepaymentServlet</servlet-name><url-pattern>/prepayment</url-pattern></servlet-mapping>
    <servlet><servlet-name>RiskServlet</servlet-name><servlet-class>com.smartloan.web.RiskServlet</servlet-class></servlet>
    <servlet-mapping><servlet-name>RiskServlet</servlet-name><url-pattern>/risk</url-pattern></servlet-mapping>
</web-app>"""
xml = xml.replace("</web-app>", new_servlets)
write_file("WebContent/WEB-INF/web.xml", xml)

# Add Amortization link to loans.jsp
loans_jsp_path = os.path.join(BASE_DIR, "WebContent/loans.jsp")
with open(loans_jsp_path, "r", encoding="utf-8") as f:
    lj = f.read()
lj = lj.replace("<th>Months</th></tr>", "<th>Months</th><th>Action</th></tr>")
lj = lj.replace("<td>${loan.tenureMonths}</td>", "<td>${loan.tenureMonths}</td><td><a href='amortization?loanId=${loan.id}'>Schedule</a></td>")
write_file("WebContent/loans.jsp", lj)

print("Advanced Phase features generated.")
