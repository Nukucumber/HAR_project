export function isCorrectDate(table_date){

    var today = new Date()
    var zero_be4_day = ""
    var zero_be4_month = ""
    if (today.getDate() < 10) {
        zero_be4_day = "0"
    }
    if (today.getMonth()+1 < 10) {
        zero_be4_month = "0"
    }
    var nowDate = String(today.getFullYear()) + zero_be4_month + String(today.getMonth()+1) + zero_be4_day + String(today.getDate())
    
    table_date = table_date.split('-').join('');


    if (Number(table_date) - Number(nowDate) < 0) {
        return false
    }
    return true
}

export function DateDiff(first_date, second_date){
    var f = new Date(Number(first_date.split('-')[0]), Number(first_date.split('-')[1]), Number(first_date.split('-')[2]))
    var s = new Date(Number(second_date.split('-')[0]), Number(second_date.split('-')[1]), Number(second_date.split('-')[2]))
    return (s-f)/(1000*60*60*24)
}