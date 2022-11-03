// (1) 좋아요 버튼
const likeBtn = document.querySelector('#like-btn')
// (2) 좋아요 버튼을 클릭하면, 함수 실행
likeBtn.addEventListener('click', function (event) {
    // 서버로 비동기 요청을 하고 싶음
    console.log(event.target.dataset)
    axios({
        method: 'get',
        url: `/articles/${event.target.dataset.articleId}/like/`
    })
        .then(response => {
            console.log(response)
            console.log(response.data)
            // event.target.classList.toggle('bi-heart')
            // event.target.classList.toggle('bi-heart-fill')
            if (response.data.isLiked === true) {
                event.target.classList.add('bi-heart-fill')
                event.target.classList.remove('bi-heart')
            } else {
                event.target.classList.add('bi-heart')
                event.target.classList.remove('bi-heart-fill')
            }
            const likeCount = document.querySelector('#like-count')
            likeCount.innerText = response.data.likeCount
        })
})