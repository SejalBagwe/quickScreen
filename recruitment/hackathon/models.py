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