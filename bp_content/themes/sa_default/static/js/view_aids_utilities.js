$(document).ready(function () {
    var disp = {};
    var ctable = $('#ctable');
    var age = null;
    var sex = null;

    $('input[name="sex"]').change(function () {
        sex = this.value;
        recalculate_lifetime();
        return false;
    });

    $('input[name="age"]').change(function () {
        var tmp = parseFloat($('input[name="age"]').val());
        if (isNaN(tmp)) {
            alert("Please enter a number for age");
            age = null;
            return false;
        }
        if (tmp < 0) {
            alert("Please enter a positive number for age");
            age = null;
            return false;
        }
        if (tmp > 100) tmp = 100;
        age = tmp;
        recalculate_lifetime();
        return false;
    });

    function calculate_yearly(inital, maintenance, replacement_freq) {
        if (replacement_freq === 0.0) {
            return maintenance;
        }
        return (inital / replacement_freq) + maintenance
    }

    function calculate_lifetime(initial, yearly) {
        if (age === null || sex === null) return false;
        return actuary[Math.round(age).toString()][sex] * yearly + initial;
    }

    function recalculate_lifetime() {
        var lt;
        for (var key in disp) {
            if (disp.hasOwnProperty(key)) {
                var td = $('#ctable').find('#' + key + ' .table_cost_life');
                td.css("background-color", "#FF3700");
                lt = calculate_lifetime(disp[key]['cost'],
                    calculate_yearly(
                        disp[key]['cost'],
                        disp[key]['maintenance'],
                        disp[key]['replacement']
                    ));
                td.text(Math.round(lt));
                td.css("background-color", "#FFFFFF");
            }
        }
    }

    $("input[class='checkbox']").change(function () {
        if (this.checked) {
            if (!(this.id in disp)) {
                var cur_id = this.id;
                $.ajax({
                    type: "POST",
                    url: "/get_full_product_info/",
                    contentType: "application/json; charset=utf-8",
                    data: JSON.stringify({'record_id': cur_id}),
                    dataType: 'json',
                    success: function (response) {
                        console.log(response);
                        if (!response['error']) {
                            disp[response.id] = response;
                            var yearly = calculate_yearly(
                                response['cost'],
                                response['maintenance'],
                                response['replacement']
                            );
                            var lifetime = calculate_lifetime(response['cost'], yearly);
                            var rows = $(
                                '<tr id="' + response['id'] + '">' +
                                    '<td class="table_name">' + response['name'] + '</td>' +
                                    '<td class="table_supplier">' + response['supplier'] + '</td>' +
                                    '<td class="table_cost_init">$' + response['cost'] + '</td>' +
                                    '<td class="table_cost_yrly">$' + Math.round(yearly) + '</td>' +
                                    '<td class="table_cost_life">$' + Math.round(lifetime) + '</td>' +
                                    '</tr>'
                            );
                            rows.hide();
                            rows.css('background-color', "#37FF00");
                            ctable.find('tbody:last').append(rows);
                            rows.fadeIn(400, function () {
                                rows.css("background-color", "#FFFFFF");
                            });
                        } else {
                            console.log('There was an error retrieving the given record' + response)
                        }
                    }
                })
            }
        } else {
            delete disp[this.id];
            var tr = $("#ctable #" + this.id).closest('tr');
            tr.css("background-color", "#FF3700");
            tr.fadeOut(400, function () {
                tr.remove();
            });
        }
        return false;
    });
});