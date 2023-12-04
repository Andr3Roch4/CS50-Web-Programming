document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.likepost').forEach(likepost => {
        likepost.addEventListener('click', function() {
            like(this.id);
        });          
    });
    document.querySelectorAll('.edit').forEach(button => {
        button.addEventListener('click', function() {
            edit(this.id)
        });
    });
    document.querySelector('#follow').addEventListener('click', function() {
        follow();
    });
});

function like(id) {
    let post = document.getElementById(id)
    const postid = post.dataset.id;
    let like = post.dataset.like;
    fetch('/like', {
        method: 'PUT',
        body: JSON.stringify({
            like: like,
            id: postid
        })
    })
    .then(response => response.json())
    .then(data => {
        let likes = data.data;
        let liked = data.liked;
        let postlikes = document.querySelector(`#postlikes${postid}`)
        postlikes.innerHTML = `${likes}`;
        if (liked === false) {
            post.innerHTML = '&#x1F90D;';
            post.appendChild(postlikes);
            post.dataset.like = '1';
        } else {
            post.innerHTML = '&#x1F9E1;';
            post.appendChild(postlikes);
            post.dataset.like = '-1';
        };
    })
}

function follow() {
    let followuser = document.querySelector('#follow');
    const id = followuser.dataset.id;
    fetch('/following', {
        method: 'PUT',
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(data => {
        const message = data.message;
        document.querySelector('#response').innerHTML = `${message}`;
        followuser.innerHTML = `${data.follow}`;
    })
}

function edit(id) {
    const edit_button = document.getElementById(id);
    const submitedit_button = document.createElement('button');
    edit_button.parentNode.replaceChild(submitedit_button, edit_button);
    submitedit_button.innerHTML = 'Submit Edit';
    const postid = edit_button.dataset.id;
    const edit_content = document.getElementById(`content${postid}`);
    const textarea = document.createElement('textarea');
    textarea.innerHTML = edit_content.innerHTML;
    textarea.id = 'newcontent';
    edit_content.parentNode.replaceChild(textarea, edit_content);
    submitedit_button.addEventListener('click', function() {
        let newcontent = document.getElementById('newcontent').value;
        fetch('/allposts', {
            method: 'POST',
            body: JSON.stringify({
                newcontent: newcontent,
                postid: postid
            })
        })
        .then(response => response.json())
        .then(data => {
            const content = data.newcontent;
            submitedit_button.parentNode.replaceChild(edit_button, submitedit_button);
            edit_content.innerHTML = `${content}`;
            textarea.parentNode.replaceChild(edit_content, textarea);
        })
    })
}