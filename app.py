from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

# Function to evaluate password strength
def evaluate_password_strength(password):
    min_length = 12
    has_lowercase = re.search(r'[a-z]', password)
    has_uppercase = re.search(r'[A-Z]', password)
    has_digit = re.search(r'[0-9]', password)
    has_special = re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
    no_spaces = not re.search(r'\s', password)

    strength = 0
    if len(password) >= min_length:
        strength += 1
    if has_lowercase:
        strength += 1
    if has_uppercase:
        strength += 1
    if has_digit:
        strength += 1
    if has_special:
        strength += 1
    if no_spaces:
        strength += 1

    # Rating strength
    if strength == 6:
        strength_rating = "Strong"
    elif strength == 5:
        strength_rating = "Moderate"
    elif strength == 4:
        strength_rating = "Weak"
    else:
        strength_rating = "Very Weak"

    return strength_rating

# Function to check for common passwords
def check_for_common_passwords(password):
    common_passwords = ["123456", "password", "qwerty", "12345", "letmein", "admin", "welcome"]
    if password.lower() in common_passwords:
        return True
    return False

# Function to generate recommendations
def generate_recommendations(strength_rating):
    recommendations = []
    if strength_rating == "Very Weak":
        recommendations.append("Your password is too weak. Consider the following improvements:")
        recommendations.append("- Use at least 12 characters.")
        recommendations.append("- Include both uppercase and lowercase letters.")
        recommendations.append("- Add numbers and special characters.")
        recommendations.append("- Avoid using easily guessable passwords such as 'password123'.")
        recommendations.append("- Do not use personal information like your name or birthdate.")
    elif strength_rating == "Weak":
        recommendations.append("Your password is weak. Consider the following improvements:")
        recommendations.append("- Use a longer password, ideally at least 12 characters.")
        recommendations.append("- Try using a mix of uppercase, lowercase, numbers, and special characters.")
    elif strength_rating == "Moderate":
        recommendations.append("Your password is moderate. To strengthen it:")
        recommendations.append("- Make it longer if possible.")
        recommendations.append("- Try using more complex combinations of characters.")
    else:
        recommendations.append("Your password is strong. However, it's always good to keep it updated regularly.")
    return recommendations


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze_password():
    data = request.get_json()  # Get the data sent in JSON format
    password = data.get('password')  # Extract the password from the data

    if not password:
        return jsonify({'error': 'Password is required'}), 400

    # Evaluate password strength
    strength_rating = evaluate_password_strength(password)

    # Check for common passwords
    common_password_warning = check_for_common_passwords(password)

    # Generate recommendations
    recommendations = generate_recommendations(strength_rating)
    if common_password_warning:
        recommendations.append("Warning: This password is too common and can be easily guessed.")

    return jsonify({
        'strength': strength_rating,
        'recommendations': recommendations
    })


if __name__ == '__main__':
    app.run(debug=True)
