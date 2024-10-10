cd ~/awsdac
files=`ls -1 *.png`
echo """
<!DOCTYPE html
        PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
         "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US" xml:lang="en-US">
<head>
<title>AWSDAC Diagrams</title>
<style>
  body    {color:#000000;font-weight:normal;font-size:10pt;font-family:Helvetica,Impact,Arial,sans-serif;}
</style>
</head>
<body>
"""
while IFS= read -r line; do
  title=$(echo $line | perl -pe "s{.png}{}")
  echo "<P>$title</P>"
  echo "<img src=\"$line\">"
done <<< "$files"
echo "</body></html>"


