"""
Email service for sending verification and password reset emails
"""
import os
from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import EmailStr
from dotenv import load_dotenv

load_dotenv()

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", ""),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", ""),
    MAIL_FROM=os.getenv("MAIL_FROM", "noreply@slideguroo.com"),
    MAIL_PORT=int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER=os.getenv("MAIL_SERVER", "smtp.gmail.com"),
    MAIL_STARTTLS=os.getenv("MAIL_STARTTLS", "True").lower() == "true",
    MAIL_SSL_TLS=os.getenv("MAIL_SSL_TLS", "False").lower() == "true",
    USE_CREDENTIALS=os.getenv("USE_CREDENTIALS", "True").lower() == "true",
    VALIDATE_CERTS=os.getenv("VALIDATE_CERTS", "True").lower() == "true"
)

fastmail = FastMail(conf)


async def send_verification_email(email: EmailStr, username: str, token: str):
    """Send email verification email"""
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    verification_link = f"{frontend_url}/verify-email?token={token}"

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0ea5e9;">Welcome to SlideGuroo! 🎓</h2>

                <p>Hi {username},</p>

                <p>Thank you for signing up for SlideGuroo! To complete your registration and start learning, please verify your email address.</p>

                <div style="margin: 30px 0;">
                    <a href="{verification_link}"
                       style="background-color: #0ea5e9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Verify Email Address
                    </a>
                </div>

                <p>Or copy and paste this link into your browser:</p>
                <p style="color: #666; font-size: 14px; word-break: break-all;">{verification_link}</p>

                <p style="margin-top: 30px; color: #666; font-size: 14px;">
                    This link will expire in 24 hours. If you didn't create an account with SlideGuroo, please ignore this email.
                </p>

                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">

                <p style="color: #999; font-size: 12px;">
                    SlideGuroo - AI-Powered Student Learning Assistant<br>
                    Transform your slides into comprehensive lessons
                </p>
            </div>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Verify Your Email - SlideGuroo",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    await fastmail.send_message(message)


async def send_password_reset_email(email: EmailStr, username: str, token: str):
    """Send password reset email"""
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    reset_link = f"{frontend_url}/reset-password?token={token}"

    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0ea5e9;">Password Reset Request</h2>

                <p>Hi {username},</p>

                <p>We received a request to reset your password for your SlideGuroo account.</p>

                <div style="margin: 30px 0;">
                    <a href="{reset_link}"
                       style="background-color: #0ea5e9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Reset Password
                    </a>
                </div>

                <p>Or copy and paste this link into your browser:</p>
                <p style="color: #666; font-size: 14px; word-break: break-all;">{reset_link}</p>

                <p style="margin-top: 30px; color: #666; font-size: 14px;">
                    This link will expire in 1 hour. If you didn't request a password reset, please ignore this email or contact support if you have concerns.
                </p>

                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">

                <p style="color: #999; font-size: 12px;">
                    SlideGuroo - AI-Powered Student Learning Assistant<br>
                    Transform your slides into comprehensive lessons
                </p>
            </div>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Reset Your Password - SlideGuroo",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    await fastmail.send_message(message)


async def send_welcome_email(email: EmailStr, username: str):
    """Send welcome email after successful verification"""
    html = f"""
    <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #0ea5e9;">Welcome to SlideGuroo! 🎉</h2>

                <p>Hi {username},</p>

                <p>Your email has been successfully verified! You're all set to start using SlideGuroo.</p>

                <h3 style="color: #0369a1;">What you can do with SlideGuroo:</h3>

                <ul style="line-height: 2;">
                    <li>📤 Upload PowerPoint, PDF, or Word documents and get AI-generated comprehensive lessons</li>
                    <li>📚 Generate lessons on any topic instantly</li>
                    <li>📊 Get intelligent diagrams to visualize complex concepts</li>
                    <li>💬 Chat with AI tutor for instant help</li>
                    <li>🌍 Learn in English or Bangla</li>
                </ul>

                <div style="margin: 30px 0;">
                    <a href="{os.getenv('FRONTEND_URL', 'http://localhost:3000')}"
                       style="background-color: #0ea5e9; color: white; padding: 12px 30px; text-decoration: none; border-radius: 5px; display: inline-block;">
                        Start Learning
                    </a>
                </div>

                <p>Happy learning!</p>

                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">

                <p style="color: #999; font-size: 12px;">
                    SlideGuroo - AI-Powered Student Learning Assistant<br>
                    Transform your slides into comprehensive lessons
                </p>
            </div>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Welcome to SlideGuroo!",
        recipients=[email],
        body=html,
        subtype=MessageType.html
    )

    await fastmail.send_message(message)
