from django.shortcuts import render
from django.http import JsonResponse
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import csv
import re

# Create your views here.
class India:
    def __init__(self,state,district,taluk,office):
        self.stateName=state.replace("_"," ").upper()
        self.districtName=district.capitalize() 
        self.taluk=taluk.capitalize() 
        self.office=office

class GetPincode(APIView):
    def return_pincode(self,india):
        with open('./data/pincodes.json') as file:
            json_file =json.load(file) 
            #print(json_file[0]['districtName'])
            for item in json_file:
                if item['stateName']==india.stateName:
                    if item['districtName']==india.districtName:
                        if item['taluk']==india.taluk:
                            return item['pincode']
        return None
    def read_csv(self,india):
        filename="./data/pincodescsv.csv"
        with open(filename) as pincodecsv:
            reader=csv.DictReader(pincodecsv,delimiter=",")
            for row in reader:
                if india.stateName==row["statename"] or india.stateName==row["circlename"]:
                    if india.districtName==row["regionname"] or india.districtName==row["Districtname"]:
                        if india.taluk==row["Taluk"]:
                            return row["pincode"]
                               
    def get( self, request, state,district,taluk, format=None):
        i=India(state=state,district=district,taluk=taluk,office=None)
        pincode=self.read_csv(india=i)
        if pincode is not None:
            return Response({"pincode": pincode})
        else :
            pincode=self.return_pincode(india=i)
            return Response({"pincode": pincode})

    def post(self, request, state,district,taluk, format=None):
        return Response({"pincode":"invalid request"},status=status.HTTP_400_BAD_REQUEST)
class GetPincode1(APIView):
    def return_pincode(self,india):
        with open('./data/pincodes.json') as file:
            json_file =json.load(file) 
            #print(json_file[0]['districtName'])
            for item in json_file:
                if item['stateName']==india.stateName:
                    if item['districtName']==india.districtName:
                        if item['taluk']==india.taluk:
                            return item['pincode']
        return None
    def read_csv(self,india):
        pincode=None
        filename="./data/pincodescsv.csv"
        with open(filename) as pincodecsv:
            reader=csv.DictReader(pincodecsv,delimiter=",")
            for row in reader:
                if india.stateName==row["statename"] or india.stateName==row["circlename"]:
                    if india.districtName==row["regionname"] or india.districtName==row["Districtname"]:
                        if india.taluk==row["Taluk"]:
                            if india.office:
                                if re.search(india.office,row["officename"]):
                                    return row["pincode"]
                                else:
                                    pincode=row["pincode"]
        return pincode
                               
    def get( self, request, state,district,taluk,office ,format=None):
        i=India(state=state,district=district,taluk=taluk,office=office)
        pincode=self.read_csv(india=i)
        if pincode is not None:
            return Response({"pincode": pincode})
        else :
            pincode=self.return_pincode(india=i)
            return Response({"pincode": pincode})
             
    def post(self, request, state,district,taluk, format=None):
        return Response({"pincode":"invalid request"},status=status.HTTP_400_BAD_REQUEST)


class GetTowns(APIView):

    def read_csv(self,district):
        towns=list()
        filename="./data/Town_Codes_2001.csv"
        with open(filename) as pincodecsv:
            reader=csv.DictReader(pincodecsv,delimiter=",")
            for row in reader:
                if district==row["District"]:
                    towns.append(row["Town"])
            return towns

    def get(self,request,format=None):
        
        if  "district" not in request.GET:
            return Response({"error":"district perameter is mising"},status=status.HTTP_400_BAD_REQUEST)
        elif len(request.GET["district"]) <= 3:
            return Response({"error":"district parameter must have length greater than 5 character"},status=status.HTTP_400_BAD_REQUEST)
        else:
            towns=self.read_csv(district=request.GET["district"])
            if towns is None:
                return Response({"error":"data for given district not available"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"towns":towns,"district":request.GET["district"]},status=status.HTTP_200_OK)
    def post(self,request,format=None):
        
        if  "district" not in request.POST:
            return Response({"error":"district perameter is mising"},status=status.HTTP_400_BAD_REQUEST)
        elif len(request.POST["district"]) < 3:
            return Response({"error":"district parameter must have length greater than 5 character"},status=status.HTTP_400_BAD_REQUEST)
        else:
            towns=self.read_csv(district=request.POST["district"])
            if towns is None:
                return Response({"error":"data for given district not available"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"towns":towns,"district":request.POST["district"]},status=status.HTTP_200_OK)

class GetDistrictname(APIView):
    def read_csv(self,State):
        district=set()
        filename="./data/Town_Codes_2001.csv"
        with open(filename) as pincodecsv:
            reader=csv.DictReader(pincodecsv,delimiter=",")
            for row in reader:
                if State==row["State"]:
                    district.add(row["District"])
            return district

    def get(self,request):
        if "State" not in request.GET:
            return Response({"error":"State perameter is mising"},status=status.HTTP_400_BAD_REQUEST)
        else:
            district=self.read_csv(State=request.GET["State"])
            return Response({"districts":district,"State":request.GET["State"]},status=status.HTTP_200_OK)
class GetStatelist(APIView):
    def read_csv(self):
        State=set()
        filename="./data/Town_Codes_2001.csv"
        with open(filename) as pincodecsv:
            reader=csv.DictReader(pincodecsv,delimiter=",")
            for row in reader:
                State.add(row["State"])
            return State

    def get(self,request):
        state=self.read_csv()
        return Response({"States":state,"Country":"India"},status=status.HTTP_200_OK)

def HomeView(request):
    return render(request,'api/homepage.html')
    

        


