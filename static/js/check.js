$('.form-check-input').click(function() {

    var $this = $(this),
        qid = $this.data('qid'),
        aid = $this.data('aid');

    if ($(this).is(':checked')){
        action = 'checked';
    } else {
        action = 'not checked';
    }

    $.ajax('/check/', {
        method: 'POST',
        data: {
            action: action,
            qid: qid,
            aid: aid,
        }
    }).done(function(data) {
        console.log("RESPONSE: ", data);
    });
});
