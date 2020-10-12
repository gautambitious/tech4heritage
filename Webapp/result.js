console.log("bruh");
function yes_bruh() {
    fetch('http://127.0.0.1:6968/feedback/yes', {
        method: 'post',
    }).then(res=>  feedback_submit());
};
function no_bruh() {
    fetch('http://127.0.0.1:6968/feedback/no', {
        method: 'post'
    }).then(res=>  feedback_submit());
}

function feedback_submit(){
    $("#feedback").hide();
    alert("Thanks for your feedback");
};
