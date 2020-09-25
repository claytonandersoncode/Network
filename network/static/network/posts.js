document.addEventListener('DOMContentLoaded', function() {

  //Add function handler to like buttons
  document.querySelectorAll('#like-button').forEach(like => {
    like.onclick = function() {
      like_post(like.dataset.id);
    }      
  });

  //Add function handler to edit buttons
  document.querySelectorAll('#edit-button').forEach(edit => {
    edit.onclick = function() {
      show_edit(edit.dataset.id);
    }      
  });

});

function like_post(id) {
    
    // Send like 
    fetch('/like', {
        method: 'POST',
        body: id
      })
      .then(response => response.json())
      .then(result => {

        //Display the updated total like count
        document.querySelector(`#like-count-${id}`).innerHTML = result.total_likes;
        
        //Display updated like without page load, use views after page load
        if (result.is_liked === true) {
          document.querySelector(`#like-look-${id}`).innerHTML = "favorite"
        } else {
          document.querySelector(`#like-look-${id}`).innerHTML = "favorite_outline"
        }

    });
};

function show_edit(id) {

  //Hide the edit buttons for the other objects while editing is taking place
  const elems = document.querySelectorAll('#edit-button');
  for (let i=0;i<elems.length;i+=1){
    elems[i].style.display = 'none';
  }
  
  //Get the contents of the post before editing
  const body = document.querySelector(`#post-body-${id}`).innerHTML; 

  //Display an editable area and include the contents from above 
  document.querySelector(`#edit-area-${id}`).innerHTML = 
  `<form id="edit-form-${id}" onsubmit="return false">
    <div class="form-group">
    <textarea id="post-body-${id}" class="form-control">${body}</textarea>            
    </div>
    <button type="submit" class="btn btn-primary btn-sm">Save</button>
  </form>`;
  document.querySelector(`#edit-form-${id}`).addEventListener('submit', () => make_edit(id));
  
} 

function make_edit(id) {

  //Get the new value of the body after editing
  const edited = document.querySelector(`#post-body-${id}`).value
  
  //Send edit
  fetch('/edit', {
    method: 'POST',
    body: JSON.stringify({
        id: id,
        body: edited,
    })
  })
  
  //Update the post with the new edited information, wihout reloading
  document.querySelector(`#edit-area-${id}`).innerHTML = `<p id="post-body-${id}}">${edited}</p>`;
  
  // Unhide all the edit buttons once the edit is made
  const elems = document.querySelectorAll('#edit-button');
  for (let i=0;i<elems.length;i+=1){
    elems[i].style.display = 'block';
  }

}