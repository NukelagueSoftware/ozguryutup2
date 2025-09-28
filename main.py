from flask import Flask, request, render_template, redirect, url_for, send_from_directory
import os
from pytubefix import YouTube, Search

username = "sokulyegeni"
password = "dOKUZakadar"

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        entered_username = request.form['username']
        entered_password = request.form['password']
        if entered_username == username and entered_password == password:
            return redirect(url_for('main_page'))
        else:
            return render_template('login.html', error="Yanlış kullanıcı adı veya şifre!")

    return render_template('login.html')

@app.route('/x3fosdkf9FdKD0fdsk9DFkdFDSKOd9EFke', methods=['GET', 'POST'])
def main_page():
    video_url = None
    error_message = None

    if request.method == 'POST':
        try:
            url = request.form['url']
            youtube_video = YouTube(url)
            video_stream = youtube_video.streams.get_highest_resolution()
            new_filename = "Yeni_Video_Adi.mp4"  

            # static klasörünün var olduğundan emin olun
            if not os.path.exists("static"):
                os.makedirs("static")

            video_stream.download("static", filename=new_filename)

            # Log dosyası yazma
            with open("save.txt", "a", encoding="utf-8") as file:
                file.write("X\n")

            video_url = f'/static/{new_filename}'  

        except Exception as e:
            error_message = f"Hata: {str(e)}"
            print(error_message)

    return render_template('index.html', video_url=video_url, error=error_message)

@app.route('/play_video', methods=['POST'])
def play_video():
    import time
    import os

    try:
        url = request.form['url']
        video_title = request.form.get('title', 'Video')

        # 1️⃣ static klasöründeki önceki mp4 videoları sil
        static_folder = "static"
        if os.path.exists(static_folder):
            for filename in os.listdir(static_folder):
                file_path = os.path.join(static_folder, filename)
                try:
                    if os.path.isfile(file_path) and filename.lower().endswith(".mp4"):
                        os.remove(file_path)
                except Exception as e:
                    print(f"Video silme hatası: {e}")

        # 2️⃣ benzersiz dosya adı
        timestamp = str(int(time.time()))
        filename = f"video_{timestamp}.mp4"

        # 3️⃣ static klasörünü oluştur (yoksa)
        if not os.path.exists(static_folder):
            os.makedirs(static_folder)

        # 4️⃣ video indir
        youtube_video = YouTube(url)
        video_stream = youtube_video.streams.get_highest_resolution()
        video_stream.download(static_folder, filename=filename)

        return render_template(
            'video_player.html', 
            video_file=filename, 
            video_title=video_title,
            original_url=url
        )

    except Exception as e:
        return f"Video indirme hatası: {str(e)}", 500


@app.route('/kesfet')
@app.route('/kesfet/<category>')
def kesfet(category=None):
    import random, unicodedata
    from pytubefix import Search

    videos = []
    search_query = request.args.get("search", "").strip()

    categories = {
        'muzik': ['türkçe rap', 'cover şarkılar', 'remix', 'akustik cover', 'piano cover'],
        'oldschool_rap': ['Ceza', 'Sagopa Kajmer', 'Allame', 'Mode XL', 'Fuat Ergin', 'Ati242'],
        'oyun': ['forza horizon 5','enis kirazoğlu'],
        'komedi': ['cem yılmaz','deep turkish web'],
        'teknoloji': ['telefon inceleme 2025', 'bilgisayar toplama', 'yapay zeka', 'iphone vs samsung', 'gaming laptop', 'teknoloji haberleri'],
        'yks_egitim': ['eyüp b', 'görkem şahin', 'özcan aykın', 'dr.biyoloji', 'rüştü hoca edebiyat'],
        'egitim': ['kali linux'],
        'spor': ['basketbol', 'formula 1', 'galatasaray', 'fenerbahçe'],
        'lifestyle': ['yemek tarifleri', 'dekorasyon', 'seyahat'],
        'trend': ['pokemon showdown']
    }

    def yt_search_fix(query, limit=16):
        """Sadece aynı query’den 16 video çek, exception varsa atla."""
        queries = [
            query,
            unicodedata.normalize("NFKD", query).encode("ascii", "ignore").decode("utf-8"),
            query + " youtube"
        ]
        for q in queries:
            try:
                s = Search(q)
                results = list(s.results)
                while len(results) < limit:
                    more = s.get_next_results()
                    if not more:
                        break
                    results.extend(more)
                if results:
                    return results[:limit]
            except Exception as e:
                print(f"Search exception ({q}): {e}")
                continue
        return []

    def format_videos(search_results):
        """Videoları dict olarak hazırla."""
        formatted = []
        for video in search_results:
            try:
                if video.title and video.watch_url:
                    title = video.title.replace('[','').replace(']','')[:80]
                    formatted.append({
                        'title': title,
                        'url': video.watch_url,
                        'thumbnail': video.thumbnail_url,
                        'channel': video.author[:25] if video.author else 'Bilinmeyen',
                        'length': f"{video.length // 60}:{video.length % 60:02d}" if video.length else '?:??'
                    })
            except Exception as e:
                print(f"Video format exception: {e}")
                continue
        return formatted

    try:
        # kullanıcı araması varsa
        if search_query:
            search_results = yt_search_fix(search_query)
        # kategori seçilmişse rastgele bir terimden çek
        elif category and category in categories:
            term = random.choice(categories[category])
            search_results = yt_search_fix(term)
        # hiçbir şey yoksa rastgele kategori
        else:
            all_terms = [t for cat_terms in categories.values() for t in cat_terms]
            term = random.choice(all_terms)
            search_results = yt_search_fix(term)

        videos = format_videos(search_results)

    except Exception as e:
        print(f"Genel keşfet hatası: {e}")
        videos = []

    return render_template(
        'discover.html',
        videos=videos,
        categories=categories.keys(),
        search_query=search_query
    )


@app.route('/static/<path:filename>')
def download_file(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':  # Düzeltildi: __name__ (çift alt çizgi)
    app.run(host='0.0.0.0', port=8080, debug=True)