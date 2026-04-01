import bcrypt
import re

def validate_register(username, email, password, confirm_password, User):
    if not username or not email or not password or not confirm_password:
        return "Invalid arguments."

    if len(username) <= 3:
        return "Username must have at least 4 characters."
    
    if not username.isalnum():
        return "Invalid character in username."
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        return "Invalid email pattern."
    
    if len(password) < 8:
        return "Password must contain at least 8 characters."
    
    if not any(char.isdigit() for char in password):
        return "Password must contain at least 1 number."
    
    if not any(not char.isalnum() for char in password):
        return "Password must contain at least 1 special character e.g., @#$%&*."
    
    if " " in password:
        return "Spaces can't be in password"
    
    if password != confirm_password:
        return "Passwords don't match."
    
    username_exists = User.query.filter_by(username=username).count()
    if username_exists != 0:
        return "Username already taken."
    
    email_exists = User.query.filter_by(email=email).count()
    if email_exists != 0:
        return "Email already in use."
    
    else:
        return None
    
def validate_login(email, password, User):
    try:
        user = User.query.filter_by(email=email).one_or_none()

        if not email or not password:
            return "Invalid arguments."
        
        if not user:
            return "Couldn't find this email-password combination in our database."

        user_hash = user.hash.encode("utf-8")
        
        if not bcrypt.checkpw(password, user_hash):
            return "Couldn't find this email-password combination in our database."
        
    except Exception:
        return "Critical error, try again."
    
    return None