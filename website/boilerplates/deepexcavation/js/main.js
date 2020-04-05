/*------------------------------------------------------------------
 * Theme Name: Hostio Responsive Template
 * Theme URI: http://www.brandio.io/envato/hostio
 * Author: Brandio
 * Author URI: http://www.brandio.io/
 * Description: A Bootstrap Responsive HTML5 Template
 * Version: 1.0
 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
 * Bootstrap v3.3.6 (http://getbootstrap.com)
 * Copyright 2016 Brandio.
 -------------------------------------------------------------------*/
"use strict";
$(window).on("load", function() {
    // Adding hover style for the feature box
    var featureBox = $(".feature-box", ".features");
    featureBox.on("mouseover",function(){
        featureBox.removeClass("active");
        $(this).addClass("active");
        return false;
    });
    // About page "about.html" and web hosting page "whosting.html"
    // Fix image resize issue.
    var storyImgHolder = $(".image-holder", ".story");
    var storyText = $(".txt-col",".story");
    var platformTooltip = $(".tool-tip", ".platforms");
    
    if ($(window).width() > 990) {
        storyImgHolder.css("height",storyText.height()+140);
        platformTooltip.removeAttr("style");
    }else{
        platformTooltip.each(function(i){
            $(this).css("margin-left",(($(this).width()+20)/2)*-1);
        });
    }
});
$(document).ready(function(){
   if (Cookies.get('collapsedbar') != undefined) {
       $('.global-sidebar-bottom').addClass('noanim').addClass('collapsed');
       $('button.toggle-button i').removeClass('fa-chevron-down').addClass('fa-chevron-up');
   }
});
$(document).on('click', 'button.toggle-button', function(){
   if ($('.global-sidebar-bottom').hasClass('collapsed')) {
       $('.global-sidebar-bottom').removeClass('noanim').removeClass('collapsed');
       $(this).find('i').removeClass('fa-chevron-up').addClass('fa-chevron-down');
   } else {
       $('.global-sidebar-bottom').addClass('collapsed');
       Cookies.set('collapsedbar', 'yes', {expires: 4, path: ''});
       $(this).find('i').removeClass('fa-chevron-down').addClass('fa-chevron-up');
   }
});
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
$(document).on('click','.add-to-cart, .buy-now', function(){
    var checked_modules = [];
    $(this).closest('div.pricing-box').find('input.software_module').each(function() {
       if ($(this).is(":checked")) {
           checked_modules.push($(this).val());
       }
    });
    var quantity = 1;
    try {
        quantity = parseInt($(this).closest('div.pricing-box').find('input[name="num-licenses"]').val());
    } catch (err) {
        quantity = 1;
    }
    var redirect = false;
    if ($(this).hasClass('buy-now')) {
        redirect = true;
    }
    $.post($(this).data('add-to-cart-url'),{software_modules:checked_modules.join(","), quantity: quantity}, function(data){
        if (redirect) {
            window.location = cart_page;
        } else {
            $('#shopping_cart .modal-body').html(data);
            $("#shopping_cart").modal('show');
        }
    });
    return false;
});
$(document).on('click', '.empty-cart', function () {
    $.post($(this).data('action-url'), {}, function (data) {
        window.location.reload()
    });
});
$(document).on('change', 'input.software_module', function(){
   var module_price = $(this).data('price');
   var pricing_box = $(this).closest('div.pricing-box').find('.pricing-amount .price .amount');
   var software_price = $(pricing_box).data('price');
   var current_total_price = $(pricing_box).data('total-price');
   if ($(this).is(":checked")) {
       current_total_price = current_total_price + module_price
   } else {
       current_total_price = current_total_price - module_price
   }
   $(pricing_box).data('total-price', current_total_price);
   $(pricing_box).html(current_total_price);
});
$(document).ready(function(){
    var url = document.location.toString();
    if (url.match('#')) {
        $('#' + url.split('#')[1]).addClass('in');
    }
    $('select.selectize').selectize({
        create: false
    });
});
$(document).on('click', '.download-software', function(){
    var download_url = $(this).data('download-url');
   $.get(sign_in_url, {next: download_url}, function(data){
      $('#download_modal .modal-title').text('Sign in or Sign Up');
      $('#download_modal .modal-body').html(data);
       $('select.selectize').selectize({
           create: false
       });
       $('#download_modal').modal('show');
   });
   return false;
});
$(document).on('submit', 'form.login.ajax, form.signup.ajax', function(){
    var form_action = $(this).attr('action');
    var form_tab = "#"+$(this).parent('div.tab-pane').attr('id');
    console.log(form_tab);
    var form_data = $(this).serialize();
    var the_form = $(this);
    $.ajax({
        method: "POST",
        beforeSend: function (xhrObj) {
            xhrObj.setRequestHeader("Accept", "application/json");
        },
        url: form_action,
        data: form_data,
    }).done(function(data, textStatus, jqXHR){
        if (data.hasOwnProperty('location')) {
            $('#download_modal').modal('hide');
            window.location = data.location;
        } else if (data.hasOwnProperty('html')) {
            $(the_form).parents('div.modal-body').html(data.html);
            $('a[href="'+form_tab+'"]').tab('show');
            $('select.selectize').selectize({
                create: false
            });
        }
    }).fail(function(jqXHR, textStatus, errorThrown){
        var response = jqXHR.responseJSON;
        if (response.hasOwnProperty('html')) {
            $(the_form).parents('div.modal-body').html(response.html);
            $('a[href="' + form_tab + '"]').tab('show');
            $('select.selectize').selectize({
                create: false
            });
        } else {
            alert('We are sorry an error has occurred');
            $('a[href="' + form_tab + '"]').tab('show');
        };
    });
    return false;
});