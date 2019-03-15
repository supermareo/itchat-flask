const uid = $('#uid').text();
console.log('generate uid', uid);
$(document).ready(function () {
    show_loading();
    refresh_qr_interval();
});

let timeIdOfQr;
let timeIdOfLogin;

function clearQrInterval() {
    clearInterval(timeIdOfQr)
}

function clearLoginStatusInterval() {
    clearInterval(timeIdOfLogin)
}

function refresh_qr_interval() {
    timeIdOfQr = setInterval(refresh_qr(), 60000);
}

//请求二维码
function refresh_qr() {
    console.log('refresh_qr');
    $.ajax({
        url: 'http://127.0.0.1:5000/api/qr/' + uid,
        beforeSend: function (xhr) {
            console.log('before send');
        },
        success: function (result, status, xhr) {
            success = result['success'];
            console.log('success', success);
            if (success === true) {
                let qr = result['data'];
                $('#qr').attr('src', qr);
                clearLoginStatusInterval();
                get_login_status();
                hide_loading();
            } else {
                refresh_qr()
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

function get_login_status() {
    timeIdOfLogin = setInterval(() => {
        console.log('get_login_status');
        $.ajax({
            url: 'http://127.0.0.1:5000/api/login_status/' + uid,
            beforeSend: function (xhr) {
                console.log('before send');
            },
            success: function (result, status, xhr) {
                // console.log('success,data=', result);
                console.log('success,data=', result);
                qr = result['qr'];
                if (qr) {
                    $('#qr').attr('src', qr);
                }
                loginStatus = result['status'];
                //如果登录成功
                if (loginStatus === 'LOGIN_SUCCESS') {
                    //删除定时器，轮询结束
                    clearQrInterval();
                    clearLoginStatusInterval();
                    //跳转到详情界面
                    window.location.href = 'http://127.0.0.1:5000/summary/' + uid
                }
                //否则继续轮询
            },
            error: function (xhr, status, error) {
                console.log('error', status, error, xhr)
            },
            complete: function (xhr, status) {
                console.log('complete', status, xhr);
            }
        })
    }, 500);
}

//显示loading
function show_loading() {
    $('#qr').addClass('blur');
    $('#loading').show();
}

//隐藏loading
function hide_loading() {
    $('#qr').removeClass('blur');
    $('#loading').hide();
}