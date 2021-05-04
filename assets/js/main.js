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

    var navToolBar = $("header nav");

    if (navToolBar.css("position") == "absolute") {
        $(".nav-btn").click(function () {
            $(this).toggleClass("rotate");
            navToolBar.slideToggle();
        });
        navToolBar.click(function () {
            $(this).hide();
        })
    }
});