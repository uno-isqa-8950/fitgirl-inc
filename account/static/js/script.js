

  $(window).on('load', function(){ 
    // executes when complete page is fully loaded, including all frames, objects and images
    var nutrition_height = $( ".nutrition-images-array" ).height();
    $(".nutrition-facts .rich-text").css("height",nutrition_height);
  });
$(document).ready(function() {


    // $(function(){
    //     // Bind the swipeleftHandler callback function to the swipe event on div.box
    //     $( "body" ).on( "swipeleft", swipeleftHandler );
       
    //     // Callback function references the event target and adds the 'swipeleft' class to it
    //     function swipeleftHandler( event ){
    //       $( event.target ).addClass( "swipeleft" );
    //       alert(1);
    //     }
    //   });

    
    function weekmenuresizing(){
        
var nutrition_height = $( ".nutrition-images-array" ).height();
$(".nutrition-facts .rich-text").css("height",nutrition_height);
    }
    (function($,sr){

        // debouncing function from John Hann
        // http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
        var debounce = function (func, threshold, execAsap) {
            var timeout;
      
            return function debounced () {
                var obj = this, args = arguments;
                function delayed () {
                    if (!execAsap)
                        func.apply(obj, args);
                    timeout = null;
                };
      
                if (timeout)
                    clearTimeout(timeout);
                else if (execAsap)
                    func.apply(obj, args);
      
                timeout = setTimeout(delayed, threshold || 100);
            };
        }
        // smartresize 
        jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };
      
      })(jQuery,'smartresize');
      
      
      // usage:
      $(window).smartresize(function(){
        // code that takes it easy...
        weekmenuresizing();
      });



    // Affirmations popup code starts here - Karthik
    if ($(".current-week").length == 0) {
        //Not the user-landing page
    } else {
        if (!sessionStorage.alreadyClicked) {
            $('#exampleModalCenter').modal('show');
            $(".modal-title .navbar-brand").animate({
                "left": "0"
            }, "slow");
            sessionStorage.alreadyClicked = "true";
        } else {
            return false;
        }
    }
    $('.logout-button').click(function() {
        window.sessionStorage.clear();
    })
    
    
    
    $('.warning-close').click(function() {
        localStorage.setItem('checkalert', true); 
    })
    var v = localStorage.getItem('checkalert'); 
    if (v == 'true') { // Check if it's equal to the string true
     $("#warning-alert").hide();
    } else {
        $("#warning-alert").show();
    }


    //Registration breadcrumb issue fix - karthik
    if ($(".registration-dashboard").length == 0) {
        $(".step.step-1").addClass("done");
    } else {
        $(".step.step-1").removeClass("done");
        $(".step.step-1").addClass("active");
    }

$( "#strength .rich-text img" ).wrapAll( "<div class='strength-images-array' />");
$( "#agility .rich-text img" ).wrapAll( "<div class='agility-images-array' />");
$( "#flexibility .rich-text img" ).wrapAll( "<div class='flexibility-images-array' />");
$("#strength .rich-text").children().not( ".strength-images-array" ).wrapAll( "<div class='strength-paragraphs' />");
$("#agility .rich-text").children().not( ".agility-images-array" ).wrapAll( "<div class='agility-paragraphs' />");
$("#flexibility .rich-text").children().not( ".flexibility-images-array" ).wrapAll( "<div class='flexibility-paragraphs' />");
$(".strength-paragraphs").insertAfter(".strength-images-array");
$(".agility-paragraphs").insertAfter(".agility-images-array");
$(".flexibility-paragraphs").insertAfter(".flexibility-images-array");


$(".physical-post-page").closest("body").addClass("physical-body");
$(".nutrition-post-page").closest("body").addClass("nutrition-body");
$(".question-page").closest("body").addClass("question-body");
$( ".physical-post-page br" ).remove();


// slider 
var slideCount = $('.slider ul li').length;
console.log(slideCount);
	var slideWidth = $('.slider ul li').width();
    console.log(slideWidth);
	var slideHeight = $('.slider ul li').height();
    console.log(slideHeight);
	var sliderUlWidth = slideCount * slideWidth;
    console.log(sliderUlWidth);
    //$('.slider').css({ width: slideWidth, height: slideHeight });
    // $('.slider ul').css({marginLeft: - slideWidth });
    // $('.slider ul li:last-child').prependTo('.slider ul');
    function moveLeft() {
        // alert("left");
        $('.slider ul').animate({
            left: + slideWidth
        }, 200, function () {
            $('.slider ul li:last-child').prependTo('.slider ul');
            $('.slider ul').css('left', '');
        });
    };
    function moveRight() {
        // alert("right");
        $('.slider ul').animate({
            left: - slideWidth
        }, 200, function () {
            $('.slider ul li:first-child').appendTo('.slider ul');
            $('.slider ul').css('left', '');
        });
    };
    $('.previous').click(function () {
        moveLeft();
    });

    $('.next').click(function () {
        moveRight();
    });

/*BEGIN Swipe*/
$(function() {			
	//Enable swiping...
	$(".slider").swipe( {
		//Generic swipe handler for all directions
		swipe:function(event, direction, distance, duration, fingerCount, fingerData) {
			if (direction == "left") {
					// $( ".previous" ).trigger( "click" );
                    console.log("left swipe");
                    $('.slider ul').animate({
                        left: + slideWidth
                    }, 200, function () {
                        $('.slider ul li:last-child').prependTo('.slider ul');
                        $('.slider ul').css('left', '');
                    });
			}
			if (direction == "right") {
					// $( ".next" ).trigger( "click" );
                    console.log("right swipe");
                    $('.slider ul').animate({
                        left: - slideWidth
                    }, 200, function () {
                        $('.slider ul li:first-child').appendTo('.slider ul');
                        $('.slider ul').css('left', '');
                    });
			}			
			// if (direction == "down") {
			// 		window.scrollBy(0,-300);
			// }
			// if (direction == "up") {
			// 		window.scrollBy(0,300);
			// }
		},
		//Default is 75px, set to 0 for demo so any distance triggers swipe
	   threshold:0
	});
});
/*END Swipe*/
    if($(".slider").width() < 1253)
{
     //Do Something
}


// Printing a particular div
function printDiv(divName) {
    var printContents = document.getElementById(divName).innerHTML;
    var originalContents = document.body.innerHTML;
    document.body.innerHTML = printContents;
    window.print();
    document.body.innerHTML = originalContents;
}
// Content manipulation in nutrition page
$( "#nutrition .rich-text img" ).wrapAll( "<div class='nutrition-images-array' />");
$( ".nutrition-facts" ).prependTo ( ".nutrition-content .rich-text" );
$( ".nutrition-images-array" ).after( "<div class='spacer-div-30 clear-left'></div>" );
var nutrition_height = $( ".nutrition-images-array" ).height();
$(".nutrition-facts .rich-text").css("height",nutrition_height);
// $( ".nutrition-facts" ).after( ".nutrition-images-array" );
$( ".nutrition-images-array" ).after( $(".nutrition-facts") );
// if($("body").hasClass("nutrition-body")){
//     // $(".fitgirlinc-footer-socialLinks").addClass("nutrition-post-page container");
// }

if ($("#dtDynamicVerticalScroll, .trigger-admin").length > 0) {
    $("body").addClass("admin-page")
}
if($("#canvas").length>0){
    $("body").attr('style', 'background-image: none !important');
    $(".back-btn").css('position','relative');
}

$( ".folder-icon" ).prependTo ( ".gallery-card-title .rich-text" );
					   

	//----------Select the first tab and div by default
	
	$('#vertical_tab_nav > ul > li > a').eq(0).addClass( "selected" );
	$('#vertical_tab_nav > div > article').eq(0).css('display','block');


	//---------- This assigns an onclick event to each tab link("a" tag) and passes a parameter to the showHideTab() function
			
		$('#vertical_tab_nav > ul').click(function(e){
			
      if($(e.target).is("a")){
      
        /*Handle Tab Nav*/
        $('#vertical_tab_nav > ul > li > a').removeClass( "selected");
        $(e.target).addClass( "selected");
        
        /*Handles Tab Content*/
        var clicked_index = $("a",this).index(e.target);
        $('#vertical_tab_nav > div > article').css('display','none');
        $('#vertical_tab_nav > div > article').eq(clicked_index).fadeIn();
        
      }
      
        $(this).blur();
        return false;
      
		});
	$(".kindness-card-button").click( function(){
       var kindness_name = $(this).siblings( ".bio" ).children(".profile-name").text();
       $(".kindness-modal-content").children(".kindness-email").remove();
       var kindness_email = $(this).siblings( ".bio" ).children(".kindness-email");
       $( kindness_email ).clone().appendTo( ".kindness-modal-content" );
       $(".popup-name").empty();
       $( ".popup-name" ).text( kindness_name );
    })	
	 
    var kindness_section = $(".tabordion").children("section").length;
    var kindness_section_children = $(".tabordion").children("section");
//    alert(abc)
    $( kindness_section_children ).each(function( index ) {
    var i = index+1;
        $(this).attr('id', 'section'+i);
        $(this).find( "#option" ).attr('id', 'option'+i);
        $(this).find( "label" ).attr('for', "option"+i);
//  console.log( index + ": " + $( this ).text() );
});
   
});


