package com.smartloan.web;
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
