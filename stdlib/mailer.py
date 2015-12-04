@cookery.action('JSON')
def send_email(subjects, args):
    print('subjects:', subjects, ', args:', args)
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    msg = MIMEMultipart()
    msg['Subject'] = args['subject']
    msg['From'] = args['from']
    msg['To'] = args['to']
    msg.attach(MIMEText(args['body']))
    for i in range(len(subjects)):
        atta = MIMEText(subjects[i])
        atta.add_header('Content-Disposition',
                        'attachment',
                        filename='result-{}.txt'.format(i))
        msg.attach(atta)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login('', '')
    mailServer.send_message(msg)
    mailServer.quit()

@cookery.subject('in', r'(.+)')
def file(path):
    print('opening file:', repr(path))
    f = open(path, 'r')
    return f.read()
