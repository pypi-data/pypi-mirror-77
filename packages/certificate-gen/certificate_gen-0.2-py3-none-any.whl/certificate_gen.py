import smtplib
import ssl
import email
import os
import csv
import sys
import xlrd

from PIL import Image, ImageDraw, ImageFont


from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Certificates:
    def __init__(self):
        self.totals = []
        self.emails = []
        self.names = []

        self.email_loaction = 0
        self.name_location = 0

        self.path = ''

        self.text_x = 0
        self.text_y = 0
        self.size = 30

        self.sample = False
        self.satisfied = 0

        self.counts = 0
        self.counts_1 = 0
        self.font_path = 'C:/Windows/Fonts/Arial/ariblk.ttf'
        
        self.server = ''
        self.port = 587

        self.attachment = ''
        self.part = ''
        self.text = ''
        self.msg = ''

        self.attachment_path = ''

    def _draw(self, certificate_file, name):
        try:
            completePath = os.path.join(self.path, name)
            img = Image.open(certificate_file, mode='r')
            image_width = img.width
            image_height = img.height
            draw = ImageDraw.Draw(img)

            font = ImageFont.truetype(self.font_path, size=self.size)
            text_width, _ = draw.textsize(name, font=font)
            draw.text(
                (
                    (image_width - (text_width - self.text_x)) / 2,
                    self.text_y
                ),
                name,
                fill='rgb(0, 0, 0)',
                font=font)
            self.counts += 1
            img.save("{}.png".format(completePath))
            print(f'{name} --------> {self.counts}')

        except FileNotFoundError:
            print('\nPlease check your filename!!!')
            sys.exit(0)

    def _createPath(self):
        try:
            if self.path == '':
                self.path = os.path.join(os.getcwd(), 'certificates')
                os.mkdir(self.path)
        except FileExistsError:
            return

    def _send_certificate_mails(self, username, password, subject, body):
        if self.emails == []:
            print('\nNo mail Ids are provided to send the mails')
            return
        else:
          
            totals = len(self.emails)
            try:
                self.server = smtplib.SMTP('smtp.gmail.com', self.port)
                self.server.starttls()
                self.server.login(username, password)
                addImages = (int(input(
                    '\nDo you want to attach Certificates to the mails (1 for yes | 0 for no) : ')))

                for i in range(len(self.emails)):
                    self.msg = MIMEMultipart()
                    self.msg['From'] = username
                    self.msg['To'] = self.emails[i]
                    self.msg['Subject'] = subject

                    self.msg.attach(MIMEText(body, 'plain'))

                    if(addImages == 1):
                        filename = os.path.join(
                            self.path, self.names[i]+'.png')
                        self.attachment = open(filename, 'rb')
                        self.part = MIMEBase('application', 'octet-stream')
                        self.part.set_payload((self.attachment).read())
                        encoders.encode_base64(self.part)
                        self.part.add_header('Content-Disposition',
                                        "self.attachment; filename= "+filename)

                        self.msg.attach(self.part)

                    self.text = self.msg.as_string()
                    self.server.sendmail(username, self.emails[i], self.text)

                    self.counts_1 += 1
                    print(
                        f'{self.counts_1} / {totals} --------- {self.emails[i]}')
                        
                self.server.quit()
            
            except smtplib.SMTPAuthenticationError:
                print('Please Check your username and Password, \n\n And make sure you have turned on the allow less secure apps for your account')

    def _send_attachment_mail(self, username, password, subject, body):
        if self.emails == []:
            print('\nNo mail Ids are provided to send the mails')
            return
        else:
            totals = len(self.emails)
            try:
                self.server = smtplib.SMTP('smtp.gmail.com', self.port)
                self.server.starttls()
                self.server.login(username, password)
                for i in range(len(self.emails)):
                    self.msg = MIMEMultipart()
                    self.msg['From'] = username
                    self.msg['To'] = self.emails[i]
                    self.msg['Subject'] = subject

                    self.msg.attach(MIMEText(body, 'plain'))

                    filename = self.attachment_path
                    self.attachment = open(filename, 'rb')
                    self.part = MIMEBase('application', 'octet-stream')
                    self.part.set_payload((self.attachment).read())
                    encoders.encode_base64(self.part)
                    self.part.add_header('Content-Disposition',
                                    "self.attachment; filename= "+filename)

                    self.msg.attach(self.part)

                    self.text = self.msg.as_string()
                    self.server.sendmail(username, self.emails[i], self.text)

                    self.counts_1 += 1
                    print(
                        f'{self.counts_1} / {totals} --------- {self.emails[i]}')
                        
                self.server.quit()
            
            except smtplib.SMTPAuthenticationError:
                print('Please Check your username and Password, \n\n And make sure you have turned on the allow less secure apps for your account')

    def renderCertificate(self, certificate_file):
        if len(self.names) > 0 and ('.png' in certificate_file or '.jpeg' in certificate_file):
            self._createPath()
            while(not self.sample):
                print('\n**************************')
                try:
                    self.text_x = int(input(
                        "\nEnter the x position (default = 0 | to continue with default press Enter) : "))
                except ValueError:
                    self.text_x = 0

                try:
                    self.text_y = int(
                        input('\nPlease enter a Text y position : (300-500) - please experiment it : '))
                except ValueError:
                    self.text_y = 300

                try:
                    self.size = int(input(
                        '\nPlease provide a text size (default value is 30), press enter to Continue : '))
                except:
                    self.size = 30

                self._draw(certificate_file, self.names[0])

                print(
                    '\nPlease preview your certificate sample in the images folder in the root directory of the program')
                print('\n**************************')
                try:
                    self.satisfied = int(input(
                        '\n Press (1 to proceed to all files) else (0 to re render the certificate) [ 1 - proceed || 0 - re-render ] : '))
                    if(self.satisfied):
                        self.sample = True
                except ValueError:
                    self.satisfied = 0

            for name in self.names:
                self._draw(certificate_file, name)
        return

    def read_file(self, filename, getEmails=True, getNames=True, encoding_f='utf-8'):
        try:
            workbook = xlrd.open_workbook(filename)
            sheet = workbook.sheet_by_index(0)

            for i in range(sheet.nrows):
                sam_lst = [str(sheet.cell_value(i,j)) for j in range(sheet.ncols)]
                self.totals.append(sam_lst)
            
            for i in self.totals[0]:
                x = ''.join(i.split())
                x = x.lower()
                if x == 'emailaddress' or x == 'email' or x == 'emailid':
                    self.email_loaction = self.totals[0].index(i)
                elif x == 'name' or x == 'fullname' or x == 'full-name':
                    self.name_location = self.totals[0].index(i)

            self.totals.pop(0)
            if getNames and getEmails:
                for i in self.totals:
                    if i[self.name_location] != '':
                        self.names.append(i[self.name_location])
                        self.emails.append(i[self.email_loaction])
            elif getEmails:
                for i in self.totals:
                    self.emails.append(i[self.email_loaction])
            else:
                for i in self.totals:
                    self.names.append(i[self.name_location])
            print('\n******************')
            print('\nFile Read Successful')
            return True

        except xlrd.biffh.XLRDError:
            try:
                with open(filename, encoding=encoding_f) as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')

                    for i in csv_reader:
                        self.totals.append(i)

                    for i in self.totals[0]:
                        x = ''.join(i.split())
                        x = x.lower()
                        if x == 'emailaddress' or x == 'email' or x == 'emailid':
                            self.email_loaction = self.totals[0].index(i)
                        elif x == 'name' or x == 'fullname' or x == 'full-name':
                            self.name_location = self.totals[0].index(i)

                    self.totals.pop(0)
                    if getNames and getEmails:
                        for i in self.totals:
                            if i[self.name_location] != '':
                                self.names.append(i[self.name_location])
                                self.emails.append(i[self.email_loaction])
                    elif getEmails:
                        for i in self.totals:
                            self.emails.append(i[self.email_loaction])
                    else:
                        for i in self.totals:
                            self.names.append(i[self.name_location])
                    csv_file.close()
                    print('\n******************')
                    print('\nFile Read Successful')
                    return True
            except UnicodeDecodeError:
                print(
                    '\nPlease try passing this parameter to the read_file\n\n self.read_file(filename, encoding_f=\'latin-1\')\n\n If that doesnt work , please choose encoders from the csv docs of pypi and pass them in...')
                return False
            except:
                print(
                    '\nPlease check your filename, make sure it is in the root folder of the program !!')
                return False
        except:
            print(
                '\nPlease check your filename, make sure it is in the root folder of the program !!')
            return False

    def _send_mail(self, username, password, subject, body):
        if self.emails == []:
            print('\nNo mail Ids are provided to send the mails')
            return
        else:
            totals = len(self.emails)
            try:
                self.server = smtplib.SMTP('smtp.gmail.com', self.port)
                self.server.starttls()
                self.server.login(username, password)
                for i in range(len(self.emails)):
                    self.msg = MIMEMultipart()
                    self.msg['From'] = username
                    self.msg['To'] = self.emails[i]
                    self.msg['Subject'] = subject

                    self.msg.attach(MIMEText(body, 'plain'))

                    # filename = self.attachment_path
                    # self.attachment = open(filename, 'rb')
                    # self.part = MIMEBase('application', 'octet-stream')
                    # self.part.set_payload((self.attachment).read())
                    # encoders.encode_base64(self.part)
                    # self.part.add_header('Content-Disposition',
                    #                 "self.attachment; filename= "+filename)s

                    # self.msg.attach(self.part)

                    self.text = self.msg.as_string()
                    self.server.sendmail(username, self.emails[i], self.text)

                    self.counts_1 += 1
                    print(
                        f'{self.counts_1} / {totals} --------- {self.emails[i]}')
                        
                self.server.quit()
            
            except smtplib.SMTPAuthenticationError:
                print('Please Check your username and Password, \n\n And make sure you have turned on the allow less secure apps for your account')


class Mailer(Certificates):
    def __init__(self):
        self.username = ''
        self.password = ''
        self.subject = ''
        self.body = ''
        Certificates.__init__(self)

    def send_certificate_mail(self):
        if(self.username and self.password and self.subject and self.body):
            self._send_certificate_mails(self.username, self.password, self.subject, self.body)
            print('\nCompleted Sending all Mails !!')
            return
        print('\nSome Error has occured')
        return
    
    def send_mail_with_attachment(self):
        if self.attachment_path == '':
            print('Please provide an attachment for this method')
            self.attachment_path = str(input('Attachment Path : '))
        self._send_attachment_mail(self.username, self.password, self.subject, self.body)
        print('\nCompleted Sending All Mails !!')

    def send_mail(self):
        if(self.username and self.password and self.subject):
            self._send_mail(self.username, self.password, self.subject, self.body)

            print('\nCompleted sending Mails')


