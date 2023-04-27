import sqlite3, uuid
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash

def Products_showAll():
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    allProducts = c.execute("SELECT * FROM Products").fetchall()
    c.close()
    con.close()
    return allProducts

def Products_showAll_for_execution():
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    allProducts = c.execute("SELECT * FROM Products WHERE product_id IN (SELECT fk_product_id FROM Orders WHERE order_id IN (SELECT fk_order_id FROM Execution_processes));").fetchall()
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

def Products_warranty_delete(product_id):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    c.execute("""UPDATE Products SET warranty_period = ""
        WHERE product_id = """ + product_id + """
    """)
    con.commit()
    c.close()
    con.close()
    return



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
            c.execute("""INSERT INTO staff_id_orders_id VALUES(
                """ + data["new_employee_id_" + str(i)] + """,
                """ + data["order_id"] + """
                )
            """)
            i += 1
    if data["employee_name_0"] != "":
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



def Execution_processes_showAll(product_id):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    if product_id == "":
        allExecution_processes = ""
        # allExecution_processes = c.execute("SELECT * FROM Execution_processes").fetchall()
    else:
        allExecution_processes = c.execute("SELECT * FROM Execution_processes WHERE fk_order_id IN (SELECT order_id FROM orders WHERE fk_product_id = " + product_id + ");").fetchall()
    c.close()
    con.close()
    if allExecution_processes == []:
        allExecution_processes = ""
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
            type_of_repair = '""" + data["type_of_repair_" + str(i)] + """',
            repair_cost = """ + data["repair_cost_" + str(i)] + """,
            message_to_the_client = '""" + data["message_to_the_client_" + str(i)] + """',
            order_execution_date = '""" + data["order_execution_date_" + str(i)] + """'
            WHERE execution_process_id = """ + data["execution_process_id_" + str(i)] + """
        """)
        i += 1

    save_warranty = True

    if data["date_of_product_receipt"] != "":
        
        second_date = data["date_of_product_receipt"]
        second_date = second_date.split('-')
        second_date = date(int(second_date[0]), int(second_date[1]), int(second_date[2]))

        allExecute = c.execute("SELECT * FROM Execution_processes WHERE fk_order_id IN (SELECT order_id FROM Orders WHERE fk_product_id = " + data["product_id"] + ");").fetchall()

        for item in allExecute:
            first_date = item[3]
            first_date = first_date.split('-')
            first_date = date(int(first_date[0]), int(first_date[1]), int(first_date[2]))
            diff_date = second_date - first_date
            if diff_date.days - 30 > 0:
                save_warranty = False
                payment_amount = float(item[2]) + float(item[2]) * 0.05 * (diff_date.days - 30)
            else:
                payment_amount = item[2]

            c.execute("UPDATE Execution_processes SET payment_amount = " + str(payment_amount) + " WHERE execution_process_id = " + str(item[0]) + ";")    

        c.execute("""UPDATE Execution_processes SET date_of_product_receipt = '""" + data['date_of_product_receipt'] + """' WHERE fk_order_id IN 
            (SELECT order_id FROM Orders WHERE fk_product_id = """ + data["product_id"] + """);
        """)


    con.commit()
    c.close()
    con.close()

    if save_warranty == False:
        Products_warranty_delete(data["product_id"])
    
    return "succesfully update"

def search_task(data):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()

    date_array = c.execute("SELECT order_execution_date FROM Execution_processes").fetchall()
    date_array_res = [] 
    for item in date_array:
        item = item[0].split('-')
        order_date = item[0] + "-" + item[1]
        if order_date == data["date"]:
            date_array_res.append(item[0] + "-" + item[1] + "-" + item[2])

    date_array_res = list(set(date_array_res))

    res = []
    product_res = []
    for item in date_array_res:
        product = (c.execute("""SELECT product_name, firm, model, product_id FROM Products 
        WHERE product_id IN (SELECT fk_product_id FROM Orders 
        WHERE order_id IN (SELECT fk_order_id FROM Execution_processes
        WHERE order_execution_date = '""" + str(item) + """'))""").fetchall())
        for i in product:
            product_res.append(i)

    product_res = list(set(product_res))
    
    for item in product_res:
        lst = list(item)
        product_set = []
        for i in date_array_res:

            order = c.execute("""SELECT order_id, client_name, client_surname, client_patronymic, client_phone_number,
            date_of_order_receipt, client_name, client_name FROM Orders WHERE fk_product_id = """ + str(lst[3]) + """ 
            AND order_id IN (SELECT fk_order_id FROM Execution_processes
            WHERE order_execution_date = '""" + str(i) + """') AND warranty = 1""").fetchall()
            if order != []:
                if item not in product_set:
                    product_set.append(tuple(item))
                    pre_res = []

                    for k in lst:
                        pre_res.append(k)

                    pre_res[3] = c.execute("""SELECT COUNT(order_id) FROM Orders WHERE fk_product_id IN 
                    (SELECT product_id FROM Products WHERE model = '""" + lst[2] + """')""").fetchall()[0][0]
                    
                    res.append(tuple(pre_res))
                for j in order:
                    order_lst = list(j)
                    order_lst[6] = i
                    order_lst[7] = (date(int(order_lst[6].split('-')[0]), int(order_lst[6].split('-')[1]), int(order_lst[6].split('-')[2])) - date(int(order_lst[5].split('-')[0]), int(order_lst[5].split('-')[1]), int(order_lst[5].split('-')[2]))).days
                    res.append(tuple(order_lst))


    c.close()
    con.close()
    return res

def staff_id_orders_id_showAll():
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    staff_id_orders_id = c.execute("SELECT * FROM staff_id_orders_id").fetchall()
    c.close()
    con.close()
    return staff_id_orders_id

def checkLogin(Nickname, psw):
    con = sqlite3.connect("DB/HAR_DB.db")
    c = con.cursor()
    dataUsers = c.execute("SELECT * FROM Users WHERE Nickname = '" + Nickname +"'").fetchall()
    c.close()
    con.close()
    if dataUsers == []:
        return False
    if list(dataUsers[0])[1] != Nickname or check_password_hash(list(dataUsers[0])[2], psw) == False:
        return False
    return True