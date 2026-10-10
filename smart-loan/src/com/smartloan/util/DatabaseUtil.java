package com.smartloan.util;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.Statement;

public class DatabaseUtil {
    private static final String URL = "jdbc:sqlite:d:/godrej3/smart-loan/smartloan.db";

    static {
        try { 
            Class.forName("org.sqlite.JDBC"); 
            initializeDatabase();
        } 
        catch (ClassNotFoundException e) { e.printStackTrace(); }
    }

    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(URL);
    }
    
    private static void initializeDatabase() {
        try (Connection conn = getConnection();
             Statement stmt = conn.createStatement()) {
            
            // Create Users Table
            stmt.execute("CREATE TABLE IF NOT EXISTS users (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "username TEXT UNIQUE NOT NULL, " +
                "password TEXT NOT NULL, " +
                "income REAL DEFAULT 0, " +
                "expenses REAL DEFAULT 0, " +
                "emergency_reserve REAL DEFAULT 0)");
                
            // Create Loans Table
            stmt.execute("CREATE TABLE IF NOT EXISTS loans (" +
                "id INTEGER PRIMARY KEY AUTOINCREMENT, " +
                "user_id INTEGER, " +
                "loan_type TEXT, " +
                "principal REAL, " +
                "interest_rate REAL, " +
                "tenure_months INTEGER, " +
                "FOREIGN KEY (user_id) REFERENCES users(id))");
                
            // Insert default user if not exists
            try {
                stmt.execute("INSERT INTO users (username, password) VALUES ('admin', 'admin')");
            } catch (Exception ignore) {
                // User already exists (UNIQUE constraint failed)
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}
