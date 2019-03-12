$(document).ready(function () {
    refresh_qr();
});

//请求二维码
function refresh_qr() {
    $.ajax({
        url: 'http://127.0.0.1:5000/api/index',
        beforeSend: function (xhr) {
            console.log('before send');
            show_loading();
        },
        success: function (result, status, xhr) {
            console.log('success', result);
            qr = result['qr'];
            $('#qr').attr('src', qr);
        },
        error: function (xhr, status, error) {
            console.log('error', status, error, xhr)
        },
        complete: function (xhr, status) {
            console.log('complete', status, xhr);
            hide_loading();
        }
    });
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