document.addEventListener('DOMContentLoaded', function() {
    document.querySelector('#likepost').addEventListener('click', () => like());
    document.querySelector('#follow').addEventListener('click', () => follow);
});

function like() {
    const likepost = document.querySelector('#likepost');
    const id = likepost.dataset.id;
    const like = likepost.dataset.like;
    fetch('/like', {
        method: 'PUT',
        body: JSON.stringify({
            like: like,
            id: id
        })
    })
    .then(response => response.json())
    .then(data => {
        const likes = String(data.data);
        document.querySelector('#postlikes').innerHTML = `${likes}`;
    })
}

function follow() {
    const followuser = document.querySelector('#follow');
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
    })
}