var tbody = document.querySelector("tbody")

if (tbody != undefined) {
    var tr = tbody.querySelectorAll("tr")
    for (let tr_index = 0; tr_index < tr.length; tr_index++) {
        
        var td = tr[tr_index].querySelectorAll("td")
    
        for (let td_index = 0; td_index < td.length; td_index++) {
            
            if (td[td_index].innerHTML.indexOf("http://") == 0 || td[td_index].innerHTML.indexOf("https://") == 0) {
                var imgref = td[td_index].innerHTML
                td[td_index].innerHTML = '<img src="' + imgref + '" alt="' + imgref + '">'
            }
        }
    }
}