from .functions import hash_manager
from .functions import encryption
from .functions import hackathon_db
import datetime
import pandas as pd

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

attempts = 0
start_time = ''
name = ''
mobile = ''
language = ''
result = ''

def start_test(request):
    return render(request, "start_test.html", {})
    # text = """<h1>welcome to my app !</h1>"""
    # return HttpResponse(text)


def test_instructions(request):
    current_site = get_current_site(request)
    # redirect user back if no language selected
    global attempts, start_time, name, mobile, language

    start_time = str(datetime.datetime.now())
    if "language" in request.GET:
        language = request.GET['language']
    else:
        return redirect('/')

    if 'mobile' in request.GET:

        mobile = request.GET['mobile']
        name = str(request.GET['name'])
        print(request.GET['name'])
        # if mobile is blank then send user back
        if name.lower() == "hr" and mobile == "105":
            candidate_data = hackathon_db.get_data()
            #tables=[candidate_data.to_html(classes='data')], titles=candidate_data.columns.values
            #return render_template("admin.html",tables=[candidate_data.to_html(classes='data')], titles=candidate_data.columns.values)
            return render(request, 'admin.html', {'data': candidate_data })
			
        elif mobile is "" or len(mobile) != 10:
            return redirect('/')

        encrypted_mobile = encryption.encrypt(mobile)
        # generated special hash link, eg. 127.0.0.1:8000/x/{{encrypted_mobile}}
        hash_site_link = "http://" + current_site.domain + "/x/" + encrypted_mobile + "/"
        if language == "Nodejs":
            return render(request, "test_instructions_nodejs.html", {'site': hash_site_link, 'language': language})
        else:
            return render(request, "test_instructions.html", {'site': current_site.domain, 'language': language})

    else:
        return redirect('/')


def evaluate_hash(request):
    global attempts, start_time, name, mobile, language,result

    # Removing the url x/ part to get the hash
    url = request.path.split('/')
    if language == 'nodejs':
        received_hash = url[3]
    else:
        received_hash = url[2]

    print(received_hash)

    attempts += 1

    if received_hash is None or received_hash == "" or len(received_hash) < 2:
        result = "Invalid Hash"
    else:
        print(received_hash)

        result = hash_manager.check_hash(received_hash)

    if result is None or result is "":
        result = ""

    if result.split(' ')[0] == 'success':
        end_time = str(datetime.datetime.now())
        hackathon_db.insert_data(name, mobile, start_time, end_time, attempts, language)
        display_result()
    #text = """<h1>""" + result + "---" + received_hash + """</h1>"""
    #return HttpResponse(text)

    return render(request, "show_result.html", {'msg':[name,result]})

def hello_template(request):
    return render(request, "hello.html", {})
