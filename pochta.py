import imaplib
import email
def get_attachments():
    mail_pass = "2e09A6xsYfSpBgqBgwuD"
    username = "testraspisania@mail.ru"
    imap_server = "imap.mail.ru"
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, mail_pass)
    #подключение к почте
    imap.select("INBOX")
    msg, res = imap.search(None, 'ALL')
    if msg == 'OK':
        mail_id = str(res[0])
        mail_id = mail_id[mail_id.rfind(" ") + 1:-1]
        mail_id = mail_id.encode()
        res, msg = imap.fetch(mail_id, "(BODY.PEEK[])")
        email_body = msg[0][1]
        email_body = email_body.decode('utf-8')
        mail = email.message_from_string(email_body)
        for part in mail.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            return part.get_payload(decode=True)