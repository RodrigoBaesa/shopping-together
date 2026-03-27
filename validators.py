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
        return "Space can't be in "
    
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