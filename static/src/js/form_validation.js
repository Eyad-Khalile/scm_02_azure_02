$('form#fill_form').find('#id_name').blur(function () {
    if ($(this).val().length < 3) {
        $('#org_name').removeClass('d-none');
    }
});
$('form#fill_form').find('#id_name_en_ku').blur(function () {
    if ($(this).val().length < 3) {
        $('#org_name_en_ku').removeClass('d-none');
    }
});
$('form#fill_form').find('#id_short_cut').blur(function () {
    if ($(this).val().length < 3) {
        $('#short_cut').removeClass('d-none');
    }
});
$('form#fill_form').find('#id_message').blur(function () {
    if ($(this).val().length < 3) {
        $('#message_alert').removeClass('d-none');
    }
});

// var forms = document.getElementsByClassName('form');
// // Loop over them and prevent submission
// var validation = Array.prototype.filter.call(forms, function (form) {
//     form.addEventListener('submit', function (event) {
//         if (form.checkValidity() === false) {
//             event.preventDefault();
//             event.stopPropagation();
//         }
//         form.classList.add('was-validated');
//     }, false);
// });