document.addEventListener('DOMContentLoaded', function() {

    // When compose form is submitted run make post
    document.querySelector('#compose-form').addEventListener('submit', () => make_post());
    
});

function make_post() {

    //Get body of post and submit it to the compose view
    fetch('/compose', {
        method: 'POST',
        body: JSON.stringify({
            body: document.querySelector('#compose-body').value,
        })
    })
    
    //Reload the page to display change
    location.reload()
};
