function upload() {
    let i = 0
    var target = document.querySelector(".upload_" + i + " tbody")

    while (target != null) {
        upload_execution(target, i)
        i += 1
        target = document.querySelector(".upload_" + i + " tbody")
    }
}


function upload_execution(target, i){
    var tr = target.querySelectorAll("tr")
    var tr_prev

    for (let tr_index = 0; tr_index < tr.length; tr_index++) {
        tr[tr_index].addEventListener("click", function(){
            
            var target_input = document.querySelectorAll(".upload_input_" + i)
            var td = tr[tr_index].querySelectorAll("td")

            if (tr_prev != undefined) {
                tr_prev.classList.remove("active")
            }
            if (tr_prev != undefined && tr_prev.querySelectorAll("td")[0].innerHTML == td[0].innerHTML) {
                
                for (let td_index = 0; td_index < td.length; td_index++) {
                    for (let target_input_index = 0; target_input_index < target_input.length; target_input_index++) {
                        if (target_input[target_input_index].querySelector(".n_" + td_index) != null) {
                            target_input[target_input_index].querySelector(".n_" + td_index).value = ""
                        }
                    }
                }

                tr_prev.classList.remove("active")
                tr_prev = undefined
            }
            else{
                for (let td_index = 0; td_index < td.length; td_index++) {
                    for (let target_input_index = 0; target_input_index < target_input.length; target_input_index++) {
                        if (target_input[target_input_index].querySelector(".n_" + td_index) != null) {
                            target_input[target_input_index].querySelector(".n_" + td_index).value = td[td_index].innerHTML
                        }
                    }
                }

                tr[tr_index].classList.add("active")
                tr_prev = tr[tr_index]
            }
        })        
    }
}


function filling(){
    let i = 0
    var target = document.querySelector(".filling_" + i + " tbody")

    while (target != null) {
        filling_execution(target, i)
        i += 1
        target = document.querySelector(".filling_" + i + " tbody")
    }
}

function filling_execution(target, i){
    
    var tr = target.querySelectorAll("tr")
    var id_array = []
    
    for (let tr_index = 0; tr_index < tr.length; tr_index++) {
        
        tr[tr_index].addEventListener("click", function(){
            var target_input = document.querySelector(".filling_input_" + i + ".empty")
            if (target_input != null) {
                
                tags_name = []
                var children_input = target_input.children
                for (let children_index = 0; children_index < children_input.length; children_index++) {
                    tags_name.push(children_input[children_index].name)
                }

                td = tr[tr_index].querySelectorAll("td")

                if (id_array.includes(td[0].innerHTML) == false) {
                    
                    for (let td_index = 0; td_index < td.length; td_index++) {
                    
                        if (target_input.querySelector(".n_" + td_index) != null) {
                            target_input.querySelector(".n_" + td_index).value = td[td_index].innerHTML
                        }                
                    }

                    id_array.push(td[0].innerHTML)
                    tr[tr_index].classList.add("active")
                    target_input.classList.remove("empty")
                    target_input.classList.add("filled")
                    target_input.insertAdjacentHTML('afterEnd', '<p class="filling_input_' + i + ' empty">' + target_input.innerHTML +'</p>')
                    
                }
                else {
                    field = document.querySelectorAll(".filling_input_" + i + ".filled")

                    for (let field_index = 0; field_index < field.length; field_index++) {
                        
                        if (field[field_index].querySelector(".n_0").value == td[0].innerHTML) {
                            field[field_index].remove(field[field_index])
                            let id_index = id_array.indexOf(td[0].innerHTML)
                            id_array.splice(id_index, 1)
                            tr[tr_index].classList.remove("active")
                        }
                    }
                }
                namedTagsForCount(".filling_input_" + i + ".filled", tags_name)
            }
        })
    }
}

function groupAdding() {
    var target = document.querySelectorAll(".group_adding")
    var tags_name = []
    for (let target_index = 0; target_index < target.length; target_index++) {

        var children = target[target_index].children
        for (let children_index = 0; children_index < children.length; children_index++) {
            tags_name.push(children[children_index].name)
        }
        namedTagsForCount(".group_adding", tags_name)


        target[target_index].onclick = add_new_field_button

        function add_new_field_button(){
            if (this.classList.contains("last") == true) {
                children = this.children
                if (children[children.length - 1].classList.contains("new_field_button") == false) {
                    children[children.length - 1].insertAdjacentHTML('afterEnd', '<br><button type="button" class="new_field_button">+</button>')
                    this.querySelector(".new_field_button").onclick = add_new_field
                }
            }
        }

        function add_new_field(){
            var field = this.parentElement
            this.remove(this)
            field.querySelector("br").remove(field.querySelector("br"))
            field.classList.remove("last")
            children = field.children
            field.insertAdjacentHTML('afterEnd', '<p class="group_adding last">' + field.innerHTML + '</p>')
            children[children.length - 1].insertAdjacentHTML('afterEnd', '<br><button type="button" class="delete_field_button">delete field</button>')
            field.querySelector(".delete_field_button").onclick = delete_field
            field.nextSibling.onclick = add_new_field_button
            namedTagsForCount(".group_adding", tags_name)
        }
        
        function delete_field(){
            this.parentElement.remove(this.parentElement)
            namedTagsForCount(".group_adding", tags_name)
        }

    }
}


function namedTagsForCount(conteiner_class, tags_name) {
    conteiner = document.querySelectorAll(conteiner_class)
    for (let conteiner_index = 0; conteiner_index < conteiner.length; conteiner_index++) {
        children = conteiner[conteiner_index].children

        for (let chidren_index = 0; chidren_index < children.length; chidren_index++) {
            children[chidren_index].name = tags_name[chidren_index] + "_" + conteiner_index            
        }
        
    }
}


upload()
groupAdding()
filling()