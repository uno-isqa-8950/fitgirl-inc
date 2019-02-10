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
    // Affirmations popup code ends here - Karthik



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

//var timer_demo= $(".physical-post-page").children(".demo");
// $(".demo").insertAfter( ".rich-text" )






// var phyiscaltimer = function(){
// $('.drawer').slideDrawer({
// showDrawer: false, // The drawer is hidden by default.
// slideTimeout: true, // Sets the drawer to slide down after set count if set to true.
// slideSpeed: 600, // Slide drawer speed. 
// slideTimeoutCount: 3000, // How long to wait before sliding drawer slides down.
// });
// };
// Code for toggling the timer
// var r = $("<input/>").attr({ type: "a", id: "field", class:" start-timer btn btn-sm btn-pink btn-rounded waves-effect waves-light",value:"start timer",href:"#"});
// $(".strength-paragraphs").append(r);
// $(".physical-post-page").on('click', '.start-timer', function(){
// //  $(".demo").slideToggle();
// $(".demo").css("visibility","visible");
// //$('#done').show();

// });
// function activityDone(){
//     alert("done");
// }
});

  