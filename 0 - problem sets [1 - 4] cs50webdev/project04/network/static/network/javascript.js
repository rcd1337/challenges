document.addEventListener("DOMContentLoaded", function() {
    const likes = document.querySelectorAll(".likes");
    likes.forEach(function(likes) {
        fetch(`/is_liked/${likes.id}`)
        .then(response => response.json())
        .then(data => {
            if (data.is_liked === true) {
                const like_button = document.querySelector(`.like-btn_${likes.id}`);
                like_button.value = '♥';
                like_button.style.color = "red";
            }
        })
    })
});

// Handles edit() Cancel button
function cancel(content, id) {
    const post = document.querySelector(`#content_${id}`);
    post.innerHTML = `${content}`
    document.querySelector(`.edit-btn_${id}`).style.display = 'inline-block';
}

// Handles edit() Confirm button
function confirm(id) {
    const new_content = (document.getElementById('edited_post').value)
    fetch(`/edit_post/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: new_content
        })
    })
    .then(function() {
        fetch(`/edit_post/${id}`)
        .then(response => response.json())
        .then(data => {
            const post_content = document.querySelector(`#content_${id}`);
            post_content.innerHTML = data.content;
            document.querySelector(`.edit-btn_${id}`).style.display = 'inline-block';
        });
    });
}


function edit(id) {
    document.querySelector(`.edit-btn_${id}`).style.display = 'none';

    fetch(`/edit_post/${id}`)
    .then(response => response.json())
    .then(data => {
    const post = document.querySelector(`#content_${id}`);
    post.innerHTML = `
        <div class="edit_post">
            <textarea class="txt_container" id="edited_post" name="edit_post" rows="6" cols="69">${data.content}</textarea>
        </div>
        <div>
            <input type="button" onclick="cancel('${data.content}', ${id})" value="Cancel">
            <input type="button" onclick="confirm(${id})" value="Confirm">
        </div>
    `
    });
}


function follow(id) {
    fetch(`/follow/${id}`, {method: 'POST'})
    .then(response => response.json())
    .then(data => {
        const follow_button = document.querySelector(".follow-btn");
        const followers_number = document.querySelector(".followers-number");
        if (data.was_following === true) {
            follow_button.value = "Follow";
            followers_number.innerHTML = `${data.followers}`;
        }
        if (data.was_following === false) {
            follow_button.value = "Unfollow";
            followers_number.innerHTML = `${data.followers}`;
        }
    });
}


function like(id) {
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then(data => {
        const like_button = document.querySelector(`.like-btn_${id}`);
        const likes = document.querySelector(`div.likes-received_${id} > span`);
        if (data.was_liked === true) {
            like_button.value = '♡';
            like_button.style.color = "rgb(59, 59, 59)";
            likes.innerHTML = `${data.likes}`
        }
        if (data.was_liked === false) {
            like_button.value = '♥';
            like_button.style.color = "red";
            likes.innerHTML = `${data.likes}`
        }
    });
}