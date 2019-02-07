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



    //Registration breadcrumb issue fix
    if ($(".registration-dashboard").length == 0) {
        $(".step.step-1").addClass("done");
    } else {
        $(".step.step-1").removeClass("done");
        $(".step.step-1").addClass("active");
    }
});