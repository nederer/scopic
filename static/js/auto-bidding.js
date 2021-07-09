window.onload = function (){
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    document.getElementById("change-bid").onclick = function (){
        let newAutoBid = document.getElementById("input-bid").value;

        const formData = new FormData();
        formData.append('max_bids', newAutoBid);
        $.ajax({
            type: "PUT",
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                'X-CSRFToken': csrfToken,
            },
            url: window.location.origin + "/api/user/bids",
            success: function(data){
                 console.log(data);
            },
            error: function(data){
                console.log(data);
            },
        });
    }
}