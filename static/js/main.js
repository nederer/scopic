window.onload = function (){
    setCurrentParams();
    function setCurrentParams(){
        setOrdering();
        setSearchText();
    }

    window.setInterval(reloadBids, 10000);
    function reloadBids(){
        const idList = getProductsId();
        $.ajax({
            type: "GET",
            url: window.location.origin + "/api/products?ids=" + idList.toString(),
            success: function(data){
                 updateBids(data);
            },
            error: function(data){
                console.log(data);
            },
        });
    }
    function getProductsId(){
        let idList = Array();
        let productPrices = document.getElementsByClassName("current-bid");
        for(let i=0; i<productPrices.length; i++){
            let productId = productPrices[i].id;
            idList.push(productId.replace("product-", ""));
        }
        return idList
    }
    function updateBids(productsInfo){
        productsInfo.forEach(elem => {
            let bidId = "product-" + elem.id;
            let productPidElem = document.getElementById(bidId);
            productPidElem.innerText = elem.current_bid;
            productPidElem.parentElement.classList.add("blue");
            setTimeout(function(){
                productPidElem.parentElement.classList.remove("blue");
            },500);
        })
    }

    let paginators = document.getElementsByClassName("page-link");
    for (let i=0; i<paginators.length; i++) {
        paginators[i].addEventListener('click', paginate,false);
    }
    function paginate(){
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        urlParams.set("page", this.name);
        window.location.href = "?" + urlParams.toString();
    }

    const searchBtn = document.getElementById("search-btn");
    const searchInput = document.getElementById("search-text");
    searchInput.addEventListener("keydown", function(event) {
        if (event.key === "Enter") {
            searchProducts();
        }
    });
    searchBtn.addEventListener("click", searchProducts);
    function searchProducts(){
        let searchText = document.getElementById("search-text");

        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        urlParams.set("search", searchText.value);
        urlParams.set("page", "1")
        window.location.href = "?" + urlParams.toString();
    }

    const orderings = document.getElementById("ordering-dropdown");
    orderings.onchange = function (){
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);

        urlParams.set("ordering", orderings.value);
        window.location.href = "?" + urlParams.toString();
    }

    function setOrdering(){
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const searchText = document.getElementById("search-text");

        if (urlParams.get("search")){
            searchText.value = urlParams.get("search");
        }
    }
    function setSearchText(){
        const queryString = window.location.search;
        const urlParams = new URLSearchParams(queryString);
        const orderings = document.getElementById("ordering-dropdown");

        if (urlParams.get("ordering")){
            orderings.value = urlParams.get("ordering");
        }
    }
}
