<?php
// serve the file as application/xml so it the browser knows the file is executable
header('Content-type: application/xml');
header('Content-Disposition: attachment; filename="TotallySafeFile.wsf"');

readfile('output.wsf');
exit();

?>