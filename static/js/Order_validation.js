import { DateDiff, isCorrectDate } from "./DateCheck.js"

function validation(form){
    var input = form.querySelectorAll("input")
    var isThereEmployeeInput = false
    var isThereEmployee = false

    document.querySelector(".fk_id").classList.remove("wrongInput")
    document.querySelector(".staff_table").classList.remove("wrongInput")
    for (let input_index = 0; input_index < input.length; input_index++) {
        input[input_index].classList.remove("wrongInput")

        if (input[input_index].name.indexOf("fk_product_id") > -1) {
            if (input[input_index].value == "") {
                document.querySelector(".fk_id").classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Choise one of the products table"
                return false
            }
        }
        
    }
    for (let input_index = 0; input_index < input.length; input_index++) {

        if (input[input_index].name.indexOf("order_id_") > -1) {
            if (input[input_index].value == "") {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Choise at least one order <br> from orders table"
                return false
            }
        }
        
        if (input[input_index].name.indexOf("client_name") > -1) {
            if (/^[A-Z][a-z]{3,15}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the client name field"
                return false
            }
        }

        if (input[input_index].name.indexOf("client_surname") > -1) {
            if (/^[A-Z][a-z]{3,25}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the client surname field"
                return false
            }
        }

        if (input[input_index].name.indexOf("client_patronymic") > -1) {
            if (input[input_index].value != "" && /^[A-Z][a-z]{3,25}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the client patronymic field"
                return false
            }
        }

        if (/^date_of_order_receipt$/.test(input[input_index].name) == true) {
            if (isCorrectDate(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the date of order receipt field"
                return false
            }
            else{
                var td = document.querySelector(".product").querySelector(".active").querySelectorAll("td")

                if (td[5].innerHTML == "" || DateDiff(input[input_index].value, td[5].innerHTML) < 0) {
                   form.querySelector(".n_4").value = "0"
                }
                else {
                   form.querySelector(".n_4").value = "1"
                }
            }
        }

        if (input[input_index].name.indexOf("client_phone_number") > -1) {
            if (/^[8][0-9]{10,10}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the client phone number field"
                return false
            }
        }

        if (input[input_index].name.indexOf("new_employee_name") > -1 || input[input_index].name.indexOf("new_employee_surname") > -1 || input[input_index].name.indexOf("new_employee_patronymic") > -1 || input[input_index].name.indexOf("new_employee_position") > -1) {
            if (input[input_index].value != "") {
                if (checkEmployeeField(input) == false){
                    return false
                }
                else{
                    isThereEmployee = true
                }
            }
            isThereEmployeeInput = true
        }

        if (input[input_index].name.indexOf("employee_id") > -1) {
            if (input[input_index].value != "") {
                isThereEmployee = true
            }

            isThereEmployeeInput = true
        }
    }
    if (isThereEmployeeInput == true && isThereEmployee == false) {
        document.querySelector(".staff_table").classList.add("wrongInput")
        document.querySelector(".message").innerHTML = "Add or select at least one employee"
        return false
    }
    return true
}


function checkEmployeeField(input){
    for (let input_index = 0; input_index < input.length; input_index++) {

        if (input[input_index].name.indexOf("new_employee_name") > -1) {
            if (/^[A-Z][a-z]{3,15}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the employee name field"
                return false
            }
        }

        if (input[input_index].name.indexOf("new_employee_surname") > -1) {
            if (/^[A-Z][a-z]{3,25}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the employee surname field"
                return false
            }
        }

        if (input[input_index].name.indexOf("new_employee_patronymic") > -1) {
            if (input[input_index].value != "" && /^[A-Z][a-z]{3,25}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the employee patronymic field"
                return false
            }
        }

        if (input[input_index].name.indexOf("new_employee_position") > -1) {
            if (/^[A-Z][a-z]{3,25}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the employee position field"
                return false
            }
        }
    }
    return true
}

var form = document.querySelectorAll('form')
for (let form_index = 0; form_index < form.length; form_index++) {
    form[form_index].addEventListener("submit", function (event) {
        var val = validation(form[form_index])
        if (val == true) {
            form[form_index].submit()
        }
        else{
            event.preventDefault()
        }
    })
}