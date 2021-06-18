$('.js-vote').click(function(ev) {
    ev.preventDefault();

    var $this = $(this),
        action = $this.data('action'),
        qid = $this.data('qid'),
        type = $this.data('type');

    var inc;
    if (action == "like") {
        inc = 1;
    } else {
        inc = -1;
    }

    var rating_label = $('[class = rating-score][data-qid = '+qid+']');
    var a = Number(rating_label.text()) + inc;
    rating_label.text(a);

    $('[data-action = '+action+'][data-qid = '+qid+']').fadeOut();
    $('[data-action != '+action+'][data-qid = '+qid+']').fadeIn();
    

    $.ajax('/vote/', {
        method: 'POST',
        data: {
            action: action,
            qid: qid,
            type: type
        }
    }).done(function(data) {
        console.log("RESPONSE: ", data);
    });
}); 
