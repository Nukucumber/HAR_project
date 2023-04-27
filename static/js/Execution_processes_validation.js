import { isCorrectDate } from "./DateCheck.js"

function validation(form){
    var input = form.querySelectorAll("input")

    var activeTags = document.querySelectorAll(".wrongInput")

    for (let activeTags_index = 0; activeTags_index < activeTags.length; activeTags_index++) {
        activeTags[activeTags_index].classList.remove("wrongInput")
    }


    for (let input_index = 0; input_index < input.length; input_index++) {
        input[input_index].classList.remove("wrongInput")

        if (input[input_index].name.indexOf("fk_order_id") > -1) {
            if (input[input_index].value == "") {
                document.querySelector(".order_table").querySelector("thead").querySelector("tr").classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Choise one of the orders table"
                return false
            }
        }
    }
    for (let input_index = 0; input_index < input.length; input_index++) {

        if (input[input_index].name.indexOf("execution_process_id_") > -1) {
            if (input[input_index].value == "") {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Choise at least one execution process <br> from execution processes table"
                return false
            }
        }

        if (/^product_id$/.test(input[input_index].name) == true) {
            if (input[input_index].value == "") {
                document.querySelector(".message").innerHTML = 'Select the product and click on the button below <br> to see execution processes'
                return false
            }
        }

        if(/^repair_cost$/.test(input[input_index].name) == true){
            
            var td = document.querySelector(".order_table").querySelector(".active").querySelectorAll("td")

            if (td[4].innerHTML == "1") {
                input[input_index].value = 0
            }
        }
        
        if (input[input_index].name.indexOf("repair_cost") > -1) {
            if (/^[0-9]+$/.test(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the repair cost field"
                return false
            }
        }
        
        if(/^order_execution_date$/.test(input[input_index].name) == true){
            if (isCorrectDate(input[input_index].value) == false) {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the order execution date field"
                return false
            }
        }

        if(/^order_execution_date_/.test(input[input_index].name) == true){
            if (input[input_index].value == "") {
                input[input_index].classList.add("wrongInput")
                document.querySelector(".message").innerHTML = "Incorrect format of the order execution date field"
                return false
            }
        }

        if (input[input_index].name.indexOf("date_of_product_receipt") > -1) {
            if (input[input_index].value != "") {
                if (isCorrectDate(input[input_index].value) == false) {
                    input[input_index].classList.add("wrongInput")
                    document.querySelector(".message").innerHTML = "Incorrect format of the date of product receipt field"
                    return false
                }
                if (is_date_of_product_receipt_correct(input[input_index].value) == false) {
                    input[input_index].classList.add("wrongInput")
                    return false
                }
            }
        }
    }

    return true
}

function is_date_of_product_receipt_correct(date_of_product_receipt){

    var tr = document.querySelector(".execution_process tbody").querySelectorAll("tr")
    for (let tr_index = 0; tr_index < tr.length; tr_index++) {
        var td = tr[tr_index].querySelectorAll("td")[3]
        var first_date = Number(date_of_product_receipt.split('-').join(''))
        var secont_date = Number(td.innerHTML.split('-').join(''))
        if (first_date - secont_date < 0) {
            document.querySelector(".message").innerHTML = "There is an execution process was not execute"
            td.classList.add("wrongInput")   
            return false
        }
    }

    tr = document.querySelector(".order_table tbody").querySelectorAll("tr")
    for (let tr_index = 0; tr_index < tr.length; tr_index++) {
        var td = tr[tr_index].querySelectorAll("td")[7]
        if (td.innerHTML == document.querySelector(".product_id").value) {
            document.querySelector(".message").innerHTML = "There is an order that has no execution process"
            tr[tr_index].classList.add("wrongInput")   
            return false
        }
    }
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