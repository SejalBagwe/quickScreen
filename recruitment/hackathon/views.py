from .functions import hash_manager
from .functions import encryption
from .functions import hackathon_db
import datetime
import pandas as pd
import os
from .models import license, candidate_info

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site

def start_test(request):
    return render(request, "start_test.html", {})

def start_admin(request):
    return render(request, "admin_login.html", {})

def admin_check(request):
    if "password" not in request.POST and "password" not in request.POST:
        return redirect('/')
    else:
        if request.POST['name'].lower() == "hr" and request.POST['password'] == "105":
            return redirect('/admin_dash')


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
        
        # if name.lower() == "hr" and mobile == "105":
        #     candidate_data = hackathon_db.get_data()
        #     return redirect('/admin_dash')
        if mobile is "" or len(mobile) != 10:
            return redirect('/')
        if len(request.POST['license']) != 10:
            return redirect('/')
        key = request.POST['license']
        license_data = license.search_license(key)
        print(license_data)
        if type(license_data) == str:
            if license_data == 'An invalid license key.':
                return render(request, "license_result.html", {'result': license_data})
        elif license_data.loc[0,'Status'] == 'Y':
            return render(request, "license_result.html", {'result': 'This license key has already been used. Please enter another license key.'})
        else:
            r = license.change_status('Y',key)

        test_time = str(datetime.datetime.now() + datetime.timedelta(minutes=25))
        candidate_info.insert_data(name, mobile, start_time, test_time, 0, language, 0)

        encrypted_mobile = encryption.encrypt(mobile)
        candidate_data = candidate_info.get_data()
        df = candidate_data[candidate_data['Mobile']==encryption.decrypt(encrypted_mobile)].reset_index(drop=True)
        test_time = df.loc[0,'End Time']
        print(test_time)
        # generated special hash link, eg. 127.0.0.1:8000/x/{{encrypted_mobile}}
        hash_site_link = "https://" + current_site.domain + "/x/" + encrypted_mobile + "/"
        if language == "nodejs":
            return render(request, "test_instructions_nodejs.html", {'site': hash_site_link, 'language': language, 'time': test_time, 'mobile':encrypted_mobile})
        elif language == "java":
            return render(request, "test_instructions_java.html", {'site': hash_site_link, 'language': language, 'time': test_time, 'mobile':encrypted_mobile})
        else:			
            return render(request, "test_instructions.html", {'site': hash_site_link, 'language': language, 'time': test_time, 'mobile':encrypted_mobile})



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
    candidate_data = candidate_info.get_data()
    df = candidate_data[candidate_data['Mobile']==mobile].reset_index(drop=True)
    end_time = df.loc[0,'End Time']
    attempts = df.loc[0,'Attempts']
    print(attempts,'\n',type(attempts))
    attempts += 1
    print(attempts)
    start_time = df.loc[0,'Start Time']
    candidate_info.update_data(mobile, start_time, end_time, attempts, 0)

    if received_hash is None or received_hash == "" or len(received_hash) < 2:
        result = "Invalid Hash"
    else:
        print(received_hash)

        result = hash_manager.check_hash(received_hash)

    if result is None or result is "":
        result = ""

    if result.split(' ')[0] == 'Success':
        end_time = str(datetime.datetime.now())
        attempts = df.loc[0,'Attempts'] + 1
        start_time = df.loc[0,'Start Time']
        candidate_info.update_data(mobile, start_time, end_time, attempts, 100)
    name = df.loc[0,'Name']
    return render(request, "show_result.html", {'msg':[name,result],'mobile': mobile })

def hello_template(request):
    return render(request, "hello.html", {})

def key_operation(request):
    op = request.POST['operation']
    key = request.POST['new_key']
    print(request.POST)
    if len(key) != 10:
        return JsonResponse({'result': 'Please enter a valid license key.'})	
    if op == 'add':
        result = license.add_license(request.POST['new_key'])
        return JsonResponse({'result': result})
        pass
    elif op == 'change':
        result = license.change_status('N',key)
        return JsonResponse({'result': result})
    elif op == 'delete':
        result = license.del_license(key)
        return JsonResponse({'result': result})
    elif op == 'deleteAll':
        result = license.del_license(key, All= True)
        return JsonResponse({'result': result})
    elif op == 'show':
        license_data = license.search_license(key)
        print(license_data)
        if type(license_data) == str:
            if license_data == 'An invalid license key.':
                result = 'An invalid license key.'
        elif license_data.loc[0,'Status'] == 'N':
            result = 'This '+key+' is New key.'
        else:
            result = 'This '+key+' is Used key.'
        return JsonResponse({'result': result})

def key_file_upload(request):

    f = request.FILES['licensefile']
    if f.name[-5:] == '.xlsx':

        # data preprocessing
        data = pd.read_excel(f)
        if len(data.columns) == 1:
            col = 'Phone Number'
            data.columns = [col]
            for i in range(data.shape[0]):
                a = str(data.at[i,col]).split(',')[0]
                if len(a) != 10:
                    a = a[-10:]
                data.at[i,col] = int(a)
            data['status'] = 'N'
            for i in range(data.shape[0]):
                r = license.add_license(int(data.at[i,col]))
                if r == 'License key already exists.':

                    license.change_status(data.at[i,'status'],int(data.at[i,col]))

            result = 'Uploaded Successfully.'
        else:
            result = 'Only 1 column is allowed.'

    else:
        result = 'Sorry! Upload only excel file.'

    return JsonResponse({'result':result})


@csrf_exempt
def getCode(request):
    print(request.POST)
    mob = request.POST['mobile']
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "media")
    try:
        f = open(os.path.join(path,mob+".txt"), "r")
        text = []
        for l in f.readlines():
            l = l.replace('    ',"&nbsp; &nbsp; ")
            l = l.replace('\t', "&nbsp; &nbsp; ")
            text.append(l)
    except:
        text = ["File not found."]
    return JsonResponse({'text': text})


def admin_dash(request):
    candidate_data = candidate_info.get_data()
    print(candidate_data.head(200))
    total = 100/len(candidate_data.index)
    nCandidate  = [list(candidate_data['Language'].str.lower() == 'python').count(True)*total,list(candidate_data['Language'].str.lower() == 'java').count(True)*total,list(candidate_data['Language'].str.lower() == 'nodejs').count(True)*total,list(candidate_data['Language'].str.lower() == 'linux').count(True)*total]
    
    avgScore = [sum(candidate_data[candidate_data['Language'].str.lower() == 'python']['Score'])/list(candidate_data['Language'].str.lower() == 'python').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'java']['Score'])/list(candidate_data['Language'].str.lower() == 'java').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'nodejs']['Score'])/list(candidate_data['Language'].str.lower() == 'nodejs').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'linux']['Score'])/list(candidate_data['Language'].str.lower() == 'linux').count(True)]
    
    nAttempt = [sum(candidate_data[candidate_data['Language'].str.lower() == 'python']['Attempts'])/list(candidate_data['Language'].str.lower() == 'python').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'java']['Attempts'])/list(candidate_data['Language'].str.lower() == 'java').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'nodejs']['Attempts'])/list(candidate_data['Language'].str.lower() == 'nodejs').count(True),sum(candidate_data[candidate_data['Language'].str.lower() == 'linux']['Attempts'])/list(candidate_data['Language'].str.lower() == 'linux').count(True)]
    
    pfRate = [list(candidate_data['Code'] == "PASS").count(True),list(candidate_data['Code'] != "PASS").count(True)]
    
    return render(request, 'admin_dash.html', {'data_num':nCandidate, 'data_score':avgScore, 'data_attempt':nAttempt, 'data_pass':pfRate })

def admin_license(request):
    license_data = license.search_license('ALL')
    status_name = {'Y':'Used','N':'New'}
    if license_data.shape[0] != 0:
        license_data['Status'] = pd.Series(license_data['Status']).map(status_name)
    return render(request, 'admin_license.html',{'data':license_data})

def admin_data(request):
    candidate_data1 = candidate_info.get_data()
    candidate_data = candidate_data1[['Name','Mobile','Date','Time','Minutes','Score','Attempts','Language','Code']]
    candidate_data.columns = ['Name','Mobile','Test_Date','Time','Minutes','Score','Attempts','Language','Code']
    rows = []
    for i in range(candidate_data.shape[0]):
        temp ={}
        if candidate_data.at[i,'Code'] == "PASS":
            temp['button_bool'] = True
        else:
            temp['button_bool'] = False
        temp['values'] = []
        for j in candidate_data.columns:
            temp['values'].append(candidate_data.at[i,j])
        rows.append(temp)
    path = path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"media")
    return render(request, 'admin_data.html', {'columns': candidate_data.columns, 'rows':rows})

def end_test(request):
    print(request.path)
    candidate_data = candidate_info.get_data()
    mobile = encryption.decrypt(request.path.split('/')[3])
    df = candidate_data[candidate_data['Mobile'] == mobile].reset_index(drop=True)
    start_time = df.loc[0, 'Start Time']
    end_time = df.loc[0, 'End Time']
    attempts = df.loc[0, 'Attempts']
    if df.loc[0,'Code'] != 'PASS':
        candidate_info.update_data(mobile, start_time, end_time, attempts, 0, Fail=True)
    print('here')
    return redirect('/')

def submission(request):
    # uploded_file = request.FILES['myfile']
    # print(uploded_file.name)
    # print(request.POST)
    code = request.POST['myfile']
    mobile = request.POST['mobile1']
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),"media")
    f = open(os.path.join(path,mobile+".txt"), "w")
    f.write(code)
    f.close()
    return render(request,'thanku.html')
