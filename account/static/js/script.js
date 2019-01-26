
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
});