document.addEventListener('DOMContentLoaded', function () {
    const video = document.getElementById('video');
    const videoSrc = 'https://tv-trt1.medya.trt.com.tr/master.m3u8';

    if (Hls.isSupported()) {
        const hls = new Hls();
        hls.loadSource(videoSrc);
        hls.attachMedia(video);
        hls.on(Hls.Events.MANIFEST_PARSED, function () {
            video.play();
        });
    } else if (video.canPlayType('application/vnd.apple.mpegurl')) {
        video.src = videoSrc;
        video.addEventListener('loadedmetadata', function () {
            video.play();
        });
    }
});
                               
