package com.smartloan.web;
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
