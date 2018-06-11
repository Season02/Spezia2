$(function()
{
    function submit_test_form(e)
    {
        var content_url = $('#content_url').val();
        var content_ruler = $('#content_ruler').val();

//        alert('start')

        $.ajax
        ({
            type: "post",
            dataType: "json",
            url: "/scanTest",
            data:
            {
                content_url: content_url,
                content_ruler: content_ruler
            },
            success: function (msg)
            {
//                alert('ing')
                alert(msg);
                alert(eval(msg))

                var obj = jQuery.parseJSON(msg);

                alert("1"+ obj.author);

                $.each(msg.comments, function(i, item) {
                  $("#display").append(
                      "<div>" + item.id + "</div>" +
                      "<div>" + item.nickname  + "</div>" +
                      "<div>" + item.content + "</div><hr/>");
                });

                var str = "";
                var data = msg;

                $("#display").text('123');

            },
            error: function ()
            {
                alert("测试失败")
            }
        });

    };
    // 绑定click事件
    $('#calculate').bind('click', submit_test_form);
});