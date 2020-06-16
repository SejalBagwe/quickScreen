from django.db import models
import pandas as pd
import datetime

# Create your models here.
class license(models.Model):
    key1 = models.BigIntegerField()
    status = models.TextField()

    def __str__(self):
        return str(self.key1)

    @staticmethod
    def add_license(Key):
        data = license.objects.filter(key1=Key).values('key1','status')
        if len(data) != 0:
            return "License key already exists."
        license.objects.create(key1=Key,status='N')
        return "License key has been successfully added."

    @staticmethod
    def del_license(Key,All=False):
        if not All:
            data = license.objects.filter(key1=Key).values('key1', 'status')
            if len(data) == 0:
                return "License key does not exists."
            license.objects.filter(key1=Key).delete()
            result = "License key has been successfully deleted."
        else:
            license.objects.all().delete()
            result = "All the license keys has been successfully deleted."
        return result

    @staticmethod
    def change_status(Status, Key):
        data = license.objects.filter(key1=Key).values('key1', 'status')
        if len(data) == 0:
            return "License key does not exists."
        data = license.objects.filter(key1=Key).update(status=Status)
        return 'Status of key change to "New".'

    @staticmethod
    def search_license(Key):
        if Key == 'ALL':
            data = license.objects.all().values('key1', 'status')
        else:
            data = license.objects.filter(key1=Key).values('key1', 'status')
            if len(data) == 0:
                return "An invalid license key."
        if len(data) == 0:
            data = pd.DataFrame(list(data),columns=['Key', 'Status'])
        else:
            data = pd.DataFrame(list(data))
            data.columns = ['Key','Status']
        data.sort_values(by=['Status'], ascending=False, inplace=True)
        data.reset_index(drop=True, inplace=True)
        return data

class candidate_info(models.Model):
    Id = models.AutoField(primary_key=True)
    Name = models.TextField()
    mobile = models.TextField()
    Start_time = models.TextField()
    End_time = models.TextField()
    Score = models.IntegerField()
    Attempts = models.IntegerField()
    Language = models.TextField()
    Date = models.TextField()
    Time = models.TextField()
    Minutes = models.IntegerField()
    Code = models.TextField()

    def __str__(self):
        return str(self.mobile)

    @staticmethod
    def get_data():
        data = candidate_info.objects.all().values()
        data = pd.DataFrame(list(data))
        data.columns = ['Id', 'Name', 'Mobile', 'Start Time', 'End Time', 'Score', 'Attempts', 'Language', 'Date',
                        'Time', 'Minutes', 'Code']
        data.set_index('Id', inplace=True)
        data.sort_values(by=['Id'], ascending=False, inplace=True)
        data.reset_index(drop=True, inplace=True)
        return data

    @staticmethod
    def insert_data(Name, Mobile, Start_time, End_time, Attempts, Language, Score):
        minutes = 0
        Date = str(datetime.datetime.strptime(Start_time, '%Y-%m-%d %H:%M:%S.%f').date())
        Time = str(datetime.datetime.strptime(Start_time, '%Y-%m-%d %H:%M:%S.%f').time().replace(microsecond=0))
        candidate_info.objects.create(Name=Name, mobile=Mobile, Start_time=Start_time, End_time=End_time, Score=Score, Attempts=Attempts, Language=Language, Date=Date, Time=Time, Minutes=minutes,Code="NA")
        return

    @staticmethod
    def update_data(Mobile, Start_time, End_time, Attempts, Score, Fail=False):
        if not Fail:
            minutes = 0
            Code = "NA"
            if Score == 100:
                minutes = round((datetime.datetime.strptime(End_time,
                                                            '%Y-%m-%d %H:%M:%S.%f') - datetime.datetime.strptime(
                    Start_time, '%Y-%m-%d %H:%M:%S.%f')).seconds / 60)
                print(minutes)
                if minutes > 10:
                    n_minutes = minutes - 10
                else:
                    n_minutes = 0
                Score = 100 - (n_minutes * 2)
                Code = "PASS"
            Topid = candidate_info.objects.filter(mobile=Mobile).order_by("-Id")[0]
            candidate_info.objects.filter(Id=Topid.Id).update(End_time=End_time, Score=Score, Attempts=Attempts, Minutes=minutes, Code=Code)
        else:
            minutes = 25
            Code = "FAIL"
            Topid = candidate_info.objects.filter(mobile=Mobile).order_by("-Id")[0]
            candidate_info.objects.filter(Id=Topid.Id).update(Minutes=minutes, Code=Code)
        return