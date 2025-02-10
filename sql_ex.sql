We'll use the schema format you provided:

casa_db_collab.lab_casa_audit.df_audit_transactions – Contains audit-related transactions.
casa_db_collab.lab_casa_audit.df_compliance_violations – Contains compliance violations found in audits.
sql
Copy
Edit
CREATE TABLE casa_db_collab.lab_casa_audit.df_audit_transactions (
    transaction_id INT PRIMARY KEY,
    transaction_date DATE,
    entity_name VARCHAR(50),
    transaction_amount DECIMAL(10,2),
    audit_status VARCHAR(20) -- (Reviewed, Pending, Flagged)
);

INSERT INTO casa_db_collab.lab_casa_audit.df_audit_transactions (transaction_id, transaction_date, entity_name, transaction_amount, audit_status) VALUES
(1, '2024-01-05', 'ABC Corp', 50000.00, 'Reviewed'),
(2, '2024-01-10', 'XYZ Ltd', 120000.00, 'Flagged'),
(3, '2024-01-15', 'Acme Inc.', 25000.00, 'Pending'),
(4, '2024-02-01', 'Global Traders', 100000.00, 'Reviewed'),
(5, '2024-02-05', 'Secure FinTech', 300000.00, 'Flagged'),
(6, '2024-02-10', 'Prime Logistics', 45000.00, 'Pending'),
(7, '2024-02-12', 'Urban Bank', 80000.00, 'Reviewed'),
(8, '2024-02-15', 'Silver Trust', 95000.00, 'Pending'),
(9, '2024-02-18', 'Capital Investments', 150000.00, 'Reviewed'),
(10, '2024-02-20', 'Digital Pay', 275000.00, 'Flagged');

CREATE TABLE casa_db_collab.lab_casa_audit.df_compliance_violations (
    violation_id INT PRIMARY KEY,
    transaction_id INT,  -- FK to Audit Transactions
    violation_type VARCHAR(50),
    severity VARCHAR(20),  -- (Low, Medium, High)
    resolution_status VARCHAR(20)  -- (Resolved, Unresolved, Under Investigation)
);

INSERT INTO casa_db_collab.lab_casa_audit.df_compliance_violations (violation_id, transaction_id, violation_type, severity, resolution_status) VALUES
(101, 2, 'Money Laundering', 'High', 'Under Investigation'),
(102, 5, 'Data Breach', 'Medium', 'Unresolved'),
(103, 10, 'Fraudulent Transaction', 'High', 'Under Investigation'),
(104, 4, 'Regulatory Non-Compliance', 'Low', 'Resolved'),
(105, 7, 'Unauthorized Access', 'Medium', 'Unresolved'),
(106, 9, 'Suspicious Wire Transfer', 'High', 'Under Investigation');
Step 2: Investigation Scenario – Fraud Detection
🚨 Scenario: The audit team is investigating high-risk flagged transactions. Some transactions have compliance violations linked to fraud, money laundering, or security breaches.

Your goal is to:

Find all transactions with compliance violations.
Identify flagged transactions that are still under investigation.
Check if there are any transactions flagged for review but with no recorded compliance violation.
View the complete dataset to understand trends.
Step 3: SQL Joins to Analyze the Investigation
1. INNER JOIN – Find transactions with compliance violations
sql
Copy
Edit
SELECT T.transaction_id, T.entity_name, T.transaction_amount, T.audit_status, 
       V.violation_type, V.severity, V.resolution_status
FROM casa_db_collab.lab_casa_audit.df_audit_transactions T
INNER JOIN casa_db_collab.lab_casa_audit.df_compliance_violations V
ON T.transaction_id = V.transaction_id;
📌 Insight: Lists only transactions with compliance violations, excluding those that passed audit checks.

2. LEFT JOIN – Identify flagged transactions without recorded violations
sql
Copy
Edit
SELECT T.transaction_id, T.entity_name, T.transaction_amount, T.audit_status, 
       V.violation_type, V.severity, V.resolution_status
FROM casa_db_collab.lab_casa_audit.df_audit_transactions T
LEFT JOIN casa_db_collab.lab_casa_audit.df_compliance_violations V
ON T.transaction_id = V.transaction_id
WHERE T.audit_status = 'Flagged' AND V.violation_id IS NULL;
📌 Insight: Shows flagged transactions that lack documented compliance violations, indicating potential oversight.

3. RIGHT JOIN – Identify unresolved high-severity violations
sql
Copy
Edit
SELECT T.transaction_id, T.entity_name, T.transaction_amount, T.audit_status, 
       V.violation_type, V.severity, V.resolution_status
FROM casa_db_collab.lab_casa_audit.df_audit_transactions T
RIGHT JOIN casa_db_collab.lab_casa_audit.df_compliance_violations V
ON T.transaction_id = V.transaction_id
WHERE V.severity = 'High' AND V.resolution_status != 'Resolved';
📌 Insight: Highlights high-severity issues that are still under investigation or unresolved.

4. FULL OUTER JOIN – View the complete audit picture
sql
Copy
Edit
SELECT T.transaction_id, T.entity_name, T.transaction_amount, T.audit_status, 
       V.violation_type, V.severity, V.resolution_status
FROM casa_db_collab.lab_casa_audit.df_audit_transactions T
FULL JOIN casa_db_collab.lab_casa_audit.df_compliance_violations V
ON T.transaction_id = V.transaction_id;
📌 Insight: Provides full visibility into transactions and compliance violations, including cases where no direct link exists.

Step 4: Conclusion
🔎 Final Action:

The audit team must review flagged transactions without violations to determine if they were mistakenly flagged.
Unresolved high-severity violations should be prioritized for investigation.
A full data review will reveal patterns of compliance risks for future prevention.
This makes SQL Joins engaging and practical for auditors! 🎯 Would you like any modifications or additional case studies? 🚀
