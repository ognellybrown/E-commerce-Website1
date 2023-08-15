
from market import app
from flask import render_template, redirect, url_for, flash, request 
from market.models import Item, User
from market.forms import RegisterForm, Loginform, PurchaseItemform, SellItemform
from market import db
from flask_login import login_user, logout_user, login_required, current_user

#login_required is a function that can be used as a decorator
# that wont take our user to the market page if the user is not logged in

@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route("/about/<username>")
def about_page(username):
    return f"This is the About page of {username}"

@app.route("/market", methods=["GET","POST"])
@login_required
def market_page():
    purchase_form = PurchaseItemform()
    selling_form = SellItemform()
    if request.method == "POST":     #to stop display the confirm form resubmission (more like validate request)
        #Purchase item Logic
        purchased_item = request.form.get('purchased_item') 
        p_item_object = Item.query.filter_by(name=purchased_item).first() #filtering the item object based on the value of purchased item
        if p_item_object:
             #assignin an ownership to the user that his logged in(making reffrences to models.py owner forign  key)
             #the .id is used to assign the owershi succesfully.
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations, you Purchased {p_item_object.name} for {p_item_object.price}$", category='success') 
            else:
                flash("Unfortunately, You don't have enough funds to purchased the {p_item_object.name}$ product.", category='danger')  

        #sell item logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations, you sold {s_item_object.name} back to the market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category ='success')

        return redirect (url_for('market_page'))
    
    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)  #Owner=none displays items purchased in owners section
        owned_items = Item.query.filter_by(owner=current_user.id)  #this query filters out the item that the current user owns
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items = owned_items, selling_form=selling_form)





@app.route("/register", methods=["GET","POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        #creating the register instance of our user
        user_to_create = User(username=form.username.data,            #Arguments required to create a user by passing field from the form
                              email_address=form.email_address.data,
                              password=form.password1.data)  
         #submitting the changes towards the database
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account Created sucessfully!, You can logged in as: {user_to_create.username}', category='success')
        #redirecting our user to another page using the url_for function
        return redirect(url_for('login_page'))
    if form.errors != {}:     #if there are no errors that arrise from validatons
        for err_msg in form.errors.values():
            flash(f'There was error with creating a user: {err_msg}', category='danger')  #displaying the errors inside our html template
    
        
    return render_template('register.html', form=form)

@app.route("/login", methods=["GET","POST"])
def login_page():
    form = Loginform()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data): #checking if the password matches the user from the password
            login_user(attempted_user)
            flash(f'Sucess!, You are logged in as: {attempted_user.username}', category='success')
            return redirect (url_for('market_page'))
        else:
            flash(f'Username does not match, please try again', category='danger') 
            #danger help us display a red color message, its going to translate in the base.html template
    return render_template('login.html', form=form)
    
#creating the logout route with flask built in function logout_user
# category info give colouring of blue when you log out    
@app.route("/logout")
def logout_page():
    logout_user()
    flash(f'You have been logged out!', category='info')
    return redirect (url_for ("home_page"))