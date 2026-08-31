const loadingMessage =
    document.getElementById("loading-message");

const errorMessage =
    document.getElementById("error-message");

const postContent =
    document.getElementById("post-content");

const postTitle =
    document.getElementById("post-title");

const postAuthor =
    document.getElementById("post-author");

const postDate =
    document.getElementById("post-date");

const postSummary =
    document.getElementById("post-summary");

const originalLink =
    document.getElementById("original-link");


async function loadPost() {

    try {

        const params =
            new URLSearchParams(window.location.search);

        const postId = params.get("id");


        if (!postId) {
            throw new Error("Post ID is missing");
        }


        const response =
            await fetch(
                `http://localhost:5000/api/posts/${postId}`
            );


        if (!response.ok) {

            if (response.status === 404) {
                throw new Error("Post not found");
            }

            throw new Error("Failed to fetch post");
        }


        const post =
            await response.json();


        displayPost(post);


    } catch (error) {

        console.error(
            "Error loading post:",
            error
        );

        loadingMessage.hidden = true;

        errorMessage.textContent =
            error.message;

        errorMessage.hidden = false;
    }
}


function displayPost(post) {

    loadingMessage.hidden = true;

    postTitle.textContent =
        post.title;

    postAuthor.textContent =
        `By ${post.author}`;

    postDate.textContent =
        new Date(
            post.published_date
        ).toLocaleDateString(
            "en-US",
            {
                year: "numeric",
                month: "long",
                day: "numeric"
            }
        );

    postSummary.textContent =
        post.summary;

    originalLink.href =
        post.url;

    postContent.hidden = false;
}


loadPost();
