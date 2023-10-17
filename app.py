# Import libraries
from flask import Flask, request, url_for, redirect, render_template
from functools import reduce

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {"id": 1, "date": "2023-06-01", "amount": 100},
    {"id": 2, "date": "2023-06-02", "amount": -200},
    {"id": 3, "date": "2023-06-03", "amount": 300},
]


# Read operation
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)


# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        transation = {
            "id": len(transactions) + 1,
            "date": request.form["date"],
            "amount": float(request.form["amount"]),
        }
        transactions.append(transation)
        return redirect(url_for("get_transactions"))

    return render_template("form.html")


# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method == "POST":
        date = request.form.get("date")
        amount = request.form.get("amount")
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["date"] = date
                transaction["amount"] = amount
                break
        return redirect(url_for("get_transactions"))

    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction=transaction)


# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            transactions.remove(transaction)
            break

    return redirect(url_for("get_transactions"))


# Search operation
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method == "POST":
        print("Inside search post --------")
        minAmount = float(request.form.get("min_amount"))
        maxAmount = float(request.form.get("max_amount"))
        print(f"min amount: {minAmount}, max_amount: {maxAmount}")

        if minAmount and maxAmount is not None:
            filtered_transactions = filter(
                lambda t: t["amount"] >= minAmount and t["amount"] <= maxAmount,
                transactions,
            )
            return render_template(
                "transactions.html", transactions=filtered_transactions
            )
        return {"Error message": "input is wrong"}, 404
    else:
        return render_template("search.html")


# Total balance
@app.route("/balance")
def total_balance():
    balance = 0
    for transaction in transactions:
        balance += transaction["amount"]

    return {"Total balance": f"{balance}"}


# Run the Flask app
if __name__ == "__main__":
    app.run(port=5001, debug=True)
