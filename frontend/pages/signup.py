import flet as ft
from flet_model import Model
from email_validator import validate_email, EmailNotValidError
from zxcvbn import zxcvbn


class SignUpModel(Model):
    route = 'signup'

    # Layout configuration
    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER
    padding = 20
    spacing = 10

    valid_email = False
    valid_username = False
    valid_password = False
    valid_password_confirm = False

    # UI Components
    email_field = ft.TextField(
        label="Email",
        on_change="validate_email",
    )

    email_label = ft.Text(
        "",
        theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
        visible=False
    )

    username_field = ft.TextField(

        label="Username",
        on_change="validate_username"
    )

    username_label = ft.Text(
        "",
        theme_style=ft.TextThemeStyle.LABEL_MEDIUM,
        visible=False
    )

    password_field = ft.TextField(
        label="Password",
        password=True,
        on_change="validate_password",
        can_reveal_password=True,
    )

    strength_indicators = ft.Row()

    confirm_password_field = ft.TextField(
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        on_change="password_match"
    )

    submit_btn = ft.OutlinedButton(
        text="Sign Up",
        disabled=True,
        on_click="request_signup"
    )

    controls = [
        ft.Text("Sign Up Page", size=24),
        email_field,
        email_label,
        username_field,
        username_label,
        password_field,
        strength_indicators,
        confirm_password_field,

        ft.Row(
            controls=[
                submit_btn,
                ft.OutlinedButton(text="Login", on_click="go_to_login"),
            ]
        )
    ]

    def go_to_login(self, e):
        self.page.go('/login')

    def validate_email(self, e):
        """
        Check if the value in email field is correct email syntax
        if it's correct turn field borders to green if not make it red
        """
        try:
            # validate and get info
            validate_email(e.data)
            self.email_field.border_color = ft.Colors.GREEN
            self.email_label.visible = True
            self.email_label.value = "Email is valid"
            self.email_label.color = ft.Colors.GREEN
            self.valid_email = True


        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            # print(str(e))
            self.email_field.border_color = ft.Colors.RED
            self.email_label.visible = True
            self.email_label.value = str(e)
            self.email_label.color = ft.Colors.RED

        self.update()
        self.check_all_valid()

    def validate_username(self, e):
        """
        Check if username is available by sending request to server
        if the username is available show green label under the field
        if username is not available turn field's borders to red
        and show red label under the field saying you should try another username
        """
        # logic for checking availability of usernames goes here
        # print(e.data)
        if e.data != "":
            self.username_label.visible = True
            self.username_label.value = "Username available"
            self.username_label.color = ft.Colors.GREEN
            self.valid_username = True
            self.check_all_valid()
        else:
            self.username_label.visible = False
        self.update()

    def validate_password(self, e):
        """
        Check password strenght and update strengh indicators accordingly
        using zxcvbn library
        """
        password = e.data
        if not password == "":
            result = zxcvbn(password)
            score = result['score']

            strength_colors = [
                "grey",  # 0: Very Weak
                "red",  # 1: Weak
                "orange",  # 2: Fair
                "yellow",  # 3: Good
                "green"  # 4: Strong
            ]

            self.strength_indicators.controls = [
                ft.Container(
                    width=10,
                    height=10,
                    bgcolor=strength_colors[i] if i <= score else "lightgray",
                    border_radius=2,
                ) for i in range(5)
            ]

            # if score =< 3:
            self.valid_password = True
            self.check_all_valid()
            self.update()

    def password_match(self, e):
        """
        Check if both Password and Confirm password values match
        if they match make the borders green if not make borders red
        """
        if self.password_field.value != e.data:
            # password and confirm password didnt match
            self.password_field.border_color = ft.Colors.RED
            self.confirm_password_field.border_color = ft.Colors.RED
            self.update()
        else:
            # password and confirm password correct
            self.password_field.border_color = ft.Colors.GREEN
            self.confirm_password_field.border_color = ft.Colors.GREEN
            self.valid_password_confirm = True
            self.check_all_valid()
            self.update()

    def check_all_valid(self):
        """
        Check if all fields are valid to enable sign up button
        """
        fields_validation = [
            self.valid_email,
            self.valid_username,
            self.valid_password,
            self.valid_password_confirm
        ]

        all_valid = True

        for field in fields_validation:
            if field == False:
                all_valid = False
                break

        if all_valid:
            self.submit_btn.disabled = False
            self.update()

    def request_signup(self, e):
        """
        Send request to server with all validated data from fields
        """

        print("signing up ...")
        self.page.go("/home")
