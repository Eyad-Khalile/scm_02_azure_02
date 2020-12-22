// make the Email in the form register required filde
// let astr = '<span class="asteriskField">*</span>';
// $('input.emailinput').parent().prev('label').addClass('requiredField').append(astr);

$("form.form-signin").find('label[for="id_username"]').addClass("d-none");
$("form.form-signin").find("#id_username").attr("placeholder", "اسم المستخدم");

$("form.form-signin").find('label[for="id_password"]').addClass("d-none");
$("form.form-signin").find("#id_password").attr("placeholder", "كلمة المرور");

// ORG PROFILE 



// DOMAIN WORK
$('#id_work_domain').change(function () {
    let domain = $('#id_work_domain').val();
    console.log(domain);
});

// CITY AJAX
$("#fill_form #id_position_work").change(function () {

    const url = $("#fill_form").attr("data-cities-url"); // get the url of the `load_cities` view
    const countryId = $(this).val(); // get the selected country ID from the HTML input

    $.ajax({ // initialize an AJAX request
        url: url, // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'position_work': countryId // add the country id to the GET parameters
        },

        success: function (data) { // `data` is the return of the `load_cities` view function
            $("#id_city_work").html(data); // replace the contents of the city input with the data that came from the server

            /*

            let html_data = '<option value="">---------</option>';
            data.forEach(function (city) {
                html_data += `<option value="${city.id}">${city.name}</option>`
            });
            console.log(html_data);
            $("#id_city").html(html_data);

            */
        }
    });

});

// $('#fill_form #id_user').change(function () {
//     let val = $('#id_user').val();
//     // console.log(val);
// });



// // JOBS CITY AJAX
$("#add_job #id_position_work").change(function () {
    const url = $("#add_job").attr("data-cities-url"); // get the url of the `load_cities` view
    const countryId = $(this).val(); // get the selected country ID from the HTML input
    $.ajax({ // initialize an AJAX request
        url: url, // set the url of the request (= /persons/ajax/load-cities/ )
        data: {
            'position_work': countryId // add the country id to the GET parameters
        },
        success: function (data) { // `data` is the return of the `load_cities` view function
            $("#id_city_work").html(data); // replace the contents of the city input with the data that came from the server
        }
    });
});

// FINANCE ORGS CITY AJAX
$("#finance_orgs #id_position_work").change(function () {
    const url = $("#finance_orgs").attr("data-cities-url");
    const countryId = $(this).val();
    $.ajax({
        url: url,
        data: {
            'position_work': countryId
        },
        success: function (data) {
            $("#id_city_work").html(data);
        }
    });
});

// FINANCE PERSO CITY AJAX
$("#add_perso_finance #id_position_work").change(function () {
    const url = $("#add_perso_finance").attr("data-cities-url");
    const countryId = $(this).val();
    $.ajax({
        url: url,
        data: {
            'position_work': countryId
        },
        success: function (data) {
            $("#id_city_work").html(data);
        }
    });
});


// CAPACITY CITY AJAX
$("#add_capacity #id_position_work").change(function () {
    const url = $("#add_capacity").attr("data-cities-url");
    const countryId = $(this).val();
    $.ajax({
        url: url,
        data: {
            'position_work': countryId
        },
        success: function (data) {
            $("#id_city_work").html(data);
        }
    });
});


// REGISTERED COUNTRY
$("#div_id_org_registered_country").hide();
if ($("#id_is_org_registered").val() == "1") {
    $("#div_id_org_registered_country").show();
}
$("#id_is_org_registered").change(function () {
    let org_reg = $("#id_is_org_registered").val();
    switch (org_reg) {
        case "1":
            $("#div_id_org_registered_country").show();
            break;
        default:
            $("#div_id_org_registered_country").hide();
            break;
    }
});

$('#id_dead_date, #id_dev_date, #id_funding_dead_date, #id_capacity_dead_date').attr('type', 'date');

// INPUT ACCEPT YEAR ONLY
$(
    "input#id_start_date,  input#id_end_date, input#id_date_of_establishment"
).attr({
    maxlength: "4",
    spellcheck: "false",
    oninput: "this.value = this.value.replace(/[^0-9]/g, '').replace(/(\\..*)\\./g, '$1').replace(/^(0*)/,'');",
    placeholder: "Ex : YYYY",
});

$('input#id_start_date_pub, input#id_end_date_pub').attr('type', 'date');

// FIELD PHONE
$("#id_phone").attr({
    maxlength: "16",
    oninput: "this.value = this.value.replace(/[^0-9+]/g, '');",
    placeholder: "Ex : 00963 / +963",
});

// LES CHARACTERS SPECIAUX
$(
    "#id_name, #id_name_en_ku, #id_short_cut, #id_message, #id_name_managing_director, #id_name_ceo, #id_name_person_contact, #id_org_adress, #id_coalition_name"
).attr({
    minlength: "3",
    oninput: "this.value = this.value.replace(/[^ا-يa-zA-Z0-9\nçêîşûłňřüḧẍ' ]/g, '');",
});

// MEMBERS COUNT
$("#id_org_members_count, #id_org_members_womans_count").attr({
    maxlength: "4",
    oninput: "this.value = this.value.replace(/[^0-9.]/g, '');",
    placeholder: "Ex : 1 - 9999",
});

$("#div_id_coalition_name").hide();
if ($("#id_org_member_with").val() == "1") {
    $("#div_id_coalition_name").show();
}

$("#id_org_member_with").change(function () {
    let mem = $("#id_org_member_with").val();
    switch (mem) {
        case "":
            $("#div_id_coalition_name").hide();
            break;
        case "0":
            $("#div_id_coalition_name").hide();
            break;
        case "1":
            $("#div_id_coalition_name").show();
            break;
    }
});

// ACCEPT ORG
$("form.confirm").find("#id_publish").hide();
$("form.confirm").submit(function () {
    $("form.confirm").find("#id_publish").attr("checked", true);
});

// REFIOUSE ORG
$("form.deconfirm").find("#id_publish").hide();
$("form.deconfirm").submit(function () {
    $("form.deconfirm").find("#id_publish").attr("checked", false);
});



// URL
var pathname = window.location.pathname; // Returns path only (/path/example.html)
// var url = window.location.href;     // Returns full URL (https://example.com/path/example.html)
var origin = window.location.origin; // Returns base URL (https://example.com)

// console.log('olde path : ' + pathname);
// console.log(url);
// console.log(origin);
// console.log(location);


function removeCharacter(str) {
    let tmp = str.split("");
    return tmp.slice(3).join("");
}


// if (pathname[1] == "e" && pathname[2] == "n") {
//     let output = removeCharacter(pathname);
//     console.log(`Output is ${output}`);
// }

// LANGE SWICHER
$("#chnage-lange").change(function () {
    let lan_sel = $("#chnage-lange").val();
    switch (lan_sel) {
        case "ar":
            document.location.href = origin + removeCharacter(pathname);
            console.log('ar pathname', pathname)
            break;
        case "en":
            if (pathname.includes('/ku')) {
                document.location.href = origin + "/en" + removeCharacter(pathname);
            } else {
                document.location.href = origin + "/en" + pathname;
            }
            break;

        case "ku":
            if (pathname.includes('/en')) {
                document.location.href = origin + "/ku" + removeCharacter(pathname);
            } else {
                document.location.href = origin + "/ku" + pathname;
            }
            break;
    }

});



// RAPPORT
$('form#form_rapport').find('#id_media').attr('accept', 'application/pdf,image/*');




// NEWSLETTER FORM AJAX
// var form = $(".form-news-latter")
// form.on('submit', function submitForm(e) {
//     form.find("input").each(function(i, v) {
//         $(this).find('#id_name, #id_work, #id_org_name, #id_email').val("");
//     });

// e.preventDefault();
// $.ajax({
//     type: 'POST',
//     // url: '{% url "home" %}',
//     // url: '',
//     data: $(".form-news-latter").serialize(),
//     dataType: 'json',
//     success: function (data) {
//         // form[0].reset();
//         // $(".form-news-latter").reset();
//         form.find("input").each(function(i, v) {
//             $(this).val("");
//         });
//         // $('#messagesModale').modal('show');
//         // alert('You have been Successfully subscribed');
//         window.location.reload();


//     }

// });
// });


// if ($('#error_1_id_email')) {
//     alert('This email already exists');
// }

let my_forms_country = $('#add_job, #finance_orgs, #add_perso_finance, #add_capacity');

my_forms_country.find('#div_id_city_work').hide();
let county_vall = $('#add_job, #finance_orgs #id_position_work').val();

if (county_vall == 'SY' ||
    county_vall == 'TR' ||
    county_vall == 'IQ' ||
    county_vall == 'LB' ||
    county_vall == 'JO' ) {
 
    my_forms_country.find('#div_id_city_work').show();
} else {
    my_forms_country.find('#div_id_city_work').hide();
}


my_forms_country.find('#id_position_work').change(function () {
    let country = $(this).val();
    switch (country) {
        case "SY":
            my_forms_country.find('#div_id_city_work').show();
            break;
        case "TR":
            my_forms_country.find('#div_id_city_work').show();
            break;
        case "JO":
            my_forms_country.find('#div_id_city_work').show();
            break;
        case "LB":
            my_forms_country.find('#div_id_city_work').show();
            break;
        case "IQ":
            my_forms_country.find('#div_id_city_work').show();
            break;
        default:
            my_forms_country.find('#div_id_city_work').hide();
            break;
    }
});



// RESOURCES
// FORM ADD JOB 
let other = '<option value="other">Other</option>';
$('#add_job #id_org_name').append(other);
$('#add_job #id_other_org_name').append(other);
// $('.edit_job #id_org_name').append(other);
// $('.edit_job #id_other_org_name').append(other);

$('#add_job, .edit_job').find('#div_id_other_org_name, #div_id_name, #div_id_logo').hide();
// $('#edit_job').find('#div_id_other_org_name, #div_id_name, #div_id_logo').hide();

if ($('.edit_job #id_org_name').val() == '') {
    $('#id_org_name').val('other');
    $('#div_id_other_org_name').show();
}

if ($('.edit_job #id_other_org_name').val() == '' && $('.edit_job #id_org_name').val() == '') {
    $('#id_other_org_name').val('other');
    $('#div_id_name, #div_id_logo').show();
}

$('#id_org_name').change(function () {
    let value = $(this).val();
    console.log(value);
    switch (value) {
        case 'other':
            if (!$('#div_id_other_org_name').parent().hasClass('list-org-0')) {
                $('#div_id_other_org_name').show();
                $('#add_job').submit(function () {
                    $('#id_org_name').val('');
                });
            } else {
                $('#div_id_name, #div_id_logo').show();
            }
            break;
        default:
            $('#div_id_other_org_name, #div_id_name, #div_id_logo').hide();
            break;
    }

});

$('#id_other_org_name').change(function () {
    let value = $(this).val();
    console.log(value);
    switch (value) {
        case 'other':
            $('#div_id_name, #div_id_logo').show();
            $('#add_job, .edit_job').submit(function () {
                $('#id_other_org_name').val('');
            });
            break;
        default:
            $('#div_id_name, #div_id_logo').hide();
            break;
    }
});

$('.add-job-from-add-job').submit(function () {
    if ($('#id_org_name').val() == 'other') {
        $('#id_org_name').val('');
    }
});
$('.edit_job').submit(function () {
    if ($('#id_org_name').val() == 'other') {
        $('#id_org_name').val('');
    }
});

// PERIOD MONTHS
$('#id_period_months').attr({
    maxlength: "3",
    oninput: "this.value = this.value.replace(/[^0-9+]/g, '');",
    placeholder: "Ex : 6",
});


// PERSO FINANCE
$('#add_perso_finance').find('#div_id_study_level, #div_id_comp_study, #div_id_domain').hide();
$('#add_perso_finance').find('#id_fund_type').change(function () {
    let value = $(this).val();
    switch (value) {
        case "study":
            $('#div_id_study_level, #div_id_comp_study').show();
            $('#add_perso_finance').find('#div_id_domain').hide();
            break;
        case "prod":
            $('#add_perso_finance').find('#div_id_domain').show();
            $('#div_id_study_level, #div_id_comp_study').hide();
            break;
        case "study & reserch":
            $('#add_perso_finance').find('#div_id_domain').show();
            $('#div_id_study_level, #div_id_comp_study').hide();
            break;
    }
});

$('#dev_form').find('#id_content').attr('accept', 'application/pdf, image/*');

// VIDEO PLACE HOLDER
$('#id_video').attr('placeholder', 'Ex:  https://www.youtube.com');





// UPDATE PROFILE -> POSITION
let olde_total_forms = $('.update-position').find('input[name=form-TOTAL_FORMS]').val();
let olde_initial_forms = $('.update-position').find('input[name=form-INITIAL_FORMS]').val();

let new_total_forms = $('.form-vio').find('input[name=form-TOTAL_FORMS]');
let new_initial_forms = $('.form-vio').find('input[name=form-INITIAL_FORMS]');

new_total_forms.attr('value', olde_total_forms);
new_initial_forms.attr('value', olde_initial_forms);

// :::::::::::: ADD POSITIONS AND CITYS ::::::::::::::::::
var form_idx = new_total_forms.val()-1;
// var form_idx = 0;
$('#add_more_vio').click(function () {
    form_idx++;
    // var form_idx = $('#id_form-TOTAL_FORMS').val();
    $('#form_set_vio').append($('#empty_form_vio').html().replace(/__prefix__/g, form_idx));
    $('#id_form-TOTAL_FORMS').val(parseInt(form_idx) + 1);


    // CITY HIDE AND SHOW
    // CITY CHOISES
    $("#div_id_form-" + form_idx + "-city_work").hide();
    if ($("#id_form-1-position_work").val() == "SY" || $("#id_position_work").val() == "TR" || $("#id_position_work").val() == "JO" || $("#id_position_work").val() == "LB" || $("#id_position_work").val() == "IQ") {
        $("#div_id_form-" + form_idx + "-city_work").show();
    }
    $("#id_form-" + form_idx + "-position_work").change(function () {
        let country = $(this).val();
        switch (country) {
            case "SY":
                $("#div_id_form-" + form_idx + "-city_work").show();
                break;
            case "TR":
                $("#div_id_form-" + form_idx + "-city_work").show();
                break;
            case "JO":
                $("#div_id_form-" + form_idx + "-city_work").show();
                break;
            case "LB":
                $("#div_id_form-" + form_idx + "-city_work").show();
                break;
            case "IQ":
                $("#div_id_form-" + form_idx + "-city_work").show();
                break;

            default:
                $("#div_id_form-" + form_idx + "-city_work").hide();
                break;
        }
    });

    // $("#id_form-"+form_idx+"-position_work").change(function () {
    //     const url = $("#fill_form").attr("data-cities-url"); 
    //     const countryId = $(this).val(); 
    //     $.ajax({ 
    //         url: url, 
    //         data: {
    //             'position_work': countryId 
    //         },

    //         success: function (data) {
    //             $("#id_city_work").html(data);

    //         }
    //     });
    // });

});

