let updateBtns = document.getElementsByClassName("update-cart")
for (let i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener("click", function(){
        let productId = this.dataset.product;
        let action = this.dataset.action;
        console.log(productId + " : " + action);

        console.log("USER:" + user);
        if(user == "AnonymousUser"){
            // console.log("User is not authenticated");
            addCookieItem(productId, action);
        }
        else{
            updateUserOrder(productId, action);
        }
    });
}

function addCookieItem(productId, action){
    console.log("User is not authenticated");
    if(action == "add"){
        if(cart[productId] == undefined){
            cart[productId] = {"quantity": 1};
        }
        else{
            cart[productId]["quantity"] += 1; 
        }
    }
    if(action == "remove"){
        cart[productId]["quantity"] -= 1;
        if(cart[productId]["quantity"] <= 0){
            delete cart[productId]
        }
    }
    console.log(cart);
    document.cookie = "cart=" + JSON.stringify(cart) + ";domain=;path=/"
    location.reload();
}

function updateUserOrder(productId, action){
    console.log("User is authenticated, sending data...");
    let url = "/update_item"
    fetch(url, {
        method: "POST",
        headers: {
            "content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({"productId": productId, "action": action})
    })
    .then((response) => {
        return response.json();
    })
    .then((data) => {
        console.log("Data: " + data);
        location.reload();
    })
}