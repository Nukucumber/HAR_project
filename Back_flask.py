from flask import Flask, render_template, redirect, url_for, flash, request, session
import DB.repos as repos, uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4().fields[-1])


@app.route("/login", methods = {"POST", "GET"})
def login():
    if "Logged" in session:

        if session["Logged"] == "admin":
            return redirect(url_for("index"))
        
        if session["Logged"] == "manager":
            return redirect(url_for("Products"))
        
        if session["Logged"] == "engineer":
            return redirect(url_for("Execution_processes"))
        
    if request.method == "POST":
        if repos.checkLogin(request.form.to_dict()["Nickname"], request.form.to_dict()["psw"]) == False:
            flash("Wrong password or nickname")
        else:
            session["Logged"] = request.form.to_dict()["Nickname"]
        return redirect(url_for("login"))
        
    return render_template("login.html", title = "login")



@app.route("/", methods = ["POST", "GET"])
def index():
    if "Logged" not in session:
        return redirect(url_for("login"))
    if session["Logged"] != "admin":
        session.pop("Logged")
        return redirect(url_for("login"))
        
    if request.method == "POST":
        if request.args.get("operation") == "search":
            session["date"] = request.form.to_dict()
            return redirect(url_for("index"))
        if request.args.get("operation") == "logout":
            session.clear()
            return redirect(url_for("login"))

    if "date" in session:
        return render_template("index.html", title = "Main report", user = session["Logged"], table = repos.search_task(session["date"]), input_date = session["date"]["date"])
    else:
        return render_template("index.html", title = "Main report", user = session["Logged"], table = "", input_date = "")
    

@app.route("/Products", methods = ["POST", "GET"])
def Products():
    if "Logged" not in session:
        return redirect(url_for("login"))
    if session["Logged"] != "manager" and session["Logged"] != "admin":
        session.pop("Logged")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        if request.args.get("operation") == "logout":
            session.clear()
            return redirect(url_for("login"))
        if request.args.get("operation") == "add":
            flash(repos.Products_add(request.form.to_dict()))
        if request.args.get("operation") == "deleteOrUpdate":
            if "delete" in request.form:
                flash(repos.Products_delete(request.form.to_dict()))
            if "update" in request.form:
                flash(repos.Products_update(request.form.to_dict()))
        return redirect(url_for("Products"))

    return render_template("Products.html", title = "Products", user = session["Logged"], table = repos.Products_showAll())


@app.route("/Staff", methods = ["POST", "GET"])
def Staff():
    if "Logged" not in session:
        return redirect(url_for("login"))
    if session["Logged"] != "admin":
        session.pop("Logged")
        return redirect(url_for("login"))

    if request.method == "POST":
        if request.args.get("operation") == "logout":
            session.clear()
            return redirect(url_for("login"))
        if "delete" in request.form:
            flash(repos.Staff_delete(request.form.to_dict()))
        if "update" in request.form:
            flash(repos.Staff_update(request.form.to_dict()))
        return redirect(url_for("Staff"))

    return render_template("Staff.html", title = "Staff", user = session["Logged"], table = repos.Staff_showAll())


@app.route("/Orders", methods = ["POST", "GET"])
def Orders():
    if "Logged" not in session:
        return redirect(url_for("login"))
    if session["Logged"] != "manager" and session["Logged"] != "admin":
        session.pop("Logged")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        if request.args.get("operation") == "logout":
            session.clear()
            return redirect(url_for("login"))
        if request.args.get("operation") == "add":
            flash(repos.Orders_add(request.form.to_dict()))
        if request.args.get("operation") == "deleteOrUpdate":
            if "delete" in request.form:
                flash(repos.Orders_delete(request.form))
            if "update" in request.form:
                flash(repos.Orders_update(request.form))
        return redirect(url_for("Orders"))

    return render_template("Orders.html", title = "Orders", user = session["Logged"], table_orders = repos.Orders_showAll(), table_products = repos.Products_showAll(), table_staff = repos.Staff_showAll())

@app.route("/Execution_processes", methods = ["POST", "GET"])
def Execution_processes():
    if "Logged" not in session:
        return redirect(url_for("login"))
    if session["Logged"] != "engineer" and session["Logged"] != "admin":
        session.pop("Logged")
        return redirect(url_for("login"))

    if request.method == "POST":
        if request.args.get("operation") == "logout":
            session.clear()
            return redirect(url_for("login"))
        if request.args.get("operation") == "show":
            session["product_id"] = request.form.to_dict()["product_id"]
        if request.args.get("operation") == "add":
            flash(repos.Execution_processes_add(request.form.to_dict()))
        if request.args.get("operation") == "deleteOrUpdate":
            if "delete" in request.form:
                flash(repos.Execution_processes_delete(request.form.to_dict()))
            if "update" in request.form:
                flash(repos.Execution_processes_update(request.form.to_dict()))
        return redirect(url_for("Execution_processes"))
    if "product_id" in session:
        return render_template("Execution_processes.html", title = "Execution processes", user = session["Logged"], product_id = session["product_id"], table_execution = repos.Execution_processes_showAll(session["product_id"]), table_orders = repos.Orders_showAll_for_execution(), table_products = repos.Products_showAll_for_execution())
    else:
        return render_template("Execution_processes.html", title = "Execution processes", user = session["Logged"], table_execution = repos.Execution_processes_showAll(""), table_orders = repos.Orders_showAll_for_execution(), table_products = repos.Products_showAll_for_execution())
    
@app.route("/staff_id_orders_id")
def staff_id_orders_id():
    if "Logged" not in session:
        return redirect(url_for("login"))
    if session["Logged"] != "admin":
        session.pop("Logged")
        return redirect(url_for("login"))
    
    return render_template("staff_id_orders_id.html", title = "staff_id orders_id", user = session["Logged"], table = repos.staff_id_orders_id_showAll())

if __name__ == "__main__":
    app.run(debug=True)