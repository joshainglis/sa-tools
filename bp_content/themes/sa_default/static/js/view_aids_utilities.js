/*jslint browser: true*/
/*global $, jQuery, alert*/

/** Put here your Scripts **/

var actuary = {
    "0": {"male": 79.9, 'female': 84.3},
    "1": {'male': 79.3, 'female': 83.5},
    "2": {'male': 78.3, 'female': 82.6},
    "3": {'male': 77.3, 'female': 81.6},
    "4": {'male': 76.3, 'female': 80.6},
    "5": {'male': 75.3, 'female': 79.6},
    "6": {'male': 74.3, 'female': 78.6},
    "7": {'male': 73.3, 'female': 77.6},
    "8": {'male': 72.3, 'female': 76.6},
    "9": {'male': 71.4, 'female': 75.6},
    "10": {'male': 70.4, 'female': 74.6},
    "11": {'male': 69.4, 'female': 73.6},
    "12": {'male': 68.4, 'female': 72.6},
    "13": {'male': 67.4, 'female': 71.6},
    "14": {'male': 66.4, 'female': 70.6},
    "15": {'male': 65.4, 'female': 69.7},
    "16": {'male': 64.4, 'female': 68.7},
    "17": {'male': 63.4, 'female': 67.7},
    "18": {'male': 62.5, 'female': 66.7},
    "19": {'male': 61.5, 'female': 65.7},
    "20": {'male': 60.5, 'female': 64.7},
    "21": {'male': 59.6, 'female': 63.8},
    "22": {'male': 58.6, 'female': 62.8},
    "23": {'male': 57.7, 'female': 61.8},
    "24": {'male': 56.7, 'female': 60.8},
    "25": {'male': 55.7, 'female': 59.8},
    "26": {'male': 54.8, 'female': 58.8},
    "27": {'male': 53.8, 'female': 57.9},
    "28": {'male': 52.8, 'female': 56.9},
    "29": {'male': 51.9, 'female': 55.9},
    "30": {'male': 50.9, 'female': 54.9},
    "31": {'male': 50.0, 'female': 53.9},
    "32": {'male': 49.0, 'female': 52.9},
    "33": {'male': 48.0, 'female': 52.0},
    "34": {'male': 47.1, 'female': 51.0},
    "35": {'male': 46.1, 'female': 50.0},
    "36": {'male': 45.2, 'female': 49.0},
    "37": {'male': 44.2, 'female': 48.1},
    "38": {'male': 43.3, 'female': 47.1},
    "39": {'male': 42.3, 'female': 46.1},
    "40": {'male': 41.4, 'female': 45.2},
    "41": {'male': 40.4, 'female': 44.2},
    "42": {'male': 39.5, 'female': 43.2},
    "43": {'male': 38.6, 'female': 42.3},
    "44": {'male': 37.6, 'female': 41.3},
    "45": {'male': 36.7, 'female': 40.4},
    "46": {'male': 35.8, 'female': 39.4},
    "47": {'male': 34.8, 'female': 38.5},
    "48": {'male': 33.9, 'female': 37.5},
    "49": {'male': 33.0, 'female': 36.6},
    "50": {'male': 32.1, 'female': 35.6},
    "51": {'male': 31.2, 'female': 34.7},
    "52": {'male': 30.3, 'female': 33.8},
    "53": {'male': 29.4, 'female': 32.8},
    "54": {'male': 28.5, 'female': 31.9},
    "55": {'male': 27.6, 'female': 31.0},
    "56": {'male': 26.7, 'female': 30.1},
    "57": {'male': 25.9, 'female': 29.2},
    "58": {'male': 25.0, 'female': 28.2},
    "59": {'male': 24.1, 'female': 27.3},
    "60": {'male': 23.3, 'female': 26.4},
    "61": {'male': 22.4, 'female': 25.5},
    "62": {'male': 21.6, 'female': 24.7},
    "63": {'male': 20.8, 'female': 23.8},
    "64": {'male': 20.0, 'female': 22.9},
    "65": {'male': 19.1, 'female': 22.0},
    "66": {'male': 18.3, 'female': 21.2},
    "67": {'male': 17.6, 'female': 20.3},
    "68": {'male': 16.8, 'female': 19.5},
    "69": {'male': 16.0, 'female': 18.6},
    "70": {'male': 15.3, 'female': 17.8},
    "71": {'male': 14.5, 'female': 17.0},
    "72": {'male': 13.8, 'female': 16.2},
    "73": {'male': 13.1, 'female': 15.4},
    "74": {'male': 12.4, 'female': 14.6},
    "75": {'male': 11.7, 'female': 13.8},
    "76": {'male': 11.0, 'female': 13.1},
    "77": {'male': 10.4, 'female': 12.3},
    "78": {'male': 9.8, 'female': 11.6},
    "79": {'male': 9.2, 'female': 10.9},
    "80": {'male': 8.6, 'female': 10.2},
    "81": {'male': 8.0, 'female': 9.6},
    "82": {'male': 7.5, 'female': 8.9},
    "83": {'male': 7.0, 'female': 8.3},
    "84": {'male': 6.5, 'female': 7.7},
    "85": {'male': 6.1, 'female': 7.2},
    "86": {'male': 5.7, 'female': 6.7},
    "87": {'male': 5.3, 'female': 6.2},
    "88": {'male': 4.9, 'female': 5.7},
    "89": {'male': 4.6, 'female': 5.3},
    "90": {'male': 4.3, 'female': 4.9},
    "91": {'male': 4.0, 'female': 4.5},
    "92": {'male': 3.8, 'female': 4.2},
    "93": {'male': 3.5, 'female': 3.9},
    "94": {'male': 3.3, 'female': 3.6},
    "95": {'male': 3.1, 'female': 3.4},
    "96": {'male': 2.9, 'female': 3.2},
    "97": {'male': 2.7, 'female': 3.0},
    "98": {'male': 2.6, 'female': 2.8},
    "99": {'male': 2.4, 'female': 2.6},
    "100": {'male': 2.3, 'female': 2.5}
};

$(document).ready(function () {
    'use strict';
    var disp, ctable, age, sex;

    disp = {};
    ctable = $('#ctable');
    age = null;
    sex = null;

    function calculate_yearly(inital, maintenance, replacement_freq) {
        if (replacement_freq === 0.0) {
            return maintenance;
        }
        return (inital / replacement_freq) + maintenance;
    }

    function calculate_lifetime(initial, yearly) {
        if (age === null || sex === null) {
            return false;
        }
        return actuary[Math.round(age).toString()][sex] * yearly + initial;
    }

    function recalculate_lifetime() {
        var lt, key, td;
        for (key in disp) {
            if (disp.hasOwnProperty(key)) {
                td = $('#ctable').find('#' + key + ' .table_cost_life');
                td.css("background-color", "#FF3700");
                lt = calculate_lifetime(disp[key].cost,
                    calculate_yearly(
                        disp[key].cost,
                        disp[key].maintenance,
                        disp[key].replacement
                    ));
                td.text(Math.round(lt));
                td.css("background-color", "#FFFFFF");
            }
        }
    }

    $('input[name="sex"]').change(function () {
        sex = this.value;
        recalculate_lifetime();
        return false;
    });

    $('input[name="age"]').change(function () {
        var tmp;
        tmp = parseFloat($('input[name="age"]').val());
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
        if (tmp > 100) {
            tmp = 100;
        }
        age = tmp;
        recalculate_lifetime();
        return false;
    });

    function add_row(response) {
        var yearly, rows, lifetime;
        if (!response.error) {
            disp[response.id] = response;
            yearly = calculate_yearly(
                response.cost,
                response.maintenance,
                response.replacement
            );
            lifetime = calculate_lifetime(response.cost, yearly);
            rows = $(
                '<tr id="' + response.id + '">' +
                    '<td class="table_name">' + response.name + '</td>' +
                    '<td class="table_supplier">' + response.supplier + '</td>' +
                    '<td class="table_cost_init">$' + response.cost + '</td>' +
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
            //noinspection JSLint
            console.log('There was an error retrieving the given record' + response);
        }
    }

    function delete_row(id) {
        var tr;
        delete disp[id];
        tr = $("#ctable #" + id).closest('tr');
        tr.css("background-color", "#FF3700");
        tr.fadeOut(400, function () {
            tr.remove();
        });
    }

    function checkbox_changed(element) {
        var cur_id;
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
        return false;
    }

    $("input[class='checkbox']").change(function () {
        checkbox_changed(this);
    });

    $('#check-all').change(function () {
        var allOn = this.checked;
        $('input[type="checkbox"]').each(function () {
            this.checked = allOn;
            checkbox_changed(this);
        });
    });

    $('#aid_table').dataTable();

});