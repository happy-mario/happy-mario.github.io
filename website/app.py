import requests
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pickle
from flask import Flask, request, render_template, jsonify
from apscheduler.schedulers.background import BackgroundScheduler


filename = 'website/spickle.pk'

person = ["vgoncalves@usn.org", "nobody", "irisbrue26@usn.org", "nobody", "brycecochran26@usn.org", "nobody", "maxavierdickson26@usn.org", "nobody", "omeedirani26@usn.org", "nobody", "glabour@usn.org", "nobody", "jacobnichols26@usn.org", "nobody", "evelynstevenson26@usn.org", "nobody", "mariotedeschi26@usn.org", "nobody"]
names = ["Mr. Gonçalves", "nobody", "Iris", "nobody", "Bryce", "nobody", "Max", "nobody", "Omeed", "nobody", "Mr. Labour", "nobody", "Big looser", "nobody", "Maeve", "nobody", "Mario", "nobody"]
photo = ["static/css/images/Goat_advisory.png", "static/css/images/nobody_advisory.png", "static/css/images/Iris_advisory.png", "static/css/images/nobody_advisory.png", "static/css/images/Bryce_advisory.png", "static/css/images/nobody_advisory.png", "static/css/images/Max_advisory.png", "static/css/images/nobody_advisory.png", "static/css/images/Omeed_advisory.png", "static/css/images/nobody_advisory.png", "static/css/images/Mr.Labour_advisory.png", "static/css/images/nobody_advisory.png", "static/css/images/Biglooser_advisory.png", "static/css/images/nobody_advisory.png", "static/css/images/Maeve_advisory.png", "static/css/images/nobody_advisory.png", "static/css/images/Mario_advisory.png", "static/css/images/nobody_advisory.png"]

def restart():
    current_num = 0

try:
    with open(filename, 'rb') as fi:
        current_num = pickle.load(fi)
except:
    current_num = 0

current_person = person[current_num]
current_name = names[current_num]
current_photo = photo[current_num]

print(f"number:{current_num}, person:{current_person}")

def update(current_num, filename):
    print("Updated")
    current_num = current_num + 1 

    if current_num > 17:
        current_num = 0 

    #SAVE NEW NUMBER AFTER INCREMENTING IT
    with open(filename, 'wb') as fi:
        # dump your data into the file
        pickle.dump(current_num, fi)
    

e = "has snack today"

f = current_name + " " + e


scheduler = BackgroundScheduler()

def job():
    print("hello world")

scheduler.add_job(update, 'interval', [current_num, filename], minutes=1)


app = Flask(__name__)

#@app.__init__
#def start_scheduler()
scheduler.start()

@app.route('/')

def home():
    return render_template('home.html', value = f, svalue = current_photo, number = current_num)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port = 8081, use_reloader=False)