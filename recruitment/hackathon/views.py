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
            if license_data == 'An invalid license key.':
                return render(request, "license_result.html", {'result': license_data})
        elif license_data.loc[0,'Status'] == 'Y':
            return render(request, "license_result.html", {'result': 'This license key has already been used. Please enter another license key.'})
        else:
            r = hackathon_db.change_status('Y',key)
			
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
    print(attempts)
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

def key_operation(request):
    op = request.POST['operation']
    key = request.POST['new_key']
    print(request.POST)
    if len(key) != 10:
        return JsonResponse({'result': 'Please enter a valid license key.'})	
    if op == 'add':
        result = hackathon_db.add_license(request.POST['new_key'])	
        return JsonResponse({'result': result})
    else:
        
        if op == 'change':
            result = hackathon_db.change_status('N',key)
            return JsonResponse({'result': result})
        if op == 'delete':
            result = hackathon_db.del_license(key)
            return JsonResponse({'result': result})

def admin_dash(request):
    candidate_data = hackathon_db.get_data()
    print(candidate_data.head(200))
    total = 100/len(candidate_data.index)
    nCandidate  = [list(candidate_data['Language'].str.lower() == 'python').count(True)*total,list(candidate_data['Language'].str.lower() == 'nodejs').count(True)*total,list(candidate_data['Language'].str.lower() == 'linux').count(True)*total]
    
    avgScore = [sum(candidate_data[candidate_data['Language'].str.lower() == 'python']['Score'])/list(candidate_data['Language'].str.lower() == 'python').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'nodejs']['Score'])/list(candidate_data['Language'].str.lower() == 'nodejs').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'linux']['Score'])/list(candidate_data['Language'].str.lower() == 'linux').count(True)]
    
    nAttempt = [sum(candidate_data[candidate_data['Language'].str.lower() == 'python']['Attempts'])/list(candidate_data['Language'].str.lower() == 'python').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'nodejs']['Attempts'])/list(candidate_data['Language'].str.lower() == 'nodejs').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'linux']['Attempts'])/list(candidate_data['Language'].str.lower() == 'linux').count(True)]
    
    pfRate = [list(candidate_data['Score'] != 0).count(True),list(candidate_data['Score'] == 0).count(True)]
    
    return render(request, 'admin_dash.html', {'data_num':nCandidate, 'data_score':avgScore, 'data_attempt':nAttempt, 'data_pass':pfRate })

def admin_license(request):
    license_data = hackathon_db.search_license('ALL')
    status_name = {'Y':'Used','N':'New'}
    license_data['Status'] = pd.Series(license_data['Status']).map(status_name)
    return render(request, 'admin_license.html',{'data':license_data})

def admin_data(request):
    candidate_data = hackathon_db.get_data()
    return render(request, 'admin_data.html', {'data': candidate_data })