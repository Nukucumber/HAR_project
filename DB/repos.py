import sqlite3, uuid


def Products_showAll():
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    allProducts = c.execute("SELECT * FROM Products").fetchall()
    c.close()
    con.close()
    return allProducts

def Products_add(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    i = 0
    while("product_name_" + str(i) in data):
        c.execute("""INSERT INTO Products VALUES (
            """ + str(uuid.uuid4().fields[-1]) + """,
            '""" + data['product_name_' + str(i)] + """',
            '""" + data['firm_' + str(i)] + """',
            '""" + data['model_' + str(i)] + """', 
            '""" + data['technical_specifications_' + str(i)] + """', 
            '""" + data['warranty_period_' + str(i)] + """', 
            '""" + data['image_' + str(i)] + """');
        """)
        i += 1
    con.commit()
    c.close()
    con.close()
    return "succesfully added"

def Products_delete(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    i = 0
    while("product_id_" + str(i) in data):
        c.execute("DELETE FROM Products WHERE product_id = " + data["product_id_" + str(i)] + ";")
        c.execute("DELETE FROM Orders WHERE fk_product_id = " + data["product_id_" + str(i)] + ";")
        c.execute("DELETE FROM Execution_processes WHERE fk_order_id NOT IN (SELECT order_id FROM Orders)")
        c.execute("DELETE FROM staff_id_orders_id WHERE order_id NOT IN (SELECT order_id FROM Orders)")
        c.execute("DELETE FROM Staff WHERE employee_id NOT IN (SELECT employee_id FROM staff_id_orders_id)")
        i += 1

    con.commit()
    c.close()
    con.close()
    return "succesfully deleted"

def Products_update(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    i = 0
    while("product_id_" + str(i) in data):
        c.execute("""UPDATE Products SET 
            product_name = '""" + data['product_name_' + str(i)] + """',
            firm = '""" + data['firm_' + str(i)] + """',
            model = '""" + data['model_' + str(i)] + """', 
            technical_specifications = '""" + data['technical_specifications_' + str(i)] + """', 
            warranty_period = '""" + data['warranty_period_' + str(i)] + """', 
            image = '""" + data['image_' + str(i)] + """'
            WHERE product_id = """ + data["product_id_" + str(i)] + """;
        """)
        i += 1

    con.commit()
    c.close()
    con.close()
    return "succesfully update"



def Staff_showAll():
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    allStaff = c.execute("SELECT * FROM Staff").fetchall()
    c.close()
    con.close()
    return allStaff

def Staff_delete(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    i = 0
    while("employee_id_" + str(i) in data):
        c.execute("DELETE FROM Staff WHERE employee_id = " + data["employee_id_" + str(i)] + ";")
        c.execute("DELETE FROM staff_id_orders_id WHERE employee_id = " + data["employee_id_" + str(i)] + ";")
        c.execute("DELETE FROM Orders WHERE order_id NOT IN (SELECT order_id FROM staff_id_orders_id)")
        c.execute("DELETE FROM Execution_processes WHERE fk_order_id NOT IN (SELECT order_id FROM Orders)")
        i += 1
    con.commit()
    c.close()
    con.close()
    return "succesfully deleted"
    
def Staff_update(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    i = 0
    while("employee_name_" + str(i) in data):
        c.execute("""UPDATE Staff SET 
            employee_name = '""" + data['employee_name_' + str(i)] + """', 
            employee_surname = '""" + data['employee_surname_' + str(i)] + """', 
            employee_patronymic = '""" + data['employee_patronymic_' + str(i)] + """', 
            employee_position = '""" + data['employee_position_' + str(i)] + """'
            WHERE employee_id = """ + data["employee_id_" + str(i)] + """
        """)
        i += 1
    con.commit()
    c.close()
    con.close()
    return "succesfully update"



def Orders_showAll():
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    allOrders = c.execute("SELECT * FROM Orders").fetchall()
    c.close()
    con.close()
    return allOrders

def Orders_showAll_for_execution():
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    
    allOrders = c.execute("SELECT * FROM Orders WHERE order_id NOT IN (SELECT fk_order_id FROM Execution_processes)").fetchall()

    c.close()
    con.close()
    return allOrders

def Orders_add(data):

    if "employee_id_0" not in data and data["new_employee_name_0"] == "":
        return "add or choise one employee"

    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    
    data["order_id"] = str(uuid.uuid4().fields[-1])
    c.execute("""INSERT INTO Orders VALUES (
        """ + data["order_id"] + """, 
        '""" + data['client_name'] + """', 
        '""" + data['client_surname'] + """', 
        '""" + data['client_patronymic'] + """', 
        '""" + data["warranty"] + """', 
        '""" + data['date_of_order_receipt'] + """',
        '""" + data["client_phone_number"] + """', 
        '""" + data["fk_product_id"] + """')
    """)

    if data["new_employee_name_0"] != "":
        i = 0
        while("new_employee_name_" + str(i) in data):
            data["new_employee_id_" + str(i)] = str(uuid.uuid4().fields[-1])
            c.execute("""INSERT INTO Staff VALUES (
                """ + data["new_employee_id_" + str(i)] + """, 
                '""" + data['new_employee_name_' + str(i)] + """', 
                '""" + data['new_employee_surname_' + str(i)] + """', 
                '""" + data['new_employee_patronymic_' + str(i)] + """', 
                '""" + data['new_employee_position_' + str(i)] + """')
            """)
            i += 1

        i = 0

        while("new_employee_id_" + str(i) in data):
            c.execute("""INSERT INTO staff_id_orders_id VALUES(
                """ + data["new_employee_id_" + str(i)] + """,
                """ + data["order_id"] + """
                )
            """)
            i += 1

    i = 0

    while("employee_id_" + str(i) in data):
        c.execute("""INSERT INTO staff_id_orders_id VALUES(
            """ + data["employee_id_" + str(i)] + """,
            """ + data["order_id"] + """
            )
        """)
        i += 1

    con.commit()
    c.close()
    con.close()
    return "succesfully added"

def Orders_delete(data):

    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    
    i = 0
    while("order_id_" + str(i) in data):
        c.execute("DELETE FROM Orders WHERE order_id = " + data["order_id_" + str(i)] + ";")
        c.execute("DELETE FROM staff_id_orders_id WHERE order_id = " + data["order_id_" + str(i)] + ";")
        c.execute("DELETE FROM Staff WHERE employee_id NOT IN (SELECT employee_id FROM staff_id_orders_id)")
        c.execute("DELETE FROM Execution_processes WHERE fk_order_id = " + data["order_id_" + str(i)] + ";")
        i += 1

    con.commit()
    c.close()
    con.close()
    return "succesfully deleted"

def Orders_update(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    i = 0
    while("order_id_" + str(i) in data):
        c.execute("""UPDATE Orders SET 
            client_name = '""" + data['client_name_' + str(i)] + """', 
            client_surname = '""" + data['client_surname_' + str(i)] + """', 
            client_patronymic = '""" + data['client_patronymic_' + str(i)] + """', 
            warranty = '""" + data["warranty_" + str(i)] + """', 
            date_of_order_receipt = '""" + data['date_of_order_receipt_' + str(i)] + """',
            client_phone_number = '""" + data["client_phone_number_" + str(i)] + """'
        WHERE order_id = """ + data["order_id_" + str(i)] + """
        """)
        i += 1

    con.commit()
    c.close()
    con.close()
    return "succesfully update"



def Execution_processes_showAll():
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    allExecution_processes = c.execute("SELECT * FROM Execution_processes").fetchall()
    c.close()
    con.close()
    return allExecution_processes

def Execution_processes_add(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    c.execute("""INSERT INTO Execution_processes VALUES (
        """ + str(uuid.uuid4().fields[-1]) + """,
        '""" + data['type_of_repair'] + """', 
        '""" + data['repair_cost'] + """', 
        '""" + data['order_execution_date'] + """', 
        '""" + data["message_to_the_client"] + """', 
        '""" + data['date_of_product_receipt'] + """',
        '""" + data["payment_amount"] + """', 
        """ + data["fk_order_id"] + """)
    """)
    con.commit()
    c.close()
    con.close()
    return "succesfully added"

def Execution_processes_delete(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    if ("fk_order_id" in data):
        c.execute("DELETE FROM Execution_processes WHERE fk_order_id = " + data["fk_order_id"] + ";")
    i = 0
    while("execution_process_id_" + str(i) in data):
        c.execute("DELETE FROM Execution_processes WHERE execution_process_id = " + data["execution_process_id_" + str(i)] + ";")
        i += 1
    con.commit()
    c.close()
    con.close()
    return "succesfully deleted"

def Execution_processes_update(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    i = 0
    while("execution_process_id_" + str(i) in data):
        c.execute("""UPDATE Execution_processes SET
            type_of_repair = '""" + data['type_of_repair_' + str(i)] + """', 
            repair_cost = '""" + data['repair_cost_' + str(i)] + """', 
            order_execution_date = '""" + data['order_execution_date_' + str(i)] + """', 
            message_to_the_client = '""" + data["message_to_the_client_" + str(i)] + """', 
            date_of_product_receipt = '""" + data['date_of_product_receipt_' + str(i)] + """',
            payment_amount = '""" + data["payment_amount_" + str(i)] + """'
            WHERE execution_process_id = """ + data["execution_process_id_" + str(i)] + """
        """)
        i += 1
    con.commit()
    c.close()
    con.close()
    return "succesfully added"



def staff_id_orders_id_showAll(): #debug display
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    allstaff_id_orders_id = c.execute("SELECT * FROM staff_id_orders_id").fetchall()
    c.close()
    con.close()
    return allstaff_id_orders_id

# def staff_id_orders_id_delete(data):    
#     if ("employee_id" in data):
#         field_id = "employee_id"
#         id = data["employee_id"]
#         second_field_id = "order_id"
#     else:
#         field_id = "order_id"
#         id = data["order_id"]
#         second_field_id = "employee_id"

#     con = sqlite3.connect("DB/HAR_DB.db")
#     c = con.cursor()
    
#     second_id = c.execute("SELECT " + second_field_id + " FROM staff_id_orders_id WHERE " + field_id + " = " + id + ";").fetchall()

#     dif = c.execute("SELECT " + second_field_id + " FROM staff_id_orders_id WHERE " + field_id + " != " + id + ";").fetchall()

#     for item in dif:
#         if item in second_id:
#             second_id.remove(item)

#     c.execute("DELETE FROM staff_id_orders_id WHERE " + field_id + " = " + id + ";")

#     con.commit()
#     c.close()
#     con.close()
#     if (second_field_id == "order_id"):
#         i = 0
#         for item in second_id:
#             data["order_id_" + str(i)] = str(item[0])
#             i += 1
#         Orders_delete(data)
#     else:
#         i = 0
#         for item in second_id:
#             data["employee_id_" + str(i)] = str(item[0])
#             i += 1
#         Staff_delete(data)
#     return second_id