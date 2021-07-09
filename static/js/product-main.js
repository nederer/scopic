window.onload = function (){
    const closeDate = document.getElementById("close-date");
    const countDownDate = new Date(closeDate.innerText).getTime();
    window.setInterval(function() {
        let now = new Date().getTime();
        let timeLeft = countDownDate - now;

        if (timeLeft <= 0){
            document.getElementById("close-date").innerText = "Bidding is closed!";
            document.getElementById("submit-bid").disabled = true;

        } else {

            let days = Math.floor(timeLeft / (1000 * 60 * 60 * 24));
            let hours = Math.floor((timeLeft % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            let minutes = Math.floor((timeLeft % (1000 * 60 * 60)) / (1000 * 60));
            let seconds = Math.floor((timeLeft % (1000 * 60)) / 1000);

            document.getElementById("close-date").innerHTML = days + " Days "
                + hours + " Hours "
                + minutes + " Minutes "
                + seconds + " Seconds";
        }
    }, 1000)

    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
    reloadBidHistory();

    window.setInterval(reloadBidHistory, 10000);
    function reloadBidHistory(){
        const productId = window.location.href.substring(window.location.href.lastIndexOf("/") + 1)
        $.ajax({
            type: "GET",
            url: window.location.origin + "/api/products/"+productId+"/history",
            success: function(data){
                 updateBidHistory(data);
            },
            error: function(data){
                console.log(data);
            },
        });
    }
    function updateBidHistory(bidsHistory){
        let bidsHistoryBlock = document.getElementById("bid-list");
        bidsHistoryBlock.innerHTML = "<thead><th>Username</th><th>Time</th><th>Bid amount</th></thead>";
        if(bidsHistory.length > 0){
            bidsHistory.forEach(elem => {
                bidsHistoryBlock.innerHTML += `<tr><td> ${elem.username} </td><td> ${elem.date} </td><td> ${elem.bid_amount} </td></tr>`
            })

            let inputBid = document.getElementById("input-bid");
            let productBid= document.getElementById("product-bid");

            productBid.innerText = bidsHistory[0].bid_amount;
            inputBid.value = bidsHistory[0].bid_amount + 1;
            inputBid.min = bidsHistory[0].bid_amount + 1;
        }
        else {
            bidsHistoryBlock.innerHTML = "<p> No bids yet </p>"
        }
    }

    const submitBtn = document.getElementById("submit-bid");
    submitBtn.onclick = function (){
        const productId = window.location.href.substring(window.location.href.lastIndexOf("/") + 1)
        const bidAmount = document.getElementById("input-bid").value;
        const autoBid = document.getElementById("auto-bid").value;

        const formData = new FormData();
        formData.append('bid_amount', bidAmount);
        formData.append('product', productId);
        formData.append('auto_bid', autoBid);
        $.ajax({
            type: "POST",
            url: window.location.origin + "/api/products/"+productId,
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrfToken,
            },
            success: function(){
                 reloadBidHistory();
            },
            error: function(data){
                console.log(data);
            },
        });

    }
}
