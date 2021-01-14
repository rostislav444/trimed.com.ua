var addToWishListForm = document.querySelectorAll('.add_to_wishlist, .remove_from_wishlist') 
const side_wishlist = document.querySelector('.side_wishlist')


function WishlistGet(data, show=false) {
    let html =     data['html']
    let length =   data['length']
    let wishlistBody =     document.querySelectorAll('.wishlist__body')
    let quantity = wishlist.querySelector('.quantity')

    for (let body of wishlistBody) {
        body.innerHTML = html 
    }
    
    
    if (show) { 
        if (!curentPage.includes('wishlist')) {
            OpenWishlist() 
        }
       
    }
    if (length > 0) {
        quantity.innerHTML = length
        quantity.classList.add('active')
    } else {
        quantity.classList.remove('active')
        if (length == 0) {
            popupClose()
        }
    }
    
    WishlistInnit()
}

function WishlistInnit() {
    addToWishListForm = document.querySelectorAll('.add_to_wishlist, .remove_from_wishlist') 
    for (let form of addToWishListForm) {
        form.onsubmit = (e) => {
            e.preventDefault()
            let data = serialize(form)
            data.ajax = true
            data = JSON.stringify(data)
            XHR('POST', form.action, data, WishlistGet, params={show : true})
        }
    }
    for (let tokenInput of document.querySelectorAll('input[name="csrfmiddlewaretoken"]')) {
        tokenInput.value = csrf
    }
}

if (userAuthenticated) {
    XHR('GET', wishlist_url, {},  WishlistGet)
}

