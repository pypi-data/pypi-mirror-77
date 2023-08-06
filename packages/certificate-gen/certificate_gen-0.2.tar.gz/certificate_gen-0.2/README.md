# CERTIFICATE-GENERATOR / MAILER 
This Package mainly focusses on creating bulk Certificates and mailing them to the corresponding respondents



# Installation
- ## pip install certificate-gen
- **This module also uses the library pillow, do not worry, it will be installed automatically**

***This Version supports only WINDOWS we are working on it to make it available for both linux and mac os***

## Please don't spam Mails this is mainly created for sending out useful information and making tedious tasks easier

# Pre Processes ( For sending Mails )
- ## Login to your account on google,
- ## [Please enable the less secure apps by clicking here] (https://myaccount.google.com/lesssecureapps)
- ## Make sure your CSV file has the name field for rendering certificates / email field for sending emails (if not make sure you add them to your csv)

# Usage
## Initial steps for sending Mails
```
from certificate_gen import Mailer

#initialize an object for the Mailer class
mail = Mailer()
mail.username = '' #Your Gmail id / the id from which the mails should be send
mail.password = '' #Your Gmail Password
mail.subject = '' #Subject of the Mail
mail.body = '' #body of the Mail
```
## Make sure you fill out all the above mentioned

## 0) To generate certificates alone, please follow the steps from 1-2 and you don't need to change any account settings as mentioned in the pre process


## 1) Reading the file (Make sure you only pass csv files)
- **This Function also accepts CSV and EXCEL Files, Feel Free to raise pull requests for issues :)**
- ###### Please pass the read_file method in an if block so we can catch any posisble errors while reading the file
```
if mail.read_file('filename.csv'):
    mail.renderCertificate('certificateTemplate.png')
```
**Possible errors in the read_file method**
 - **At times the encoding of the csv files might not match and you will be prompted for an error pass the encoding format in the read_file method**
 ```mail.read_file('filename.csv', encoding_f = 'latin-1')``` 
  - ## You can also try to pass any encoding formats available for csv_reader available online for PYTHON
  ## 1.1) You can also read only the mails and names by passing an optional argument to the read_file method
   - **This will only red the Emails in the CSV file**
     ```
     if mail.read_file('filename.csv', getNames=False ,encoding_f='latin-1'):
     ```
   - **This will only read the Names in the CSV file**
     ```
     if mail.read_file('filename.csv', getEmails=False ,encoding_f='latin-1'):
     ```
   - ## By default everything will be read

## 2) Rendering the Certificates
 - **Pre Processes ** 
   - **Make sure Your certificate template is present in the root directory of the program / or mention a complete path to it, and The Csv file also has the name field and you have read it from the csv file using read_file**
   - ## The Type of the certificate template should be a '.png' format for better results
 - ## Usage
   ```
   if mail.read_file('filename.csv'):
    mail.renderCertificate('certificateTemplate.png')
   ```
   **Now if you are Probably working with VS-code it would be more efficient**
   - open the folder name that will created on the root directory of the project only One image will be rendered for sample purpose
   - As the Terminal will promt you for the position of the text in the certificate Template
   - Make sure You experiment with your values and the the font-size,
   - Once satisfied press (1) when prompted to create the certificates for all the names in the CSV file
## 3) Now if you have a email section in your csv file and wish to send mails, make sure you comeplete the Initial Steps
- Right after that Call the send_certificate_mail() method in the mail object
- ```
  if mail.read_file('filename.csv'):
    mail.renderCertificate('certificateTemplate.png')
    mail.send_certificate_mail()
  ```
## 3.1) Possible Errors:
   - Please enter your mailId and password correctly,
   - And also follow the PreProcesses
   - **You will have a Mailing limit, and if the process quit with limit exceeded error, please wait for 24 hours and re run the program, ( and make sure you have deleted the previous entries, you will be prompted about the entries sent in the terminal you can refer there)**

## 4) Sending out single Mails:
   ```
  from certificate_gen import Mailer
  mail = Mailer()
  mail.username = '' # Username
  mail.password = '' # Password
  mail.subject = '' # subject
  mail.body = '''Body of the Mail'''

  mail.attachment_path = 'sample_pic.png' # You can add attachments if you want to

  mail.emails.append('') # For sending simple mails, just append the elements or simply target the object to a list of Email ids,
  mail.send_mail_with_attachment() #If you have added attachments Please use this,
  mail.send_mail() #Else this can be used to send single Mails
   ``` 
## 4.1) Sending multiple Mails:
   ```
  from certificate_gen import Mailer
  mail = Mailer()
  mail.username = '' # Username
  mail.password = '' # Password
  mail.subject = '' # subject
  mail.body = '''Body of the Mail'''
  if mail.read_file('csv file path'):
    mail.send_mail
   ```
