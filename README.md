# QuickScreen

Coding Test Platform that quickly screens a candidates coding ability 
Creates a time based hash test (hash is based on mobile number, to have epoch start time in future).
For Javascript shows a js editor as well
User is asked to create a hash based on epoch time in required language, hash is verified in real time to check at 
what time was the hash successfully created. Hash's go stale so that users can't copy another users hash.

### Installation
* Install Django 

* Install other requirements (requirements file to be created, please take up)

### Run Application 
1) cd into quickScreen/recruitment folder 

2) python manage.py runserver 

3) Open 127.0.0.1:8000 on your browser

### Development
The hackathon app within recruitment is where all the key functionality rests. The hackathon app consist some folder like db folder, functions folder, templates folder, etc. and some files like views.py, urls.py, etc. The db folder contain our database, functions folder contain python files and templates folder contain html files.

### Dashboard
Enter 'hr' and 105 in place of name and password in the <b>'/fluidai_admin'</b> page and click on submit. Now you are able to see general dashboard, candidate results and also you can manage license keys.

#####General dashboard

In this section are able to see general statistics of test i.e. no of candidates appeared in test, avg score as per subject, pass/ fail rate and avg no of attempts required to generate hash.

#####Candidate Result

In this section you are able to see the results of candidates and you can see how many attempts, minutes required to complete the test (refresh the page for new results). You see the code of the candidate using code button (code button appear for those student who pass the test).

#####License key

In this section you are able to see all the license keys with their current status. You can add key, update status of key and delete key.

1. Add key:<br>
Enter a new 10 digit key, select ‘Add key’ from drop down and click on submit. It will add Key at the end of the list.

2. Change Status of key:<br>
Enter the existing key, select ‘Change Status of key’ from drop down and click on submit. It will change status to ‘New’.
Delete key:
Enter the existing key, select ‘Delete key’ from drop down and click on submit. It will delete the key from the license table.

3. Show Status:<br>
Enter the existing key, select ‘Show status’ from drop down and click on submit. It will show the current status of the key.

4. Delete all the license keys:<br>
Enter any existing key, select ‘Delete all the license keys’ from drop down and click on submit. It will delete all the keys from the license table.

### Instruction for candidate login
1) Enter your full name, your mobile number, provided license key and select the language that you have applied for.
2) Make sure you enter your own mobile number because if you are selected we will contact you on this number.
3) You can use license key only once.
4) Select programming language correctly. Once you are login you are not allowed to change.
5) Click on submit to start test and follow instruction shown on the page.
