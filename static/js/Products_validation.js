import { isCorrectDate } from "./DateCheck.js"

function validation(form){
    var input = form.querySelectorAll("input")
    for (let input_index = 0; input_index < input.length; input_index++) {
        input[input_index].classList.remove("wrongInput")        
    }
    for (let input_index = 0; input_index < input.length; input_index++) {

        if (input[input_index].name.indexOf("product_id_") > -1) {
            if (input[input_index].value == "") {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Choise at least one product <br> from products table "
                return false
            }
        }

        if (input[input_index].name.indexOf("product_name") > -1) {
            if (/^[A-Z А-Я0-9]{3,40}$/i.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the product name field"
                return false
            }
        }

        if (input[input_index].name.indexOf("model") > -1) {
            if (/^[A-Z0-9 _/\-]{3,40}$/i.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the model field"
                return false
            }
        }

        if (input[input_index].name.indexOf("warranty_period") > -1) {
            if (isCorrectDate(input[input_index].value) == false) {
                
                input[input_index].value = ""
            }
        }

        if (input[input_index].name.indexOf("image") > -1) {
            if (input[input_index].value != "" && /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w\.-]*)*\/?$/i.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the image field"
                return false
            }
        }
    }

    var textarea = form.querySelectorAll("textarea")

    for (let textarea_index = 0; textarea_index < textarea.length; textarea_index++) {
        if (textarea[textarea_index].value != "" && /^[A-ZА-ЯЁ0-9_/:,.;\-\n ]{3,400}$/i.test(textarea[textarea_index].value) == false) {
            textarea[textarea_index].classList.add("wrongInput")
            document.querySelector(".message").innerHTML = "Incorrect format of the technical specifications field"
            return false
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