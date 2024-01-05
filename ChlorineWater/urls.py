from . import views
from django.urls import path,include

urlpatterns = [
    path('',views.LoginPage,name="LoginPage"),
    #path('Chlorine_Pressure',views.LoginPage,name="LoginPage"),
    path('Login',views.LoginPage,name="LoginPage"),
    path('ForgotPassword',views.ForgotPassword,name="ForgotPassword"),
    path('logout', views.logoutUser, name="logout"),
    ####### device information
    path('Device_Info',views.Device_Info,name="Device_Info"),
    
    ##### show device data
    
    path('Show_device_Setting',views.Show_device_Setting,name="Show_device_Setting"),
    
    ######## Device Data Page
    path('Device_Data', views.Device_Data,name="Device_Data"),
    path('Get_Install_Date', views.Get_Install_Date,name="Get_InstallationDate"),
    path('Get_Device_Data', views.Get_Device_Data,name="Get_DeviceData"),
    
    ######## Setting Command  Page
    path('Setting_Data', views.Setting_Data,name="SettingData"),
    path('Get_SettingDevice_Data', views.Get_SettingDevice_Data,name="Get_SettingCommand"),
    
    path('Dashboard_Page',views.Dashboard_Page,name="Dashboard_Page"),
   # path('Get_district', views.Get_district, name="Get_districtData"),
    path('Get_Site_Status', views.Get_Site_Status, name="Get_SiteStatus"),
    path('Get_Device_Status', views.Get_Device_Status, name="Get_DeviceStatus"),
    path('Get_GMap', views.Get_GMap, name="Get_GoogalMap"),
    path('Get_Alter', views.Get_Alter, name="GetAlter"),
    path('Get_Alter_Details',views.Get_Alter_Details,name="Get_AlterDetails"),
    path('StatusPanel', views.Get_StatusPanel, name="StatusPanel"),
    path('ShowSiteDetails', views.ShowSiteDetails, name="ShowSiteDetails"),
    path('Get_Water_Details', views.Get_Water_Details, name="GetwaterDetails"),
    path('Get_Pressure_Chart',views.Get_Pressure_Chart, name="Get_PressureChart"),
    path('Get_Chlorine_Chart', views.Get_Chlorine_Chart, name="Get_ChlorineChart"),
    path('get_city_list', views.get_city_list, name='Get_CityList'),
    path('Get_pdf', views.pdf_view, name="Get_pdf"),
    path('Setting_pdf_view', views.Setting_pdf_view, name="Setting_pdf_view")
    

]