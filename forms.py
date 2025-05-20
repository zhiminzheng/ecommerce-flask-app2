from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,DateField,PasswordField,IntegerField,RadioField
from wtforms.validators import InputRequired,EqualTo




class RegistrationForm(FlaskForm):
    user_id=StringField("Username:", validators=[InputRequired()])
    password=PasswordField("Password:",validators=[InputRequired()])
    password2=PasswordField("Please entre your password again:",
                            validators=[InputRequired(),EqualTo("password")])
    submit=SubmitField("Create",render_kw={'class':'btn'})


class AdminRegistrationForm(FlaskForm):
    admin_id=StringField("Admin name:", validators=[InputRequired()])
    password=PasswordField("Password:",validators=[InputRequired()])
    password2=PasswordField("Please entre your password again:",
                            validators=[InputRequired(),EqualTo("password")])
    submit=SubmitField("Create",render_kw={'class':'btn'})
class LoginForm(FlaskForm):
    user_id=StringField("Username:", validators=[InputRequired()])
    password=PasswordField("Password:",validators=[InputRequired()])
    submit=SubmitField("Log in",render_kw={'class':'btn'})

class AdminLoginForm(FlaskForm):
    admin_id=StringField("Admin name:", validators=[InputRequired()])
    password=PasswordField("Password:",validators=[InputRequired()])
    submit=SubmitField("log in",render_kw={'class':'btn'})

class ClassCommoditiesForm(FlaskForm):
    gender=RadioField("Gender",
                      choices=["all","female","male"],
                      default="all")
    price=RadioField("Price",
                      choices=["all","0~100","100~500","over 500"],
                      default="all")
    type=RadioField("Type",
                      choices=["all","ring","necklace","earrings","bracelet"],
                      default="all")
    submit=SubmitField("classify",render_kw={'class':'btn'})

class AddProductForm(FlaskForm):
    name=StringField("Product Name:",
                     validators=[InputRequired()])
    price=IntegerField("Price:",
                      validators=[InputRequired()])
    type=RadioField("Type:",validators=[InputRequired()],
                      choices=["ring","necklace","earrings","bracelet"],
                      default="ring")
    gender=RadioField("Gender",validators=[InputRequired()],
                      choices=["female","male"],
                      default="female")
    description=StringField("Description:")
    stock=IntegerField("Stock:",
                      validators=[InputRequired()])
    submit=SubmitField("Add New Product",render_kw={'class':'btn'})

class BuyForm(FlaskForm):
    address=StringField("Your Address:",
                        validators=[InputRequired()])
    phone_number=StringField("Contact phone number:",
                              validators=[InputRequired()])
    submit=SubmitField("Buy",render_kw={'class':'btn'})
        

