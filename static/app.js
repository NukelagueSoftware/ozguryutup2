$(document).ready(function() {
    $('#download-form').submit(function(e) {
        e.preventDefault(); // Sayfa yenilemeyi engelle

        var url = $('#url').val(); // Formdan URL'yi al

        // Form verilerini JSON formatında sunucuya gönder
        $.ajax({
            url: '/',
            type: 'POST',
            data: { 'url': url },
            success: function(data) {
                if (data) {
                    displayVideo(data); // İndirilen videoyu göster
                } else {
                    alert('Video indirme hatası oluştu.');
                }
            },
            error: function(error) {
                alert('Hata oluştu: ' + error.statusText); // Hata durumunda mesaj göster
            }
        });
    });

    // İndirilen videoyu gösteren işlev
    function displayVideo(videoUrl) {
        $('#video-container').html('<video controls><source src="' + videoUrl + '" type="video/mp4">Tarayıcınız video etiketini desteklemiyor.</video>');
    }
});
