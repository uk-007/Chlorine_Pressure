from django.shortcuts import render ,HttpResponse,redirect
#from ChlorineWater.models import ChlorineData
import uuid
import requests
import json
import django
import urllib
import pyodbc  #For python3 MSSQL
from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth import authenticate
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction

device_data_detail = ""
install_date=""
name=""
address=""
serial=""
cursor = connections['default'].cursor()



def createCaptcha():       #function to create captcha
    id = uuid.uuid1()
    id = id.hex
    #print(type(id))
    #print(id)
    captcha = id[:4]
    #print(captcha)
    return captcha

generate_captcha = True

def LoginPage(request):
    # user = User.objects.create_user(username="Utkarsh", password="water@123")
    # UserProfile.objects.create(user=user, Name="Utkarsh", loginid="utkarsh1")
    # user_profile = UserProfile.objects.get(loginid='kevin1')
    # print(user_profile)
    #user = User.objects.get(username='Utkarsh')        #entering data into user_profile, hard coding details of user for login
    #user_profile = UserProfile.objects.create(user=user, Name="Utkarsh", loginid="utkarsh1")  
    
    global generate_captcha
    #print(generate_captcha)
    global contextC
    global c
    if generate_captcha == True:
        c = createCaptcha()
        #print("DDDDDDDDDDDDDD")
        #print(c)
        contextC = {
            "captcha": c
        }
        generate_captcha = False
        
    if request.method == 'POST':
        
        login_id = request.POST.get('email') 
        print(login_id)
        #login_id = str(login_id)
        #print(type(login_id))
        password = request.POST.get('password')
        #password = str(password)
        #user_profile = UserProfile.objects.get(loginid=login_id)
        #user_profiles = UserProfile.objects.filter(loginid="kevin1")
        #print(user_profile)
        captcha_entered = request.POST.get('cptch')
        captcha_displayed = request.POST.get('cpt')
        # logger.debug(f"User entered loginid: {login_id}")
        # logger.debug(f"User entered password: {password}")
        # logger.debug(f"User entered captcha: {captcha_entered}")
        if captcha_entered != captcha_displayed :       #if user enters wrong captcha
            c = createCaptcha()
            generate_captcha = False
            context = {
                "message":"wrong captcha entered",
                "captcha": c 
            }
            return render(request,'LoginPage.html',context)
        else:
            try:
                user_profile = UserProfile.objects.get(loginid=login_id)   #if loginid entered by user does not exist line 74 may throw exception
                print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                print(user_profile)
            except Exception as e:
                print(str(e))
                print("I N C OR R E C T U S E R ")
                
                c = createCaptcha()
                generate_captcha = False
                context = {
                    "message":"Incorrect loginid",
                    "captcha": c 
                }
                return render(request,'LoginPage.html',context)
                      
            user = authenticate(username=user_profile.user.username,password=password)   
            if user is not None:   #valid user
                login(request, user)
                print("user is valid")
                #user_profile = UserProfile.objects.filter(Name=request.user.username)
                #role_id = user_profile.get().roleid
                #request.session['session_id'] = role_id
            
                return redirect('/Dashboard_Page')
                #return render(request, "Dashboard.html")
            else:                                               #if loginid and password does not match
                c = createCaptcha()
                generate_captcha = False
                context = {
                    "message":"Incorrect password",
                    "captcha": c 
                }
                return render(request,'LoginPage.html',context)  
        
    return render(request,'LoginPage.html',contextC)


@login_required
def logoutUser(request):
    logout(request)
    global generate_captcha
    generate_captcha = True
    return redirect('/Login')   

@csrf_exempt 
def ForgotPassword(request):
  #  print("hhhhhhhh")
    global c
    global generate_captcha
    if request.method=="POST":
        login_id = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('repassword')   
        
    #what if user.save() is not executed, there is some issue like internet issue, database connectivity etc , so change is not
    # commited in database, so to handle this situation you can consider using Django's transaction module to ensure that
    # the update operation is atomic. An atomic operation in this context means that either all changes are saved, 
    # or none of them are. If an exception occurs during the transaction, it will be rolled back, and the database will 
    # be left unchanged.
        if password == re_password:
            try:
                with transaction.atomic():
                    user_profile = UserProfile.objects.get(loginid=login_id)
                    user = User.objects.get(username=user_profile.user.username)
                    user.set_password(password)
                    user.save()
                    c = createCaptcha()
                    generate_captcha = False
                    context = {
                        "message":f"Password has been changed for {login_id}",
                        "fmsg":"pswrd changed",
                        "captcha": c 
                    }
                    return render(request,'LoginPage.html', context)
                    
            except UserProfile.DoesNotExist:
                context = {
                  "message":"Invalid loginid"
                }    
                return render(request,'ForgotPassword.html',context)
            
            except Exception as e:
                context={
                    "message":"some error occured"
                }
                print(str(e))
                return render(request,'ForgotPassword.html',context)
            
        else:
            context = {
                "message":"Passwords entered does not match"
            }
            return render(request,'ForgotPassword.html',context)
        
    return render (request,'ForgotPassword.html')

    
    



# function to create Dashboard
@login_required #to restric access of dashboard view to authorized user only(i.e. only loggedin user)
@csrf_exempt 
def Dashboard_Page(request):
    try:
        cursor = connections['default'].cursor()

        cursor.execute("select id,Name  from StateMaster")
        result=cursor.fetchall()
        #print(result)
        
        value_list = []

        len_state = len(result)
        state_Dict = []
        for i in range(len_state):
            state_Dict.append(result[i][1])

        #print(result[0][1])
        #print(state_Dict)

        #state_Dict = []
        #state_Dict = [] 
        # for i in range(len_state): 
        #     state_Dict.append(result[i]) 
        context = {
            "state_Dict" : result
        }
        return render(request, "Dashboard.html", context)
    finally:
        cursor.close()





from django.shortcuts import render
from django.http import JsonResponse

# @csrf_exempt
# def Get_district(request):
#     if request.method == "POST":
#         cursor = connections['default'].cursor()
#         state_id = request.POST.get("Stateid")
#         print(state_id)
#         query = f"Exec Get_District_Name_List @State_id={state_id}"
#         cursor.execute(query)
#         # Fetch the results
#         result = cursor.fetchall()
#         #print(result)

#         # Check if there is any data to render
#         if result:
#             len_District = len(result)
    
#             District_Dict = []

#             for i in range(len_District):
#                 District_Dict.append(result[i][1])

#             # Render the data in a dropdown template
#             # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
#             return JsonResponse(result, safe=False) 
#         else:
#             # If there's no data, return an empty response or appropriate message
#             return JsonResponse(result, safe=False)
#     else:
#         # Handle non-POST requests here
#         return JsonResponse({"error": "Invalid request method"})
    
    
    

##################### Get Site  Data
@csrf_exempt
def Get_Site_Status(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()
        state_id = request.POST.get("Stateid")
        district_id=request.POST.get("Districtid")
       # print(state_id,district_id)
        query = f"Exec Get_Site_Status @Stateid={state_id}, @Districid={district_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        #print(result)

        # Check if there is any data to render
        if result:
            len_site = len(result)
    
            Site_Dict = []

            for i in range(len_site):
                Site_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False) 
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
    



@csrf_exempt
def Get_Device_Status(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()
        state_id = request.POST.get("Stateid")
        district_id=request.POST.get("Districtid")
        #print(state_id,district_id)
        query = f"Exec Get_Device_Status @Stateid={state_id}, @Districid={district_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        #print(result)

        # Check if there is any data to render
        if result:
            len_Device = len(result)
    
            Device_Dict = []

            for i in range(len_Device):
                Device_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False) 
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
    
@csrf_exempt
def Get_StatusPanel(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()
        state_id = request.POST.get("Stateid")
        district_id=request.POST.get("Districtid")
        #devive_no="All"
        #print(state_id,district_id)
        query = f"Exec Show_Status_Panel @State_id={state_id}, @Distict_id={district_id},@Device_No='ALL'"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
       # print(result)
        # Check if there is any data to render
        if result:
            len_Device = len(result)
    
            Device_Dict = []

            for i in range(len_Device):
                Device_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False) 
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})


@csrf_exempt
def Get_Alter(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()
        state_id = request.POST.get("Stateid")
        district_id=request.POST.get("Districtid")
        #devive_no="All"
        #print(state_id,district_id)
        query = f"Exec Alart_Py  @State_id={state_id}, @Distict_id={district_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        print(result)
        # Check if there is any data to render
        
        return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
    
    
    
    
@csrf_exempt
def Get_Alter_Details(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()
        type=request.POST.get("type")
        state_id = request.POST.get("Stateid")
        district_id=request.POST.get("Districtid")
        #devive_no="All"
        #print(state_id,district_id)
        query = f"Exec Alart_Count_Py  @COUNTER={type},@State_id={state_id}, @Distict_id={district_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        print(result)
        # Check if there is any data to render
        
        return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})    




    
@csrf_exempt    
def Get_GMap(request):
    if request.method == "POST":

        cursor = connections['default'].cursor()
        state_id = request.POST.get("Stateid")
        #print(state_id);
        district_id=request.POST.get("Districtid")
        print(state_id,district_id)

        query = f"Exec Show_Map @StatesId={state_id}, @CityId={district_id}, @DeviceNo='ALL', @Orgid=1"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        #print(result)

        # Check if there is any data to render
        if result:
            len_Device = len(result)
    
            Device_Dict = []

            for i in range(len_Device):
                Device_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False) 
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
    
def Device_Info(request):
    context={
        
    }
    return render(request, "DeviceInfo.html", context)

@csrf_exempt
def ShowSiteDetails(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()
        Site_id = request.POST.get("Site_id")
        #devive_no="All"
        #print(state_id,district_id)
        query = f"Exec Get_SiteDetails @Siteid={Site_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
       # print(result)
        # Check if there is any data to render
        #Get_Device_Data(request);
        if result:
            len_Device = len(result)
    
            Device_Dict = []

            for i in range(len_Device):
                Device_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False) 
        
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"}) 
    
   
@csrf_exempt   
def Get_Water_Details(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()

        Site_id = request.POST.get("Site_id")
        #devive_no="All"
        #print(state_id,district_id)
        query = f"Exec Get_Water_Status @Siteid={Site_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        #print(result);
        # Check if there is any data to render
        if result:
            len_Device = len(result)
    
            Device_Dict = []

            for i in range(len_Device):
                Device_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False) 
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
    
@csrf_exempt
def Get_Chlorine_Chart(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()

        Site_id = request.POST.get("Site_id")
        #devive_no="All"   
        query = f"Exec Water_Chlorine_Char @site_id={Site_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        #print(result);
        # Check if there is any data to render
        if result:
            len_Chlorine = len(result)
    
            Chlorine_Dict = []

            for i in range(len_Chlorine):
                Chlorine_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False) 
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})


    
@csrf_exempt
def Get_Pressure_Chart(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()

        Site_id = request.POST.get("Site_id")
        #devive_no="All"
        #print(state_id,district_id)
        query = f"Exec Water_Pressure_Char @site_id={Site_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        #print(result);
        # Check if there is any data to render
        if result:
            len_Chlorine = len(result)
    
            Chlorine_Dict = []

            for i in range(len_Chlorine):
                Chlorine_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False) 
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
    
    
def Show_device_Setting(request):
    context={
        
    }
    return render(request, "Show_device_Setting.html", context)



def Device_Data(request):
    context={
        
    }
    return render(request, "deviceData.html", context)


@csrf_exempt
def Get_Install_Date(request):
    #print("ttttttt")
    if request.method == "POST":
        cursor = connections['default'].cursor()
        Site_id = request.POST.get("Site_id")
        query = f"Exec Get_Installationdate @Site_id={Site_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
       # print("rrrrrrrrrrr");
        #print(result);
        # Check if there is any data to render
        if result:
            len_Chlorine = len(result)
    
            Chlorine_Dict = []

            #for i in range(len_Chlorine):
            Chlorine_Dict.append(result)

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False)
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
@csrf_exempt
def Get_Device_Data(request):
    #print("ttttttt")
    global device_data_detail
    if request.method == "POST":
        cursor = connections['default'].cursor()
        Site_id = request.POST.get("Site_id")
        FromDate = request.POST.get("fromDate")
        ToDate = request.POST.get("toDate")
        Chlorine=request.POST.get("chlorineValue")
        #print(Chlorine)
        Pressure =request.POST.get("pressureValue")
        #devive_no="All"
        #print(state_id,district_id)
        query = f"Exec Get_Device_Data_List_py @Site_id={Site_id},@DateFrom='{FromDate}',@dateTo='{ToDate}',@Chlorine='{Chlorine}',@Pressure='{Pressure}'"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
        device_data_detail = result
        Get_Install_Date_pdf(Site_id);
       # print("rrrrrrrrrrr");
        #print(result);
        # Check if there is any data to render
        if result:
            len_Chlorine = len(result)
    
            Chlorine_Dict = []

            for i in range(len_Chlorine):
                Chlorine_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False)
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
    
       # return render(request, "HtmlFolder/deviceData.html", context)



def Setting_Data(request):
    context={
        
    }
    return render(request, "SettingCommand.html", context) 


@csrf_exempt
def Get_SettingDevice_Data(request):
    if request.method == "POST":
        cursor = connections['default'].cursor()
        comm_id = request.POST.get("comm_id")
       
        device = request.POST.get("device")
        
        Str1 = request.POST.get("Str1")
  
        Str2 = request.POST.get("Str2")
        
        query = f"Exec Update_Device_Setting_Py @Comm_id='{comm_id}',@device_number='{device}',@Str1='{Str1}',@Str2='{Str2}'"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
       # print("rrrrrrrrrrr");
        #print(result);
        # Check if there is any data to render
        if result:
            len_Chlorine = len(result)
    
            Chlorine_Dict = []

            #for i in range(len_Chlorine):
            Chlorine_Dict.append(result)
            #Chlorine_Dict.append(result[i][1])

            # Render the data in a dropdown template
            # return render(request, "HtmlFolder/Dashboard.html", {"District_Dict": District_Dict})
            return JsonResponse(result, safe=False)
        else:
            # If there's no data, return an empty response or appropriate message
            return JsonResponse(result, safe=False)
    else:
        # Handle non-POST requests here
        return JsonResponse({"error": "Invalid request method"})
    
       # return render(request, "HtmlFolder/deviceData.html", context)
       
       
       
    
@csrf_exempt 
def get_city_list(request):
    try:
        if request.method == "POST":
            cursor = connections['default'].cursor()
            stateId = request.POST.get("StateId")
          
            query = f"exec [dbo].[GetCityList_Py] {stateId};"
            cursor.execute(query)
            result = cursor.fetchall()
            #print(result)
            return JsonResponse(result, safe=False)
        else:
            return JsonResponse({"error": "Invalid request method"})
    except Exception as e:
        return JsonResponse({"error":str(e)})
    
    
    
    
def Get_Install_Date_pdf(Site_id):
    #print("ttttttt")
    #if request.method == "POST":
        cursor = connections['default'].cursor()
        Site_id = Site_id
        query = f"Exec Get_Installationdate @Site_id={Site_id}"
        cursor.execute(query)
        # Fetch the results
        result = cursor.fetchall()
     
        global install_date
        global name
        global address
        global serial
        
        install_date = result[0][0]
        name = result[0][1]
        address =result[0][2]
        serial = result[0][3]    
    
    
    ####### pdf genetrator and download 
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if pdf.err:
        return HttpResponse("Invalid PDF", status_code=400, content_type='text/plain')
    return HttpResponse(result.getvalue(), content_type='application/pdf')

def pdf_view(request, *args, **kwargs):
    data = {
        'result': device_data_detail,
        'install_date' : install_date,
        'name'  :  name,
        'address': address,
        'serial' : serial
    }
    return render_to_pdf('Device_DataPdf.html', data)

def Setting_pdf_view(request, *args, **kwargs):
    data = {
        'result': device_data_detail,
        'install_date' : install_date,
        'name'  :  name,
        'address': address,
        'serial' : serial
    }
    return render_to_pdf('Setting_data_Pdf.html', data)









    






