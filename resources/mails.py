
from email.message import EmailMessage
from flask_restful import Resource, reqparse
from models.user import UserModel
# from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash

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
        content = "From: " + email + "\n\n" + message
        msg.set_content(content)
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

        msg = EmailMessage()
        msg["Subject"] = "Chordex - Password reset"
        msg["From"] = EMAIL_ADRESS
        msg["To"] = user.email
        token = user.generate_authenticity_token(user.id)
        reset_link = "https://chordex.net/resetpswd?token={0}&email={1}".format(
            token, user.email)
        # reset_link ="http://localhost:8080/resetpswd?token={}".format(token)
        msg_content = "Someone requested that the password be reset for the following account:\n\nhttps://chordex.net\n\nEmail: {0}\n\nIf this was a mistake, just ignore this email and nothing will happen.\n\nTo reset your password, visit the following address:\n\nLink is valid for 30 minutes.\n\n {1}".format(
            user.email, reset_link)

        msg.set_content(msg_content)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

            smtp.send_message(msg)

        return {"message": "We received your request. Please check your email."}


class DeleteAccountRequest(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def post(self):
        data = DeleteAccountRequest.parser.parse_args()
        email = data["email"]
        user = UserModel.find_by_email(email)
        if not user:
            return {"message": "User with that email doesnt exist."}, 400

        requested_user_id = get_jwt_identity()
        if not user.id == requested_user_id:
            return {"message": "You can only request account deletion for your own account."}, 403

        msg = EmailMessage()
        msg["Subject"] = "Chordex - Deleting account"
        msg["From"] = EMAIL_ADRESS
        msg["To"] = user.email
        token = user.generate_authenticity_token(user.id)
        delete_acc_link = "https://chordex.net/delete-acc?token={0}&email={1}".format(
            token, user.email)
        # delete_acc_link ="http://localhost:8080/delete-acc?token={0}&email={1}".format(token,user.email)
        msg_content = "Someone requested that the account be deleted for the following account:\n\nhttps://chordex.net\n\nEmail: {0}\n\nIf this was a mistake, just ignore this email and nothing will happen.\n\nTo delete your account, visit the following address:\n\nLink is valid for 30 minutes.\n\n {1}".format(
            user.email, delete_acc_link)

        msg.set_content(msg_content)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)

            smtp.send_message(msg)

        return {"message": "We received your request. Please check your email."}

# ako zelim svima poslati mail
# contacts=["test@test.com","test2@gmail.com"]
# msg["To"] = ", ".join(contacts)
