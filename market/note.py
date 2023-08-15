''' 
- Template inheritance is a method to avoid copying and pasting alot of html code. inorder to this. create a new
html template called base.html.

- A database service running in the background should be used when storing a large amout of information due to a lot 
of users causing traffic on the website
but due to this being on the local for this we use SQLITE 3 (install flask sqlalchemy for database.) 

-URI stands for Unform Reources Identifier


-Make sure you have a Flask application instance created in your project. This instance is usually named app.
Before executing the db.create_all() command, set up an application context using app.app_context(). 
This step ensures that the necessary application context is established.

inorder to avoid circular imports , flask came up with a package feature
'''

'''
DataBase Relationship
study more on relationship on database .......

To create a user, assign an item to the user and create a relationship:
import db from market.models
drop all existing tables with (db.drop_all) and create a new table
import your built models form market.models
create a new user
add and commit your changes 
create a list of items to add to your added user

step by step write up on the database model structure.

 python
Python 3.11.1 (tags/v3.11.1:a7a450f, Dec  6 2022, 19:58:39) [MSC v.1934 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from market.models import db
>>> db.drop_all()
>>> db.create_all()
>>> from market.models import User,Item  
>>> u1= User(username='kelly', email_address='kelly1@gmail.com', password_harsh='123456') 
>>> db.session.add(u1) 
>>> db.session.commit()
>>> User.query.all() 
[<User 1>]
>>> i1 = Item (name='Iphone 10', price= '300,000', barcode='12345678', description='Silver Color')
>>> db.session.add(i1)
>>> db.session.commit()
>>> i2 = Item (name='Samsung s12', price= '250,000', barcode='1234535628', description='Browm Color') 
db.session.add(i2)
>>> db.session.commit()
>>> i3 = Item (name='Mac Pro', price= '700,000', barcode='23434535628', description='White Color')      
>>> db.session.add(i3)
>>> db.session.commit()
>>> Item.query.all()
[Item Iphone 10, Item Samsung s12, Item Mac Pro]
>>> Item.query.filter_by(name='Iphone 10').first()
Item Iphone 10
>>> item1 = Item.query.filter_by(name='Iphone 10').first()
>>> item1
Item Iphone 10
>>> item1.owner = User.query.filter_by(username='kelly').first().id
>>> db.session.add(item1)
>>> db.session.commit()
>>> item1.owner
1
>>> i = Item.query.filter_by(name='Iphone 10').first()
>>> i.owned_user
<User 1>


def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_harsh, attempted_password)

'''