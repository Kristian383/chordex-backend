
from email.message import EmailMessage
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import generate_password_hash


import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADRESS = os.environ.get("EMAIL_USER")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASS")


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
        msg["From"] = EMAIL_ADRESS
        msg["To"] = EMAIL_ADRESS
        content="From: "+email+"\n\n"+message
        msg.set_content(content)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            try:
                smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
                smtp.send_message(msg)
            except:
                return {"message": "An error occured sending an message."}, 500
        return {"message": "Message has been sent."}

class PasswordReset(Resource):
        parser = reqparse.RequestParser()
        parser.add_argument('new',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
        parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

        def post(self,token):
            data = PasswordReset.parser.parse_args()
            new = data["new"]
            email = data["email"]
            user=UserModel.verify_reset_pass_token(token,email)
            if user is None:
                return {"message":"That is an invalid or expired token."},400
            
            user.password=generate_password_hash(new, method="sha256")
            try:
                user.save_to_db()
            except:
                return {"message":"Something went wrong with saving new password."}

            return {"message":"Done"}

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

        msg = EmailMessage()
        msg["Subject"] = "Chordex - Password reset"
        msg["From"] = EMAIL_ADRESS
        msg["To"] = user.email  # ovo staviti user.email
        token=user.get_reset_pass_token(user.id) 
        reset_link ="http://localhost:8080/resetpswd?token={0}&email={1}".format(token,user.email)
        # reset_link ="http://localhost:8080/resetpswd?token={}".format(token)
        msg_content = "Someone requested that the password be reset for the following account:\n\nhttps://chordex.app\n\nEmail: {0}\n\nIf this was a mistake, just ignore this email and nothing will happen.\n\nTo reset your password, visit the following address:\n\nLink is valid for 30 minutes.\n\n {1}".format(
            user.email, reset_link)

        msg.set_content(msg_content)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

            smtp.send_message(msg)

        return {"message": "We received your request. Please check your email."}


# ako zelim svima poslat mail
# contacts=["test@test.com","test2@gmail.com"]
# msg["To"] = ", ".join(contacts)
