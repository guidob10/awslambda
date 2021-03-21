## Process:
Upload files to two differents folders in s3 bucket, both of them in .zip format. This files will be unzip and
the uploaded to other s3 bucket, this is for safety on recursives triggered functions.
Then when the data is in a .txt file on other bucket, it will trigger a new aws lambda function which its going to 
copy that data in tables on a RDS postgre database. 

* One of the functions will cut the lines in the position 60 and write only the first part
* The other function will analize which of the files are uploades, because it can have 2 types of file per zip. Depending
on which filename its, it will write in one table or another.
* Then the script copy a part of the line, and write in other column.

## Considerations:

* Accordly of file size, you have to set more o less memory and timeout.
* You have to create a s3 bucket trigger  with the properly prefix and suffix in the lambda function.
* You have to give permissions to read/write in s3 and so in RDS to.


