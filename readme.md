# **IAM Risk Analyzer CLI**

This command-line interface (CLI) tool allows you to perform various risk analysis tasks on Identity and Access Management (IAM) data. It leverages a data loading mechanism to ingest IAM information into an in-memory SQLite database and then executes predefined SQL queries to identify potential security risks.

## **Features**

* **Data Integrity Checks:** Verifies the presence and structure of essential IAM data tables.  
* **Predefined Risk Queries:** Executes SQL queries to identify common security risks such as:  
  * Partially Offboarded Users  
  * Inactive Users  
  * Never Logged In Users  
  * Users Without MFA  
  * Users with Weak MFA  
  * Service Accounts  
  * Local Accounts  
  * Recently Joined Users  
* **Interactive CLI:** A simple menu-driven interface for easy navigation and execution of tasks.

## **Prerequisites**

Before running the tool, ensure you have the following files in your project directory:

* risk\_analyzer.py: The main CLI script (this tool).  
* data\_loader.py: Handles loading your IAM data into a database.  
* sql\_queries.py: Contains the definitions of various security risk SQL queries.  
* data/data.json: A directory named data containing your IAM data in data.json format. This file should contain JSON objects for Users, Roles, Applications, Groups, and Resources.
* packages listed on requirements.txt are installed


## **Usage**

1. **Open your terminal or command prompt.**  
2. **Navigate to the directory** where you have saved risk\_analyzer.py and the other necessary files.  
3. **Run the script** using Python:  
   python risk\_analyzer.py

4. **Follow the on-screen menu:**  
   * Upon starting, the tool will load the data and perform initial integrity checks.  
   * You will then be presented with a menu of options.  
   * Enter the number corresponding to the task you wish to perform.  
   * Enter 0 to exit the application.

### **Example Interaction:**

Loading IAM data and performing integrity checks...  
Data loading complete.

\--- Risk Analysis Menu \---  
1\. View Data Integrity Check Results  
2\. Partially Offboarded Users: Users who have not been completely removed from all systems post-offboarding  
3\. Inactive Users: Users who have not logged in for a significant period  
4\. Never Logged In Users: Users who have never logged into the system after being provisioned  
5\. No MFA: Users who do not have MFA enabled  
6\. Weak MFA: Users with MFA methods that are considered weak or less secure  
7\. Service Accounts: Non-human accounts used for application or service access  
8\. Local Accounts: Accounts that are local to a specific system or application, not managed centrally  
9\. Recently Joined Users: Users who have recently joined and may require additional monitoring  
0\. Exit  
\--------------------------  
Enter your choice: 3

\--- Running: Inactive Users \---  
Description: Users who have not logged in for a significant period  
Executing SQL query...

\--- Results \---  
UserID       Name         Email   LastLogin  
  U003   Alice Brown  alice@example.com  2023-01-01  
  U005     Bob White    bob@example.com  2023-02-10

\--- Risk Analysis Menu \---  
... (menu continues)  
Enter your choice: 0  
Exiting Risk Analyzer. Goodbye\!  
