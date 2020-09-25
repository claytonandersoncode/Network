document.addEventListener('DOMContentLoaded', function() {

    //Add function handler to follow button
    document.querySelectorAll('#follow-button').forEach(follow => {
      follow.onclick = function() {
        follow_unfollow(follow.dataset.id);
      }      
    });
  
  });



function follow_unfollow(id) {
    
    // Send follow id
    fetch('/follow', {
        method: 'POST',
        body: id
      })
      .then(response => response.json())
      .then(result => {
        
        //Display updated followers count
        document.querySelector(`#followers`).innerHTML = result.total_follows;
        
        //Display updated follow button without page load, use views after page load
        if (result.is_followed === true) {
            document.querySelector(`#follow-button`).innerHTML = "Unfollow"
        } else {
            document.querySelector(`#follow-button`).innerHTML = "Follow"
        }
    });
  }