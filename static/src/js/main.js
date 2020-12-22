// pre loader
$(window).on("load", function () {
    setInterval(function () {
        $('.loader').addClass('hidden');
    });
});



$('body').css('padding-top', $('.navbar').outerHeight() + 'px')

$('#navbarSupportedContent').find('.nav-link').css('height', $('.navbar').outerHeight() + 'px');


$('#list-collapse').addClass('d-none');
$('a.nav-toggle').on('click', function () {
    $('#list-collapse').toggleClass('d-none');
});




// AOS.init();

// $('#sidebar-wrapper').css('height', $('#sidebar-wrapper').parent().parent('div.col-2').outerHeight() + 'px');
// $('#sidebar-wrapper').css('height', $('div.min-vh-100').outerHeight() + 'px');

$(".alert").delay(4000).slideUp(1000, function () {
    $(this).alert('close');
    $(this).removeClass('messagesModale');
});

// setTimeout(function () {
//     $('#messagesModale').modal().hide();
// }, 3000);


// NAVBAR ANIMATIONS
if ($('nav').length > 0) { // check if element exists
    var last_scroll_top = 0;
    $(window).on('scroll', function () {
        scroll_top = $(this).scrollTop();
        if (scroll_top < last_scroll_top) {
            $('nav').removeClass('scrolled-down').addClass('scrolled-up');
            $('#carouselHomePage').find('.carousel-control-prev, .carousel-control-next').show();
            $('.sym-mouse').show();
            
        } else {
            $('nav').removeClass('scrolled-up').addClass('scrolled-down');
            $('#carouselHomePage').find('.carousel-control-prev, .carousel-control-next').hide();
            $('.sym-mouse').hide();
        }
        last_scroll_top = scroll_top;
    });
}


// URL
// var pathname = window.location.pathname;
// if (pathname == "/profile_supper/" || pathname == "/en/profile_supper/") {
//     $('div.main-container').removeClass('container').addClass('container-fluid');
// }

// TOGEL CLASS SHOW FROM THE COLLEPAS
$('a[data-toggle="collapse"]').on('click', function () {
    $('div.collapse.show').removeClass('show');
    $(this).addClass('show');
});

// DASHBOARD SIDEBAR
let width_col = $('.col-2.min-vh-100').outerWidth();
// $('#sidebar-wrapper').css('width', width_col);

$('#menu-toggle').click(function (e) {
    e.preventDefault();

    // $('#sidebar-wrapper').css('width', '50px');
    $('#wrapper').toggleClass('menuDisplayed', 7000, "easeInQuad");
    $('.sidebar-navbar').find('a').toggleClass('d-none', 7000, "easeOutSine");

    // $('.fa-tachometer-alt').toggleClass('d-none');

    // $('.nav-link').toggleClass('d-none');

    $('#menu-toggle svg').toggleClass('fa-angle-double-right fa-angle-double-left');
    // $('i.fa')

    $('#wrapper').parent().toggleClass('col-2');
    $('#wrapper').parent().toggleClass('min-vh-100');
    $('#wrapper').parent().next().toggleClass('col-10 col-12');

});


// SLIDER HEIGHT
let nav_height = $('.navbar').outerHeight();
let screen_height = $(window).height();






// SLIDER
// $('.skitter-large').skitter();
// $('.slider').bxSlider();


// $('#org_lider').slick({
//     autoplay: true,
// });


// URL
var pathname = window.location.pathname; // Returns path only (/path/example.html)

if (pathname == '/' || pathname == 'en') {
    $('#sider_bg').css('height', screen_height + 'px');
}

$('#wrapper').css('height', nav_height + 'px');


// READ MORE AND READ LESS
$('#collapsRead').on('click', function () {
    $(this).toggleClass('read-moin');
    if ($('#collapsRead').hasClass('read-moin')) {

        if (pathname.includes('/en')) {
            $('.read-moin').html('Read Less');
        } else if (pathname.includes('/ku')) {
            $('.read-moin').html('Read Less');
        } else {
            $('.read-moin').html('إقراء أقل');
        }
    } else if (!$('#collapsRead').hasClass('read-moin')) {
        if (pathname.includes('/en')) {
            $('#collapsRead').html('Read More');
        } else if (pathname.includes('/ku')) {
            $('#collapsRead').html('Read More');
        } else {
            $('#collapsRead').html('إقراء المزيد');
        }
    }
});

// GET THE SELECTED FILE NAME
// $('#id_logo').change(function (e) {
//     var fileName = e.target.files[0].name;
//     $('.logo_file_name').html('The logo "' + fileName + '" has been selected.');
//     $('input#logo').val(fileName);
// });


// SLIDE HOME PAGE 
$('#carouselHomePage').css('height', screen_height + 'px !important');
$('#carouselHomePage').find('img').css('height', screen_height + 'px !important');

// console.log($('#carouselHomePage').height());
// console.log($('#carouselHomePage').find('img').height());


$('#carouselHomePage').carousel({
    pause: false,
    interval: 5000,
});



// FUNCTION FOR THE SCROLL 
$(window).scroll(function () {

    // NAVBAR
    if ($(document).scrollTop() > ($(window).height() - 50)) {
        $('nav').addClass('nav-bg-scroll');
    } else {
        $('nav').removeClass('nav-bg-scroll');
    }

    // BTN TOP
    if ($(document).scrollTop() > ($(window).height() - 500)) {
        $('#f-5-top').fadeOut(1500).removeClass('d-none').fadeIn(1500);
    } else {
        $('#f-5-top').fadeIn(1500).addClass('d-none').fadeOut(1500);
    }

});




$('#carouselOrgs').carousel({
    pause: false,
    interval: 4000,
    // prev: false,
    // next: false,
});

$('#carouselOrgs').carousel({
    pause: false,
    interval: 60000,
});

// SCROLL TOP 
$("#scroll_top").click(function () {
    $("html, body").animate({
        scrollTop: 0
    }, "slow");
    return false;
});


// SIDE NAVBAR UP AND DOWN  
$('#sidebar-wrapper').find('.btn-down').on('click', function () {

    let m_t = $('#sidebar-wrapper').find('ul.sidebar-navbar').css('margin-top'); // Margin top
    let li_height = $('#sidebar-wrapper').find('li.nav-item').css('height'); // Height of the Li
    let li_count = $('ul.sidebar-navbar li').length - 9; // Number of li
    let lemite = Math.abs(parseInt(li_height)) * li_count; // Lemite of animation 
    console.log(li_height + '-' + li_count + '-' + lemite);
    console.log(m_t);

    if (parseInt(m_t) > -(lemite)) {
        $('#sidebar-wrapper').find('ul.sidebar-navbar').animate({
            'margin-top': '-=' + li_height
        }, 500);
    } else {
        $('#sidebar-wrapper').find('ul.sidebar-navbar').animate({
            'margin-top': '-780px'
        }, 500);
    }

});

$('#sidebar-wrapper').find('.btn-up').on('click', function () {
    let m_t = $('#sidebar-wrapper').find('ul.sidebar-navbar').css('margin-top');
    let li_height = $('#sidebar-wrapper').find('li.nav-item').css('height');

    if (parseInt(m_t) < 0) {
        $('#sidebar-wrapper').find('ul.sidebar-navbar').animate({
            'margin-top': '+=' + li_height
        }, 500);
    } else {
        $('#sidebar-wrapper').find('ul.sidebar-navbar').animate({
            'margin-top': '0'
        }, 500);
    }
});


// COUNT UP
$(function () {
    function count($this) {
        var current = parseInt($this.html(), 10);
        current = current + 1; /* Where 50 is increment */

        $this.html(++current);
        if (current > $this.data('count')) {
            $this.html($this.data('count'));
        } else {
            setTimeout(function () {
                count($this)
            }, 10);
        }
    }

    $(".stat-count").each(function () {
        $(this).data('count', parseInt($(this).html(), 10));
        $(this).html('0');
        count($(this));
    });

});

// MINI MENU
$('#span-menu').on('click', function () {
    $('#mini-menu').toggleClass('d-none', "slow", "easeOutSine");
});


// escape menu
document.onkeydown = function (evt) {
    let key = evt.keyCode;
    if (key === 27) {
        $('#mini-menu').addClass('d-none');
    }
}


// if ($("Your p tag").val().length == 0)

let p_empty = $('.job-card').find('p');



// $('.job-card').find('p').each(function () {
//     if (p_empty === "" || p_empty === "\u200b" ) {
//         $('.job-card').find('p').css('display', 'none');
//     }
// });

$('div.safe-content').find('p').addClass('safe-content');