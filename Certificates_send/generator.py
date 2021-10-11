from PIL import Image, ImageDraw, ImageFont
from sendgrid.helpers.mail import *
import json
import pandas as pd
import sendgrid
import smtplib, ssl, base64

data = pd.read_excel (r'users.xlsx') 
id_list = data['id'].tolist() 
mail_list = data['email'].tolist()
f = open('scoreboard.json') 
data= json.load(f)
data=data['data']
for i in data:
    try:
        #write name
        im = Image.open(r'Certificate.png')
        d = ImageDraw.Draw(im)
        text_color = (150, 192, 14)
        font = ImageFont.truetype("NeusaNextPro-Light.ttf", 250)
        w, h = d.textsize(i['name'], font=font)
        location = ((2700-w)/2, 1000)
        d.text(location, i['name'], fill = text_color, font = font)
        #write score
        text_color = (255, 255, 255)
        font = ImageFont.truetype("NeusaNextPro-Regular.ttf", 100)
        w, h = d.textsize(str(i['score']), font=font)
        location = ((4250-w)/2, 1650)
        d.text(location, str(i['score']), fill = text_color, font = font)
        #write positions
        text_color = (255, 255, 255)
        font = ImageFont.truetype("NeusaNextPro-Regular.ttf", 100)
        w, h = d.textsize(str(i['pos'])+"#", font=font)
        location = ((1100-w)/2, 1650)
        d.text(location, str(i['pos'])+"#", fill = text_color, font = font)
        im.save("certificate_" + str(i['pos']) +".pdf")
        sg = sendgrid.SendGridAPIClient(api_key="###SENDGRID_API_KEY###")
        from_email = Email("contact@fword.tech")
        x = id_list.index(i['members'][0]['id'])
        to_email = To(mail_list[x])
        mail = Mail(from_email, to_email)
        mail.dynamic_template_data = {'team' : i['name']}
        mail.template_id = "###SENDGRID_TEMPLATE_ID###"
        #with open("certificate_" + i +".pdf", 'rb') as sigf:
        #    sig = sigf.read()
        sig = open("certificate_" + str(i['pos']) +".pdf", "rb").read()
        encoded = base64.b64encode(sig).decode()
        attachment = Attachment()
        attachment.file_content = FileContent(encoded)
        attachment.file_type = FileType('pdf')
        attachment.file_name = FileName("certificate_" + str(i['pos']) +".pdf")
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('Example Content ID')
        mail.attachment = attachment
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print("Succesfully sent to",end=" ")
        print(i['name'],end=" - ")
        print(mail_list[x])
        count_success+=1
        print("Succes Count: ",end='')
        print(str(count_success))
        j+=1
    except Exception:
        print("Error: ",end='')
        print(i,end=" - ")
        print(mail_list[x])
        continue


