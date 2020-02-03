/*
* проверка полей
*/
function checkFields() {
    
// Проверка одного поля - остальные required
// "Поступило из"
var court_id = $('#court_name');
if(court_id.val() == 0){
    court_id.addClass("is-invalid")
    court_id.removeClass("is-valid")
    court_id.tooltip('show')
    return false
}
else{
    court_id.removeClass("is-invalid")
    court_id.addClass("is-valid")
    court_id.tooltip('hide')
    return true
}
}

// при изменении значений
$('#court_name').change(function(){
    // проверка полей на корректность ввода
    checkFields();
}); // end change()


// MAIN FORM - Submit event
$('form#add_record_form').submit(function(event){

    // check form fields values
    if(!checkFields()){
    // prevent default submit behaviour
    event.preventDefault();
    }

    // serialize form data
    var data = $(this).serialize()

    // DEBUG Console logging
    console.log("Main form data: " + data);
}); // end submit()

// ADD COMPANY FORM - Submit event
$('form#add_company_form').submit(function(event){
    // prevent default submit behaviour
    event.preventDefault();

    // serialize form data
    var data = $(this).serialize()
    // DEBUG Console logging
    console.log("Add company form data: " + data);

    // AJAX запрос
    $.ajax({
        url: '/courts',
        type: 'POST',
        data: data,

        // при успешной отправке выводим ответ
        success: function(response){
            // обновляем список организаций на странице
            loadCourtList(court_id=response);
            console.log("New company record_id: " + response);
        }, // end success()
        error: function() { alert("Ошибка при добавлении организации!"); }
    }); // end $.ajax({

    // reset form after saving data
    // $('form#add_company_form')[0].reset();
    document.getElementById("add_company_form").reset();
    $('#add_company_modal').modal('hide')
}); // end submit()

// ADD EMPLOYEE FORM - Submit event
$('form#add_empl_form').submit(function(event){
    // prevent default submit behaviour
    event.preventDefault();

    // serialize form data
    var data = $(this).serialize()
    // DEBUG Console logging
    console.log("Add_employee_form data: " + data);

    // AJAX запрос
    $.ajax({
        url: '/employee',
        type: 'POST',
        data: data,

        // при успешной отправке выводим ответ
        success: function(response){
            // обновляем список сотрудников на странице
            loadEmplList(empl_id=response);
            console.log("New employee record_id: " + response);
        }, // end success()
        error: function() { alert("Ошибка при добавлении сотрудника!"); }
    }); // end $.ajax({

    // reset form after saving data
    // $('form#add_company_form')[0].reset();
    document.getElementById("add_empl_form").reset();
    $('#add_empl_modal').modal('hide')
}); // end submit()


function loadCourtList(court_id){
    // AJAX запрос
    $.ajax({
        url: 'courts', /* скрипт выполняющий наш запрос (список) */
        type: 'get',

        // при успешной отправке выводим ответ
        success: function(response){

            // парсим JSON ответ скрипта в массив
            // result_arr = jQuery.parseJSON(response);
            result_arr = JSON.parse(response);

            // выводим список
            // очищаем блок
            $('#court_name').empty();
            // добавляем информационную строку
            $("#court_name").append("<option selected value='0'>Выберите организацию</option>");
            
            // построчный разбор данных из массива result_arr
            // каждая строка массива попадает в data[]
            $.each(result_arr, function(index,data){
                var option_str = ""; 
                // если есть id организации, то выбираем его в списке
                if(data["id"] == court_id) {
                    // выбранный пункт
                    option_str = "<option selected value='"+data["id"]+"'>"+data["name"]+"</option>";
                }
                else {
                    // обычный пункт списка
                    option_str = "<option value='"+data["id"]+"'>"+data["name"]+"</option>";
                }
                // добавляем этот пункт в список
                $("#court_name").append(option_str);

            }); // end each()
        } // end success()
    }); // end $.ajax({
} // end loadCourtList()

function loadEmplList(empl_id){
    // AJAX запрос
    $.ajax({
        url: 'employee', /* скрипт выполняющий наш запрос (список) */
        type: 'get',

        // при успешной отправке выводим ответ
        success: function(response){

            // парсим JSON ответ скрипта в массив
            // result_arr = jQuery.parseJSON(response);
            result_arr = JSON.parse(response);

            // выводим список
            // очищаем блок
            $('#empl_name').empty();
            // добавляем информационную строку
            $("#empl_name").append("<option selected value='0'>Выберите сотрудника</option>");
            
            // построчный разбор данных из массива result_arr
            // каждая строка массива попадает в data[]
            $.each(result_arr, function(index,data){
                var option_str = ""; 
                // если есть id организации, то выбираем его в списке
                if(data["id"] == empl_id) {
                    // выбранный пункт
                    option_str = "<option selected value='"+data["id"]+"'>"+data["name"]+"</option>";
                }
                else {
                    // обычный пункт списка
                    option_str = "<option value='"+data["id"]+"'>"+data["name"]+"</option>";
                }
                // добавляем этот пункт в список
                $("#empl_name").append(option_str);

            }); // end each()
        } // end success()
    }); // end $.ajax({
} // end loadEmplList()