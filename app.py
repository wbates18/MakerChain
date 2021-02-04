# App.py Flask MakerChain Website

# Imports
from flask import Flask, render_template, request, session, redirect, url_for, send_file
import hashlib  # hashing passwords
import pymysql as mysql  # mysql connection
import re
import requests
from datetime import timedelta
import os, shutil  # os paths
import smtplib, ssl  # ssl email server connections
from email.mime.text import MIMEText  # email server smtp formatting
from email.mime.multipart import MIMEMultipart  # email server smtp formatting
from math import radians, sin, atan2, sqrt, cos  # math algorithms for distance and cost calculations
import trimesh  # stl file analyzing
from itsdangerous import URLSafeTimedSerializer  # sending emails with tokens
app = Flask(__name__)
uploads_dir = os.path.join("/Users/home/PycharmProjects/MakerChainFlask/static", 'UploadedPictures')


def Sort_Tuple(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][1] > tup[j + 1][1]):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

app.secret_key = 'mQ^Ow]IE}$9y[nN~m+<1Q(FnrN:/ZM'
ALLOWED_EXTENTIONS = ".png", ".jpeg", ".jpg", ".JPG", ".JPEG", ".PNG"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECURITY_PASSWORD_SALT'] = 'two_hippos_in_a_bath'

conn = mysql.connect(user='root', password='KaulBates2020a', host='127.0.0.1', database='sys1')  #connection to mysql -- will be hashed
cursor = conn.cursor()



@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

@app.before_request
def perm():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(hours=4)


@app.route('/MakerOptions.html', methods=["POST", "GET"])
def MOptions():
    # sql query
    temp = "SELECT Printer, Printer2, Printer3, Printer4, Size, Size2, Size3, Size4, Material, Colour, Range1 FROM \
    sys1.MUser WHERE id = %s"
    t = session['id']
    temp3 = cursor.execute(temp, t)
    conn.commit()
    ex = list(cursor)
    p1 = ex[0][0]
    p2 = ex[0][1]
    p3 = ex[0][2]
    p4 = ex[0][3]
    s1 = ex[0][4]
    s2 = ex[0][5]
    s3 = ex[0][6]
    s4 = ex[0][7]
    mat = ex[0][8]
    colour = ex[0][9]
    Range = ex[0][10]
    if "abs" in mat:  # What colours and materials to show
        m1 = True
    else:
        m1 = False
    if "pla" in mat:
        m2 = True
    else:
        m2 = False
    if "nylon" in mat:
        m3 = True
    else:
        m3 = False
    if "resin" in mat:
        m4 = True
    else:
        m4 = False
    if "petg" in mat:
        m5 = True
    else:
        m5 = False
    if "black" in colour:
        c1 = True
    else:
        c1 = False
    if "white" in colour:
        c2 = True
    else:
        c2 = False
    if "gold" in colour:
        c3 = True
    else:
        c3 = False
    if "red" in colour:
        c4 = True
    else:
        c4 = False
    if "green" in colour:
        c5 = True
    else:
        c5 = False
    if "blue" in colour:
        c6 = True
    else:
        c6 = False
    mat = str(mat)  # 122 - 163 -- formatting
    mat = mat.replace("abs, ", "")
    mat = mat.replace("pla, ", "")
    mat = mat.replace("resin, ", "")
    mat = mat.replace("nylon, ", "")
    mat = mat.replace("petg, ", "")
    omat = mat
    colour = str(colour)
    colour = colour.replace("black, ", "")
    colour = colour.replace("white, ", "")
    colour = colour.replace("gold, ", "")
    colour = colour.replace("red, ", "")
    colour = colour.replace("green, ", "")
    colour = colour.replace("blue, ", "")
    ocolour = colour
    if request.method == "POST":
        id = session['id']
        size = request.form.get('size')
        size2 = request.form.get("size2")
        size3 = request.form.get('size3')
        size4 = request.form.get('size4')
        printer = request.form.get('Printer')
        printer2 = request.form.get('Printer2')
        printer3 = request.form.get("Printer3")
        printer4 = request.form.get("Printer4")
        material = request.form.getlist('mat')
        colour = request.form.getlist('colour')
        othercolour = request.form.get('othercolour')
        othermat = request.form.get('othermat')
        range = request.form.get('range')
        material = str(material)
        test = material.replace("'", "")
        test1 = test.replace("[", "")
        material = test1.replace("]", "")
        colour = str(colour)
        test = colour.replace("'", "")
        test1 = test.replace("[", "")
        colour = test1.replace("]", "")
        if othercolour != '':
            colour = colour + ", " + othercolour
        if othermat != '':
            material = material + ", " + othermat
        temp5 = "UPDATE sys1.MUser SET Material = %s, Colour = %s, Range1 = %s, Size = %s, Size2 = %s, Size3 = %s,\
                Size4 = %s, Printer = %s, Printer2 = %s, Printer3 = %s, Printer4 = %s WHERE id = %s"
        temp6 = (material, colour, range, size, size2, size3, size4, printer, printer2, printer3, printer4,
                 session['id'])
        temp3 = cursor.execute(temp5, temp6)
        conn.commit()
        session['maker'] = True
        return render_template("profilemaker.html", variable=session['name'], variable2=session['email'],
                               variable3=session['address'], variable4=session['city'], pfp=session['pfp'])
    return render_template('MakerOptions.html', p1=p1, p2=p2, p3=p3, p4=p4, s1=s1, s2=s2, s3=s3, s4=s4, m1=m1, m2=m2,
                           m3=m3, m4=m4, m5=m5, c1=c1, c2=c2, c3=c3, c4=c4, c5=c5, c6=c6, othermat=omat,
                           othercolour=ocolour, r1=Range, variable=session['name'], pfp=session['pfp'])


@app.route('/profilemaker.html')  # Display profile for maker
def profileM():
    name = session['name']
    email = session['email']
    address = session['address']
    city = session['city']
    if session['maker'] != True:
        return render_template("profile.html", variable=name, variable2=email, variable3=address, variable4=city,
                               pfp=session['pfp'])
    else:
        return render_template("profilemaker.html", variable=name, variable2=email, variable3=address, variable4=city,
                               pfp=session['pfp'])


@app.route('/profile.html')  # Display profile for customer
def profile():
    if session.get('loggedin') == True:
        name = session['name']
        email = session['email']
        address = session['address']
        city = session['city']
        if session['maker'] == True:
            return render_template("profilemaker.html", variable=name, variable2=email, variable3=address, variable4=city, pfp=session['pfp'])
        else:
            return render_template("profile.html", variable=name, variable2=email, variable3=address, variable4=city, pfp=session['pfp'])
    else:
        return render_template("index.html")


@app.route('/index.html')  # Main Page
def h():
    session['loggedin'] = False
    return render_template("index.html")


@app.route('/logout.html')  # Logout page clears all the sessions -- cookies
def logout():
    x = 0
    session.clear()
    return render_template("index.html")



@app.route('/')  # Page when just on makerchain.ca
def home():
    folder = 'static/UploadedPictures'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))  # Deletes all temp files
    folder = 'static/UploadedFiles'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    session['loggedin'] = False
    return render_template("index.html")


@app.route('/login.html', methods=["GET", "POST"])  # Login page
def login():
    if request.method == "POST":
        email = request.form.get('email')
        email = email.lower()
        password = request.form.get('password')
        temp = "SELECT Email, Password1, Name, id FROM sys1.CUser WHERE Email = %s"  # Credential verification
        temp1 = email
        temp3 = cursor.execute(temp, temp1)
        conn.commit()
        temp4 = list(cursor)
        if email == temp4[0][0]:
            if hashlib.sha256(password.encode()).hexdigest() == temp4[0][1]:  # Formatting and checking hashed password
                name = temp4[0][2]
                id = temp4[0][3]
                temp = "SELECT Address FROM sys1.CUser WHERE id = %s"  # getting session information to allow transfer of information
                temp2 = id
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                temp4 = list(cursor)
                Address = temp4[0][0]
                temp = "SELECT City FROM sys1.CUser WHERE id = %s"
                temp2 = id
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                temp4 = list(cursor)
                City = temp4[0][0]
                session['loggedin'] = True
                session['id'] = str(id)
                session['name'] = name
                session['email'] = email
                session['address'] = Address
                session['city'] = City
                temp = "SELECT pfp FROM sys1.CUser WHERE id = %s"
                temp3 = cursor.execute(temp, session['id'])
                result = cursor.fetchone()
                if result[0] == None:
                    pfp = os.path.join("/static/dashboard/", "picture.jpg")  # if pfp isn't uploaded use default
                    session['pfp'] = pfp
                else:
                    file_extention1 = ''
                    if 'PNG' in str(result[0][0]):
                        file_extention1 = '.png'
                    elif 'JPG' in str(result[0][0]):
                        file_extention1 = '.jpg'
                    elif 'JPEG' in str(result[0][0]):
                        file_extention1 = '.jpeg'
                    else:
                        file_extention1 = '.png'
                    with open('static/UploadedPictures/pfp' + session['id'] + file_extention1, 'wb') as file:  # write temp pfp file so it can display on html page
                        file.write(result[0])
                        session['pfp'] = 'static/UploadedPictures/pfp' + session['id'] + file_extention1
                        session['ext'] = file_extention1
                        file.close()
                name = session['name']
                temp = "SELECT Name FROM sys1.MUser WHERE id = %s"
                temp2 = id
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                test = list(cursor)
                id = session['id']
                if test == []:
                    session['maker'] = False
                    query = "SELECT Verified FROM sys1.CUser WHERE id = %s"
                    query2 = id
                    cursor.execute(query, query2)
                    result2 = list(cursor)
                    print(result2)
                    if result2[0] != ('1',):
                        return redirect(url_for('ver'))  # send verification email
                    else:
                        session['Verified'] = True
                        return redirect(url_for("Chome"))
                else:
                    session['maker'] = True  # if the account is a maker
                    select = "SELECT Material, Colour, LongLat, Range1, Printer, Printer2, Printer3, Printer4, Size,\
                        Size2, Size3, Size4 FROM sys1.MUser WHERE id = %s"  # all session information
                    ss = id
                    cursor.execute(select, ss)
                    conn.commit()
                    ss1 = list(cursor)
                    material = ss1[0][0]
                    colour = ss1[0][1]
                    longlat = ss1[0][2]
                    range1 = ss1[0][3]
                    p1 = ss1[0][4]
                    p2 = ss1[0][5]
                    p3 = ss1[0][6]
                    p4 = ss1[0][7]
                    s1 = ss1[0][8]
                    s2 = ss1[0][9]
                    s3 = ss1[0][10]
                    s4 = ss1[0][11]
                    session['longlat'] = longlat
                    session['range'] = range1
                    query = "SELECT Verified FROM sys1.CUser WHERE id = %s"
                    query2 = id
                    cursor.execute(query, query2)
                    result2 = list(cursor)
                    if result2[0] != ('1',):
                        return redirect(url_for('ver'))  # send verification email
                    else:
                        session['Verified'] = True
                        return redirect(url_for("Mhome"))
            else:
                return render_template('login.html', Incorrect=1)
        else:
            return render_template('login.html', Email=0)
    return render_template('login.html')


@app.route('/resetpass.html', methods=["POST", "GET"])  # reset password module
def passr():
    if request.method == "POST":
        email = request.form.get('email')
        session['temail'] = email
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['token'] = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])  # Create token
        session['email'] = email

        sender_email = "makerchain.canada@gmail.com"
        receiver_email = email
        password = 'KaulBates2020'

        message = MIMEMultipart('alternative')
        message['Subject'] = "Password Reset"
        message['From'] = sender_email
        message['To'] = receiver_email

        text = """\
               Hi,
               Reset your password by clicking here"""
        html = """\
               <html>
                   <body>
                       <p>Hi,<br>
                       Reset your password by clicking <a href="http://127.0.0.1:5000/reset/{}">here</a><br>
                       </p>
                   </body>
               </html>
             """.format(session['token'])  # Email prep

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())  # send email via SMTP server

        return render_template('resetpasssent.html')
    return render_template("resetpass.html")

@app.route('/reset/<token>')  # When you click the link
def passv(token):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=86400  # Verify
        )
    except:  # If not valid

        email = session['email']
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['token'] = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

        sender_email = "makerchain.canada@gmail.com"
        receiver_email = email
        password = 'KaulBates2020'

        message = MIMEMultipart('alternative')
        message['Subject'] = "Password Reset"
        message['From'] = sender_email
        message['To'] = receiver_email

        text = """\
                       Hi,
                       Reset your password by clicking here"""
        html = """\
                       <html>
                           <body>
                               <p>Hi,<br>
                               Reset your password by clicking <a href="http://127.0.0.1:5000/reset/{}">here</a><br>
                               </p>
                           </body>
                       </html>
                     """.format(session['token'])  # create token link

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())  # send email again

        return render_template("LinknotValid.html")
    if session['email'] == email:  # if valid, check if email is correct and return to the next function
        return render_template("ChangePass.html")



@app.route('/ChangePass.html', methods=["POST", "GET"])  # Enter new password
def reset():
    if request.method == "POST":
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        if password1 == password2:  # confirm password twice
            query = "UPDATE sys1.CUser SET Password1 = %s WHERE email = %s"  # Set new password in DB
            query2 = (hashlib.sha256(password1.encode()).hexdigest(), session['email'])  # hashed password
            session.pop('email')  # clear session email
            cursor.execute(query, query2)
            conn.commit()
            return render_template("login.html")
        else:
            return render_template("ChangePass.html", Failed=1)
    return render_template("ChangePass.html")


@app.route('/DeleteOrder.html')  # Deletes order from DB when declined -- after email sent
def DelOrder():
    query1 = "DELETE FROM sys1.Orders WHERE OrderNum = %s"
    cursor.execute(query1, session['OrderNum'])
    conn.commit()
    if session['maker'] == True:
        return render_template("clientHomemaker.html")
    else:
        return render_template("clientHome.html")


@app.route('/clientHomemaker.html')  # Home page for maker
def Mhome():
    #Orders
    def Nmaxelements(list1, N):
        final_list = []

        for i in range(0, N):
            max1 = 0

            for j in range(len(list1)):
                if list1[j] > max1:
                    max1 = list1[j];

            list1.remove(max1);
            final_list.append(max1)

        return final_list
        # Orders

    def Current():
        final_listC = []
        query3 = "SELECT OrderNum FROM sys1.Orders WHERE Cid = %s AND PROGRESS != %s"
        query4 = (session['id'], "FINISHED")
        cursor.execute(query3, query4)
        result3 = list(cursor)
        print(result3)
        resultC = []
        for x in result3:
            resultC.append(x[0])
        if len(resultC) == 1:
            final_listC = Nmaxelements(resultC, 1)
        elif len(resultC) == 2:
            final_listC = Nmaxelements(resultC, 2)
        elif len(resultC) == 3:
            final_listC = Nmaxelements(resultC, 3)
        elif len(resultC) == 4:
            final_listC = Nmaxelements(resultC, 4)
        elif len(resultC) >= 5:
            final_listC = Nmaxelements(resultC, 5)
        else:
            return [], 0, 0, 0, 0, 0, 0, 0, 0, 0
        resultC = final_listC

        result_listC = []
        for i in range(0, len(final_listC)):
            result_list1C = []
            query = "SELECT OrderNum, Mid, PROGRESS, Quantity, File, Colours, Material, Infill, Quality, Distance FROM sys1.Orders WHERE OrderNum = %s"
            cursor.execute(query, final_listC[i])
            result1C = list(cursor)
            if result1C[0][1] == None:
                continue
            query2 = "SELECT Name, Email FROM sys1.CUser WHERE id = %s"
            cursor.execute(query2, result1C[0][1])
            result2C = list(cursor)
            for x in range(0, len(result1C[0])):
                result_list1C.insert(x, result1C[0][x])
            result_list1C.insert(10, result2C[0][0])
            result_list1C.insert(11, result2C[0][1])
            result_listC.append(result_list1C)
        nameC = []
        for x in range(0, len(result_listC)):
            nameC.append(result_listC[x][10])
        emailC = []
        for x in range(0, len(result_listC)):
            emailC.append(result_listC[x][11])
        # file = []
        # for x in range(0, len(result_list)):      FILEDOWNLOAD.HTML --- WITH THIS STUFF IN IT
        #     file.append(result_list[x][10])
        quantityC = []
        for x in range(0, len(result_listC)):
            quantityC.append(result_listC[x][3])
        progressC = []
        for x in range(0, len(result_listC)):
            progressC.append(result_listC[x][2])
        infillC = []
        for x in range(0, len(result_listC)):
            infillC.append(result_listC[x][7])
        qualityC = []
        for x in range(0, len(result_listC)):
            qualityC.append(result_listC[x][8])
        distanceC = []
        for x in range(0, len(result_listC)):
            distanceC.append(result_listC[x][9])
        y = 1
        finalC = str()
        FinalC = []
        for x in range(0, len(result_listC)):
            material = result_listC[x][6]
            material = material.title()
            materialsep = material.split(", ")
            colour = result_listC[x][5]
            colour = colour.title()
            coloursep = colour.split(", ")
            for i in range(0, len(coloursep)):
                if y == 1:
                    colourb = "(" + coloursep[i] + ")"
                    colourb = colourb.replace(" ", "")
                    finalC = materialsep[i] + colourb
                    y += 1
                else:
                    colourb = "(" + coloursep[i] + ")"
                    colourb = colourb.replace(" ", "")
                    finalC = finalC + ", " + materialsep[i] + colourb
            FinalC.append(finalC)

        if len(resultC) == 1:
            session['OrderNumC1'] = result_listC[0][0]
        if len(resultC) == 2:
            session['OrderNumC1'] = result_listC[0][0]
            session['OrderNumC2'] = result_listC[1][0]
        if len(resultC) == 3:
            session['OrderNumC1'] = result_listC[0][0]
            session['OrderNumC2'] = result_listC[1][0]
            session['OrderNumC3'] = result_listC[2][0]
        if len(resultC) == 4:
            session['OrderNumC1'] = result_listC[0][0]
            session['OrderNumC2'] = result_listC[1][0]
            session['OrderNumC3'] = result_listC[2][0]
            session['OrderNumC4'] = result_listC[3][0]
        if len(resultC) >= 5:
            session['OrderNumC1'] = result_listC[0][0]
            session['OrderNumC2'] = result_listC[1][0]
            session['OrderNumC3'] = result_listC[2][0]
            session['OrderNumC4'] = result_listC[3][0]
            session['OrderNumC5'] = result_listC[4][0]

        print(resultC, nameC, emailC, quantityC, progressC, infillC, qualityC, distanceC, FinalC)

        return resultC, nameC, emailC, quantityC, progressC, infillC, qualityC, distanceC, FinalC

    def Previous():
        final_listP = []
        query3 = "SELECT OrderNum FROM sys1.Orders WHERE Mid = %s AND PROGRESS = %s"
        query4 = (session['id'], "FINISHED")
        cursor.execute(query3, query4)
        result3 = list(cursor)
        resultP = []
        for x in result3:
            resultP.append(x[0])
        if len(resultP) == 1:
            final_listP = Nmaxelements(resultP, 1)
        elif len(resultP) == 2:
            final_listP = Nmaxelements(resultP, 2)
        elif len(resultP) == 3:
            final_listP = Nmaxelements(resultP, 3)
        elif len(resultP) == 4:
            final_listP = Nmaxelements(resultP, 4)
        elif len(resultP) >= 5:
            final_listP = Nmaxelements(resultP, 5)
        else:
            return [], 0, 0, 0, 0, 0, 0, 0, 0
        resultP = final_listP

        result_listP = []
        for i in range(0, len(final_listP)):
            result_list1P = []
            query = "SELECT OrderNum, Cid, PROGRESS, Quantity, File, Colours, Material, Infill, Quality, Distance FROM sys1.Orders WHERE OrderNum = %s"
            cursor.execute(query, final_listP[i])
            result1P = list(cursor)
            if result1P[0][1] == None:
                continue
            query2 = "SELECT Name, Email FROM sys1.CUser WHERE id = %s"
            cursor.execute(query2, result1P[0][1])
            result2P = list(cursor)
            for x in range(0, len(result1P[0])):
                result_list1P.insert(x, result1P[0][x])
            result_list1P.insert(10, result2P[0][0])
            result_list1P.insert(11, result2P[0][1])
            result_listP.append(result_list1P)

        nameP = []
        for x in range(0, len(result_listP)):
            nameP.append(result_listP[x][10])
        emailP = []
        for x in range(0, len(result_listP)):
            emailP.append(result_listP[x][11])
        # file = []
        # for x in range(0, len(result_list)):      FILEDOWNLOAD.HTML --- WITH THIS STUFF IN IT
        #     file.append(result_list[x][10])
        # print(file)
        quantityP = []
        for x in range(0, len(result_listP)):
            quantityP.append(result_listP[x][3])
        progressP = []
        for x in range(0, len(result_listP)):
            progressP.append(result_listP[x][2])
        infillP = []
        for x in range(0, len(result_listP)):
            infillP.append(result_listP[x][7])
        qualityP = []
        for x in range(0, len(result_listP)):
            qualityP.append(result_listP[x][8])
        distanceP = []
        for x in range(0, len(result_listP)):
            distanceP.append(result_listP[x][9])
        y = 1
        finalP = str()
        FinalP = []
        for x in range(0, len(result_listP)):
            material = result_listP[x][6]
            material = material.title()
            materialsep = material.split(", ")
            colour = result_listP[x][5]
            colour = colour.title()
            coloursep = colour.split(", ")
            for i in range(0, len(coloursep)):
                if y == 1:
                    colourb = "(" + coloursep[i] + ")"
                    colourb = colourb.replace(" ", "")
                    finalP = materialsep[i] + colourb
                    y = 2
                else:
                    colourb = "(" + coloursep[i] + ")"
                    colourb = colourb.replace(" ", "")
                    finalP = finalP + ", " + materialsep[i] + colourb
            FinalP.append(finalP)

        if len(resultP) == 1:
            session['OrderNumP1'] = result_listP[0][0]
        if len(resultP) == 2:
            session['OrderNumP1'] = result_listP[0][0]
            session['OrderNumP2'] = result_listP[1][0]
        if len(resultP) == 3:
            session['OrderNumP1'] = result_listP[0][0]
            session['OrderNumP2'] = result_listP[1][0]
            session['OrderNumP3'] = result_listP[2][0]
        if len(resultP) == 4:
            session['OrderNumP1'] = result_listP[0][0]
            session['OrderNumP2'] = result_listP[1][0]
            session['OrderNumP3'] = result_listP[2][0]
            session['OrderNumP4'] = result_listP[3][0]
        if len(resultP) >= 5:
            session['OrderNumP1'] = result_listP[0][0]
            session['OrderNumP2'] = result_listP[1][0]
            session['OrderNumP3'] = result_listP[2][0]
            session['OrderNumP4'] = result_listP[3][0]
            session['OrderNumP5'] = result_listP[4][0]

        print(resultP, nameP, emailP, quantityP, progressP, infillP, qualityP, distanceP, FinalP)

        return resultP, nameP, emailP, quantityP, progressP, infillP, qualityP, distanceP, FinalP

    resultP, nameP, emailP, quantityP, progressP, infillP, qualityP, distanceP, FinalP = Previous()
    resultC, nameC, emailC, quantityC, progressC, infillC, qualityC, distanceC, FinalC = Current()

    P = 0
    C = 0
    if session.get('loggedin') != True:
        return render_template("index.html")
    else:
        session['log'] = True
        items = []
        if session['Verified'] == True:
            if len(resultP) == 1:
                P = 1
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 2:
                P = 2
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 3:
                P = 3
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 4:
                P = 4
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) >= 5:
                P = 5
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            else:
                P = 0
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            return render_template("clientHomemaker.html", variable=session['name'], variable2="Signed Up",
                                   pfp=session['pfp'], numbP=P, nameP=nameP, emailP=emailP,
                                   quantityP=quantityP,
                                   progressP=progressP, infillP=infillP, qualityP=qualityP,
                                   distanceP=distanceP,
                                   FinalP=FinalP, numbC=C, nameC=nameC,
                                   emailC=emailC, quantityC=quantityC, progressC=progressC, infillC=infillC,
                                   qualityC=qualityC, distanceC=distanceC, FinalC=FinalC)
        else:
            if len(resultP) == 1:
                P = 1
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 2:
                P = 2
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 3:
                P = 3
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 4:
                P = 4
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) >= 5:
                P = 5
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            else:
                P = 0
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            return render_template("clientHomemaker.html", variable=session['name'], variable2=False, pfp=session['pfp'],
                                   numbP=P, nameP=nameP, emailP=emailP,
                                   quantityP=quantityP,
                                   progressP=progressP, infillP=infillP, qualityP=qualityP,
                                   distanceP=distanceP,
                                   FinalP=FinalP, numbC=C, nameC=nameC,
                                   emailC=emailC, quantityC=quantityC, progressC=progressC, infillC=infillC,
                                   qualityC=qualityC, distanceC=distanceC, FinalC=FinalC)


@app.route('/clientHome.html')  # Same as above for customer
def Chome():

    def Nmaxelements(list1, N):
        final_list = []

        for i in range(0, N):
            max1 = 0

            for j in range(len(list1)):
                if list1[j] > max1:
                    max1 = list1[j];

            list1.remove(max1);
            final_list.append(max1)

        return final_list
        # Orders

    def Current():
        final_listC = []
        query3 = "SELECT OrderNum FROM sys1.Orders WHERE Cid = %s AND PROGRESS != %s"
        query4 = (session['id'], "FINISHED")
        cursor.execute(query3, query4)
        result3 = list(cursor)
        print(result3)
        resultC = []
        for x in result3:
            resultC.append(x[0])
        if len(resultC) == 1:
            final_listC = Nmaxelements(resultC, 1)
        elif len(resultC) == 2:
            final_listC = Nmaxelements(resultC, 2)
        elif len(resultC) == 3:
            final_listC = Nmaxelements(resultC, 3)
        elif len(resultC) == 4:
            final_listC = Nmaxelements(resultC, 4)
        elif len(resultC) >= 5:
            final_listC = Nmaxelements(resultC, 5)
        else:
            return [], 0, 0, 0, 0, 0, 0, 0, 0
        resultC = final_listC

        result_listC = []
        for i in range(0, len(final_listC)):
            result_list1C = []
            query = "SELECT OrderNum, Mid, PROGRESS, Quantity, File, Colours, Material, Infill, Quality, Distance FROM sys1.Orders WHERE OrderNum = %s"
            cursor.execute(query, final_listC[i])
            result1C = list(cursor)
            if result1C[0][1] == None:
                continue
            query2 = "SELECT Name, Email FROM sys1.CUser WHERE id = %s"
            cursor.execute(query2, result1C[0][1])
            result2C = list(cursor)
            for x in range(0, len(result1C[0])):
                result_list1C.insert(x, result1C[0][x])
            result_list1C.insert(10, result2C[0][0])
            result_list1C.insert(11, result2C[0][1])
            result_listC.append(result_list1C)
        nameC = []
        for x in range(0, len(result_listC)):
            nameC.append(result_listC[x][10])
        emailC = []
        for x in range(0, len(result_listC)):
            emailC.append(result_listC[x][11])
        # file = []
        # for x in range(0, len(result_list)):      FILEDOWNLOAD.HTML --- WITH THIS STUFF IN IT
        #     file.append(result_list[x][10])
        quantityC = []
        for x in range(0, len(result_listC)):
            quantityC.append(result_listC[x][3])
        progressC = []
        for x in range(0, len(result_listC)):
            progressC.append(result_listC[x][2])
        infillC = []
        for x in range(0, len(result_listC)):
            infillC.append(result_listC[x][7])
        qualityC = []
        for x in range(0, len(result_listC)):
            qualityC.append(result_listC[x][8])
        distanceC = []
        for x in range(0, len(result_listC)):
            distanceC.append(result_listC[x][9])
        y = 1
        finalC = str()
        FinalC = []
        for x in range(0, len(result_listC)):
            material = result_listC[x][6]
            material = material.title()
            materialsep = material.split(", ")
            colour = result_listC[x][5]
            colour = colour.title()
            coloursep = colour.split(", ")
            for i in range(0, len(coloursep)):
                if y == 1:
                    colourb = "(" + coloursep[i] + ")"
                    colourb = colourb.replace(" ", "")
                    finalC = materialsep[i] + colourb
                    y += 1
                else:
                    colourb = "(" + coloursep[i] + ")"
                    colourb = colourb.replace(" ", "")
                    finalC = finalC + ", " + materialsep[i] + colourb
            FinalC.append(finalC)


        if len(resultC) == 1:
            session['OrderNumC1'] = result_listC[0][0]
        if len(resultC) == 2:
            session['OrderNumC1'] = result_listC[0][0]
            session['OrderNumC2'] = result_listC[1][0]
        if len(resultC) == 3:
            session['OrderNumC1'] = result_listC[0][0]
            session['OrderNumC2'] = result_listC[1][0]
            session['OrderNumC3'] = result_listC[2][0]
        if len(resultC) == 4:
            session['OrderNumC1'] = result_listC[0][0]
            session['OrderNumC2'] = result_listC[1][0]
            session['OrderNumC3'] = result_listC[2][0]
            session['OrderNumC4'] = result_listC[3][0]
        if len(resultC) >= 5:
            session['OrderNumC1'] = result_listC[0][0]
            session['OrderNumC2'] = result_listC[1][0]
            session['OrderNumC3'] = result_listC[2][0]
            session['OrderNumC4'] = result_listC[3][0]
            session['OrderNumC5'] = result_listC[4][0]

        print(resultC, nameC, emailC, quantityC, progressC, infillC, qualityC, distanceC, FinalC)

        return resultC, nameC, emailC, quantityC, progressC, infillC, qualityC, distanceC, FinalC



    def Previous():
        final_listP = []
        query3 = "SELECT OrderNum FROM sys1.Orders WHERE Cid = %s AND PROGRESS = %s"
        query4 = (session['id'], "FINISHED")
        cursor.execute(query3, query4)
        result3 = list(cursor)
        print(result3)
        resultP = []
        for x in result3:
            resultP.append(x[0])
        if len(resultP) == 1:
            final_listP = Nmaxelements(resultP, 1)
        elif len(resultP) == 2:
            final_listP = Nmaxelements(resultP, 2)
        elif len(resultP) == 3:
            final_listP = Nmaxelements(resultP, 3)
        elif len(resultP) == 4:
            final_listP = Nmaxelements(resultP, 4)
        elif len(resultP) >= 5:
            final_listP = Nmaxelements(resultP, 5)
        else:
            return [], 0, 0, 0, 0, 0, 0, 0, 0, 0
        resultP = final_listP

        result_listP = []
        for i in range(0, len(final_listP)):
            result_list1P = []
            query = "SELECT OrderNum, Mid, PROGRESS, Quantity, File, Colours, Material, Infill, Quality, Distance FROM sys1.Orders WHERE OrderNum = %s"
            cursor.execute(query, final_listP[i])
            result1P = list(cursor)
            if result1P[0][1] == None:
                continue
            query2 = "SELECT Name, Email FROM sys1.CUser WHERE id = %s"
            cursor.execute(query2, result1P[0][1])
            result2P = list(cursor)
            for x in range(0, len(result1P[0])):
                result_list1P.insert(x, result1P[0][x])
            result_list1P.insert(10, result2P[0][0])
            result_list1P.insert(11, result2P[0][1])
            result_listP.append(result_list1P)

        nameP = []
        for x in range(0, len(result_listP)):
            nameP.append(result_listP[x][10])
        emailP = []
        for x in range(0, len(result_listP)):
            emailP.append(result_listP[x][11])
        # file = []
        # for x in range(0, len(result_list)):      FILEDOWNLOAD.HTML --- WITH THIS STUFF IN IT
        #     file.append(result_list[x][10])
        # print(file)
        quantityP = []
        for x in range(0, len(result_listP)):
            quantityP.append(result_listP[x][3])
        progressP = []
        for x in range(0, len(result_listP)):
            progressP.append(result_listP[x][2])
        infillP = []
        for x in range(0, len(result_listP)):
            infillP.append(result_listP[x][7])
        qualityP = []
        for x in range(0, len(result_listP)):
            qualityP.append(result_listP[x][8])
        distanceP = []
        for x in range(0, len(result_listP)):
            distanceP.append(result_listP[x][9])
        y = 1
        finalP = str()
        FinalP = []
        for x in range(0, len(result_listP)):
            material = result_listP[x][6]
            material = material.title()
            materialsep = material.split(", ")
            colour = result_listP[x][5]
            colour = colour.title()
            coloursep = colour.split(", ")
            for i in range(0, len(coloursep)):
                if y == 1:
                    colourb = "(" + coloursep[i] + ")"
                    colourb = colourb.replace(" ", "")
                    finalP = materialsep[i] + colourb
                    y = 2
                else:
                    colourb = "(" + coloursep[i] + ")"
                    colourb = colourb.replace(" ", "")
                    finalP = finalP + ", " + materialsep[i] + colourb
            FinalP.append(finalP)


        if len(resultP) == 1:
            session['OrderNumP1'] = result_listP[0][0]
        if len(resultP) == 2:
            session['OrderNumP1'] = result_listP[0][0]
            session['OrderNumP2'] = result_listP[1][0]
        if len(resultP) == 3:
            session['OrderNumP1'] = result_listP[0][0]
            session['OrderNumP2'] = result_listP[1][0]
            session['OrderNumP3'] = result_listP[2][0]
        if len(resultP) == 4:
            session['OrderNumP1'] = result_listP[0][0]
            session['OrderNumP2'] = result_listP[1][0]
            session['OrderNumP3'] = result_listP[2][0]
            session['OrderNumP4'] = result_listP[3][0]
        if len(resultP) >= 5:
            session['OrderNumP1'] = result_listP[0][0]
            session['OrderNumP2'] = result_listP[1][0]
            session['OrderNumP3'] = result_listP[2][0]
            session['OrderNumP4'] = result_listP[3][0]
            session['OrderNumP5'] = result_listP[4][0]

        print(resultP, nameP, emailP, quantityP, progressP, infillP, qualityP, distanceP, FinalP)

        return resultP, nameP, emailP, quantityP, progressP, infillP, qualityP, distanceP, FinalP


    resultP, nameP, emailP, quantityP, progressP, infillP, qualityP, distanceP, FinalP = Previous()
    resultC, nameC, emailC, quantityC, progressC, infillC, qualityC, distanceC, FinalC = Current()

    P = 0
    C = 0
    if session.get('loggedin') != True:
        return render_template("index.html")
    else:
        session['log'] = True
        items = []
        if session['Verified'] == True:
            if len(resultP) == 1:
                P = 1
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 2:
                P = 2
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 3:
                P = 3
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 4:
                P = 4
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) >= 5:
                P = 5
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            else:
                P = 0
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            return render_template("clientHome.html", variable=session['name'], variable2="Signed Up",
                                   pfp=session['pfp'], numbP=P, nameP=nameP, emailP=emailP,
                                   quantityP=quantityP,
                                   progressP=progressP, infillP=infillP, qualityP=qualityP,
                                   distanceP=distanceP,
                                   FinalP=FinalP, numbC=C, nameC=nameC,
                                   emailC=emailC, quantityC=quantityC, progressC=progressC, infillC=infillC,
                                   qualityC=qualityC, distanceC=distanceC, FinalC=FinalC)
        else:
            if len(resultP) == 1:
                P = 1
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 2:
                P = 2
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 3:
                P = 3
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) == 4:
                P = 4
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            elif len(resultP) >= 5:
                P = 5
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            else:
                P = 0
                if len(resultC) == 1:
                    C = 1
                elif len(resultC) == 2:
                    C = 2
                elif len(resultC) == 3:
                    C = 3
                elif len(resultC) == 4:
                    C = 4
                elif len(resultC) >= 5:
                    C = 5
                else:
                    C = 0
            return render_template("clientHome.html", variable=session['name'], variable2=False, pfp=session['pfp'],
                                   numbP=P, nameP=nameP, emailP=emailP,
                                   quantityP=quantityP,
                                   progressP=progressP, infillP=infillP, qualityP=qualityP,
                                   distanceP=distanceP,
                                   FinalP=FinalP, numbC=C, nameC=nameC,
                                   emailC=emailC, quantityC=quantityC, progressC=progressC, infillC=infillC,
                                   qualityC=qualityC, distanceC=distanceC, FinalC=FinalC)


@app.route('/signup.html', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        fname = request.form.get('fname')  # access the data inside
        lname = request.form.get('lname')
        email = request.form.get('email')
        email = email.lower()
        address = request.form.get('address')
        city = request.form.get('city')
        password = request.form.get('pass')
        cpassword = request.form.get('cpass')
        if password == cpassword:  # If confirm and pass are same
            password = hashlib.sha256(password.encode()).hexdigest()  # hash password
            temp = cursor.execute("SELECT Email FROM sys1.CUser")
            ifemail = (list(cursor))
            ifemail = str(ifemail)
            if email in ifemail:
                return render_template('signup.html', Email=1)  # Already used email
            else:
                URL = "https://maps.googleapis.com/maps/api/geocode/json"  # 546 - 551 -- google maps api
                key = 'AIzaSyBkR6KAsXVhAM1FhMMCi9IneisUHJ_EwVQ'
                city = 'Toronto'
                PARAMS = {'address': address, 'components=locality': city, 'key': key, }
                r = requests.get(url=URL, params=PARAMS).json()
                json_longlatv = r
                if json_longlatv == {'results': [], 'status': 'ZERO_RESULTS'}:
                    return render_template('signup.html', Add=1)
                else:
                    name = fname + ' ' + lname
                    test = "INSERT INTO sys1.CUser (Name, Email, Address, City, Password1, Verified) VALUES\
                        (%s, %s, %s, %s, %s, 0)"
                    test2 = (name, email, address, city, password)
                    test3 = cursor.execute(test, test2)
                    conn.commit()
                    temp = "SELECT id FROM sys1.CUser WHERE Email = %s"
                    temp2 = email
                    temp3 = cursor.execute(temp, temp2)
                    id = list(cursor)
                    id = str(id)
                    temp1 = id.replace("[(", "")
                    id = temp1.replace(",)]", "")
                    session['loggedin'] = True
                    session['id'] = id
                    session['name'] = name
                    session['email'] = email
                    session['address'] = address
                    session['city'] = city
                    session['maker'] = False  # all sessions set up
                    pfp = os.path.join("/static/dashboard/", "picture.jpg")  # set default pfp
                    session['pfp'] = pfp
                    name = session['name']
                    session['maker'] = False
                    return redirect(url_for('ver'))  # verify email
        else:
            return render_template('signup.html', Match=0)

    return render_template("signup.html")


@app.route('/confirm/<token>')  # Conformation Email link
def verification(token):

    serializer4 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer4.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=86400  # If it is within a day, and all valid
        )
    except:

        serializer4 = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # else resend
        session['tokenV'] = serializer4.dumps(session['email'], salt=app.config['SECURITY_PASSWORD_SALT'])

        sender_email = "makerchain.canada@gmail.com"
        receiver_email = session['email']
        password = 'KaulBates2020'

        message = MIMEMultipart('alternative')
        message['Subject'] = "Email Confirmation"
        message['From'] = sender_email
        message['To'] = receiver_email

        text = """\
                   Hi,
                   Please verify your account by clicking here"""
        html = """\
                   <html>
                       <body>
                           <p>Hi,<br>
                           Please verify your account by clicking \
                           <a href="http://127.0.0.1:5000/confirm/{}">here</a><br>
                           </p>
                       </body>
                   </html>
                 """.format(session['tokenV'])

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())  # Send email
        return render_template("LinknotValid.html")

    if session['email'] == email:
        query = "SELECT Verified FROM sys1.CUser WHERE Email = %s"
        query2 = session['email']
        cursor.execute(query, query2)
        result = list(cursor)
        if result[0] == ('1',):
            return render_template("AlreadyConfirmed.html")
        else:
            query3 = "UPDATE sys1.CUser SET Verified = 1 WHERE Email = %s"
            query4 = email
            cursor.execute(query3, query4)
            conn.commit()
            result = list(cursor)
            if session['maker'] == True:
                session['Verified'] = True
                return redirect(url_for('Mhome'))  # Return home after verification
            else:
                session['Verified'] = True
                return redirect(url_for('Chome'))


@app.route('/verification.html')
def ver():
    serializer4 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    session['tokenV'] = serializer4.dumps(session['email'], salt=app.config['SECURITY_PASSWORD_SALT'])

    sender_email = "makerchain.canada@gmail.com"
    receiver_email = session['email']
    password = 'KaulBates2020'

    message = MIMEMultipart('alternative')
    message['Subject'] = "Account Verification"
    message['From'] = sender_email
    message['To'] = receiver_email

    text = """\
           Hi,
           Please verify your account by clicking here"""
    html = """\
           <html>
               <body>
                   <p>Hi,<br>
                   Please verify your account by clicking <a href="http://127.0.0.1:5000/confirm/{}">here</a><br>
                   </p>
               </body>
           </html>
         """.format(session['tokenV'])  # Confirmation email

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    return render_template('verification.html')


@app.route('/upgrade.html', methods=["POST", "GET"])  # Upgrade to maker
def upgrade():
    name = session['name']
    if request.method == "POST":
        if session.get('loggedin') == True:
            id = session['id']
            address = session['address']
            size = request.form.get('size')
            size2 = request.form.get("size2")
            size3 = request.form.get('size3')
            size4 = request.form.get('size4')
            printer = request.form.get('Printer')
            printer2 = request.form.get('Printer2')
            printer3 = request.form.get("Printer3")
            printer4 = request.form.get("Printer4")
            material = request.form.getlist('mat')
            colour = request.form.getlist('colour')
            material2 = request.form.getlist('mat2')
            colour2 = request.form.getlist('colour2')
            material3 = request.form.getlist('mat3')
            colour3 = request.form.getlist('colour3')
            material4 = request.form.getlist('mat4')
            colour4 = request.form.getlist('colour4')
            othercolour = request.form.get('othercolour')
            othermat = request.form.get('othermat')
            othercolour2 = request.form.get('othercolour2')
            othermat2 = request.form.get('othermat2')
            othercolour3 = request.form.get('othercolour3')
            othermat3 = request.form.get('othermat3')
            othercolour4 = request.form.get('othercolour4')
            othermat4 = request.form.get('othermat4')
            range1 = request.form.get('range')
            extruder1 = request.form.get('extrude')
            extruder2 = request.form.get('extrude2')
            extruder3 = request.form.get('extrude3')
            extruder4 = request.form.get('extrude4')
            if printer == '' or size == '' or (material == [] and othermat == '') or \
                    (colour == [] and othercolour == '') or range1 == '' or extruder1 == []:  # If some fields are empty
                return render_template('upgrade.html', variable=name, NotFilled=True)
            else:
                if (material != [] and othermat != '') or (material2 != [] and othermat2 != '') or \
                        (material3 != [] and othermat3 != '') or (material4 != [] and othermat4 != ''):  # Materials or colours repeat
                    return render_template('upgrade.html', variable=name, oneMat=True)
                else:
                    if othermat != '' and material == []:  # Formatting
                        material = othermat + ", "
                    if othermat2 != '' and material2 == []:
                        material2 = othermat2 + ", "
                    if othermat3 != '' and material3 == []:
                        material3 = othermat3 + ", "
                    if othermat4 != '' and material4 == []:
                        material4 = othermat4 + ", "

                    if material3 == []:
                        if material == material2:
                            return render_template('upgrade.html', variable=name, repeat=True)
                    elif material4 == []:
                        if material == material2 or material == material3 or material2 == material3:
                            return render_template('upgrade.html', variable=name, repeat=True)
                    elif material4 != []:
                        if material == material2 or material == material3 or material == material4 or \
                                material2 == material3 or material2 == material4 or material3 == material4:
                            return render_template('upgrade.html', variable=name, repeat=True)

                    coloursa = ''
                    coloursa2 = ''
                    coloursa3 = ''
                    coloursa4 = ''
                    y = 0
                    for y in range(0, len(colour)):
                        if y == 0:
                            coloursa = colour[y]
                        else:
                            coloursa = coloursa + ", " + colour[y]
                    if othercolour != '':
                        colour = othercolour + ", "
                    else:
                        colour = coloursa + ", " + othercolour
                    y = 0
                    for y in range(0, len(colour2)):
                        if y == 0:
                            coloursa2 = colour2[y]
                        else:
                            coloursa2 = coloursa2 + ", " + colour2[y]
                    if othercolour2 != '':
                        colour2 = othercolour2 + ", "
                    else:
                        colour2 = coloursa2 + ", " + othercolour2
                    y = 0
                    for y in range(0, len(colour3)):
                        if y == 0:
                            coloursa3 = colour3[y]
                        else:
                            coloursa3 = coloursa3 + ", " + colour3[y]
                    if othercolour3 != '':
                        colour3 = othercolour3 + ", "
                    else:
                        colour3 = coloursa3 + ", " + othercolour3
                    y = 0
                    for y in range(0, len(colour4)):
                        if y == 0:
                            coloursa4 = colour4[y]
                        else:
                            coloursa4 = coloursa4 + ", " + colour4[y]
                    if othercolour4 != '':
                        colour4 = othercolour4 + ", "
                    else:
                        colour4 = coloursa4 + ", " + othercolour4

                    if material2 == []:
                        material2 = ''
                    if material3 == []:
                        material3 = ''
                    if material4 == []:
                        material4 = ''
                    if colour2 == ', ':
                        colour2 = ''
                    if colour3 == ', ':
                        colour3 = ''
                    if colour4 == ', ':
                        colour4 = ''
                    URL = "https://maps.googleapis.com/maps/api/geocode/json"
                    key = 'AIzaSyBkR6KAsXVhAM1FhMMCi9IneisUHJ_EwVQ'
                    city = 'Toronto'
                    PARAMS = {'address': address, 'components=locality': city, 'key': key }  # Distance
                    r = requests.get(url=URL, params=PARAMS).json()
                    json_longlatv = r
                    Value = json_longlatv['results'][0]['geometry']['location']
                    Value = str(Value)
                    Value = Value.replace("{", "")
                    Value = Value.replace("}", "")
                    Value = Value.replace("'", "")
                    temp = "INSERT INTO sys1.MUser (id, Name, Address, Material, Colour, Material2, Colour2, Material3,\
                        Colour3, Material4, Colour4, LongLat, Range1, Printer, Printer2, Printer3, Printer4, Size,\
                        Size2, Size3, Size4, Extruder1, Extruder2, Extruder3, Extruder4) VALUES\
                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,\
                        %s, %s, %s, %s)"  # Insert data into db
                    temp2 = (id, name, address, material, colour, material2, colour2, material3, colour3, material4,
                             colour4, Value, range1, printer, printer2, printer3, printer4, size, size2, size3, size4,
                             extruder1, extruder2, extruder3, extruder4)
                    temp3 = cursor.execute(temp, temp2)
                    conn.commit()
                    session['maker'] = True
                    session['longlat'] = Value
                    session['range'] = range1
                    return render_template('clientHomemaker.html', variable=name, variable5=True, pfp=session['pfp'])
        else:
            return render_template("index.html")
    return render_template("upgrade.html", variable=name, pfp=session['pfp'])


@app.route('/order.html', methods=["POST", "GET"])  # Order Module
def order():
    SutableM = []
    SutableMN = []
    if request.method == "POST":
        file = request.files['file']
        if file == "<FileStorage: '' ('application/octet-stream')>":  # If file is empty
            return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
        upload = file.stream.read()
        with open('static/UploadedFiles/Upload' + session['id'] + ".stl", 'wb') as file:
            file.write(upload)
            file.close()  # Upload file to storage temporaily for calculations
        mesh1 = trimesh.load('static/UploadedFiles/Upload' + session['id'] + ".stl")
        Length = mesh1.extents[0]
        Width = mesh1.extents[1]
        Height = mesh1.extents[2]
        EstimateInv = False
        valid_volume = mesh1.is_winding_consistent and mesh1.is_watertight and mesh1.volume > 0  # mesh1.volume = volume
        if valid_volume == False:
            return render_template("Invalidstl.html")
        if (mesh1.volume / 1000) > 1000:
            EstimateInv = True  # It is unrealistically large, meaning en error has occured, set into invalid mode.
        Psize = str()
        if Width <= 100 or Length <= 100 or Height <= 100:  # Calculate size
            Psize = "XS"
        if (101 <= Width <= 200) or (101 <= Length <= 200) or (101 <= Height <= 200):
            Psize = "SM"
        if (201 <= Width <= 300) or (201 <= Length <= 300) or (201 <= Height <= 300):
            Psize = "ME"
        if (301 <= Width <= 400) or (301 <= Length <= 400) or (301 <= Height <= 400):
            Psize = "LA"
        if Width > 400 or Length > 400 or Height > 400:
            Psize = "XL"

        extruder = 0
        materials = []
        colours = []
        Quantity = request.form.get('Quantity')
        material = request.form.get('material')
        materialo = request.form.get('materialo')
        material2 = request.form.get('material2')
        materialo2 = request.form.get('materialo2')
        material3 = request.form.get('material3')
        materialo3 = request.form.get('materialo3')
        material4 = request.form.get('material4')
        materialo4 = request.form.get('materialo4')
        material5 = request.form.get('material5')
        materialo5 = request.form.get('materialo5')
        colour = request.form.get('colour')
        colouro = request.form.get('colouro')
        colour2 = request.form.get('colour2')
        colouro2 = request.form.get('colouro2')
        colour3 = request.form.get('colour3')
        colouro3 = request.form.get('colouro3')
        colour4 = request.form.get('colour4')
        colouro4 = request.form.get('colouro4')
        colour5 = request.form.get('colour5')
        colouro5 = request.form.get('colouro5')
        infill = request.form.get('infill')
        infillo = request.form.get('infillo')
        quality = request.form.get('quality')
        qualityo = request.form.get('qualityo')
        waters = request.form.get('waters')
        multi = request.form.get('multi')  # get all variables
        try:
            Quantity = int(Quantity)
        except:
            return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])  # If anything in't filled or filled twice
        if Quantity == 0:
            return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
        if waters == 'y':
            waters = True
        if waters == None:
            waters = False
        if infillo != None and infill == 'on':
            infill = infillo
        if infill == None and infillo == None:
            return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
        if infillo == None and infill == 'on':
            return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
        if qualityo != None and quality == 'on':
            quality = qualityo
        if quality == None and qualityo == None:
            return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
        if quality == 'on' and qualityo == None:
            return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
        if materialo != "":
            material = materialo.lower()
        if materialo2 != "":
            material2 = materialo2.lower()
        if materialo3 != "":
            material3 = materialo3.lower()
        if materialo4 != "":
            material4 = materialo4.lower()
        if materialo5 != "":
            material5 = materialo5.lower()
        if colouro != "":
            colour = colouro.lower()
        if colouro2 != "":
            colour2 = colouro2.lower()
        if colouro3 != "":
            colour3 = colouro3.lower()
        if colouro4 != "":
            colour4 = colouro4.lower()
        if colouro5 != "":
            colour5 = colouro5.lower()
        if multi == '1' or multi == None:  # Make lists of materials and colours
            extruder = [1, 2, 3, 4, 5]
            if material == '' or colour == '':
                return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
            else:
                if waters == True:
                    materials = [material, "waters"]
                else:
                    materials = [material]
                colours = [colour]
        if multi == '2':
            extruder = [2, 3, 4, 5]
            if material == '' or colour == '' or material2 == '' or colour2 == '':
                return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
            else:
                if waters == True:
                    materials = [material, material2, "waters"]
                else:
                    materials = [material, material2]
                colours = [colour, colour2]
        if multi == '3':
            extruder = [3, 4, 5]
            if material == '' or colour == '' or material2 == '' or colour2 == '' or material3 == '' or colour3 == '':
                return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
            else:
                if waters == True:
                    materials = [material, material2, material3, "waters"]
                else:
                    materials = [material, material2, material3]
                colours = [colour, colour2, colour3]
        if multi == '4':
            extruder = [4, 5]
            if material == '' or colour == '' or material2 == '' or colour2 == '' or material3 == '' or\
                    colour3 == '' or material4 == '' or colour4 == '':
                return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
            else:
                if waters == True:
                    materials = [material, material2, material3, material4, "waters"]
                else:
                    materials = [material, material2, material3, material4]
                colours = [colour, colour2, colour3, colour4]
        if multi == "5":
            extruder = [5]
            if material == '' or colour == '' or material2 == '' or colour2 == '' or material3 == '' or\
                    colour3 == '' or material4 == '' or colour4 == '' or material5 == '' or colour5 == '':
                return render_template('order.html', Failed=1, pfp=session['pfp'], variable=session['name'])
            else:
                if waters == True:
                    materials = [material, material2, material3, material4, material5, "waters"]
                else:
                    materials = [material, material2, material3, material4, material5]
                colours = [colour, colour2, colour3, colour4, colour5]

        # Material -- 1st step, find makers with materials available.
        query = "SELECT * FROM sys1.MUser"
        cursor.execute(query)
        conn.commit()
        result2 = list(cursor)
        result3 = str(result2)

        amount = result3.count("(")
        z = 0
        for x in range(0, amount):
            zneed = len(materials)
            for y in range(0, len(materials)):  # For each user for each material, if it is available, with colour
                if materials[y] in result2[x][3]:
                    if materials[y] == 'waters':
                        continue
                    else:
                        if colours[y] in result2[x][4]:
                            z = z + 1
                elif (materials[y] + ", ") == result2[x][5]:
                    if colours[y] in result2[x][6]:
                        z = z + 1
                elif (materials[y] + ", ") == result2[x][7]:
                    if colours[y] in result2[x][8]:
                        z = z + 1
                elif (materials[y] + ", ") == result2[x][9]:
                    if colours[y] in result2[x][10]:
                        z = z + 1
            if zneed == z:
                z = 0
                SutableM.append(result2[x][0])
            else:
                continue


        if SutableM == []:
            return render_template("order.html", Match=0, pfp=session['pfp'], variable=session['name'])

        #Size -- 2nd step. Find makers with materials and sizes
        query = "SELECT Size, Size2, Size3, Size4, Extruder1, Extruder2, Extruder3, Extruder4, id FROM sys1.MUser"
        cursor.execute(query)
        conn.commit()
        result = list(cursor)
        result1 = str(result)
        amount = result1.count("(")
        for x in range(0, amount):
            if result[x][8] in SutableM:
                if result[x][1] != '':
                    if result[x][2] != '':
                        if result[x][3] != '':
                            for y in range(len(extruder)):  # For each sutable material maker, check size requirments.
                                if result[x][4] == extruder[y]:
                                    if result[x][0] == Psize:
                                        SutableMN.append(result[x][8])
                                        break
                                if result[x][5] == extruder[y]:
                                    if result[x][1] == Psize:
                                        SutableMN.append(result[x][8])
                                        break
                                if result[x][6] == extruder[y]:
                                    if result[x][2] == Psize:
                                        SutableMN.append(result[x][8])
                                        break
                                if result[x][7] == extruder[y]:
                                    if result[x][3] == Psize:
                                        SutableMN.append(result[x][8])
                                        break

                        else:
                            for y in range(len(extruder)):
                                if result[x][4] == extruder[y]:
                                    if result[x][0] == Psize:
                                        SutableMN.append(result[x][8])
                                        break
                                if result[x][5] == extruder[y]:
                                    if result[x][1] == Psize:
                                        SutableMN.append(result[x][8])
                                        break
                                if result[x][6] == extruder[y]:
                                    if result[x][2] == Psize:
                                        SutableMN.append(result[x][8])
                                        break
                    else:
                        for y in range(len(extruder)):
                            if result[x][4] == extruder[y]:
                                if result[x][0] == Psize:
                                    SutableMN.append(result[x][8])
                                    break
                            if result[x][5] == extruder[y]:
                                if result[x][1] == Psize:
                                    SutableMN.append(result[x][8])
                                    break
                else:
                    for y in range(len(extruder)):
                        if result[x][4] == extruder[y]:
                            if result[x][0] == Psize:
                                SutableMN.append(result[x][8])
                                break

        def test(SutableM, amount):  # If size not available, run other sizes
            SutableMN = []
            for x in range(0, amount):
                if result[x][8] in SutableM:
                    if result[x][1] != '':
                        if result[x][2] != '':
                            if result[x][3] != '':
                                for y in range(len(extruder)):
                                    if result[x][4] == extruder[y]:
                                        if result[x][0] in PsizeL:
                                            SutableMN.append(result[x][8])
                                            break
                                    if result[x][5] == extruder[y]:
                                        if result[x][1] in PsizeL:
                                            SutableMN.append(result[x][8])
                                            break
                                    if result[x][6] == extruder[y]:
                                        if result[x][2] in PsizeL:
                                            SutableMN.append(result[x][8])
                                            break
                                    if result[x][7] == extruder[y]:
                                        if result[x][3] in PsizeL:
                                            SutableMN.append(result[x][8])
                                            break

                            else:
                                for y in range(len(extruder)):
                                    if result[x][4] == extruder[y]:
                                        if result[x][0] in PsizeL:
                                            SutableMN.append(result[x][8])
                                            break
                                    if result[x][5] == extruder[y]:
                                        if result[x][1] in PsizeL:
                                            SutableMN.append(result[x][8])
                                            break
                                    if result[x][6] == extruder[y]:
                                        if result[x][2] in PsizeL:
                                            SutableMN.append(result[x][8])
                                            break
                        else:
                            for y in range(len(extruder)):
                                if result[x][4] == extruder[y]:
                                    if result[x][0] in PsizeL:
                                        SutableMN.append(result[x][8])
                                        break
                                if result[x][5] == extruder[y]:
                                    if result[x][1] in PsizeL:
                                        SutableMN.append(result[x][8])
                                        break
                    else:
                        for y in range(len(extruder)):
                            if result[x][4] == extruder[y]:
                                if result[x][0] in PsizeL:
                                    SutableMN.append(result[x][8])
                                    break

            return SutableMN

        # Size Adjust -- 3rd step. If size isn't available allow all others that could work.
        while SutableMN == []:  # If sizes aren't avaiable, run other sizes available
            if Psize == "XS":
                PsizeL = ["XS", "SM", "ME", "LA", "XL"]
                SutableMN = test(SutableM, amount)
                if SutableMN != []:
                    break
            if Psize == "SM":
                PsizeL = ["SM", "ME", "LA", "XL"]
                SutableMN = test(SutableM, amount)
                if SutableMN != []:
                    break
            if Psize == "ME":
                PsizeL = ["ME", "LA", "XL"]
                SutableMN = test(SutableM, amount)
                if SutableMN != []:
                    break
            if Psize == "LA":
                PsizeL = ["LA", "XL"]
                SutableMN = test(SutableM, amount)
                if SutableMN != []:
                    break
            else:
                return render_template("order.html", Match=0, pfp=session['pfp'], variable=session['name'])

        address = session["address"]
        city = session['city']
        URL = "https://maps.googleapis.com/maps/api/geocode/json"
        key = 'AIzaSyBkR6KAsXVhAM1FhMMCi9IneisUHJ_EwVQ'
        PARAMS = {'address': address, 'components=locality': city, 'key': key, }  # Distance Calculations
        r = requests.get(url=URL, params=PARAMS).json()
        CLongLat1 = r
        Value = CLongLat1['results'][0]['geometry']['location']
        CLongLat = str(Value)
        pairs = []
        res1 = [float(s) for s in re.findall(r'-?\d+\.?\d*', CLongLat)]
        for x in range(0, amount):
            if result2[x][0] in SutableMN:
                res2 = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(result2[x][11]))]
                R = 6373.0

                lat1 = radians(res1[0])
                lon1 = radians(res1[1])
                lat2 = radians(res2[0])
                lon2 = radians(res2[1])

                dlon = lon2 - lon1
                dlat = lat2 - lat1

                a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                c = 2 * atan2(sqrt(a), sqrt(1 - a))

                distance = R * c

                if distance <= int(result2[x][12]):
                    delivery = True

                else:
                    delivery = False
                pairs.append((int(result2[x][0]), distance))  # Id, distance
        price = []
        Sort_Tuple(pairs)
        best = pairs[0][0]
        P = 0
        x = 0
        for j in range(0, len(materials)):  # Price calculations
            if "pla" in str(materials[j]):
                price.append(0.06)
            if materials[j] == "abs":
                price.append(0.04)
            if materials[j] == "nylon":
                price.append(0.08)
            if materials[j] == "resin":
                price.append(0.06)
            if materials[j] == "petg":
                price.append(0.10)
            if materials[j] == "waters":
                price.append(0.13)
        for x in range(0, len(price)):
            P = P + price[x]
        x += 1
        distance = 0
        PriceW = P / x
        PriceM = PriceW * (mesh1.volume / 1000)
        PriceM = round(PriceM, 2)
        makerid = best
        customerid = session['id']
        quality1 = quality
        infill1 = infill
        quality = quality1 + 'mm'
        infill = infill1 + '%'
        PriceD = int()
        distance = float(distance)
        if distance == 0.0:
            PriceD = 0
        elif distance <= 5 and distance != 0.0:
            PriceD = 5
        elif distance <= 10 and distance >= 5.000001:
            PriceD = 7
        elif distance <= 20 and distance >= 10.00001:
            PriceD = 9
        elif distance <= 30 and distance >= 20.00001:
            PriceD = 12
        elif distance <= 40 and distance >= 30.00001:
            PriceD = 15
        elif distance <= 50 and distance >= 40.00001:
            PriceD = 18
        elif distance >= 50.000001:
            PriceD = 20

        add = int()
        if Psize == "XS":
            add = 4
        if Psize == "SM":
            add = 6
        if Psize == "ME":
            add = 9
        if Psize == "LA":
            add = 13
        if Psize == "XL":
            add = 17
        PriceM = PriceM * (int(infill1) / 100)
        PriceM = PriceM * Quantity
        PriceT = PriceM + PriceD + add
        PriceT = round(PriceT, 2)
        PriceM = round(PriceM, 2)
        volume = mesh1.volume / 1000

        volume = round(volume, 2)
        Mat = str()
        Col = str()
        for x in range(0, len(materials)):
            if x == 0:
                Mat = materials[x]
                Col = colours[x]
            else:
                Mat = Mat + ", " + materials[x]
                Col = Col + ", " + colours[x]

        customerid = int(customerid)  # All variables
        volume = float(volume)
        Psize = str(Psize)
        PriceM = float(PriceM)
        PriceD = float(PriceD)
        PriceT = float(PriceT)
        infill = str(infill)
        quality = str(quality)
        distance = float(distance)
        Quantity = int(Quantity)

        if EstimateInv == True:
            PriceM = 0
            PriceT = 0


        query = "INSERT INTO sys1.Orders (Cid, Mvol, Size, Material, Colours, PriceM, PriceD, PriceT, Infill, Quality,\
            Quantity, File, PROGRESS) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        query2 = (customerid, volume, Psize, Mat, Col, PriceM, PriceD, PriceT, infill, quality, Quantity, upload, "Pending")
        cursor.execute(query, query2)
        conn.commit()

        test = "SELECT LAST_INSERT_ID();"
        cursor.execute(test)
        conn.commit()
        OrderNum = list(cursor)
        OrderNum = OrderNum[0][0]
        session['OrderNum'] = OrderNum

        session['pairs'] = pairs

        if EstimateInv == True:  # Invalid trimesh calculation catch
            return render_template("OrderStlNotCalc.html")

        return redirect(url_for('viewoptions'))  # View options
    return render_template("order.html", pfp=session['pfp'], variable=session['name'])


@app.route('/viewoptions.html', methods=['GET', "POST"])
def viewoptions():
    pairs = session['pairs']
    Applicable = 0
    if len(pairs) <= 5:
        Applicable = len(pairs)
    elif len(pairs) >= 6:
        Applicable = 5

    Names = []
    Address = []
    Distance = []
    MatCol = []
    Email = []
    Printers = []
    PFP = []
    Id = []

    query5 = "SELECT PriceT FROM sys1.Orders WHERE OrderNum = %s"
    cursor.execute(query5, session['OrderNum'])
    resulte = list(cursor)
    PriceT = ''

    if resulte[0][0] == 0:
        PriceT = "?"  # Invalid trimesh
    else:
        PriceT = float(resulte[0][0])

    for x in range(0, len(pairs)):
        query = "SELECT * FROM sys1.MUser WHERE id = %s"
        query2 = pairs[x][0]
        cursor.execute(query, query2)
        result = list(cursor)

        query3 = "SELECT id, Name, Email, Address, City, Password1, pfp FROM sys1.CUser WHERE id = %s"
        query4 = pairs[x][0]
        cursor.execute(query3, query4)
        result5 = list(cursor)

        materialsColours = str()
        Names.append(result[0][1])
        Address.append(result[0][2])
        Distance.append(round(pairs[x][1], 1))
        Email.append(result5[0][2])
        Id.append(result[0][0])

        if result[0][5] != "":
            if result[0][7] != "":
                if result[0][9] != "":
                    materials1 = str(result[0][3]).replace(",", ":").upper()  # Formatting
                    col1 = str(result[0][4])
                    if col1[-1] == " ":
                        materialsColours1 = materials1 + (col1[:-2].title() + " - ")
                    else:
                        materialsColours1 = materials1 + (col1[:-1].title() + " - ")
                    materials2 = str(result[0][5]).replace(",", ":").upper()
                    col2 = str(result[0][6])
                    if col2[-1] == " ":
                        materialsColours2 = materials2 + (col2[:-2].title() + " - ")
                    else:
                        materialsColours2 = materials2 + (col2[:-1].title() + " - ")
                    materials3 = str(result[0][7]).replace(",", ":").upper()
                    col3 = str(result[0][8])
                    if col3[-1] == " ":
                        materialsColours3 = materials3 + (col3[:-2].title() + " - ")
                    else:
                        materialsColours3 = materials3 + (col3[:-1].title() + " - ")
                    materials4 = str(result[0][9]).replace(",", ":").upper()
                    col4 = str(result[0][10])
                    if col4[-1] == " ":
                        materialsColours4 = materials4 + col4[:-2].title()
                    else:
                        materialsColours4 = materials4 + col4[:-1].title()
                    materialsColours = materialsColours1 + materialsColours2 + materialsColours3 + materialsColours4

                else:
                    materials1 = str(result[0][3]).replace(",", ":").upper()
                    col1 = str(result[0][4])
                    if col1[-1] == " ":
                        materialsColours1 = materials1 + (col1[:-2].title() + " - ")
                    else:
                        materialsColours1 = materials1 + (col1[:-1].title() + " - ")
                    materials2 = str(result[0][5]).replace(",", ":").upper()
                    col2 = str(result[0][6])
                    if col2[-1] == " ":
                        materialsColours2 = materials2 + (col2[:-2].title() + " - ")
                    else:
                        materialsColours2 = materials2 + (col2[:-1].title() + " - ")
                    materials3 = str(result[0][7]).replace(",", ":").upper()
                    col3 = str(result[0][8])
                    if col3[-1] == " ":
                        materialsColours3 = materials3 + col3[:-2].title()
                    else:
                        materialsColours3 = materials3 + col3[:-1].title()
                    materialsColours = materialsColours1 + materialsColours2 + materialsColours3
            else:
                materials1 = str(result[0][3]).replace(",", ":").upper()
                col1 = str(result[0][4])
                if col1[-1] == " ":
                    materialsColours1 = materials1 + (col1[:-2].title() + " - ")
                else:
                    materialsColours1 = materials1 + (col1[:-1].title() + " - ")
                materials2 = str(result[0][5]).replace(",", ": ").upper()
                col2 = str(result[0][6])
                if col2[-1] == " ":
                    materialsColours2 = materials2 + col2[:-2].title()
                else:
                    materialsColours2 = materials2 + col2[:-1].title()
                materialsColours = materialsColours1 + materialsColours2
        else:
            materials = str(result[0][3]).replace(",", ":").upper()
            col = str(result[0][4])
            if col[-1] == " ":
                materialsColours = materials + col[:-2].title()
            else:
                materialsColours = materials + col[:-1].title()

        MatCol.append(materialsColours)

        if result[0][15] != "":
            if result[0][16] != "":
                if result[0][17] != "":
                    Printers1 = str(result[0][13]) + ", " + str(result[0][14]) + ", " + str(result[0][15]) + ", "\
                                + str(result[0][16])
                else:
                    Printers1 = str(result[0][13]) + ", " + str(result[0][14]) + ", " + str(result[0][15])
            else:
                Printers1 = str(result[0][13]) + ", " + str(result[0][14])
        else:
            Printers1 = str(result[0][13])

        Printers.append(Printers1)

        if result5[0][6] == None or str(result5[0][6]) == 'None':
            pfp = '/static/dashboard/picture.jpg'
        else:
            with open('static/UploadedPictures/pfp' + str(result[0][0]), 'wb') as file:  # pfp fetch
                file.write(result5[0][6])
                file.close()

            pfp = '/static/UploadedPictures/pfp' + str(result[0][0])

        PFP.append(pfp)

    if request.method == "POST":  # Get choice
        makerid = int()
        email = str()
        if request.form.get('submit1') == 'Choose':
            makerid = Id[0]
            email = Email[0]
        elif request.form.get('submit2') == 'Choose':
            makerid = Id[1]
            email = Email[1]
        elif request.form.get('submit3') == 'Choose':
            makerid = Id[2]
            email = Email[2]
        elif request.form.get('submit4') == 'Choose':
            makerid = Id[3]
            email = Email[3]
        elif request.form.get('submit5') == 'Choose':
            makerid = Id[4]
            email = Email[4]

        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Prep email
        session['tokenA'] = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenA = session['tokenA']

        serializer2 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenD'] = serializer2.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenD = session['tokenD']

        serializer3 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenF'] = serializer3.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenF = session['tokenF']

        sender_email = "makerchain.canada@gmail.com"
        receiver_email = email
        password = 'KaulBates2020'

        message = MIMEMultipart('alternative')
        message['Subject'] = "Order Requested"
        message['From'] = sender_email
        message['To'] = receiver_email

        OrderNum = session['OrderNum']

        req = "SELECT Mvol, Material, Colours, Infill, Quality, File, Cid, PriceT, Quantity FROM sys1.Orders WHERE\
         OrderNum = %s"  # 1528 - 1594 GETTING ALL INFO
        req1 = OrderNum
        cursor.execute(req, req1)
        results = list(cursor)

        customerid = results[0][6]
        session['CPrice'] = results[0][7]  # Get all price info


        req2 = "SELECT Name, Address, Email, City FROM sys1.CUser WHERE id = %s"
        req3 = customerid
        cursor.execute(req2, req3)
        results2 = list(cursor)
        session['CAddress'] = results2[0][1]


        req4 = "SELECT LongLat FROM sys1.MUser WHERE id = %s"
        req5 = makerid
        cursor.execute(req4, req5)
        results3 = list(cursor)

        req6 = "UPDATE sys1.Orders SET Mid = %s WHERE OrderNum = %s"
        req7 = (makerid, session['OrderNum'])
        cursor.execute(req6, req7)
        conn.commit()

        req8 = "SELECT Email FROM sys1.CUser WHERE id = %s"
        req9 = makerid
        cursor.execute(req8, req9)
        conn.commit()
        results5 = list(cursor)
        session['MC'] = results5[0][0]
        address = results2[0][1]
        city = results2[0][3]
        URL = "https://maps.googleapis.com/maps/api/geocode/json"
        key = 'AIzaSyBkR6KAsXVhAM1FhMMCi9IneisUHJ_EwVQ'
        PARAMS = {'address': address, 'components=locality': city, 'key': key, }
        r = requests.get(url=URL, params=PARAMS).json()
        CLongLat1 = r
        Value = CLongLat1['results'][0]['geometry']['location']
        CLongLat = str(Value)
        res1 = [float(s) for s in re.findall(r'-?\d+\.?\d*', CLongLat)]
        res2 = [float(s) for s in re.findall(r'-?\d+\.?\d*', str(results3[0]))]
        R = 6373.0

        lat1 = radians(res1[0])
        lon1 = radians(res1[1])
        lat2 = radians(res2[0])
        lon2 = radians(res2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        distance = round(distance, 1)

        session['CDistance'] = distance

        query1 = "UPDATE sys1.Orders SET Distance = %s WHERE OrderNum = %s"
        query2 = (distance, session['OrderNum'])
        cursor.execute(query1, query2)
        conn.commit()


        text = """\
                   Hi,
                   An order has been requested from a client:
                   Name:
                   Address:
                   Email:
                           
                           
                   Volume:
                   Materials:
                   Colours:
                   Infill:
                   Quality:
                   Quantity:
                   Distance:
                   """
        html = """\
                   <html>
                       <body>
                           <p>Hi,<br>
                           An order has been requested from a client:<br>
                           <br>
                           Name: {}<br>
                           Address: {}<br>
                           Email: {}<br>
                           <br>
                           <br>
                           Volume: {}<br>
                           Materials: {}<br>
                           Colours: {}<br>
                           Infill: {}<br>
                           Quality: {}<br>
                           Quantity: {}<br>
                           Distance: {} km<br>
                           
                           
                           <a href="http://127.0.0.1:5000/file/{}/{}">File Download Link</a><br>
                           
                           <a href="http://127.0.0.1:5000/accept/{}/{}">Accept</a><br>
                           Or<br>
                           <a href="http://127.0.0.1:5000/decline/{}/{}">Decline</a><br>
                           </p>
                       </body>
                   </html>
                 """.format(results2[0][0], results2[0][1], results2[0][2], results[0][0], results[0][1],
                            results[0][2], results[0][3], results[0][4], results[0][8], distance, session['tokenF'],
                            session['OrderNum'], session['tokenA'], session['OrderNum'], session['tokenD'],
                            session['OrderNum'])  # Sending email with info


        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())  # email send

        return render_template('OrderWaitForVer.html')

    return render_template("viewoptions.html", Names=Names, Email=Email, Address=Address, Distance=Distance,
                           MatCol=MatCol, Printers=Printers, Applicable=Applicable, pfp=PFP, Estimate=PriceT)


@app.route('/file/<token>/<OrderNum>')  # Download file for order
def file(token, OrderNum):

    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=86400  # If within the day
        )
    except:
        email = session['MC']
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])  # Else resend
        session['tokenA'] = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenA = session['tokenA']

        serializer2 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenD'] = serializer2.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenD = session['tokenD']

        serializer3 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenF'] = serializer3.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenF = session['tokenF']

        session['OrderNum'] = OrderNum

        sender_email = "makerchain.canada@gmail.com"
        receiver_email = email
        password = 'KaulBates2020'

        message = MIMEMultipart('alternative')
        message['Subject'] = "Order Requested - Resend"
        message['From'] = sender_email
        message['To'] = receiver_email

        text = """\
                           """
        html = """\
                           <html>
                               <body>
                                   <p>
                                   <a href="http://127.0.0.1:5000/file/{}/{}">File Download Link</a><br>

                                   <a href="http://127.0.0.1:5000/accept/{}/{}">Accept</a><br>
                                   Or<br>
                                   <a href="http://127.0.0.1:5000/decline/{}/{}">Decline</a><br>
                                   </p>
                               </body>
                           </html>
                         """.format(session['tokenF'], session['OrderNum'],
                                    session['tokenA'], session['OrderNum'], session['tokenD'], session['OrderNum'])

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return render_template("LinknotValid.html")
    return redirect(url_for('FileDownload'))  # File download


@app.route('/FileDownload.html')
def FileDownload():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNum']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]

    with open("static/UploadedFiles/File" + str(session['OrderNum']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNum']) + "O" + ".stl", as_attachment=True)  # Auto Download


@app.route('/FileDownloadP1.html')
def FileDownloadP1():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumP1']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]

    with open("static/UploadedFiles/File" + str(session['OrderNumP1']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumP1']) + "O" + ".stl", as_attachment=True)  # Auto Download

@app.route('/FileDownloadP2.html')
def FileDownloadP2():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumP2']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]

    with open("static/UploadedFiles/File" + str(session['OrderNumP2']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumP2']) + "O" + ".stl", as_attachment=True)  # Auto Download

@app.route('/FileDownloadP3.html')
def FileDownloadP3():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumP3']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]


    with open("static/UploadedFiles/File" + str(session['OrderNumP3']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumP3']) + "O" + ".stl", as_attachment=True)  # Auto Download


@app.route('/FileDownloadP4.html')
def FileDownloadP4():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumP4']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]


    with open("static/UploadedFiles/File" + str(session['OrderNumP4']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumP4']) + "O" + ".stl", as_attachment=True)  # Auto Download

@app.route('/FileDownloadP5.html')
def FileDownloadP5():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumP5']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]


    with open("static/UploadedFiles/File" + str(session['OrderNumP5']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumP5']) + "O" + ".stl", as_attachment=True)  # Auto Download

@app.route('/FileDownloadC1.html')
def FileDownloadC1():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumC1']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]

    with open("static/UploadedFiles/File" + str(session['OrderNumC1']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumC1']) + "O" + ".stl", as_attachment=True)  # Auto Download

@app.route('/FileDownloadC2.html')
def FileDownloadC2():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumC2']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]

    with open("static/UploadedFiles/File" + str(session['OrderNumC2']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumC2']) + "O" + ".stl", as_attachment=True)  # Auto Download

@app.route('/FileDownloadC3.html')
def FileDownloadC3():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumC3']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]


    with open("static/UploadedFiles/File" + str(session['OrderNumC3']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumC3']) + "O" + ".stl", as_attachment=True)  # Auto Download


@app.route('/FileDownloadC4.html')
def FileDownloadC4():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumC4']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]


    with open("static/UploadedFiles/File" + str(session['OrderNumC4']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumC4']) + "O" + ".stl", as_attachment=True)  # Auto Download

@app.route('/FileDownloadC5.html')
def FileDownloadC5():
    req5 = "SELECT File FROM sys1.Orders WHERE OrderNum = %s"
    req6 = session['OrderNumC5']
    cursor.execute(req5, req6)
    results = list(cursor)

    upload = results[0][0]


    with open("static/UploadedFiles/File" + str(session['OrderNumC5']) + "O" + ".stl", 'wb') as file:
        file.write(upload)
        file.close()  # get from db

    return send_file("static/UploadedFiles/File" + str(session['OrderNumC5']) + "O" + ".stl", as_attachment=True)  # Auto Download



def Delivery(OrderNumS):
    query1 = "SELECT Cid FROM sys1.Orders WHERE OrderNum = %s"
    query2 = OrderNumS
    cursor.execute(query1, query2)
    results = list(cursor)

    cid = results[0][0]

    query3 = "SELECT Email FROM sys1.CUser WHERE id = %s"
    query4 = cid
    cursor.execute(query3, query4)
    results2 = list(cursor)
    email = results2[0][0]

    sender_email = "makerchain.canada@gmail.com"
    receiver_email = email
    password = 'KaulBates2020'

    message = MIMEMultipart('alternative')
    message['Subject'] = "Order Completed"
    message['From'] = sender_email
    message['To'] = receiver_email

    text = """\
                                   """
    html = """\
                                   <html>
                                       <body>
                                           <p>
                                                The Maker that completed your order says it is done. 
                                                If it isn't delivered, or you have an issue please reply to this email.
                                                Thank you for using MakerChain 
                                           </p>
                                       </body>
                                   </html>
                                 """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    query1 = "SELECT PriceT FROM sys1.Orders WHERE OrderNum = %s"
    query2 = OrderNumS
    cursor.execute(query1, query2)
    results3 = list(cursor)
    Price = results3[0][0]

    sender_email = "makerchain.canada@gmail.com"
    receiver_email = "makerchain.canada@gmail.com"
    password = 'KaulBates2020'

    message = MIMEMultipart('alternative')
    message['Subject'] = "Order Completed"
    message['From'] = sender_email
    message['To'] = receiver_email

    text = """\
                                           """
    html = """\
                                           <html>
                                               <body>
                                                   <p>
                                                        OrderNum = {}
                                                        Price = {}
                                                        Release payment
                                                   </p>
                                               </body>
                                           </html>
                                         """.format(Price, query2)

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())


@app.route('/DeliveryC1.html')
def DeliveryC1():
    Delivery(session['OrderNumC1'])


@app.route('/DeliveryC2.html')
def DeliveryC2():
    Delivery(session['OrderNumC2'])


@app.route('/DeliveryC3.html')
def DeliveryC3():
    Delivery(session['OrderNumC3'])


@app.route('/DeliveryC4.html')
def DeliveryC4():
    Delivery(session['OrderNumC4'])


@app.route('/DeliveryC5.html')
def DeliveryC5():
    Delivery(session['OrderNumC5'])


@app.route('/DeliveryP1.html')
def DeliveryP1():
    Delivery(session['OrderNumP1'])


@app.route('/DeliveryP2.html')
def DeliveryP2():
    Delivery(session['OrderNumP2'])


@app.route('/DeliveryP3.html')
def DeliveryP3():
    Delivery(session['OrderNumP3'])


@app.route('/DeliveryP4.html')
def DeliveryP4():
    Delivery(session['OrderNumP4'])


@app.route('/DeliveryP5.html')
def DeliveryP5():
    Delivery(session['OrderNumP5'])


@app.route('/accept/<token>/<OrderNum>', methods=['GET', 'POST'])  # If accepted order
def OAccept(token, OrderNum):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=86400
        )
    except:
        email = session['MC']
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenA'] = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenA = session['tokenA']

        serializer2 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenD'] = serializer2.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenD = session['tokenD']

        serializer3 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenF'] = serializer3.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenF = session['tokenF']

        session['OrderNum'] = OrderNum

        sender_email = "makerchain.canada@gmail.com"
        receiver_email = email
        password = 'KaulBates2020'

        message = MIMEMultipart('alternative')
        message['Subject'] = "Order Requested - Resend"
        message['From'] = sender_email
        message['To'] = receiver_email

        text = """\
               """
        html = """\
                    <html>
                        <body>
                            <p>
                            <a href="http://127.0.0.1:5000/file/{}/{}">File Download Link</a><br>

                            <a href="http://127.0.0.1:5000/accept/{}/{}">Accept</a><br>
                            Or<br>
                            <a href="http://127.0.0.1:5000/decline/{}/{}">Decline</a><br>
                            </p>
                        </body>
                    </html>
                """.format(session['tokenF'], session['OrderNum'], session['tokenA'], session['OrderNum'],
                           session['tokenD'], session['OrderNum'])

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return render_template("LinknotValid.html")

    est = session['CPrice']  # Invalid trimesh
    if session['CPrice'] == 0.0:
        est = "Unknown. Please download the file, slice it, and create a cost that is appropriate for the whole order"\
              " (delivery cost included)."

    if request.method == "POST":
        price = request.form.get('Price')  # Get price made by maker

        price = float(price)

        percent = 0

        est = session['CPrice']
        if session['CPrice'] == 0.0:
            query = "UPDATE sys1.Orders SET PriceT = %s WHERE OrderNum = %s"
            query2 = (price, OrderNum)
            cursor.execute(query, query2)
            conn.commit()

            query = "UPDATE sys1.Orders SET PROGESS = %s WHERE OrderNum = %s"
            query2 = ("Awaiting Payment", OrderNum)
            cursor.execute(query, query2)
            conn.commit()

            query = "SELECT Cid, PriceT FROM sys1.Orders WHERE OrderNum = %s"
            cursor.execute(query, OrderNum)
            result = list(cursor)
            id = result[0][0]
            query2 = "SELECT Email FROM sys1.CUser WHERE id = %s"
            cursor.execute(query2, id)
            result2 = list(cursor)
            email = result2[0][0]
            total = result[0][1]

            percent = total / 5
            Price = total + percent # 20% Fee
            Price = Price * 1.13 # Tax
            Price = Price + 1.50 # Interac Fee for both

            sender_email = "makerchain.canada@gmail.com"
            receiver_email = "makerchain.canada@gmail.com"
            password = 'KaulBates2020'

            message = MIMEMultipart('alternative')
            message['Subject'] = "Payment Request"
            message['From'] = sender_email
            message['To'] = receiver_email  # SEND EMAIL TO MYSELF TO SEND OFF PAYMENT

            text = """\
                            
                   """
            html = """\
                                <html>
                                    <body>
                                        <p>
                                        email = {}
                                        total = {}
                                        ordernum = {}
                                        REMEMBER TO SET PROGRESS TO "Printing" AFTER PAYMENT COMES THROUGH
                                        </p>
                                    </body>
                                </html>
                            """.format(email, Price, OrderNum)

            part1 = MIMEText(text, "plain")
            part2 = MIMEText(html, "html")

            message.attach(part1)
            message.attach(part2)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, message.as_string())



            return redirect(url_for("Mhome"))


            
        else:
            percent = est / 5  # If wasn't trimesh invalid, check if in range
            if (est - percent) <= price <= (est + percent):
                query = "UPDATE sys1.Orders SET PriceT = %s WHERE OrderNum = %s"
                query2 = (price, OrderNum)
                cursor.execute(query, query2)
                conn.commit()

                query = "UPDATE sys1.Orders SET PROGRESS = %s WHERE OrderNum = %s"
                query2 = ("Awaiting Payment", OrderNum)
                cursor.execute(query, query2)
                conn.commit()

                query = "SELECT Cid, PriceT FROM sys1.Orders WHERE OrderNum = %s"
                cursor.execute(query, OrderNum)
                result = list(cursor)
                email = result[0][0]
                total = result[0][1]

                percent = total / 5
                Price = total + percent  # 20% Fee
                Price = Price * 1.13  # Tax
                Price = Price + 1.50  # Interac Fee for both

                sender_email = "makerchain.canada@gmail.com"
                receiver_email = "makerchain.canada@gmail.com"
                password = 'KaulBates2020'

                message = MIMEMultipart('alternative')
                message['Subject'] = "Payment Request"
                message['From'] = sender_email
                message['To'] = receiver_email

                text = """\

                                   """
                html = """\
                                <html>
                                    <body>
                                        <p>
                                        email = {}
                                        total = {}
                                        ordernum = {}
                                        REMEMBER TO SET PROGRESS TO "Printing" AFTER PAYMENT COMES THROUGH
                                        </p>
                                    </body>
                                </html>
                            """.format(email, Price, OrderNum)

                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")

                message.attach(part1)
                message.attach(part2)

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())

                return redirect(url_for("Mhome"))



            else:
                return render_template("OrderAccepted.html", Estimate=est, Distance=session['CDistance'],
                                       Address=session['CAddress'], Failed='1')

    return render_template("OrderAccepted.html", Estimate=est, Distance=session['CDistance'],
                           Address=session['CAddress'], Failed='0')


@app.route('/decline/<token>/<OrderNum>')  # Order gets declined
def ODecline(token, OrderNum):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=86400
        )
    except:
        email = session['MC']
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenA'] = serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenA = session['tokenA']

        serializer2 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenD'] = serializer2.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenD = session['tokenD']

        serializer3 = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        session['tokenF'] = serializer3.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])
        tokenF = session['tokenF']

        session['OrderNum'] = OrderNum

        sender_email = "makerchain.canada@gmail.com"
        receiver_email = email
        password = 'KaulBates2020'

        message = MIMEMultipart('alternative')
        message['Subject'] = "Order Requested - Resend"
        message['From'] = sender_email
        message['To'] = receiver_email

        text = """\
                       """
        html = """\
                            <html>
                                <body>
                                    <p>
                                    <a href="http://127.0.0.1:5000/file/{}/{}">File Download Link</a><br>

                                    <a href="http://127.0.0.1:5000/accept/{}/{}">Accept</a><br>
                                    Or<br>
                                    <a href="http://127.0.0.1:5000/decline/{}/{}">Decline</a><br>
                                    </p>
                                </body>
                            </html>
                        """.format(session['tokenF'], session['OrderNum'], session['tokenA'],
                                   session['OrderNum'], session['tokenD'], session['OrderNum'])

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return render_template("LinknotValid.html")

    quer1 = "SELECT Cid FROM sys1.Orders WHERE OrderNum = %s"  # Deletes order from db and sends customer email
    quer2 = session['OrderNum']
    cursor.execute(quer1, quer2)
    result = list(cursor)

    quer3 = "SELECT Email FROM sys1.CUser WHERE id = %s"
    quer4 = result[0][0]
    cursor.execute(quer3, quer4)
    result2 = list(cursor)

    sender_email = "makerchain.canada@gmail.com"
    receiver_email = result2[0][0]
    password = 'KaulBates2020'

    message = MIMEMultipart('alternative')
    message['Subject'] = "Order Declined By Maker"
    message['From'] = sender_email
    message['To'] = receiver_email

    text = """\
               Hi,
               Your Order has been declined. Please go back to the order page and reorder (Choose another maker).
           """
    html = """\
               <html>
                   <body>
                       <p>Hi,<br>
                       Your Order has been declined. Please go back to the order page and reorder\
                        (Choose another maker).
                       </p>
                   </body>
               </html>
             """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    message.attach(part1)
    message.attach(part2)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    quer5 = "DELETE FROM sys1.Orders WHERE OrderNum = %s"
    quer6 = session['OrderNum']
    cursor.execute(quer5, quer6)
    conn.commit()
    return render_template("OrderDeclined.html")


@app.route('/editprofile.html', methods=["GET", "POST"])
def editprofile():
    if request.method == "POST":
        file = request.files['file']
        if file != '':
            filename1, file_extention = os.path.splitext(file.filename)
            if file_extention not in ALLOWED_EXTENTIONS:
                print("file extension not allowed") # Change to html page or maybe javascript
            else:
                file_con1 = file.stream.read()
                query = "UPDATE sys1.CUser SET pfp = %s WHERE id = %s"  # Set pfp to new pfp
                t = (file_con1, session['id'])
                cursor.execute(query, t)
                conn.commit()
                temp = "SELECT pfp FROM sys1.CUser WHERE id = %s"
                temp3 = cursor.execute(temp, session['id'])
                result = cursor.fetchone()
                if 'PNG' in str(result[0]):
                    file_extention2 = '.png'
                    session['ext'] = file_extention2
                if 'JPG' in str(result[0]):
                    file_extention2 = '.jpg'
                    session['ext'] = file_extention2
                if 'JPEG' in str(result[0]):
                    file_extention2 = '.jpeg'
                    session['ext'] = file_extention2
                else:
                    file_extention2 = '.png'
                    session['ext'] = file_extention2
                with open('static/UploadedPictures/pfp' + session['id'] + file_extention2, 'wb') as file:
                    file.write(result[0])
                    session['pfp'] = 'static/UploadedPictures/pfp' + session['id'] + file_extention2
                    file.close()
        Address = session['address']
        City = session['city']
        Name = session['name']
        Email = session['email']
        NAddress = request.form.get("EAddress")
        NCity = request.form.get("ECity")
        NName = request.form.get("EName")
        NEmail = request.form.get("EEmail")  # Set all fields to new data if provided, if not stay the same
        if NCity != '':
            if NCity != City:
                temp = "UPDATE sys1.CUser SET City = %s WHERE id = %s"
                temp2 = (NCity, session['id'])
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                session['city'] = NCity
        if NAddress != '':
            if NAddress != Address:
                URL = "https://maps.googleapis.com/maps/api/geocode/json"
                key = 'AIzaSyBkR6KAsXVhAM1FhMMCi9IneisUHJ_EwVQ'
                city = 'Toronto'
                PARAMS = {'address': NAddress, 'components=locality': session['city'], 'key': key, }
                r = requests.get(url=URL, params=PARAMS).json()
                json_longlatv = r
                if json_longlatv == {'results': [], 'status': 'ZERO_RESULTS'}:
                    # make error message of not valid address
                    return render_template('editprofile.html', variable=session['name'], variable2=session['email'],
                           variable3=session['address'], variable4=session['city'], pfp=session['pfp'], Add=0)
                else:
                    temp = "UPDATE sys1.CUser SET Address = %s WHERE id = %s"
                    temp2 = (NAddress, session['id'])
                    temp3 = cursor.execute(temp, temp2)
                    conn.commit()
                    temp4 = "UPDATE sys1.MUser SET Address = %s WHERE id = %s"
                    temp2 = (NAddress, session['id'])
                    temp3 = cursor.execute(temp4, temp2)
                    conn.commit()
                    session['address'] = Address
        if NName != '':
            if NName != Name:
                temp = "UPDATE sys1.CUser SET Name = %s WHERE id = %s"
                temp2 = (NName, session['id'])
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                temp4 = "UPDATE sys1.MUser SET Name = %s WHERE id = %s"
                temp2 = (NName, session['id'])
                temp3 = cursor.execute(temp4, temp2)
                conn.commit()
                session['name'] = NName
        if NEmail != '':
            if NEmail != Email:
                temp = "UPDATE sys1.CUser SET Email = %s WHERE id = %s"
                temp2 = (NEmail, session['id'])
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                session['email'] = NEmail
        return render_template("profile.html", variable=session['name'], variable2=session['email'],
                               variable3=session['address'], variable4=session['city'], pfp=session['pfp'])
    return render_template('editprofile.html', variable=session['name'], variable2=session['email'],
                           variable3=session['address'], variable4=session['city'], pfp=session['pfp'])


@app.route('/editprofilemaker.html', methods=["GET", "POST"])
def editprofileM():
    if request.method == "POST":
        file = request.files['file']
        if file != '':
            filename1, file_extention = os.path.splitext(file.filename)
            if file_extention not in ALLOWED_EXTENTIONS:
                print("file extension not allowed")
            else:
                file_con1 = file.stream.read()
                query = "UPDATE sys1.CUser SET pfp = %s WHERE id = %s"  # Set pfp to new pfp
                t = (file_con1, session['id'])
                cursor.execute(query, t)
                conn.commit()
                temp = "SELECT pfp FROM sys1.CUser WHERE id = %s"
                temp3 = cursor.execute(temp, session['id'])
                result = cursor.fetchone()
                if 'PNG' in str(result[0]):
                    file_extention3 = '.png'
                    session['ext'] = file_extention3
                if 'JPG' in str(result[0]):
                    file_extention3 = '.jpg'
                    session['ext'] = file_extention3
                if 'JPEG' in str(result[0]):
                    file_extention3 = '.jpeg'
                    session['ext'] = file_extention3
                with open('static/UploadedPictures/pfp' + session['id'] + file_extention, 'wb') as file:
                    file.write(result[0])
                    session['pfp'] = 'static/UploadedPictures/pfp' + session['id'] + file_extention
                    file.close()
        Address = session['address']
        City = session['city']
        Name = session['name']
        Email = session['email']
        NAddress = request.form.get("EAddress")
        NCity = request.form.get("ECity")
        NName = request.form.get("EName")
        NEmail = request.form.get("EEmail")  # Set all fields to new data if provided, if not stay the same
        if NCity != '':
            if NCity != City:
                temp = "UPDATE sys1.CUser SET City = %s WHERE id = %s"
                temp2 = (NCity, session['id'])
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                session['city'] = NCity
        if NAddress != '':
            if NAddress != Address:
                URL = "https://maps.googleapis.com/maps/api/geocode/json"
                key = 'AIzaSyBkR6KAsXVhAM1FhMMCi9IneisUHJ_EwVQ'
                city = 'Toronto'
                PARAMS = {'address': NAddress, 'components=locality': session['city'], 'key': key, }
                r = requests.get(url=URL, params=PARAMS).json()
                json_longlatv = r
                if json_longlatv == {'results': [], 'status': 'ZERO_RESULTS'}:
                    # make error message of not valid address
                    return render_template("editprofilemaker.html", variable=session['name'], variable2=session['email'],
                           variable3=session['address'], variable4=session['city'], pfp=session['pfp'], Add=0)
                else:
                    temp = "UPDATE sys1.CUser SET Address = %s WHERE id = %s"
                    temp2 = (NAddress, session['id'])
                    temp3 = cursor.execute(temp, temp2)
                    conn.commit()
                    session['address'] = Address
        if NName != '':
            if NName != Name:
                temp = "UPDATE sys1.CUser SET Name = %s WHERE id = %s"
                temp2 = (NName, session['id'])
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                session['name'] = NName
        if NEmail != '':
            if NEmail != Email:
                temp = "UPDATE sys1.CUser SET Email = %s WHERE id = %s"
                temp2 = (NEmail, session['id'])
                temp3 = cursor.execute(temp, temp2)
                conn.commit()
                session['email'] = NEmail
        return render_template("profilemaker.html", variable=session['name'], variable2=session['email'],
                               variable3=session['address'], variable4=session['city'], pfp=session['pfp'])
    return render_template("editprofilemaker.html", variable=session['name'], variable2=session['email'],
                           variable3=session['address'], variable4=session['city'], pfp=session['pfp'])


if __name__ == '__main__':
    app.run()
    id = session['id']
    ext = session['ext']
    session.clear()
    cursor.close()