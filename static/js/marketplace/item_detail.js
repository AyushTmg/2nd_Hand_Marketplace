document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('show-comments').addEventListener('click', function () {
        var commentsContainer = document.getElementById('comments-container');
        commentsContainer.style.display = (commentsContainer.style.display === 'none') ? 'block' : 'none';
    });
});