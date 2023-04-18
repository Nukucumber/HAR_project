function validation(form){
    var input = form.querySelectorAll("input")
    for (let input_index = 0; input_index < input.length; input_index++) {
        input[input_index].classList.remove("wrongInput")        
    }
    for (let input_index = 0; input_index < input.length; input_index++) {

        if (input[input_index].name.indexOf("employee_id_") > -1) {
            if (input[input_index].value == "") {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Choise at least one employee <br> from staff table"
                return false
            }
        }

        if (input[input_index].name.indexOf("employee_name") > -1) {
            if (/^[A-Z][a-z]{3,15}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the employee name field"
                return false
            }
        }

        if (input[input_index].name.indexOf("employee_surname") > -1) {
            if (/^[A-Z][a-z]{3,25}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the employee surname field"
                return false
            }
        }

        if (input[input_index].name.indexOf("employee_patronymic") > -1) {
            if (input[input_index].value != "" && /^[A-Z][a-z]{3,25}$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the employee patronymic field"
                return false
            }
        }

        if (input[input_index].name.indexOf("employee_position") > -1) {
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