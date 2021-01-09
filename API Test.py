import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import re
from math import sin, cos, sqrt, atan2, radians

list1 = []
list2 = []
list3 = []
list4 = []
list5 = []
list6 = []
list7 = []
list8 = []
res1 = []
CoordV = 0

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open("MakerDB").sheet1
data = sheet.get_all_records()
endrow = len(data)
endrow = endrow + 1


def Size(list1):
    input1 = input("Size:")

    if input1 == "ME":
        LOS = sheet.findall("ME")
        ROS = sheet.findall("LA")
        IOS = sheet.findall("XL")
        LOS = LOS + ROS + IOS
    elif input1 == "SM":
        LOS = sheet.findall("ME")
        ROS = sheet.findall("LA")
        IOS = sheet.findall("XL")
        SOS = sheet.findall("SM")
        LOS = LOS + ROS + IOS + SOS
    elif input1 == "XS":
        LOS = sheet.findall("ME")
        ROS = sheet.findall("LA")
        IOS = sheet.findall("XL")
        SOS = sheet.findall("SM")
        AOS = sheet.findall("XS")
        LOS = LOS + ROS + IOS + SOS + AOS
    elif input1 == "LA":
        ROS = sheet.findall("LA")
        IOS = sheet.findall("XL")
        LOS = ROS + IOS
    elif input1 == "XL":
        IOS = sheet.findall("XL")
        LOS = IOS

    LOS = str(LOS)
    for x in range(1, endrow + 1):
        x = str(x)
        find = "R" + x + "C"
        if find in LOS:
            Name = sheet.cell(x, 1).value
            list1.append(Name)


def Material(list1, list2, list3):
    input2 = input("Material:")


    if input2 == "ABS":
        IRS = sheet.findall("ABS")
    if input2 == "PLA":
        IRS = sheet.findall("PLA")
    IRS = str(IRS)
    x = 1
    for x in range(1, endrow + 1):
        x = str(x)
        find = "R" + x + "C"
        if find in IRS:
            Name = sheet.cell(x, 1).value
            if Name in list1:
                list2.append(Name)
                list3.append(x)

def CoordC(CoordV):
    CoordV = 0
    URL = "https://maps.googleapis.com/maps/api/geocode/json"
    key = 'AIzaSyBkR6KAsXVhAM1FhMMCi9IneisUHJ_EwVQ'
    city = 'Toronto'
    PARAMS = {'address':input("Input origin address:"), 'components=locality':city, 'key':key,}
    r = requests.get(url=URL, params=PARAMS).json()
    json_longlatv = r
    Value = json_longlatv['results'][0]['geometry']['location']
    CoordV = Value
    print(CoordV)
    return CoordV


def CompareCM(list3, list4, list7):
    x = 0
    Customer = CoordC(CoordV)
    Customer = str(Customer)
    res1 = [float(s) for s in re.findall(r'-?\d+\.?\d*', Customer)]
    for p in range(0, len(list3)):
        MakerC = sheet.cell(list3[x], 7)
        MakerC = str(MakerC)
        res = [float(s) for s in re.findall(r'-?\d+\.?\d*', MakerC)]
        list6 = res
        list6.remove(int(7.0))
        list7.append(list6)
        x = x + 1
    return res1

def compareLL(list7, list3):

    # approximate radius of earth in km
    res1 = CompareCM(list3, list4, list7)
    R = 6373.0
    lat1 = radians(int(res1[0]))
    lon1 = radians(int(res1[1]))
    for i in range(0, len(list3)):
        lat2 = radians(list7[i][1])
        lon2 = radians(list7[i][2])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        result1 = (distance, int(list3[i]))
        list8.append(result1)
        i = i + 1
    return list8

def sortFirst(val):
    return val[0]

def List():
    result = compareLL(list7, list3)
    result.sort(key=sortFirst)
    x = 0
    candeliver = 0
    for x in range(0, len(result)):
        temp = result[x][1]
        distance = str(result[x][0])
        name = sheet.cell(temp, 1).value
        deliver = str(sheet.cell(temp, 9).value)
        if deliver == 'FALSE':
            print(name)
            print(temp)
            print('Can not deliver')
            candeliver = False
        if deliver > distance:
            print(name)
            print(temp)
            print('Can not deliver')
            candeliver = False
        if deliver < distance:
            print(name)
            print(temp)
            print('Can deliver')
            candeliver = True








Size(list1)
Material(list1, list2, list3)
List()