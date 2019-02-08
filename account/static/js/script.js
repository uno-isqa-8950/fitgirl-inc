$(document).ready(function() {

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
    // Affirmations popup code starts here - Karthik


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
$( "#strength .rich-text p" ).wrapAll( "<div class='strength-paragraphs' />");
$( "#agility .rich-text p" ).wrapAll( "<div class='agility-paragraphs' />");
$( "#flexibility .rich-text p" ).wrapAll( "<div class='flexibility-paragraphs' />");
$(".strength-paragraphs").insertAfter(".strength-images-array");
$(".agility-paragraphs").insertAfter(".agility-images-array");
$(".flexibility-paragraphs").insertAfter(".flexibility-images-array");


$(".physical-post-page").closest("body").addClass("physical-body");
$( ".physical-post-page br" ).remove();
// $( "h2" ).appendTo( $( ".container" ) )



});