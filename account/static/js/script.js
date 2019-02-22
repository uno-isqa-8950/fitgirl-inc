$(document).ready(function() {

    function weekmenuresizing(){
    
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
    // Affirmations popup code ends here - Karthik
// if($(".footer-from-disclaimer").length == 0){
// }else{
//
//     $("#userLandingContent1").css("display","none")
// }


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



    if($(".slider").width() < 1250)
{
     //Do Something
}


});

  