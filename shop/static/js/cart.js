var updateButtons = document.getElementsByClassName('update-cart')

for( var i = 0; i < updateButtons.length; i++)
{
    updateButtons[i].addEventListener('click', function(){
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'action:', action)
        
        console.log('User:', user)
        if(user != "AnonymousUser")
            updateCart(productId, action)
        else
            console.log("User is not authenticated.")
    })
}

function updateCart(productId, action){
    // console.log("User is authenticated.")

    var url = '/update_item/'
    console.log('URL:', url)

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response) => {
        return response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()  /* refresh the page */
    })
}

