
$( document ).ready(function() {

    // Affirmations popup code starts here - Karthik
                    if($("#userLandingContent1").length == 0) {
                        //Not the user-landing page
                    } else { 
                        if (!sessionStorage.alreadyClicked) { 
                                $('#exampleModalCenter').modal('show');
                                $( ".modal-title .navbar-brand" ).animate({ "left": "0" }, "slow" );
                                sessionStorage.alreadyClicked = "true";
                        } else{
                                return false;
                        }
                    }
                    $('.logout-button').click(function () {
                        window.sessionStorage.clear();
                    })
                    // Affirmations popup code starts here - Karthik


    //Registration breadcrumb issue fix
    if($(".registration-dashboard").length == 0){
        $(".step.step-1").addClass( "done" );
    }else{
        $(".step.step-1").removeClass( "done" );
        $(".step.step-1").addClass( "active" );
    }

        
//Wrapping the image in a div
$( ".physical-post-page .rich-text img" ).wrapAll( "<div class='rich-text-images' />");
$( ".physical-post-page .rich-text p" ).wrapAll( "<div class='rich-text-paragraphs' />");

});