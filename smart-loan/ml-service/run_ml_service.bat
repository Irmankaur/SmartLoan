@echo off
echo ========================================================
echo Starting Smart Loan Machine Learning REST Service
echo Environment: Python 3.12, scikit-learn, Flask
echo Port: 5001
echo ========================================================
cd /d "%~dp0"
python app.py
pause
