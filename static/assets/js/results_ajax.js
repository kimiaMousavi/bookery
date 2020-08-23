$(function () {
    $("#submit").click(sent_mark);

});

function sent_mark() {
    var status;
    var id;


    status =  $("#staus").val().toString();
    id =  $("#id").val().toString();

    $.ajax
    ({
        type: "PUT",
        url: "http://127.0.0.1:8000/add_bookmark/",
        data: JSON.stringify({
                    status : status,
                    id :id,

                }),
     });
}
