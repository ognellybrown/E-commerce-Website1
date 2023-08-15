
from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email_address = db.Column(db.String(60), unique=True, nullable=False)
    password_harsh = db.Column(db.String(60), nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1600000)
    items = db.relationship('Item', backref='owned_user', lazy=True)  #A relationship argument allowing to model to understand that users can own items.
                                                                        #backref - a back refrences to the user model 
                                                                        #lazy = this allows the sqlalchemy to grab all the objects of items in one shot




    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    




#Note on bcrypt- from ORP
#The "getter" function helps you see the password when needed, 
# and the "setter" function transforms and saves the new password securely inside the database.
#By using these function, you can keep your passwords safe 

    @property
    def password(self):
        return self.password
    
    #setting password to end user instance
    #@password-setter- This is another special decorator that works with the @property. 
    #It defines a setter for the password property. When we try to set a value to password, this method will be called automatically.


    @password.setter       
    def password(self, plain_text_password):    #Taking extra parameter (password to be filled in "plain_text_password")
        self.password_harsh = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')



#bcrypt.generate_password_hash(plain_text_password).decode('utf-8'):
# In this line, we generate a secure hash (also known as a "password hash") from the plain text password
#  using a library called bcrypt. A password hash is a one-way transformation of the password,
#  making it difficult for anyone to reverse-engineer the original password. 
# The bcrypt.generate_password_hash() method takes the plain_text_password as input,
#  generates the hash, and then we convert it to a string using .decode('utf-8').

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_harsh, attempted_password)


#returning a boolean value which is either true or false to verify that the user could purchase the item .
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
        return item_obj in self.items




class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    barcode = db.Column(db.String(15), nullable=False, unique=True)
    description = db.Column(db.String(1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):                     #Donda repr helps return a formatted string in our database.
        return f'Item {self.name}'                      
    

    def buy(self , user):
        self.owner = user.id
        user.budget -= self.price #Decreasing the budget of the user.
        db.session.commit()

    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
    
  
