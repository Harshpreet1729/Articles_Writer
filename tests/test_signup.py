import re
from django.core import mail
from playwright.sync_api import Page
from allauth.account.models import EmailAddress
from tests.pages.auth import SignupPage, ConfirmationPage
from app.models import UserProfile

def test_signup(page:Page):
    page.goto("/")
    signup_page=SignupPage(page)
    signup_page.email_field.fill("q3zylr3dcm@xkxkud.com")
    signup_page.passowrd_field.fill("test_password123")
    signup_page.signup_button.click()

    confirmation_link=re.search(
        r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
        mail.outbox[0].body

    ).group()

    page.goto(confirmation_link)

    confirmation_page=ConfirmationPage(page)
    confirmation_page.confirm_button.click()


    user=UserProfile.objects.get(email="q3zylr3dcm@xkxkud.com")
    email_address=EmailAddress.objects.get(user=user, email="q3zylr3dcm@xkxkud.com")
    assert email_address.verified


