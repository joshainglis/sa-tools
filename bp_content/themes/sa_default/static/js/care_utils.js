/**
 * Created by josha_000 on 10/04/14.
 */

$().ready(function () {
    $("#client_select").change(function () {
        var s = $(this);
        if (s.val() === 'new') {
            $("#client-name_first").val('');
            $("#client-name_last").val('');
            $("#client-dob").val('');
            $("#client-sex").val('male');
            $("#client-contact").val('');
            $("#client-address-unit").val('');
            $("#client-address-address1").val('');
            $("#client-address-address2").val('');
            $("#client-address-suburb").val('');
            $("#client-address-state").val('QLD');
        } else {
            $.ajax({
                type: "POST",
                url: "/get_client_info/",
                contentType: "application/json; charset=utf-8",
                data: JSON.stringify({'record_id': s.val()}),
                dataType: 'json',
                success: function (response) {
                    if (!response.error) {
                        $("#client-name_first").val(response.name_first);
                        $("#client-name_last").val(response.name_last);
                        $("#client-dob").val(response.dob);
                        $("#client-sex").val(response.sex);
                        $("#client-contact").val(response.contact);
                        $("#client-address-unit").val(response.unit);
                        $("#client-address-address1").val(response.address1);
                        $("#client-address-address2").val(response.address2);
                        $("#client-address-suburb").val(response.suburb);
                        $("#client-address-state").val(response.state);
                    } else {
                        console.log("Ajax failed!: Client:" + s.val())
                    }
                }
            });

        }
    });

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
        $("#client-dob").datepicker({
            defaultDate: "-1m",
            changeMonth: true,
            changeYear: true,
            dateFormat: "yy-mm-dd",
            numberOfMonths: 1
        });
        $(".date_start").each(function () {
            $(this).datepicker({
                defaultDate: "-1m",
                changeMonth: true,
                changeYear: true,
                dateFormat: "yy-mm-dd",
                numberOfMonths: 1,
                onClose: function (selectedDate) {
                    $("#" + this.id.substring(0, this.id.length - 5) + "end").datepicker("option", "minDate", selectedDate);
                }
            });
        });
        $(".date_end").each(function () {
            $(this).datepicker({
                defaultDate: "-1d",
                changeMonth: true,
                changeYear: true,
                dateFormat: "yy-mm-dd",
                numberOfMonths: 1,
                onClose: function (selectedDate) {
                    $("#" + this.id.substring(0, this.id.length - 3) + "start").datepicker("option", "maxDate", selectedDate);
                }
            });
        });
    });

    function checkbox_changed(element) {
        var cur_id;
        if (element.id !== 'check-all') {
            if (element.checked) {
                if (!disp.hasOwnProperty(element.id)) {
                    cur_id = element.id;
                    $.ajax({
                        type: "POST",
                        url: "/get_full_product_info/",
                        contentType: "application/json; charset=utf-8",
                        data: JSON.stringify({'record_id': cur_id}),
                        dataType: 'json',
                        success: add_row
                    });
                }
            } else {
                delete_row(element.id);
            }
        }
        event.preventDefault();
    }

});
