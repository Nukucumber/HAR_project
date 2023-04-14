from flask import Flask, render_template, redirect, url_for, flash, request, session
import DB.repos as repos, uuid

app = Flask(__name__)
app.secret_key = str(uuid.uuid4().fields[-1])
username = "tolik"
psw = "qwert"


@app.route("/")
def index():

    return render_template("index.html", title = "Main")


@app.route("/Products", methods = ["POST", "GET"])
def Products():
    if request.method == "POST":
        if request.args.get("operation") == "add":
            flash(repos.Products_add(request.form.to_dict()))
        if request.args.get("operation") == "deleteOrUpdate":
            if "delete" in request.form:
                flash(repos.Products_delete(request.form.to_dict()))
            if "update" in request.form:
                flash(repos.Products_update(request.form.to_dict()))
        return redirect(url_for("Products"))

    return render_template("Products.html", title = "Products", table = repos.Products_showAll())


@app.route("/Staff", methods = ["POST", "GET"])
def Staff():
    if request.method == "POST":
        if "delete" in request.form:
            flash(repos.Staff_delete(request.form.to_dict()))
        if "update" in request.form:
            flash(repos.Staff_update(request.form.to_dict()))
        return redirect(url_for("Staff"))

    return render_template("Staff.html", title = "Staff", table = repos.Staff_showAll())


@app.route("/Orders", methods = ["POST", "GET"])
def Orders():
    if request.method == "POST":
        if request.args.get("operation") == "add":
            flash(repos.Orders_add(request.form.to_dict()))
        if request.args.get("operation") == "deleteOrUpdate":
            if "delete" in request.form:
                flash(repos.Orders_delete(request.form))
            if "update" in request.form:
                flash(repos.Orders_update(request.form))
        return redirect(url_for("Orders"))

    return render_template("Orders.html", title = "Orders", table_orders = repos.Orders_showAll(), table_products = repos.Products_showAll(), table_staff = repos.Staff_showAll())


@app.route("/Execution_processes", methods = ["POST", "GET"])
def Execution_processes():
    if request.method == "POST":
        if request.args.get("operation") == "add":
            flash(repos.Execution_processes_add(request.form.to_dict()))
        if request.args.get("operation") == "deleteOrUpdate":
            if "delete" in request.form:
                flash(repos.Execution_processes_delete(request.form.to_dict()))
            if "update" in request.form:
                flash(repos.Execution_processes_update(request.form.to_dict()))
        return redirect(url_for("Execution_processes"))
    return render_template("Execution_processes.html", title = "Execution_processes", table_execution = repos.Execution_processes_showAll(), table_orders = repos.Orders_showAll_for_execution())
    

@app.route("/staff_id_orders_id", methods = ["POST", "GET"])
def staff_id_orders_id():

    return render_template("staff_id_orders_id.html", table = repos.staff_id_orders_id_showAll())


if __name__ == "__main__":
    app.run(debug=True)