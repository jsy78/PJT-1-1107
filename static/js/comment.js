const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

function commentDelete() {
    const commentDeleteForms = document.querySelectorAll('.comment-delete-form')
    commentDeleteForms.forEach((commentDeleteForm) => {
        commentDeleteForm.addEventListener('submit', function (event) {
            event.preventDefault()
            const articleId = event.currentTarget.dataset.articleId
            const commentId = event.currentTarget.dataset.commentId
            axios({
                method: 'POST',
                url: `/articles/${articleId}/comments/${commentId}/delete/`,
                headers: { 'X-CSRFToken': csrftoken }
            })
                .then(response => {
                    const comments = response.data.comments

                    const commentsArea = document.querySelector('#comments-area')

                    while (commentsArea.hasChildNodes()) {
                        commentsArea.removeChild(commentsArea.firstChild)
                    }

                    commentsArea.insertAdjacentHTML('beforeend',
                        `
              <h5>${response.data.comments_count}개의 댓글</h5>
              <hr class="mb-0">
              <ul id="comments-list" class="list-group list-group-flush rounded-2">
              </ul>
              `
                    )
                    const commentsList = document.querySelector('#comments-list')
                    for (let i = 0; i < comments.length; i++) {
                        if (response.data.request_username == comments[i].username) {
                            commentsList.insertAdjacentHTML('beforeend',
                                `
              <li class="list-group-item bg-light px-0">
                <div class="d-flex justify-content-between align-items-center">
                  <a class="card-text m-2 comment-user" href="/accounts/mypage/">${comments[i].username}</a>
                  <p class="card-text text-muted">${comments[i].created_at}</p>
                </div>
                <div class="d-flex justify-content-between m-2">
                  <p>${comments[i].content}</p>
                  <form class="comment-delete-form" data-article-id="${response.data.article_pk}" data-comment-id="${comments[i].pk}">
                    <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                    <button class="btn btn-sm p-0 border-0 text-danger text-decoration-none me-2" type="submit"><i class="bi bi-x-square"></i></button>
                  </form>
                </div>
              </li>
              `
                            )
                        }
                        else {
                            commentsList.insertAdjacentHTML('beforeend',
                                `
              <li class="list-group-item bg-light px-0">
                <div class="d-flex justify-content-between align-items-center">
                  <a class="card-text m-2 comment-user" href="/accounts/profile/${comments[i].username}/">${comments[i].username}</a>
                  <p class="card-text text-muted">${comments[i].created_at}</p>
                </div>
                <div class="d-flex justify-content-between m-2">
                  <p>${comments[i].content}</p>
                </div>
              </li>
              `
                            )
                        }
                    }
                    return commentDeleteForms
                })
                .then(response => {
                    commentDelete()
                })
                .catch(error => {
                    console.log(error.response)
                })
        })
    })
}
function commentCreate() {
    const commentCreateForm = document.querySelector('#comment-create-form')
    commentCreateForm.addEventListener('submit', function (event) {
        event.preventDefault()
        const articleId = event.currentTarget.dataset.articleId
        axios({
            method: 'POST',
            url: `/articles/${articleId}/comments/`,
            headers: { 'X-CSRFToken': csrftoken },
            data: new FormData(commentCreateForm) // 폼에 있는 정보를 data로 넘겨줄 수 있도록 변환
        })
            .then(response => {
                const comments = response.data.comments

                const commentsArea = document.querySelector('#comments-area')

                while (commentsArea.hasChildNodes()) {
                    commentsArea.removeChild(commentsArea.firstChild)
                }

                commentsArea.insertAdjacentHTML('beforeend',
                    `
            <h5>${response.data.comments_count}개의 댓글</h5>
            <hr class="mb-0">
            <ul id="comments-list" class="list-group list-group-flush rounded-2">
            </ul>
            `
                )
                const commentsList = document.querySelector('#comments-list')
                for (let i = 0; i < comments.length; i++) {
                    if (response.data.request_username == comments[i].username) {
                        commentsList.insertAdjacentHTML('beforeend',
                            `
            <li class="list-group-item bg-light px-0">
              <div class="d-flex justify-content-between align-items-center">
                <a class="card-text m-2 comment-user" href="/accounts/mypage/">${comments[i].username}</a>
                <p class="card-text text-muted">${comments[i].created_at}</p>
              </div>
              <div class="d-flex justify-content-between m-2">
                <p>${comments[i].content}</p>
                <form class="comment-delete-form" data-article-id="${response.data.article_pk}" data-comment-id="${comments[i].pk}">
                  <input type="hidden" name="csrfmiddlewaretoken" value="${csrftoken}">
                  <button class="btn btn-sm p-0 border-0 text-danger text-decoration-none me-2" type="submit"><i class="bi bi-x-square"></i></button>
                </form>
              </div>
            </li>
            `
                        )
                    }
                    else {
                        commentsList.insertAdjacentHTML('beforeend',
                            `
            <li class="list-group-item bg-light px-0">
              <div class="d-flex justify-content-between align-items-center">
                <a class="card-text m-2 comment-user" href="/accounts/profile/${comments[i].username}/">${comments[i].username}</a>
                <p class="card-text text-muted">${comments[i].created_at}</p>
              </div>
              <div class="d-flex justify-content-between m-2">
                <p>${comments[i].content}</p>
              </div>
            </li>
            `
                        )
                    }
                }
                commentCreateForm.reset()
                return commentCreateForm
            })
            .then(response => {
                commentDelete()
            })
            .catch(error => {
                console.log(error.response)
            })
    })
}

commentDelete()
commentCreate()