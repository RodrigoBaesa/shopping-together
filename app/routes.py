import bcrypt
from flask import Blueprint, render_template, request, flash, redirect, session, url_for
from app import db
from app.models import Family, Item, List, User, Invite
import app.validators as valid
from app.decorators import login_required

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def index():
    user = User.query.get(session["user_id"])
    if user.family:
        lists = List.query.filter_by(family_id=user.family).all()
    else:
        lists = []
    return render_template("index.html", lists=lists)


@main.route('/create-family', methods=["GET", "POST"])
@login_required
def create_family():
    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if user.family:
        flash("You are already part of a family.", "danger")
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")

        if not name or len(name) > 40:
            flash("Family name must be between 1 and 40 characters.", "danger")
            return redirect("/create-family")

        new_family = Family(
            name=name,
        )

        try:
            db.session.add(new_family)
            db.session.commit()
            user.family = new_family.id
            db.session.commit()
            flash("Family created.", "success")
            return redirect("/")
        
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("Something went wrong. Try again.", "danger")
            return redirect("/create-family")
        
    else:
        return render_template("create-family.html")


@main.route('/invite-family', methods=["GET", "POST"])
@login_required
def invite_family():
    user_id = session.get("user_id")
    user = User.query.get(user_id)

    if not user.family:
        flash("You must be in a family to invite members.", "danger")
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")

        if not name or len(name) > 40:
            flash("Input must be between 1 and 40 characters.", "danger")
            return redirect("/invite-family")

        invitee_username = name
        invitee = User.query.filter_by(username=invitee_username).first()
        if not invitee:
            flash("User not found.", "danger")
            return redirect("/invite-family")
        
        if invitee.family:
            flash("User is already in a family.", "danger")
            return redirect("/invite-family")

        existing_invite = Invite.query.filter_by(invitee_username=invitee_username, family_id=user.family, status='pending').first()
        if existing_invite:
            flash("Invite already sent.", "danger")
            return redirect("/invite-family")
        
        new_invite = Invite(
            inviter_id=user.id,
            invitee_username=invitee_username,
            family_id=user.family
        )

        try:
            db.session.add(new_invite)
            db.session.commit()
            flash("Invite sent.", "success")
            return redirect("/")
        
        except Exception as e:
            db.session.rollback()
            print(e)
            flash("Something went wrong. Try again.", "danger")
            return redirect("/invite-family")
    else:
        return render_template("invite-family.html")


@main.route('/create-list', methods=["GET", "POST"])
@login_required
def create_list():
    user = User.query.get(session["user_id"])
    if not user.family:
        flash("You must be in a family to create lists.", "danger")
        return redirect("/")

    if request.method == "POST":
        title = request.form.get("title")

        new_list = List(
            title=title,
            family_id=user.family
        )
        try:
            db.session.add(new_list)
            db.session.commit()
            flash("List created.", "success")

            return redirect("/")

        except Exception:
            db.session.rollback()
            flash("Something went wrong. Try again.", "danger")

            return redirect("/create-list")
    else:
        return render_template("create-list.html")
    
    
@main.route('/list/<int:list_id>', methods = ["GET", "POST"])
@login_required
def show_list(list_id):
    list = List.query.get(list_id)

    if not list:
        flash("List not found")
        return redirect("/")

    user = User.query.get(session["user_id"])
    if user.family != list.family_id:
        flash("Access denied")
        return redirect("/")

    title = list.title

    if request.method == "POST":
        product = request.form.get("product")
        quantity = request.form.get("quantity")
        brand = request.form.get("brand")
        
        new_item = Item(
            product=product,
            quantity=quantity,
            brand=brand,
            list_id=list.id
        )

        try:
            db.session.add(new_item)
            db.session.commit()

            return redirect(f'/list/{list_id}')
            
        except Exception:
            db.session.rollback()
            flash("Something went wrong while adding new item. Try again.", "danger")


    items = Item.query.filter_by(list_id=list.id).all()

    return render_template("list-details.html", title=title, items=items)


@main.route('/list/<int:list_id>/delete', methods=["POST"])
@login_required
def delete_list(list_id):
    list = List.query.get(list_id)
    if not list:
        flash("List not found.", "danger")
        return redirect("/")

    user = User.query.get(session["user_id"])
    if user.family != list.family_id:
        flash("Access denied.", "danger")
        return redirect("/")

    try:
        # Delete items first
        Item.query.filter_by(list_id=list_id).delete()
        db.session.delete(list)
        db.session.commit()
        flash("List deleted.", "success")
    except Exception:
        db.session.rollback()
        flash("Something went wrong.", "danger")

    return redirect("/")


@main.route('/login', methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect("/")

    error = None

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password").encode("utf-8")

        error = valid.validate_login(email, password, User)

        if error:
            flash(error, "danger")
            return redirect("/login")
        
        else:
            user = User.query.filter_by(email=email).one()
            session["user_id"] = user.id

            flash("Logged in!", "success")
            return redirect ("/")
            
    return render_template("login.html")


@main.route('/item/<int:item_id>/toggle', methods=["POST"])
@login_required
def toggle_item(item_id):
    item = Item.query.get(item_id)
    
    if not item:
        flash("Item not found.", "danger")
        return redirect("/")

    user = User.query.get(session["user_id"])
    list_obj = List.query.get(item.list_id)
    if not list_obj or user.family != list_obj.family_id:
        flash("Access denied.", "danger")
        return redirect("/")
    
    try:
        item.bought = not item.bought
        db.session.commit()
        flash(f"Item marked as {'bought' if item.bought else 'not bought'}!", "success")
        
    except Exception:
        db.session.rollback()
        flash("Something went wrong while updating item. Try again.", "danger")
        return redirect(f"/list/{item.list_id}")


@main.route('/family/<int:family_id>')
@login_required
def show_family(family_id):
    family = Family.query.get(family_id)
    if not family:
        flash("Family not found.", "danger")
        return redirect("/")
    
    user = User.query.get(session["user_id"])
    if user.family != family_id:
        flash("Access denied.", "danger")
        return redirect("/")
    
    members = User.query.filter_by(family=family_id).all()
    return render_template("family-details.html", family=family, members=members)


@main.route('/invites')
@login_required
def view_invites():
    user = User.query.get(session["user_id"])
    if user.family:
        invites = Invite.query.filter_by(inviter_id=user.id).all()
        return render_template("invites.html", invites=invites, sent=True)
    else:
        invites = Invite.query.filter_by(invitee_username=user.username, status='pending').all()
        return render_template("invites.html", invites=invites, sent=False)


@main.route('/invite/<int:invite_id>/accept', methods=['POST'])
@login_required
def accept_invite(invite_id):
    invite = Invite.query.get(invite_id)
    user = User.query.get(session["user_id"])
    if not invite or invite.invitee_username != user.username or invite.status != 'pending':
        flash("Invalid invite.", "danger")
        return redirect("/invites")
    if user.family:
        flash("You are already in a family.", "danger")
        return redirect("/invites")
    try:
        user.family = invite.family_id
        invite.status = 'accepted'
        db.session.commit()
        flash("Joined family!", "success")
    except Exception:
        db.session.rollback()
        flash("Error joining family.", "danger")
    return redirect("/")


@main.route('/logout')
def logout():
    session.clear()
    flash("Logged out!", "success")

    return redirect(url_for('main.login'))


@main.route('/register', methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect("/")
    
    if request.method == "POST":
        error = None

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        error = valid.validate_register(username, email, password, confirm_password, User)
        
        if error:
            flash(error, "danger")
            return redirect("/register")

        password = password.encode("utf-8")
        hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode("utf-8")
        
        new_user = User(
            username=username,
            email=email,
            hash=hash,
        )

        try:
            db.session.add(new_user)
            db.session.commit()

            flash("Account Created, login!", "success")
            return redirect("/login")
        
        except Exception:
            db.session.rollback()
            return redirect("/register")

    else:
        return render_template("register.html")