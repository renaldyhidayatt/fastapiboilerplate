from fastapi_mail import ConnectionConfig, MessageSchema, FastMail


config = ConnectionConfig(
    MAIL_USERNAME="karolann.ritchie63@ethereal.email",
    MAIL_PASSWORD="9TfhcKk9EWCRCRcJVF",
    MAIL_FROM="lane.mcglynn@ethereal.email",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.ethereal.email",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

html = """
    
        Dear {}, \n\n You have successfully placed an order.\n\n\
                 Your order id is {}.
    
"""


class Mail(object):
    def __init__(self):
        pass

    async def send_notification(self, email: str, order_id: int, first_name: str):

        message = MessageSchema(
            subject="Order nr. {}".format(order_id),
            recipients=[email],
            body=html.format(first_name, order_id),
        )

        fm = FastMail(config)
        await fm.send_message(message)

    async def sendEmailVerify(self, verifyToken: str, email: str):
        verify_url = "http://localhost:8000/verify-email?token={}".format(verifyToken)
        message = """
            Please click the below link to verify your email address
            <a href="{}">{}</a>
        """.format(
            verify_url, verify_url
        )

        message = MessageSchema(
            subject="Sign-up Verification API",
            recipients=[email],
            body=message,
            subtype="html",
        )

        fm = FastMail(config)

        await fm.send_message(message)

    async def sendForgotPasswordEmail(self, resetPasswordToken: str, email: str):
        url_me = "http://localhost:8000/user/reset-password?token={}".format(
            resetPasswordToken
        )
        verify_message = """
            Please click the below link to reset your password
            <a href={}>Reset Password</a>
        """.format(
            url_me
        )

        message = MessageSchema(
            subject="Sign-up Reset Password API",
            recipients=[email],
            body=verify_message,
            subtype="html",
        )
        fm = FastMail(config)

        await fm.send_message(message)
