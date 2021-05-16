// Upon page load
document.addEventListener('DOMContentLoaded', () => {

    // Retrieve view data passed in from server through template
    const data = JSON.parse(document.querySelector('#data').textContent);
    
    // Display header
    headings(data);

    // Show/hide option to add or edit profile details
    show_hide_profile_details(data);

})

// Display appropriate header based on view
function headings(data) {
    if (data.view === 'index') {
        document.querySelector('#profile-header').style.display = 'none';
        document.querySelector('#follows-header').style.display = 'none';
        document.querySelector('#directory').style.display = 'none';
    }
    else if (data.view === 'follows') {
        document.querySelector('#profile-header').style.display = 'none';
        document.querySelector('#follows-header').style.display = 'block';
        document.querySelector('#directory').style.display = 'none';
    }
    else if (data.view === 'profile') {
        document.querySelector('#profile-header').style.display = 'block';
        document.querySelector('#follows-header').style.display = 'none';
        document.querySelector('#directory').style.display = 'none';
        follow(data);
    }
    else if (data.view === 'directory') {
        document.querySelector('#profile-header').style.display = 'none';
        document.querySelector('#follows-header').style.display = 'none';
        document.querySelector('#feed').style.display = 'none';
        document.querySelector('#directory').style.display = 'block';
        document.querySelector('#paginator').style.display = "none";
    }
}

// Next three functions cover the mechanics of adding a profile picture
function add_profile_picture() {
    event.preventDefault();
    document.querySelector('#profile-pic-form').style.display = "block";
}

function submit_pic() {
    event.preventDefault();
    document.querySelector('#profile-pic-form').submit();
}

function cancel_pic() {
    event.preventDefault();
    document.querySelector('#profile-pic-form').style.display = "none";
}

// Animation for displaying profile details (personal info, education, get-to-know)
// Increases profile details div height, hides "show more" button, displays "show less button"
// If viewing own profile, also displays "add or edit details" button
function show_more(show_more_button) {
    let profile_details_div = document.querySelector('#profile-details');
    let show_less_button = document.querySelector('#show-less-button');
    let add_or_edit_details_button = document.querySelector('#add-or-edit-details');
    profile_details_div.style.height = "200px";
    show_more_button.style.display = "none";
    show_less_button.style.display = "inline-block";
    add_or_edit_details_button.style.display = "inline-block";
}

// Animation for hiding profile details (personal info, education, get-to-know)
// Brings profile details div height to zero, shows "show more" button, hides "show less button"
// If viewing own profile, also hides "add or edit details" and "save changes" buttons and, 
// if visible, hides "add or edit details" div
function show_less(show_less_button) {
    let profile_details_div = document.querySelector('#profile-details');
    let show_more_button = document.querySelector('#show-more-button');
    let add_or_edit_details_button = document.querySelector('#add-or-edit-details');
    let add_or_edit_details_div = document.querySelector('#add-or-edit-profile-details');
    let save_details_changes_button = document.querySelector('#save-details-changes');
    profile_details_div.style.display = "inline-flex";
    profile_details_div.style.height = "0";
    show_less_button.style.display = "none";
    show_more_button.style.display = "inline-block";
    add_or_edit_details_button.style.display = "none";
    add_or_edit_details_div.style.display = "none";
    save_details_changes_button.style.display = "none";
}

// Limiting access to "add profile details" to profile owner
function show_hide_profile_details(data) {

    // If not logged in or not viewing own profile, no adding or editing progile details
    if ((data.user_id !== data.profile_id) || (!data.is_authenticated)) {
        document.querySelector('#add-or-edit-details').style.display = 'none';
    }
}

// Upon clicking "add or edit details" button, hide profile details div and display
// form version of it, pre-filled with current data; hide "add or edit details" button
// and show "save changes" button instead
function add_or_edit_details() {
    let profile_details_div = document.querySelector('#profile-details');
    let add_or_edit_details_div = document.querySelector('#add-or-edit-profile-details');
    let add_or_edit_details_button = document.querySelector('#add-or-edit-details');
    let save_details_changes_button = document.querySelector('#save-details-changes');
    profile_details_div.style.display = "none";
    add_or_edit_details_div.style.display = "inline-flex";
    add_or_edit_details_button.style.display = "none";
    save_details_changes_button.style.display = "inline-block";
}

// 
function save_changes() {
    document.querySelector('#profile-details-form').submit();
}

// Mechanics for following and unfollowing users
function follow(data) {

    // If not logged in or viewing own profile, no following or unfollowing
    if ((data.user_id === data.profile_id) || (!data.is_authenticated)) {
        document.querySelector('#follow-button').style.display = 'none';
        document.querySelector('#unfollow-button').style.display = 'none';
    }
    // else if logged in and following, only show option to unfollow
    else if (data.is_following) {
        document.querySelector('#follow-button').style.display = 'none';
    }
    // else (if logged in and not following), only show option to follow
    else {
        document.querySelector('#unfollow-button').style.display = 'none';
    }

    // Upon clicking to follow, make PUT request to add to user's follows
    document.querySelector('#follow-button').addEventListener('click', () => {
        fetch(`/profile/${data.profile_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                follow: true
            })
        });

        // Hide option to follow and show option to unfollow instead
        document.querySelector('#follow-button').style.display = 'none';
        document.querySelector('#unfollow-button').style.display = 'block';
    });

    // Upon clicking to unfollow, make PUT request to remove from user's follows
    document.querySelector('#unfollow-button').addEventListener('click', () => {
        fetch(`/profile/${data.profile_id}`, {
            method: 'PUT',
            body: JSON.stringify({
                follow: false
            })
        });

        // Hide option to unfollow and show option to follow instead
        document.querySelector('#follow-button').style.display = 'block';
        document.querySelector('#unfollow-button').style.display = 'none';
    });
}

// Mechanics for liking and unliking posts
async function like_dislike(post) {

    // Upon clicking like/dislike button, check like status of all posts
    let user_likes_string = await fetch('../likes')
    .then(response => response.json());
    const user_likes = JSON.parse(user_likes_string);

    // If this post is in user's likes, make PUT request to remove it,
    // change button to "Like" 
    if (user_likes.includes(parseInt(post.dataset.id))) {
        fetch('../likes', {
            method: 'PUT',
            body: JSON.stringify({
                post_id: post.dataset.id,
                like: false
            })
        });
        post.innerHTML = "Like";
    }
    // Otherwise, if post is not in user's likes, make PUT request to add it,
    // change button to "Unlike"
    else {
        fetch('../likes', {
            method: 'PUT',
            body: JSON.stringify({
                post_id: post.dataset.id,
                like: true
            })
        });
        post.innerHTML = "Unlike";
    }
}
