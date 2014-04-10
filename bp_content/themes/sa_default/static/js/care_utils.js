/**
 * Created by josha_000 on 10/04/14.
 */

$().ready(function () {
    $("#form_add_care").validate({
        errorPlacement: function (error, element) {
            element.parent().parent().addClass("error");
            error.addClass("help-inline").appendTo(element.parent());
        }
    });

    $(".supplier-input").change(function (o) {
        $("#" + o.id).parent().prev().children().first().html(o.html())
    });

    $(".care-type-other").on('input', function (o) {
        var otid = o.target.id;
        var ot = $("#" + otid);
        var s = $("#" + otid.substring(0, otid.length - 6));
        var v = ot.val();
        s.val('other');
        ot.parents().eq(6).children().eq(0).children().html(v);
    });

    $(".care-type-selector").change(function (o) {
        var s = $("#" + o.target.id);
        var ot = $("#" + o.target.id + "_other");
        var v = s.val();
        ot.val(v);
        s.parents().eq(6).children().eq(0).children().html(v);
    });

    $(function () {
        $(".date_start").each(function () {
            $(this).datepicker({
                defaultDate: "-1y",
                changeMonth: true,
                numberOfMonths: 3,
                onClose: function (selectedDate) {
                    $("#" + this.id.substring(0, this.id.length-5) + "end").datepicker("option", "minDate", selectedDate);
                }
            });
        });
        $(".date_end").each(function () {
            $(this).datepicker({
                defaultDate: "-1y",
                changeMonth: true,
                numberOfMonths: 3,
                onClose: function (selectedDate) {
                    $("#" + this.id.substring(0, this.id.length-3) + "start").datepicker("option", "maxDate", selectedDate);
                }
            });
        });
    });

});
