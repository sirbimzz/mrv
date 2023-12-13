@ECHO OFF
TITLE Execute python script on anaconda environment
ECHO Please Wait...
:: Section 1: Activate the environment.
ECHO ============================
ECHO Conda Activate
ECHO ============================
@CALL "E:\Digital\Anaconda\Scripts\activate.bat" base
:: Section 2: Execute python script.
ECHO ============================
ECHO Python mrv_pi_live.py
ECHO ============================
python "E:\Digital\dashboards\mrv\py\mrv_waste_monthly.py"



ECHO ============================
ECHO End
ECHO ============================