import string
import random

template = """
    <?xml version="1.0" ?>
 <job id="{job}">
   <script language="JScript">{js}</script>
   <script language="VBScript">
    '    <![CDATA[
    Function {func}()
        {run} 1
    End Function

    {func}
'    ]]>
   </script>
 </job>
"""


def rand_str(length=5):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def get_code(js, js_entry="main", caller_name=None, job_name=None):
    if not caller_name:
        caller_name = rand_str(6)
    if not job_name:
        job_name = rand_str(6)

    temp = str(template)
    temp = temp.replace('{func}', caller_name)
    temp = temp.replace('{job}', job_name)
    temp = temp.replace('{run}', js_entry)
    temp = temp.replace('{js}', js)
    return temp.strip()


