(function($){
	"use strict";


	$('[data-bg-image]').each(function(){
		$(this).css({ 'background-image': 'url('+$(this).data('bg-image')+')' });
	});

	$('[data-bg-color]').each(function(){
		$(this).css({ 'background-color': $(this).data('bg-color') });
	});

	$('[data-width]').each(function(){
		$(this).css({ 'width': $(this).data('width') });
	});

	$('[data-height]').each(function(){
		$(this).css({ 'height': $(this).data('height') });
	});


	$('.service-group').each(function(){
		var $services = $(this);
		$services.find('.tt-el-service').each(function(){ $(this).addClass('has-group'); });
		$services.find('.tt-el-service').eq(0).addClass('group-first');
		$services.find('.tt-el-service').eq(-1).addClass('group-last');
	});

	


	
	// Master Slider
	var slider = new MasterSlider();
 
    slider.control('arrows' ,{insertTo:'#masterslider'});  
    slider.control('bullets'); 
 
    slider.setup('masterslider' , {
        width: 1140,
        height: 768,
        space: 5,
        view: 'basic',
        layout: 'fullscreen',
        fullscreenMargin: 57,
        speed: 20
    });


    
    var slider = new MasterSlider();
    slider.setup('masterslider_promo' , {
        width: 1440,
        height: 553, //413
        //space:100,
        fullwidth:true,
        centerControls:false,
        speed:18,
        view:'basic'
    });






    $('.tt-el-tabs').each(function(){
    	var $tabs = $(this);
    	var _active = 0;

    	if( $tabs.find('.el-nav').find('.el-item.active').length ){
    		_active = $tabs.find('.el-nav').find('.el-item').index( $tabs.find('.el-nav').find('.el-item.active') );
    	}
    	else{
    		$tabs.find('.el-nav').find('.el-item').eq(0).addClass('active');
    	}

    	$tabs.find('.el-content').find('.el-content-item').eq(_active).slideDown();


    	$tabs.find('.el-nav').find('.el-item').on('click', function(){
    		var _active = $tabs.find('.el-nav').find('.el-item').index( $(this) );

    		$tabs.find('.el-nav').find('.el-item.active').removeClass('active');
    		$(this).addClass('active');

    		$tabs.find('.el-content').find('.el-content-item').slideUp();
    		$tabs.find('.el-content').find('.el-content-item').eq(_active).slideDown();
    	});

    });




    $('.tt-el-progress').each(function(){
    	var $line = $(this);
    	var _val = $line.find('.el-label').find('span').text() + '';
    	_val = _val.replace('%', '');
    	$line.find('.el-current').css('width', _val + '%');
    });




	$('.tt-el-blog-carousel').each(function(){
		var $carousel = $(this).find('.owl-carousel');
		$carousel.owlCarousel({
			singleItem: true,
			pagination: true,
			paginationNumbers: false
		});
	});



	$('.tt-el-quote-carousel').each(function(){
		var $carousel = $(this).find('.owl-carousel');
		$carousel.owlCarousel({
			singleItem: true,
			pagination: false,
			navigation: true,
			navigationText: ["<i class='fa fa-caret-left'></i>","<i class='fa fa-caret-right'></i>"]
		});
	});



	$('.tt-el-carousel-container').each(function(){
		var $carousel = $(this).find('.owl-carousel');
		var _item = parseInt($(this).data('item'), 10);
		$carousel.owlCarousel({
			items: _item,
			itemsDesktop: [1199,_item],
			itemsDesktopSmall: [979,_item],
			itemsTablet: [768,_item],
			itemsMobile: [600,1],
			singleItem: false,
			pagination: true,
			paginationNumbers: false
		});
	});


	

	$('.tt-el-accordion').each(function(){
		var $acc = $(this);
		if( $acc.find('.el-accordion.active').length<1 ){
			$acc.find('.el-accordion').eq(0).addClass('active');
		}

		$acc.find('.el-accordion').each(function(){
			var $panel = $(this);

			$panel.find('.el-ac-title h4 a').on('click', function(){
				$acc.find('.el-accordion.active').find('.el-ac-content').slideUp();
				$acc.find('.el-accordion.active').removeClass('active');
				$panel.find('.el-ac-content').slideDown();
				$panel.addClass('active');
			});
		});
	});




	$('#toggle-header-search').on('click', function(){
		$('#header').toggleClass('show-search');
		if( $('#header').hasClass('show-search') ){
			$('#header').find('.header-search input[name="s"]').focus();
		}
	});

	$('#header').find('.header-search a').on('click', function(){
		$('#header').toggleClass('show-search');
		$('#header').find('.header-search input[name="s"]').val('');
	});



	// Mobile menu handler
	$('#mobile-menu').on('click', function(){
		if( $('#mobile-menu-wrapper').find('.menu-content').find('ul').length<1 ){
			var _menu = $('<div/>').append( $('#header').find('ul.menu').clone() );
			_menu.find('ul.menu').removeClass('menu');
			$('#mobile-menu-wrapper').find('.menu-content').html(_menu.html());
		}
		$('#mobile-menu-wrapper').toggleClass('active-menu');
	});


	$('#mobile-menu-wrapper').find('.menu-close').on('click', function(){
		$('#mobile-menu-wrapper').toggleClass('active-menu');
	});


	$('.portfolio-item').each(function(){
		var $item = $(this);
		var _src = $item.find('.entry-image > img').attr('src');
		$item.find('.el-zoom').attr('href', _src);
		$item.find('.el-zoom').prettyPhoto();
	});



})(jQuery);