const watchlist_wrapper = document.querySelector('.watchlist_wrapper')
const watchlist_products = document.querySelector('.watchlist_products')


function WatchListSwiper() {
    var WatchList = new Swiper('.watchlist', {
        loop: false,
        slidesPerView: 5,
        slidesPerGroup: 1,
        spaceBetween: 2,
        height: 'auto',
        navigation: {
            nextEl: '.watchlist-button-next',
            prevEl: '.watchlist-button-prev',
        },
        breakpoints: {
          0: {
          slidesPerView: 2,
          },
          480: {
          slidesPerView: 2,
          },
          720: {
          slidesPerView: 3,
          },
          1200: {
          slidesPerView: 4,
          },
          1440: {
              slidesPerView: 5,
          }
      }
       
    })
}

function setWatchList(data) {
    html = data['html']
    length = data['length']
    if (length > 0) {
        watchlist_products.innerHTML = html
        watchlist_wrapper.style.display = 'block'
        WatchListSwiper()
    }
    for (let tokenInput of document.querySelectorAll('input[name="csrfmiddlewaretoken"]')) {
        tokenInput.value = csrf
    }
}

XHR('GET', watchlist_url, data={}, setWatchList)