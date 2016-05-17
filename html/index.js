/*
 * author: winton
 */

var STAT = null;

$(document).on('click', '#btn-start', function(e) {
    $('.select-view').html('<p>请稍后...</p>');
    $.ajax({
        url: '/app/parsexlsx?hasTitle=true&type=gradestat',
        type: 'POST',
        cache: false,
        data: new FormData($('#uploadForm')[0]),
        processData: false,
        contentType: false,
        dataType: 'json',
    }).done(function(res) {
        STAT = res.stat;
        drawDiscription();
    });
});

function drawDiscription() {
    var $view = $('.select-view').empty();
    $view.append('<p>请选择课程</p>');
    var $sel = $('<select></select>').appendTo($view);
    for (var cid in STAT) {
        cItem = STAT[cid];
        $sel.append('<option value="' + cid + '">' + cItem.name + '</option>');
    }
    $sel.change(function() {
        var cid = $(this).val();
        var cItem = STAT[cid];

        var formatedData = [];
        n = 10;
        for (var i = 0; i <= n; i++) {
            formatedData[i] = 0;
        }
        for (var i in cItem['grade']) {
            var grade = cItem['grade'][i];
            if (isNaN(grade))
                continue;
            var index = parseInt(grade * n / 100);
            formatedData[parseInt(grade * n / 100)] += 1;
        }

        // 绘图
        $('.charts-view').highcharts({
            chart: {type: 'areaspline'},
            title: {text: cItem.name + ' 成绩分布'},
            xAxis: {
                labels: {
                    formatter: function() {
                        return 10 * this.value;
                    }
                }
            },
            tooltip: {
                formatter: function() {
                    return '人数:' + this.point.y + '<br/> 分数段:' + this.point.x * 10 + '~' + (this.point.x + 1) * 10 ;
                }
            },
            yAxis: {title: {text: '人数'}},
            series: [{
                name: cItem.name,
                data: formatedData,
            }]
        });
    });
}

