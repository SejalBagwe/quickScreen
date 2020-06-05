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
Enter 'hr' and 105 in place of name and mobile number in the login page and click on submit. Now you are able to see general dashboard, candidate results and also you can manage license keys.

### Instruction for candidate login
1) Enter your full name, your mobile number, provided license key and select the language that you have applied for.
2) Make sure you enter your own mobile number because if you are selected we will contact you on this number.
3) You can use license key only once.
4) Select programming language correctly. Once you are login you are not allowed to change.
5) Click on submit to start test and follow instruction shown on the page.
