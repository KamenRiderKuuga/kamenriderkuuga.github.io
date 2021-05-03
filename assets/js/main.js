$(function () {
    var pageHeight = $(window).height(); //窗口高
    var scroll = 0; // 网页卷去的头部，先=0

    addMove();
    $(window).scroll(function () {
        //进入视窗时播放 动画
        scroll = $(this).scrollTop();
        addMove();
    });

    function addMove() {
        // 添加move类，这个是用来控制动画的
        $('.skill span').each(function (i, ele) {
            var top = $(this).offset().top;
            if (top <= pageHeight + scroll) {
                $(this).addClass('move');
            }
        });
    }

    $(".nav-btn").click(function () {
        $(this).toggleClass("rotate");
        $("header nav").slideToggle();
    });
    $("header nav").click(function () {
        $(this).hide();
    })
    // $('.btn-slider').click(function () {
    //     $('.banner').slideToggle();
    //     $(this).css("buttom", "-30")
    // });

    // setInterval(() => {
    //     $(".banner img").each(function () {
    //         $(this).fadeToggle(1000);
    //     });
    // }, 5000);


    // console.log(111);
    // window.addEventListener('scroll', function () {
    //     let t = $('body, html').scrollTop();   // 目前监听的是整个body的滚动条距离
    //     if (t > 0) {
    //         $('header').addClass('header-active')
    //     } else {
    //         $('header').removeClass('header-active')
    //     }
    // })
});