const uid = $('#uid').text();
console.log('generate uid', uid);
//底部扩展键
$(function () {
    $('#doc-dropdown-js').dropdown({justify: '#doc-dropdown-justify-js'});
    $(".office_text").panel({iWheelStep: 32});
});

//tab for three icon	
$(document).ready(function () {
    $(".sidestrip_icon a").click(function () {
        $(".sidestrip_icon a").eq($(this).index()).addClass("cur").siblings().removeClass('cur');
        $(".middle").hide().eq($(this).index()).show();
    });
});

//input box focus
$(document).ready(function () {
    $("#input_box").focus(function () {
        $('.windows_input').css('background', '#fff');
        $('#input_box').css('background', '#fff');
    });
    $("#input_box").blur(function () {
        $('.windows_input').css('background', '');
        $('#input_box').css('background', '');
    });
});

window.onload = function b() {
    var text = document.getElementById('input_box');
    var chat = document.getElementById('chatbox');
    var btn = document.getElementById('send');
    var talk = document.getElementById('talkbox');

    btn.onclick = function () {
        if (text.value == '') {
            alert('不能发送空消息');
        } else {
            chat.innerHTML += '<li class="me"><img src="' + '../images/own_head.jpg' + '"><span>' + text.value + '</span></li>';
            text.value = '';
            chat.scrollTop = chat.scrollHeight;
            talk.style.background = "#fff";
            text.style.background = "#fff";
        }
    };
};

function changeTab(iid, did) {
    $('.tab').removeClass('cur');
    $('#' + iid).addClass('cur');
    $('.middle').removeClass('on');
    $('#' + did).addClass('on');
}

let is_sex_loaded = false;
let is_avatar_loaded = false;
let is_word_cloud_loaded = false;
let is_location_loaded = false;
//个人信息
let self = {};

//加载个人信息
function load_self_info() {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/self/' + uid,
        beforeSend: function (xhr) {
            console.log('before send');
        },
        success: function (result, status, xhr) {
            success = result['success'];
            data = result['data'];
            console.log('success', success, data);
            self = data;
            fill_self_info();
        },
        error: function (xhr, status, error) {
            console.log('error', status, error, xhr)
        },
        complete: function (xhr, status) {
            console.log('complete', status, xhr);
        }
    })
}

//填充个人信息
function fill_self_info() {
    $('#avatar_1').attr('src', self['avatar']);
    $('#username').text(self['NickName']);
    $('#account').text(self['Uin']);
    $('#location').text(self['Province'] + ' ' + self['City']);
    $('#avatar_2').attr('src', self['avatar']);
    if (self['Sex'] === 1) {
        $('#gender').attr('src', '../static/images/icon/male.png');
    } else {
        $('#gender').attr('src', '../static/images/icon/female.png');
    }
}

//加载好友性别分布信息
function load_sex_info() {
    if (is_sex_loaded) {
        return
    }
    $.ajax({
        url: 'http://127.0.0.1:5000/api/sex/' + uid,
        beforeSend: function (xhr) {
            console.log('before send');
        },
        success: function (result, status, xhr) {
            success = result['success'];
            data = result['data'];
            console.log('success', success, data);
            is_sex_loaded = true;
            fill_sex_info(data);
        },
        error: function (xhr, status, error) {
            console.log('error', status, error, xhr)
        },
        complete: function (xhr, status) {
            console.log('complete', status, xhr);
        }
    })
}

//填充好友性别分布信息
function fill_sex_info(data) {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('ec-gender'));

    // 指定图表的配置项和数据
    var option = {
        backgroundColor: '#2c343c',
        title: {
            text: '好友性别分布',
            left: 'center',
            top: 20,
            textStyle: {
                color: '#ccc'
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)"
        },
        visualMap: {
            show: false,
            min: 80,
            max: 600,
            inRange: {
                colorLightness: [0.5, 1]
            }
        },
        series: [
            {
                name: '性别',
                type: 'pie',
                radius: '55%',
                center: ['50%', '50%'],
                data: data,
                roseType: 'radius',
                label: {
                    normal: {
                        textStyle: {
                            color: 'rgba(255, 255, 255, 0.3)'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        lineStyle: {
                            color: 'rgba(255, 255, 255, 0.3)'
                        },
                        smooth: 0.2,
                        length: 10,
                        length2: 20
                    }
                },
                itemStyle: {
                    normal: {
                        color: '#c23531',
                        shadowBlur: 200,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },

                animationType: 'scale',
                animationEasing: 'elasticOut',
                animationDelay: function (idx) {
                    return Math.random() * 200;
                }
            }
        ]
    };

    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}

//加载好友头像照片墙
function load_avatars() {
    if (is_avatar_loaded) {
        return
    }
    $.ajax({
        url: 'http://127.0.0.1:5000/api/avatars/' + uid,
        beforeSend: function (xhr) {
            console.log('before send');
        },
        success: function (result, status, xhr) {
            success = result['success'];
            data = result['data'];
            console.log('success', success, data);
            is_avatar_loaded = true;
            for (let i = 0; i < data.length; i++) {
                $('#avatar-wall').append('<img style="width: 50px;height: 50px;margin: 5px" alt="" src=' + data[i] + '>')
            }
        },
        error: function (xhr, status, error) {
            console.log('error', status, error, xhr)
        },
        complete: function (xhr, status) {
            console.log('complete', status, xhr);
        }
    });

}

//加载词云
function load_wordcloud() {
    if (is_word_cloud_loaded) {
        return
    }
    $.ajax({
        url: 'http://127.0.0.1:5000/api/word_cloud/' + uid,
        beforeSend: function (xhr) {
            console.log('before send');
        },
        success: function (result, status, xhr) {
            success = result['success'];
            data = result['data'];
            console.log('success', success, data);
            is_word_cloud_loaded = true;
            fill_wordcloud(data)
        },
        error: function (xhr, status, error) {
            console.log('error', status, error, xhr)
        },
        complete: function (xhr, status) {
            console.log('complete', status, xhr);
        }
    });
}

function fill_wordcloud(data) {
    let word_list = [];
    let freq_list = [];
    let max = 0;
    $.each(data, function (word, freq) {
        word_list.push(word);
        freq_list.push(freq);
        if (max < freq) {
            max = freq
        }
    });
    while (max > 100) {
        max = Math.sqrt(max);
        for (let i = 0; i < freq_list.length; i++) {
            freq_list[i] = Math.sqrt(freq_list[i])
        }
    }

    var wordFreqData = [];
    for (let i = 0; i < word_list.length; i++) {
        wordFreqData.push([word_list[i], freq_list[i]])
    }

    console.log('wordFreqData', wordFreqData);
    var canvas = document.getElementById('word-cloud');
    var options = eval({
        list: wordFreqData,
        gridSize: Math.round(16 * $('#word-cloud').width() / 1024),
        weightFactor: function (size) {
            result = size * $('#word-cloud').width() / 80;
            while (result < 30) {
                result = result * 1.4;
            }
            console.log(size, result, wordFreqData.length, $('#word-cloud').width());
            return result
        },
        fontFamily: 'Times, serif',
        color: "random-light",
        rotateRatio: 0.5,
        // rotationSteps: 2,
        backgroundColor: '#2c343c',
        minFontSize: 6, //最小字号
        maxFontSize: 50,
        fontWeight: 'normal', //字体粗细
    });
    //生成
    WordCloud(canvas, options);
}

//加载地域分布表
function load_locations() {
    if (is_location_loaded) {
        return
    }
    $.ajax({
        url: 'http://127.0.0.1:5000/api/locations/' + uid,
        beforeSend: function (xhr) {
            console.log('before send');
        },
        success: function (result, status, xhr) {
            success = result['success'];
            data = result['data'];
            console.log('success', success, data);
            is_location_loaded = true;
            fill_location_info(data);
        },
        error: function (xhr, status, error) {
            console.log('error', status, error, xhr)
        },
        complete: function (xhr, status) {
            console.log('complete', status, xhr);
        }
    });
}

function fill_location_info(data) {
    // 基于准备好的dom，初始化echarts实例
    var myChart = echarts.init(document.getElementById('ec-locations'));

    option = {
        backgroundColor: '#2c343c',
        title: {
            text: '好友地区分布',
            left: 'center',
            top: 20,
            textStyle: {
                color: '#ccc'
            }
        },
        tooltip: {
            trigger: 'axis'
        },
        xAxis: {
            type: 'category',
            //['江苏', '河北', '河南', '安徽', '浙江', '深圳', '乌鲁木齐', 'A', 'B', 'C', 'D', 'E', 'F']
            data: data['province'],
            axisLabel: {
                interval: 0,
                color: '#ccc',
                rotate: 40
            },
            axisLine: {
                lineStyle: {
                    color: '#ccc'
                }
            }
        },
        yAxis: {
            type: 'value',
            splitLine: {
                show: false
            },
            axisLabel: {
                color: '#ccc'
            },
            axisLine: {
                lineStyle: {
                    color: '#ccc'
                }
            }
        },
        series: [{
            //[120, 2000, 150, 80, 70, 110, 130, 99, 120, 221, 324, 112, 90]
            data: data['count'],
            type: 'bar'
        }]
    };
    // 使用刚指定的配置项和数据显示图表。
    myChart.setOption(option);
}
