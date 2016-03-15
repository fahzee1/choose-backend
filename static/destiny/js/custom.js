	jQuery(function () {
		"use strict";		
		
		/*global jQuery, fakewaffle */ 
			
		
		jQuery('.nav').onePageNav();
		
		jQuery(function() {
			jQuery('#nav-wrapper').height(jQuery("#nav").height());
			
			jQuery('#nav').affix({
				offset: { top: jQuery('#nav').offset().top }
			});
		});		
		
		// animation number
		
        jQuery(document).ready(function() {
		
			jQuery("#intro-loader").delay(1000).fadeOut();
			jQuery(".mask").delay(1000).fadeOut("slow");		
		
		
			jQuery('#slides').superslides({
				animation: 'fade',
				play:2000,
				pagination:false,
				inherit_width_from: '.top',
				inherit_height_from: '.top'
			});			
				
            jQuery("#pageLoad").animateNumbers(768, true, 2000);
						
			jQuery('.about_us_bg').parallax("50%", 0.2);
			jQuery('.how_can_you_help_bg').parallax("50%", 0.2);
			jQuery('.gallery-bg').parallax("50%", 0.2);			
			jQuery('.contact-bg').parallax("50%", 0.2);	

			jQuery('.bxslider_story').bxSlider({
				controls:false,	
				minSlides: 1,
				maxSlides: 3,
				slideWidth: 360,
				moveSlides: 1,
				slideMargin: 30
			});			


			//Elements Appear from top
			jQuery('.animate_top').each(function() {
				jQuery(this).appear(function() {
					jQuery(this).delay(200).animate({
						opacity : 1,
						top : "0px"
					}, 1000);
				});
			});

			//Elements Appear from bottom
			jQuery('.animate_bottom').each(function() {
				jQuery(this).appear(function() {
					jQuery(this).delay(200).animate({
						opacity : 1,
						bottom : "0px"
					}, 1000);
				});
			});
			//Elements Appear from left
			jQuery('.animate_left').each(function() {
				jQuery(this).appear(function() {
					jQuery(this).delay(200).animate({
						opacity : 1,
						left : "0px"
					}, 1000);
				});
			});
			
			//Elements Appear from right
			jQuery('.animate_right').each(function() {
				jQuery(this).appear(function() {
					jQuery(this).delay(200).animate({
						opacity : 1,
						right : "0px"
					}, 1000);
				});
			});
			
			//Elements Appear in fadeIn effect
			jQuery('.animate_fade_in').each(function() {
				jQuery(this).appear(function() {
					jQuery(this).delay(250).animate({
						opacity : 1,
						right : "0px"
					}, 1500);
				});
			});	
			
			
			jQuery('.ajax-popup-link').magnificPopup({
				type: 'ajax'
			});
			
			
        });
		
	
		// responsive tab
		
		jQuery('#myTab1 a').click(function (e) {
		e.preventDefault();
		jQuery(this).tab('show');
		});		
		
		jQuery('#myTab a').click(function (e) {
		e.preventDefault();
		jQuery(this).tab('show');
		});

		(function() {
			fakewaffle.responsiveTabs(['xs', 'sm']);
		})(jQuery);	

		new grid3D( document.getElementById( 'grid3d' ) );		
	
	}());