# User requests for password reset through the app
# User receives an email of the password reset link
# User clicks on the link and is directed to a page to enter a new password
from email.message import EmailMessage
from flask_restful import Resource, reqparse
from models.user import UserModel


import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")

print(EMAIL_ADRESS, EMAIL_PASSWORD)






class ContactMe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('message',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = ContactMe.parser.parse_args()
        email = data["email"]
        message = data["message"]
        msg = EmailMessage()
        msg["Subject"] = "Chordex - Contact me"
        msg["From"] = email
        msg["To"] = "nenadovic.kristian@gmail.com"
        msg.set_content(message)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            try:
                smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

                smtp.send_message(msg)
            except:
                return {"message": "An error occured sending an message."}, 500
        return {"message": "Message has been sent."}


class ForgotPassword(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = ForgotPassword.parser.parse_args()
        email = data["email"]
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User with that email doesnt exist."}, 400

        # generate a JWT in the form of a link sent to the user through email
        # JWT payload consists of the username to uniquely identify the user. JWT expiration is set to a limited time say 30mins.
        # JWT signature is signed with a secret: the user’s password hash
        # JWT could be appended in the query of the link: https://exampletest.com/reset/password?token={Insert JWT here} i ovo ce biti ruta na frontendu

        
        msg = EmailMessage()
        msg["Subject"] = "Chordex - Password reset"
        msg["From"] = EMAIL_ADRESS
        msg["To"] = "kristian383@gmail.com"  # ovo staviti email
        token=user.get_reset_pass_token(user.id) #ili passwrod
        reset_link ="https://chordex.com/resetpswd?token="+token
        print("reset_link",reset_link)
        # reset_link="blablabla"
        msg_content = "Someone requested that the password be reset for the following account:\n\n\nhttps://chordex.app\n\nEmail: {0}\n\nIf this was a mistake, just ignore this email and nothing will happen.\n\nTo reset your password, visit the following address:\n\n {1}".format(
            user.email, reset_link)

        msg.set_content(msg_content)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

            smtp.send_message(msg)

        return {"message": "email sent"}

# Someone requested that the password be reset for the following account:

# https://frontendmasters.com/

# Username: kristian3833@gmail.com

# If this was a mistake, just ignore this email and nothing will happen.

# To reset your password, visit the following address:








# with smtplib.SMTP("smtp.gmail.com",587) as smtp:
#     smtp.ehlo()
#     smtp.starttls()
#     smtp.ehlo()
#     smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)
# with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:

#     smtp.login(EMAIL_ADRESS,EMAIL_PASSWORD)

#     subject="Play guitar and enjoy it"
#     body="Do you want to learn how to play?"

#     msg=f'Subject: {subject}\n\n{body}'

#     smtp.sendmail(EMAIL_ADRESS,"kristian383@gmail.com",msg)


# ako zelim svima poslat mail
# contacts=["test@test.com","test2@gmail.com"]
# msg["To"] = ", ".join(contacts)
