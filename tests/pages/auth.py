from playwright.sync_api import Page

class SignupPage:
    def __init__(self,page:Page):
        self.page=page
        self.email_field=page.get_by_placeholder("Email address")
        self.passowrd_field=page.get_by_placeholder("Password")
        self.signup_button=page.get_by_role("button",name="Create your account")



class LoginPage:
    def __init__(self,page:Page):
        self.page=page
        self.email_field=page.get_by_placeholder("Email address")
        self.passowrd_field=page.get_by_placeholder("Password")
        self.signup_button=page.get_by_role("button",name="sign in")


class ConfirmationPage:
    def __init__(self,page:Page):
        self.page=page
        self.confirm_button=page.get_by_role("button",name="Confirm")