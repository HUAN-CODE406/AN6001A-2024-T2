from flask import Flask, request, jsonify

app = Flask(__name__)

# Function to calculate credit score
def calculate_credit_score(income, employment_status, has_default_record, loan_amount):
    score = 700  # Base score
    if income > 5000:
        score += 50  # Add points for higher income
    if employment_status in ["employed", "self-employed"]:
        score += 30  # Add points for stable employment
    if has_default_record:
        score -= 100  # Subtract points for past defaults
    if loan_amount > (income * 3):
        score -= 50  # Subtract points for a large loan relative to income
    return score

# Function to approve or reject loan
def approve_loan(score, loan_amount, income):
    score_threshold = 650
    max_loan_amount = income * 3  # Limit loan amount to 3x income
    if score >= score_threshold and loan_amount <= max_loan_amount:
        return "Approved"
    else:
        return "Rejected"

# Route to handle loan application
@app.route('/apply_loan', methods=['POST'])
def apply_loan():
    data = request.json  # Get data from the frontend (JSON)

    # Extract data from the request
    name = data.get("name")
    account = data.get("account")
    employment_status = data.get("employment_status")
    income = data.get("income")
    has_default_record = data.get("has_default_record", False)
    loan_amount = data.get("loan_amount")
    loan_period = data.get("loan_period")

    # Calculate credit score
    credit_score = calculate_credit_score(income, employment_status, has_default_record, loan_amount)
    
    # Approve or reject loan
    loan_status = approve_loan(credit_score, loan_amount, income)

    # Return the result as JSON
    return jsonify({
        "name": name,
        "credit_score": credit_score,
        "loan_status": loan_status,
        "loan_amount": loan_amount,
        "loan_period": loan_period
    })

if __name__ == '__main__':
    app.run(debug=True)


