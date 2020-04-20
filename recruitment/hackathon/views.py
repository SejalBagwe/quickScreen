from .functions import hash_manager
from .functions import encryption
from .functions import hackathon_db
import datetime
import pandas as pd

# Create your views here.
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

def start_test(request):

    return render(request, "start_test.html", {})
    # text = """<h1>welcome to my app !</h1>"""
    # return HttpResponse(text)


def test_instructions(request):

    current_site = get_current_site(request)
    
    start_time = str(datetime.datetime.now())
    print(request.POST)
    if "language" not in request.POST and "mobile" not in request.POST and "name" not in request.POST and "license" not in request.POST:
        return redirect('/')
    else:
        language = request.POST['language']
        mobile = request.POST['mobile']
        name = str(request.POST['name'])
        
        if name.lower() == "hr" and mobile == "105":
            candidate_data = hackathon_db.get_data()
            return redirect('/admin_dash')
        elif mobile is "" or len(mobile) != 10:
            return redirect('/')
			
        if len(request.POST['license']) != 10:
            return redirect('/')
        key = request.POST['license']
        license_data = hackathon_db.search_license(key)
        print(license_data)
        if type(license_data) == str:
            if license_data == 'Invalid Key':
                return render(request, "license_result.html", {'result': license_data})
        elif license_data.loc[0,'Status'] == 'Y':
            return render(request, "license_result.html", {'result': 'Used Key'})
        else:
            hackathon_db.change_status(key)
			
        test_time = str(datetime.datetime.now() + datetime.timedelta(minutes=15))
        hackathon_db.insert_data(name, mobile, start_time, test_time, 0, language, 0)

        encrypted_mobile = encryption.encrypt(mobile)
		#########test_time retrive
        candidate_data = hackathon_db.get_data()
        df = candidate_data[candidate_data['Mobile']==encryption.decrypt(encrypted_mobile)].reset_index(drop=True)
        test_time = df.loc[0,'End Time']
        print(test_time)
        # generated special hash link, eg. 127.0.0.1:8000/x/{{encrypted_mobile}}
        hash_site_link = "http://" + current_site.domain + "/x/" + encrypted_mobile + "/"
        if language == "nodejs":
            return render(request, "test_instructions_nodejs.html", {'site': hash_site_link, 'language': language, 'time': test_time})
        else:			
            return render(request, "test_instructions.html", {'site': hash_site_link, 'language': language, 'time': test_time})



def evaluate_hash(request):
    
    # Removing the url x/ part to get the hash
    print(request.path)
    url = request.path.split('/')
    received_hash = url[3]

    print(received_hash)
    encrypted_mobile = url[2]
	
    mobile = encryption.decrypt(encrypted_mobile)
    print(mobile)
    print(type(mobile))
    candidate_data = hackathon_db.get_data()
    df = candidate_data[candidate_data['Mobile']==mobile].reset_index(drop=True)
    end_time = df.loc[0,'End Time']
    attempts = df.loc[0,'Attempts']
    print(attempts,'\n',type(attempts))
    attempts += 1
    start_time = df.loc[0,'Start Time']
    hackathon_db.update_data(mobile, start_time, end_time, attempts, 0)

    if received_hash is None or received_hash == "" or len(received_hash) < 2:
        result = "Invalid Hash"
    else:
        print(received_hash)

        result = hash_manager.check_hash(received_hash)

    if result is None or result is "":
        result = ""

    if result.split(' ')[0] == 'success':
        end_time = str(datetime.datetime.now())
        attempts = df.loc[0,'Attempts'] + 1
        start_time = df.loc[0,'Start Time']
        hackathon_db.update_data(mobile, start_time, end_time, attempts, 100)
        #display_result()
    #text = """<h1>""" + result + "---" + received_hash + """</h1>"""
    #return HttpResponse(text)
    name = df.loc[0,'Name']
    return render(request, "show_result.html", {'msg':[name,result]})

def hello_template(request):
    return render(request, "hello.html", {})

def add_key(request):
    key = request.POST['new_key']
    print(request.POST)
    if len(key) != 10:
        return JsonResponse({'insert_result': 'Add Proper Key'})
    result = hackathon_db.add_license(request.POST['new_key'])	
    return JsonResponse({'insert_result': result})
    #return render(request, "admin.html", {'insert_result': result})
    #return redirect('/admin_dash', insert_result= result)
	
def admin_dash(request):
    candidate_data = hackathon_db.get_data()
    total = 100/len(candidate_data.index)
    info = [list(candidate_data['Language'] == 'python').count(True)*total,list(candidate_data['Language'] == 'nodejs').count(True)*total,list(candidate_data['Language'] == 'linux').count(True)*total]
    return render(request, 'admin_dash.html', {'data': info })

def admin_license(request):
    return render(request, 'admin_license.html')

def admin_data(request):
    candidate_data = hackathon_db.get_data()
    print(candidate_data.head(10))
    return render(request, 'admin_data.html', {'data': candidate_data })