import io
import pandas as pd
import streamlit as st

# 1. Sayfa Konfigürasyonu
st.set_page_config(
    page_title="Mevlânâ Celâleddîn-i Rûmî Portalı",
    page_icon="🕊️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Özel Stil (CSS) ve Güvenlik Koruması (JavaScript ile Sağ Tık/Kısayol Engelleme)
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cinzel:wght@500;700&family=Inter:wght@300;400;600&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        -webkit-user-select: none !important;
        -moz-user-select: none !important;
        -ms-user-select: none !important;
        user-select: none !important;
    }
    .main-title {
        font-family: 'Cinzel', serif;
        font-size: 2.6rem;
        color: #581845;
        text-align: center;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.15rem;
        color: #6C7A89;
        text-align: center;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .quote-card {
        background-color: #FCFBF7;
        border-left: 5px solid #900C3F;
        border-right: 1px solid #EAECEE;
        border-top: 1px solid #EAECEE;
        border-bottom: 1px solid #EAECEE;
        padding: 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.03);
    }
    .quote-text {
        font-size: 1.1rem;
        line-height: 1.7;
        color: #2C3E50;
        background-color: #FFF9F0;
        padding: 1rem;
        border-radius: 6px;
        border-left: 3px solid #FFC300;
        margin: 0.8rem 0;
    }
    .quote-ref {
        display: inline-block;
        background-color: #EAECEE;
        color: #515A5A;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    .quote-theme {
        display: inline-block;
        background-color: #581845;
        color: #FFFFFF;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 5px;
    }
    .analysis-box {
        font-size: 0.98rem;
        color: #34495E;
        margin-top: 0.8rem;
        line-height: 1.6;
    }
    .bio-card {
        background-color: #F4F6F7;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #D5D8DC;
        margin-bottom: 1rem;
    }
    .legal-card {
        background-color: #FAFAFA;
        border: 1px solid #E0E0E0;
        border-left: 4px solid #581845;
        padding: 1.2rem;
        border-radius: 6px;
        font-size: 0.88rem;
        color: #424242;
        line-height: 1.5;
        margin-top: 1rem;
    }
    </style>

    <script>
    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && (e.keyCode === 67 || e.keyCode === 86 || e.keyCode === 85 || e.keyCode === 65 || e.keyCode === 83)) {
            e.preventDefault();
        }
    });
    </script>
""",
    unsafe_allow_html=True,
)

# Kenar Çubuğu Dil Seçimi
st.sidebar.header("🌐 Dil / Language")
selected_lang = st.sidebar.selectbox(
    "Dil Seçiniz / Select Language:", ["Türkçe", "English"]
)

# --- TÜM İÇERİK VE İKTİBASLAR İÇİN DİNAMİK ÇEVİRİ VERİTABANI ---
TRANSLATIONS = {
    "Türkçe": {
        "page_title": "MEVLÂNÂ CELÂLEDDÎN-İ RÛMÎ (K.S.)",
        "sub_title": "Hayatı, Dönemi, Eserleri ve Mesnevî-i Şerif'ten Hikmetli İktibaslar Veritabanı",
        "tab1": "📖 Mesnevî İktibasları ve Şerhleri",
        "tab2": "👤 Hayatı ve Biyografisi",
        "tab3": "🌍 Yaşadığı Dönem ve Tarihçe",
        "tab4": "📚 Büyüleyici Eserleri",
        "tab5": "⚖️ Yasal Bildirim & Kullanım Koşulları",
        "sidebar_filter": "🔍 İktibas Filtreleme",
        "theme_select": "Tema Seçiniz:",
        "all_themes": "Tümü",
        "search_input": "Metin İçinde Ara (Örn: Ömer, Türk, Sirke, Mum, Biat):",
        "record_count": "Gösterilen Kayıt Sayısı:",
        "no_record": "Arama kriterlerinize uygun beyit veya iktibas bulunamadı.",
        "analysis_label": "🔍 Tasavvufi Açıklama ve Şerh:",
        "translation_label": "Tercüme/Kaynak:",
        "sidebar_info": (
            "💡 *Not:* Bu web uygulaması ücretsiz sunucularda barındırılmaktadır."
            " Uzun süre işlem yapılmadığında uygulama uyku moduna geçebilir"
            " (ekranda 'Zzzz' simgesi çıkabilir).\n\n💤 Eğer böyle bir ekranla"
            " karşılaşırsanız, ekranda beliren mavi renkli *'Yes, get this app"
            " back up!'* butonuna tıklayın ve uygulamanın yeniden uyanması"
            " için 15-30 saniye bekleyin."
        ),
        # Sekme 2 Biyografi
        "bio_title": "👤 Hz. Mevlânâ'nın Mübarek Hayat Çizgisi",
        "id_card": "📋 Kimlik Kartı",
        "bio_name": "Tam Adı:",
        "bio_title_lbl": "Unvanları:",
        "bio_dob": "Doğum Tarihi:",
        "bio_pob": "Doğum Yeri:",
        "bio_dod": "Vefat Tarihi:",
        "bio_pod": "Vefat Yeri:",
        "bio_day": "Vefat Günü İsmi:",
        "bio_father": "Babası:",
        "bio_guides": "Mürşidleri:",
        "bio_text": """
        ### Hayatının Safhaları
         
        *1. Belh'ten Anadolu'ya Hicret:*
        Mevlânâ Hazretleri, Horasan'ın Belh şehrinde doğmuştur. Babası "Sultânü'l-Ulemâ" (Âlimlerin Sultanı) unvanıyla tanınan Bahaeddin Veled'dir. Moğol istilasının yaklaşması ve siyasi huzursuzluklar sebebiyle aile Belh'ten ayrılmış; Nişabur, Bağdat, Mekke, Medine, Şam, Erzincan, Karaman güzergahını izleyerek Selçuklu poytahtı *Konya'ya* yerleşmiştir. Nişabur'da büyük mutasavvıf *Ferîdüddin Attâr* ile karşılaşmış, Attâr bu küçük çocuğun ilerideki azametini müjdelemiştir.

        *2. İlim ve İrşad Dönemi:*
        Babasının vefatından sonra onun medresedeki derslerini üstlenen Mevlânâ, Şer'î ilimlerde, fıkıhta, tefsirde ve edebiyatta büyük bir otorite haline gelmiştir. Babasının halifesi *Seyyid Burhaneddin Muhakkik-i Tirmizî*'nin rahle-i tedrisinde zühd, riyazet ve tasavvufi seyr-i sülukunu tamamlamıştır.

        *3. Şems-i Tebrizî ile Karşılaşma (Güneşin Doğuşu):*
        1244 yılında Konya'da *Şems-i Tebrizî* ile buluşması hayatının dönüm noktası olmuştur. Bu karşılaşma, zahirî bir müderrisi, aşk ve cezbe denizi bir mutasavvıfa dönüştürmüştür. Şems ile yaptığı derin sohbetler sonrasında medrese derslerini bırakmış, tamamen sema, zikir ve ilahi aşk vadisine yönelmiştir.

        *4. Şeb-i Arûs (Rabb'e Vuslat):*
        Mevlânâ 17 Aralık 1273 tarihinde Konya'da vefat etmiştir. O, ölümü bir ayrılık değil, sevgilinin Sevgiliye (Hakk'a) kavuşması olarak gördüğünden vefat gecesine *"Şeb-i Arûs" (Düğün Gecesi)* denilmiştir.
        """,
        # Sekme 3 Tarihçe
        "history_title": "🌍 13. Yüzyıl Anadolu Selçuklu Dönemi ve Tarihsel Bağlam",
        "history_text": """
        Hz. Mevlânâ, İslam medeniyeti tarihinin en çalkantılı, en buhranlı fakat manevi açıdan en verimli çağlarından biri olan *13. Yüzyılda (Anadolu Selçuklu Devleti)* yaşamıştır.

        #### 1. Siyasi ve Sosyal Bunalım (Moğol İstilası ve Haçlı Seferleri)
        * *Moğol Kasırgası:* Doğudan gelen Moğol istilaları (Cengiz Han ve Hülagü), İslam dünyasının şehirlerini, kütüphanelerini, medreselerini yakıp yıkmış; milyonlarca insanın katledilmesine sebep olmuştur.
        * *Köse Dağ Savaşı (1243):* Selçukluların Moğollara yenilmesiyle Anadolu siyasi birliğini kaybetmiş, ağır vergiler ve iç karışıklıklar baş göstermiştir.
        * *Haçlı Seferleri:* Batıdan gelen Haçlı akınları da bölgedeki huzursuzluğu artırmıştır.

        #### 2. Manevi İmar ve Gönül Erleri
        Böylesine büyük bir siyasi yıkım ve ümitsizlik çağında, Cenâb-ı Hak Anadolu'yu manevi mimarlarla donatmıştır. İnsanların ruhsal çöküntüye düşmesini engelleyen gönül sultanları aynı dönemde yetişmiştir:
        * *Mevlânâ Celâleddîn-i Rûmî:* Sevgi, hoşgörü, ilahi aşk ve birleştirici vahdet anlayışıyla halka ümit aşılamıştır.
        * *Yunus Emre & Hacı Bektaş-ı Velî:* Türkçe ile manevi hakikatleri en ücra köylere kadar yaymışlardır.
        * *İbnü'l-Arabî & Sadreddin Konevî:* Vahdet-i Vücud düşüncesiyle irfanî felsefenin zirvesini kurmuşlardır (Konevî ile Mevlânâ samimi dosttur).

        #### 3. Mevlânâ'nın Tarihsel Siyasi Duruşu
        Mevlânâ, Selçuklu sultanları ve devlet adamları nezdinde büyük hürmet görmüştür. Onlara yazdığı mektuplarla adaletle hükmetmelerini, halka şefkat göstermelerini ve zalimleşmemelerini tavsiye etmiştir.
        """,
        # Sekme 4 Eserler
        "books_title": "📚 Mevlânâ Hazretleri'nin Ölümsüz Eserleri",
        "manzum": "Manzum Eserleri",
        "mensur": "Mensur (Nesir) Eserleri",
        "books_desc": """
        #### 1. Mesnevî-i Şerîf
        * *Mahiyeti:* 6 cilt ve yaklaşık 25.600 beyitten oluşan devasa bir irfan külliyatıdır.
        * *Dili:* Farsça (Arapça ve Türkçe ifadeler içerir).
        * *Yazılışı:* Çelebi Hüsameddin'in ricası ve kâtipliği ile kaleme alınmıştır. "Dinle bu neyden..." (Bişnev ez ney) diye başlar.
         
        #### 2. Dîvân-ı Kebîr (Dîvân-ı Şems-i Tebrizî)
        * *Mahiyeti:* 40.000 beyti aşan gazel, müstezad ve rubailerden oluşur. İlahi aşkın ve coşkunluğun zirvesidir.
        """,
        "books_desc2": """
        #### 3. Fîhi Mâ Fîh (Ne Varsa İçindedir)
        * Mevlânâ'nın meclislerinde yaptığı sohbetlerin not edilmesiyle oluşmuştur. Tasavvufi ve felsefi görüşlerini sade bir nesirle açıklar.

        #### 4. Mecâlis-i Seb'a (Yedi Meclis)
        * Mevlânâ'nın vaaz verdiği 7 ayrı meclisteki konuşmalarından oluşur.

        #### 5. Mektûbât (Mektuplar)
        * Devlet adamlarına ve dostlarına yazdığı 147 adet mektuptan müteşekkildir.
        """,
        # Sekme 5 Yasal
        "legal_title": "⚖️ Yasal Bildirim, Sorumluluk Reddi ve Kullanım Şartları",
        "legal_content": """
        <div class="legal-card">
            <h4>📌 Telif Hakkı ve Yasal Kullanım Koşulları</h4>
            <p><b>1. Amaç:</b> Bu yazılım ve içerisindeki veritabanı, yalnızca <b>eğitim, kültür, akademik inceleme ve bilgi paylaşımı</b> amacıyla hazırlanmıştır.</p>
            <p><b>2. Ticari Kullanım Yasağı:</b> Bu uygulamanın kaynak kodları, veri kümesi, tasarımı ve içeriği doğrudan veya dolaylı olarak hiçbir şekilde <b>ticari amaçla satılamaz, kiralanamaz, pazarlanamaz veya gelir elde etme amacıyla kullanılamaz</b>.</p>
            <p><b>3. Çoğaltma ve Kopyalama Yasağı:</b> Yazılımın tamamı veya bir kısmı; hak sahibinin açık ve yazılı izni olmaksızın <b>kopyalanamaz, çoğaltılamaz, dağıtılamaz, başka platformlara aktarılamaz veya kaynak kodları tersine mühendislikle işlenemaz</b>.</p>
            <p><b>4. Kaynak Atfı:</b> Bu uygulamada sunulan bazı içerik ve derlemelerin oluşturulmasında <b>hakikat.com</b> internet sitesinden ve kaynaklarından istifade edilmiştir.</p>
            <p><b>5. Fikri Mülkiyet ve Yasal Sorumluluk:</b> 5846 Sayılı Fikir ve Sanat Eserleri Kanunu ile Türk Ceza Kanunu hükümleri kapsamında aksi davranışlar yasal takibata tabidir.</p>
        </div>
        """,
        "footer_text": '<b>Kaddesallâhu Sırrahu\'l-A\'lâ</b> | <i>"Bizim tekkemiz aşk tekkesidir; oraya giren safa bulur."</i>',
        "footer_legal": "<b>⚖️ YASAL UYARI & KAYNAK:</b> Bu yazılım ve içeriği <b>bilgi paylaşımı ve akademik/kültür</b> amacıyla sunulmuştur. İçerik oluşturulmasında <b>hakikat.com</b> kaynaklarından yararlanılmıştır. Tüm hakları saklıdır. © 2026",
        # İktibaslar (Quotes) Veritabanı - Türkçe (12 Adet)
        "quotes": [
            {
                "id": 1,
                "Cilt_Kaynak": "Mesnevî, Cilt 5, Beyit: 875 vd. (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Gönül Sahibi (İnsan-ı Kâmil) Vasıtası ve Rızık",
                "Tercume_Eden": "Veled İzbudak / Şefik Can",
                "Metin": "Altı cihette bulunan, bu cihetlerden kurtulamayan kişiye Allah, o gönül sâhibi vâsıta olmadıkça nazar etmez! Birisini reddederse onun için eder; kabul ederse, yine şefaatçi odur. O olmadıkça Allah kimseye rızık vermez. İşte ben, vuslata ulaşan kişinin ahvâlinden bir miktarcığını sana söyledim. Allah, ihsânını onun eline kor da, acıdıklarına onun elinden ihsanda bulunur. O'nun eli, bütünlük denizi ile birleşmiştir. O, neliksiz ve niteliksizdir ve tam kemâl sâhibidir.",
                "Aciklama_Serh": "Mevlânâ Hazretleri bu beyitlerde, maddî ve mekânsal (altı cihet) kayıtlara hapsolmuş insanın, Hakk'a ulaşmasında 'İnsan-ı Kâmil' veya 'Mürşid-i Kâmil'in rolünü anlatır. Allah'ın feyz ve rahmetinin kâmil velinin eliyle dağıtıldığını, o elin Hakk'ın kudret eliyle birleştiğini (Yedullah sırrı) ifade eder.",
            },
            {
                "id": 2,
                "Cilt_Kaynak": "Mesnevî, Cilt 5, Beyit: 740 vd. (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Biat Sırrı, Vaktin Peygamberi ve Hudeybiye Ruhî Bağı",
                "Tercume_Eden": "Veled İzbudak",
                "Metin": "Allah: 'Allah'ın eli onların elleri üstündedir.' (Fetih: 10) buyurdu ya, işte senin elin de o biat ehlinin eli olur. …O her şeyi bilen ulu pîre uydun mu kurtuldun demektir. Çünkü o, ey mürid, vaktinin peygamberidir, Peygamber'in nûru ondan zuhûr eder. Ona uydun, onun elini tuttun mu, Hudeybiye'de bulunup Peygamber Aleyhisselâm'a biat eden sahâbeden olursun; cennetle müjdelenen on kişiden sayılırsın, hâlis ve potada erise bile ayarı düşmez altın adönersin…",
                "Aciklama_Serh": "Kâmil mürşide biat etmenin, hakikatte Hz. Peygamber’e (s.a.v.) ve O’nun vasıtasıyla Allah’a biat etmek demek olduğu açıklanır. Mürşid, peygamberlik müessesesinin bâtınî/manevi temsilcisi kabul edilir. O el, Hudeybiye'deki Biat-ı Rıdvân'ın manevi devamıdır.",
            },
            {
                "id": 3,
                "Cilt_Kaynak": "Mesnevî, Cilt 6, Beyit: 1510 vd. (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Allah Vekili, Adalet Gölgesi ve Fenâ Makamı",
                "Tercume_Eden": "Veled İzbudak",
                "Metin": "O Allah vekîlidir, Allah'ın adâletinin gölgesidir. Her hak sahibiyle, cezâya müstehak olanın aynasıdır o!.. O, mazlumun hakkını hak ettirmek için cezâ verir, kendi ırzı için, kızgınlığından yâhut bir şey kazanmak için değil! Onun cezâsı Allah içindir, kıyâmet günü içindir. Bu cezâda bir hata olsa bile ona diyet lâzım gelmez…",
                "Aciklama_Serh": "Bu beyitlerde Veliyy-i Kâmil'in nefsi arzularından, öfkesinden ve benliğinden tamamen sıyrıldığı (Fena fillah) vurgulanır. O bir ayna gibidir; muameleleri şahsî hırsına değil, doğrudan ilahi adalete ve rızaya dayanır.",
            },
            {
                "id": 4,
                "Cilt_Kaynak": "Mesnevî, Cilt 6, Beyit: 3195 vd. (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Nûr-ı Muhammedî, 'Mâ Rameyte' Sırrı ve Bâtın Penceresi",
                "Tercume_Eden": "Veled İzbudak",
                "Metin": "Ten görme de, o sağır ve dilsizler gibi kendilerine doğru bir şey söylenince inkâr edenlerden olma! O zât: 'Attığın vakit sen atmadın, Allah attı.' (Enfâl: 17) Sırrına mazhar olmuştur; onun görüşü, Allah'ın görüşüdür. O'na hizmet Allah'a hizmettir. Gündüzü görmek, bu pencereyi görmektir. Hele şu pencere yok mu? O kendinden parlamadadır; ondaki Nûr, güneşin yâhut Ferkad yıldızının eğreti nûru değildir!",
                "Aciklama_Serh": "İnsan-ı Kâmil'in ten elbisesine değil, onda tecelli eden zatî nûra bakılması gerektiği ihtarıdır. Enfâl Suresi 17. ayetindeki 'Sen atmadın, Allah attı' fehvasınca, o zatın fiil ve nazarı Hakk'a vasıldır.",
            },
            {
                "id": 5,
                "Cilt_Kaynak": "Mesnevî, Cilt 6, Beyit: 20 vd. (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Allah'ın Velisi, Şeker ve Sirke Temsili",
                "Tercume_Eden": "Veled İzbudak",
                "Metin": "Nûh'un kavmi de ona sirke söküp duruyorlardı, fakat Allah'ın lütuf ve ihsan denizi ona daha fazla şeker dökmekteydi. Onun şekerine cömertlik denizinden yardım edilmekte idi de, o yüzden âlem halkının sirkesinden fazlaydı onun şekeri! Tek bir kişi amma, bine bedel... Kimdir o? Allâh'ın 'Velî'si!.. Hattâ o yüce Allah kulu, yüzlerce zamanın tek eridir. Denize yol bulmuş olan küpün önünde ırmaklar bile diz çöker!",
                "Aciklama_Serh": "Ehl-i dünya ve inkârcıların eziyeti (sirke) karşısında, ilahi vahiy ve lütuf ile beslenen velinin sabrı, sevgisi ve hikmeti (şeker) galip gelir. Veli tek bir fert gibi görünse de bir ümmet hükmündedir.",
            },
            {
                "id": 6,
                "Cilt_Kaynak": "Mesnevî, Cilt 1, Beyit: 420-424 (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Zıllullâh (Allah'ın Gölgesi) ve Ahir Zaman Fitnelerinden Kurtuluş",
                "Tercume_Eden": "Veled İzbudak",
                "Metin": "Ömrünün çokluğu boşaldı, ömür gitti; gölge avı ardında koşmada yandı, eridi! Bir kişinin terbiyecisi Allah gölgesi (Zıllu'llâh) olursa, onu gölgeden ve hayâlden kurtarır. Allah'a kul olan Allah'ın kölesidir; o bu âlemden yana ölmüş, Allah ile dirilmiştir. Fırsatı kaçırmadan ve şüphe etmeden onun eteğine sarıl ki, âhir zamanın sonundaki fitnelerden kurtulasın!..",
                "Aciklama_Serh": "Dünya hayatının fani hayallerinin ('gölge avı') peşinde koşarak ömrü heba etmeme uyarısıdır. Gerçek diriliş, Allah ile diri olmaktır. Ahir zamanın yakıcı fitnelerinden sıyrılmanın yolu, hakiki mürşidlerin irşad eteğine tutunmaktır.",
            },
            {
                "id": 7,
                "Cilt_Kaynak": "Fusûsu'l-Hikem Şerhi (A. Avni Konuk, s. 215) (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Mustafa (s.a.v.) Zühuru ve Fuyûzat Hazinesi",
                "Tercume_Eden": "Ahmet Avni Konuk Şerhi",
                "Metin": "Açtılar kenz-i füyûzu olunuz hil'at-pûş / Mustafâ geldi yine cümleniz îmân ediniz.",
                "Aciklama_Serh": "Nûr-ı Muhammedî'nin (s.a.v.) her devirde kâmil velilerin ve aktabın kalbinde tecelli ederek irşad faaliyetini sürdürdüğünü ifade eden tasavvufi beyittir. Feyizler hazinesi açılmış, manevi hil'atlar giydirilmiştir.",
            },
            {
                "id": 8,
                "Cilt_Kaynak": "Mesnevî, Cilt 3, s. 253 (Hakikat.com Kaynaklı)",
                "Konu_Tema": "İlahî Kerem ve Bayrakların Dikilmesi",
                "Tercume_Eden": "Veled İzbudak",
                "Metin": "Âlemin altı ciheti de onun keremiyle dolu. Nereye baksan onun bayrakları orada dikildi.",
                "Aciklama_Serh": "Cenâb-ı Hakk'ın ve O'nun temsilcisi olan velinin kerem ve ihsanının evrensel boyutunu, altı ciheti (sağ, sol, ön, arka, üst, alt) kuşatan manevi hakimiyetini beyan eder.",
            },
            {
                "id": 9,
                "Cilt_Kaynak": "Mesnevî, Cilt 3, Beyit: 3613-3615 (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Kâmil İnsan (Ne Mutlu O Türk'e) ve Ateş Hendeklerini Aşmak",
                "Tercume_Eden": "Şefik Can",
                "Metin": "Ne mutlu o Türk'e, yani kâmil insana ki; çekinmeden, korkmadan konuşmasına devam eder ve atını ateşle dolu hendekten sıçratıverir. Yani ölümü (bile) göze alarak, çok tehlikeli bir iş olan hakikatleri söylemeyi başarır. O, heyecanla, İlâhî aşkla atını öyle bir hızlı sürer, öyle şahlandırır ki, onu ötelere, göklerin üstüne çıkarmayı düşünür! O yalnız Allah'ı düşünür. Ne kimseyi görür, ne kimsenin hasedine bakar. Her şeyden gözünü yummuştur; ateş gibi kuruyu da yakmıştır, yaşı da…",
                "Aciklama_Serh": "Buradaki 'Türk' kelimesi tasavvufi sembolizmde 'güçlü, cesur, kâmil, güzel insan' anlamında kullanılmıştır. Hakikati söylemek hususundaki korkusuzluk, dünyevi dedikodu ve hasetlere aldırış etmeden ilahi aşka kilitlenme hali tasvir edilir.",
            },
            {
                "id": 10,
                "Cilt_Kaynak": "Mesnevî, Cilt 5, s. 156 / Beyit: 2655 (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Vehim Denizinden Kurtuluş ve Hz. Ömer'in (r.a.) Nûru",
                "Tercume_Eden": "Veled İzbudak / Şefik Can",
                "Metin": "Dağ gibi akıllar bile vehim denizine ve hayal girdabına gark olup batmıştır. Bu kötülük tufanı dağları bile aşarken; Nuh'un gemisine binenlerden başka kim aman bulur, kurtulur? Yakîn yolunu kesen bu hayal yüzünden din ehli (müslümanlar), tam yetmiş iki fırka oldu. Yalnız yakîn eri, vehim ve hayalden kurtulur. Kaşının kılını hilâl (yeni ay) sanmaz. Fakat bir kimseye ÖMER'in nuru (ışığı) dayanak olmadıkça, yolunu kaşının eğri kılı keser. Yüz binlerce büyük ve dehşetli gemi, vehim denizinde paramparça olmuştur.",
                "Aciklama_Serh": "Akıl ve felsefenin kendi başına vehimlerden kurtulamayacağı, yakîn (kesin bilgi) için Nuh'un Gemisi mesabesindeki irşad ve Hz. Ömer (r.a.) gibi hak ile batılı ayıran 'Farukî' bir basiret nûruna ihtiyaç olduğu vurgulanır.",
            },
            {
                "id": 11,
                "Cilt_Kaynak": "Mesnevî, Cilt 3, s. 253 (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Kerem Sahibine İtaat ve Ateşe Atılmak",
                "Tercume_Eden": "Veled İzbudak",
                "Metin": "Bir kerem sahibi, sana 'Gel, ateşe gir!' dese hemencecik atıl ateşe... Beni yakar mı deme bile.",
                "Aciklama_Serh": "Hz. İbrahim'in (a.s.) ateşe atılması teslimiyetine atıf yapılır. Hakiki kâmil mürşidin emrindeki hikmete şeksiz şüphesiz teslim olmanın ruhani yakıcılıkları dahi gülistana çevireceği beyan edilir.",
            },
            {
                "id": 12,
                "Cilt_Kaynak": "Mesnevî, Cilt 1, s. 380 (Hakikat.com Kaynaklı)",
                "Konu_Tema": "Mum Misali Nûr-ı Muhammedî'nin İntikali",
                "Tercume_Eden": "Veled İzbudak",
                "Metin": "Mustafa: 'Ne mutlu benim yüzümü görene, ne mutlu yüzümü göreni görene.' dedi. Bir mumdan yakılan mumu gören, gerçekten de asıl mumu görmüş sayılır. Böylece o mumun ışığı, yüz muma nakledilse, o mumdan yüzlerce mum yakılsa, sonuncusunu gören bile asıl ilk mumu görmüş sayılır. Işığı istersen son mumdan al; istersen can mumundan, hiçbir fark yoktur. İstersen son mumun ışığını gör, istersen geçmişlerin mumunu gör.",
                "Aciklama_Serh": "Hz. Peygamber'in (s.a.v.) nûrunun çağlar boyunca velilerin, âlimlerin kalbinden kalbine bir muma diğer mumdan ışık nakledilir gibi aktarıldığını anlatır. Çağındaki kâmil bir mürşidi gören, manen Hz. Peygamber'in ışığını görmüş demektir.",
            },
        ],
    },
    "English": {
        "page_title": "MAWLANA JALAL AL-DIN RUMI (Q.S.)",
        "sub_title": "Life, Era, Works and Database of Wise Excerpts from Masnavi-i Sharif",
        "tab1": "📖 Masnavi Quotes & Commentaries",
        "tab2": "👤 Life & Biography",
        "tab3": "🌍 Historical Era & Context",
        "tab4": "📚 Enigmatic Works",
        "tab5": "⚖️ Legal Notice & Terms",
        "sidebar_filter": "🔍 Quote Filtering",
        "theme_select": "Select Theme:",
        "all_themes": "All",
        "search_input": "Search in Text:",
        "record_count": "Displayed Record Count:",
        "no_record": "No couplets or excerpts found matching your search criteria.",
        "analysis_label": "🔍 Mystical Explanation & Commentary:",
        "translation_label": "Translation/Source:",
        "sidebar_info": (
            "💡 *Note:* This web application is hosted on free servers. If left"
            " inactive for a long time, the application may go into sleep mode"
            " (a 'Zzzz' icon may appear on the screen).\n\n💤 If you encounter such"
            " a screen, click the blue *'Yes, get this app back up!'* button that"
            " appears on the screen and wait 15-30 seconds for the application"
            " to wake back up."
        ),
        # Tab 2 Bio
        "bio_title": "👤 The Blessed Life Path of Mawlana Rumi",
        "id_card": "📋 Identity Card",
        "bio_name": "Full Name:",
        "bio_title_lbl": "Titles:",
        "bio_dob": "Date of Birth:",
        "bio_pob": "Place of Birth:",
        "bio_dod": "Date of Death:",
        "bio_pod": "Place of Death:",
        "bio_day": "Death Anniversary:",
        "bio_father": "Father:",
        "bio_guides": "Spiritual Guides:",
        "bio_text": """
        ### Stages of His Life
         
        *1. Migration from Balkh to Anatolia:*
        Mawlana Rumi was born in Balkh, Khorasan. His father was Bahaeddin Veled, known as "Sultânü'l-Ulemâ" (Sultan of Scholars). Due to the approaching Mongol invasion and political unrest, the family left Balkh and settled in Konya, the capital of the Seljuk Empire, traveling through Nishapur, Baghdad, Mecca, Medina, Damascus, Erzincan, and Karaman. In Nishapur, he met the great mystic Farid al-Din Attar, who prophesied the boy's future greatness.

        *2. Period of Knowledge and Guidance:*
        After his father's death, Mawlana took over his lectures at the madrasa and became a major authority in Islamic jurisprudence, exegesis, and literature. He completed his spiritual path (sayr-i suluk) under the tutelage of his father's successor, Seyyid Burhaneddin Muhakkik-i Tirmizî.

        *3. Encounter with Shams Tabrizi (The Rising of the Sun):*
        His meeting with Shams Tabrizi in Konya in 1244 was the turning point of his life. This encounter transformed an exoteric scholar into a mystic of divine love and ecstasy. After deep conversations with Shams, he abandoned formal madrasa lectures and dedicated himself entirely to Sama, remembrance, and divine love.

        *4. Sheb-i Arûs (Union with the Divine):*
        Mawlana passed away in Konya on December 17, 1273. Since he viewed death not as a separation but as a reunion with the Beloved, his passing night is named *"Sheb-i Arûs" (The Wedding Night)*.
        """,
        # Tab 3 History
        "history_title": "🌍 13th Century Anatolian Seljuk Period and Historical Context",
        "history_text": """
        Mawlana lived in the 13th Century (Anatolian Seljuk State), one of the most turbulent, crisis-ridden yet spiritually fertile eras in the history of Islamic civilization.

        #### 1. Political and Social Crisis (Mongol Invasion and Crusades)
        * *The Mongol Hurricane:* Mongol invasions from the east (Genghis Khan and Hulagu) destroyed cities, libraries, and madrasas of the Islamic world, causing millions of deaths.
        * *Battle of Köse Dağ (1243):* With the defeat of the Seljuks by the Mongols, Anatolia lost its political unity, leading to heavy taxes and internal strife.
        * *Crusades:* Crusader raids from the west further increased unrest in the region.

        #### 2. Spiritual Reconstruction and Heart Masters
        During such an era of political collapse and despair, God endowed Anatolia with spiritual architects. Heart sultans who prevented spiritual collapse arose in the same era:
        * *Mawlana Jalal al-Din Rumi:* Instilled hope in the people with his understanding of love, tolerance, divine love, and unifying unity (wahdah).
        * *Yunus Emre & Hacı Bektaş-ı Velî:* Spread spiritual truths across the remotest villages using Turkish.
        * *Ibn Arabi & Sadreddin Qunawi:* Established the peak of mystical philosophy through the concept of Wahdat al-Wujud (Unity of Existence).

        #### 3. Mawlana's Historical and Political Stance
        Mawlana received great reverence from Seljuk sultans and statesmen. Through his letters (Maktubât), he advised them to rule with justice, show compassion to the people, and avoid tyranny.
        """,
        # Tab 4 Books
        "books_title": "📚 The Immortal Works of Mawlana Rumi",
        "manzum": "Poetic Works",
        "mensur": "Prose Works",
        "books_desc": """
        #### 1. Masnavi-i Sharif
        * *Nature:* A massive compendium of wisdom consisting of 6 volumes and approximately 25,600 couplets.
        * *Language:* Persian (containing Arabic and Turkish expressions).
        * *Composition:* Written at the request and scribing of Çelebi Hüsameddin. Begins with "Listen to the reed...".
         
        #### 2. Divan-ı Kebir (Divan-ı Shams-i Tabrizi)
        * *Nature:* Consists of ghazals, mustazads, and quatrains exceeding 40,000 couplets. The peak of divine love and ecstasy.
        """,
        "books_desc2": """
        #### 3. Fihi Ma Fih (In It Is What Is In It)
        * Formed by notes taken by his disciples of Mawlana's talks and Q&A sessions in his assemblies. Explains his mystical and philosophical views.

        #### 4. Majaalis-i Sab'a (Seven Assemblies)
        * Comprises Mawlana's speeches across 7 separate sermon assemblies.

        #### 5. Maktubât (Letters)
        * Consists of 147 letters written to statesmen, friends, and disciples regarding justice and aid.
        """,
        # Tab 5 Legal
        "legal_title": "⚖️ Legal Notice, Disclaimer and Terms of Use",
        "legal_content": """
        <div class="legal-card">
            <h4>📌 Copyright and Legal Terms of Use</h4>
            <p><b>1. Purpose:</b> This software and its database are prepared solely for <b>educational, cultural, academic review, and information-sharing</b> purposes.</p>
            <p><b>2. Prohibition of Commercial Use:</b> The source codes, dataset, design, and content of this application <b>cannot be sold, rented, marketed, or used for profit-making purposes</b> directly or indirectly in any way.</p>
            <p><b>3. Prohibition of Duplication and Copying:</b> All or part of the software <b>cannot be copied, reproduced, distributed, transferred to other platforms, or reverse-engineered</b> without express written permission.</p>
            <p><b>4. Source Attribution:</b> Resources and information from the website <b>hakikat.com</b> have been utilized in compiling certain contents of this application.</p>
            <p><b>5. Intellectual Property:</b> Violations are subject to legal prosecution under intellectual property laws.</p>
        </div>
        """,
        "footer_text": '<b>Kaddesallâhu Sırrahu\'l-A\'lâ</b> | <i>"Our dervish lodge is the lodge of love; whoever enters it finds serenity."</i>',
        "footer_legal": "<b>⚖️ LEGAL NOTICE & SOURCE:</b> Provided for <b>information sharing and academic review</b>. Resources from <b>hakikat.com</b> were utilized. All rights reserved. © 2026",
        # İktibaslar (Quotes) Veritabanı - İngilizce (12 Adet)
        "quotes": [
            {
                "id": 1,
                "Cilt_Kaynak": "Masnavi, Vol 5, Couplet: 875 ff. (via Hakikat.com)",
                "Konu_Tema": "Intercession of the Perfect Human & Sustenance",
                "Tercume_Eden": "Veled Izbudak / Sefik Can",
                "Metin": "God does not look upon the person trapped within the six directions unless that owner of the heart acts as a means! If He rejects someone, He does it through him; if He accepts, he is again the intercessor. Without him, God grants sustenance to no one. Here I have told you a fraction of the states of the one who reached Union. God places His bounty in his hand and bestows grace upon those He pities through his hand. His hand is united with the ocean of Wholeness. He is beyond quality, without condition, and possesses absolute perfection.",
                "Aciklama_Serh": "In these couplets, Mawlana explains the role of the 'Perfect Human' (Insan-i Kamil) or 'Perfect Master' in helping man, who is imprisoned by physical and spatial bounds (six directions), reach the Divine Truth. It expresses that God's grace and mercy are distributed through the hand of the perfect saint, and that hand unites with the power hand of the Divine.",
            },
            {
                "id": 2,
                "Cilt_Kaynak": "Masnavi, Vol 5, Couplet: 740 ff. (via Hakikat.com)",
                "Konu_Tema": "Secret of Pledge, Prophet of the Time & Spiritual Bond",
                "Tercume_Eden": "Veled Izbudak",
                "Metin": "God said: 'The hand of God is over their hands.' (Al-Fath: 10). Thus your hand becomes the hand of those people of allegiance... If you follow that all-knowing ancient master, you are saved. For he, O seeker, is the prophet of his time; the light of the Prophet manifests through him. If you follow him and hold his hand, you become like the companions who pledged allegiance at Hudaybiyyah; you are counted among the ten promised paradise, turning into pure gold whose fineness does not drop even if melted in a crucible...",
                "Aciklama_Serh": "It is explained that pledging allegiance to a Perfect Master is in reality pledging allegiance to the Prophet (pbuh) and through him to God. The Master is accepted as the esoteric/spiritual representative of the institution of prophethood.",
            },
            {
                "id": 3,
                "Cilt_Kaynak": "Masnavi, Vol 6, Couplet: 1510 ff. (via Hakikat.com)",
                "Konu_Tema": "Representative of God, Shadow of Justice & Station of Fana",
                "Tercume_Eden": "Veled Izbudak",
                "Metin": "He is the deputy of God, the shadow of God's justice. He is the mirror for every rightful owner and every person deserving punishment!.. He punishes only to deliver the right of the oppressed, not for his own pride, out of anger, or to gain anything! His punishment is for God's sake, for the Day of Judgment. Even if there were an error in this punishment, no blood-money would be required of him...",
                "Aciklama_Serh": "Emphasizes that the Perfect Saint is completely stripped of egoistic desires, anger, and selfhood (Fana Fillah). He acts as a pure mirror reflecting divine justice rather than personal ambition.",
            },
            {
                "id": 4,
                "Cilt_Kaynak": "Masnavi, Vol 6, Couplet: 3195 ff. (via Hakikat.com)",
                "Konu_Tema": "Muhammadan Light, Secret of 'Ma Ramayta' & Inner Window",
                "Tercume_Eden": "Veled Izbudak",
                "Metin": "Do not look merely at the bodily frame, nor be like those deaf and mute who deny truth when spoken to them! That person has attained the secret: 'You threw not when you threw, but God threw.' (Al-Anfal: 17); his vision is the vision of God. Serving him is serving God. To see the daylight is to see through this window. Look at this window—it shines by itself; the Light in it is not a borrowed light like that of the sun or the star!",
                "Aciklama_Serh": "A warning to look not at the bodily garment of the Perfect Human, but at the essential Divine Light manifested within him. As implied in Surah Al-Anfal 17, his actions and gaze reach the Divine Truth.",
            },
            {
                "id": 5,
                "Cilt_Kaynak": "Masnavi, Vol 6, Couplet: 20 ff. (via Hakikat.com)",
                "Konu_Tema": "The Saint of God, Representation of Sugar and Vinegar",
                "Tercume_Eden": "Veled Izbudak",
                "Metin": "Noah's people kept pouring vinegar upon him, yet God's ocean of grace and favor poured more sugar upon him. His sugar was assisted by the ocean of generosity, hence his sugar outweighed all the vinegar of the world's people! A single person, yet worth a thousand... Who is he? The 'Saint' of God!.. Indeed that noble servant of God is the unique man of hundreds of ages. Even rivers kneel before the jar that has found its path to the sea!",
                "Aciklama_Serh": "In the face of the torment (vinegar) of worldly people and deniers, the patience, love, and wisdom (sugar) of the saint fed by divine revelation and grace prevail. Although a saint appears as a single individual, he holds the weight of an entire nation.",
            },
            {
                "id": 6,
                "Cilt_Kaynak": "Masnavi, Vol 1, Couplet: 420-424 (via Hakikat.com)",
                "Konu_Tema": "Zillullah (Shadow of God) & Deliverance from End-Time Trials",
                "Tercume_Eden": "Veled Izbudak",
                "Metin": "The length of your life is exhausted, life is gone; it burned and melted away chasing shadows! If a person's mentor is the Shadow of God (Zillullah), he saves him from shadows and illusions. A servant of God is a slave of God; he has died to this world and become alive through God. Hold fast to his garment without missing the chance or doubting, so that you may be saved from the tribulations of the end times!..",
                "Aciklama_Serh": "A warning not to waste life pursuing fleeting illusions of worldly existence. True resurrection is being alive with God. The way to escape the burning trials of the end times is to hold fast to the guidance of true spiritual masters.",
            },
            {
                "id": 7,
                "Cilt_Kaynak": "Commentary on Fusus al-Hikam (A. Avni Konuk, p. 215) (via Hakikat.com)",
                "Konu_Tema": "Manifestation of Mustafa (pbuh) & Treasure of Grace",
                "Tercume_Eden": "Ahmet Avni Konuk Commentary",
                "Metin": "They opened the treasure of spiritual grace, wear your robes of honor / Mustafa has come again, let all of you believe.",
                "Aciklama_Serh": "A mystical couplet expressing that the Muhammadan Light (pbuh) continues its guidance in every age by manifesting in the hearts of perfect saints and spiritual poles.",
            },
            {
                "id": 8,
                "Cilt_Kaynak": "Masnavi, Vol 3, p. 253 (via Hakikat.com)",
                "Konu_Tema": "Divine Generosity and Raising the Banners",
                "Tercume_Eden": "Veled Izbudak",
                "Metin": "All six directions of the world are filled with His generosity. Wherever you look, His banners are raised there.",
                "Aciklama_Serh": "Declares the universal dimension of the generosity and grace of God and the saint representing Him, encompassing spiritual sovereignty over all six directions.",
            },
            {
                "id": 9,
                "Cilt_Kaynak": "Masnavi, Vol 3, Couplet: 3613-3615 (via Hakikat.com)",
                "Konu_Tema": "The Perfect Human & Leap over Trenches of Fire",
                "Tercume_Eden": "Sefik Can",
                "Metin": "How happy is that Turk, meaning the perfect human who continues to speak without hesitation or fear, and leaps his horse across the trench filled with fire! That is, even facing death, he succeeds in declaring the truths of a very dangerous task. Driven by enthusiasm and Divine love, he gallops his steed so fast and rears it so high that he thinks of taking it beyond, above the heavens! He thinks of God alone. He sees no one, nor does he care for anyone's envy. He has closed his eyes to everything; like fire, he has burned both dry and wet...",
                "Aciklama_Serh": "The word 'Turk' here is used in Sufi symbolism to mean 'strong, courageous, perfect, beautiful person'. It depicts fearlessness in telling the truth and focus on divine love without regarding worldly gossip.",
            },
            {
                "id": 10,
                "Cilt_Kaynak": "Masnavi, Vol 5, p. 156 / Couplet: 2655 (via Hakikat.com)",
                "Konu_Tema": "Salvation from Ocean of Illusion & Light of Omar (r.a.)",
                "Tercume_Eden": "Veled Izbudak / Sefik Can",
                "Metin": "Even mountain-like intellects have drowned and sunk in the sea of illusion and whirlpool of imagination. While this storm of evil overflows mountains, who can find safety or salvation except those who board Noah's Ark? Because of this fantasy cutting off the path of certainty, religious people split into seventy-two sects. Only the man of certainty is saved from illusion. But unless the light of OMAR supports a person, his curved eyebrow cuts off his sight. Hundreds of thousands of grand ships have broken to pieces in the sea of illusion.",
                "Aciklama_Serh": "It is emphasized that intellect and philosophy alone cannot escape illusions; for certainty (yakin), one needs guidance like Noah's Ark and a discerning insight like Omar (r.a.) that separates truth from falsehood.",
            },
            {
                "id": 11,
                "Cilt_Kaynak": "Masnavi, Vol 3, p. 253 (via Hakikat.com)",
                "Konu_Tema": "Obedience to the Generous One and Entering Fire",
                "Tercume_Eden": "Veled Izbudak",
                "Metin": "If a generous master says to you 'Come, enter the fire!', leap into the fire immediately... Do not even say 'Will it burn me?'",
                "Aciklama_Serh": "Refers to the submission of Abraham (a.s.) when thrown into the fire. It declares that unquestioning surrender to the wisdom under a true master's command will transform even spiritual burning into a rose garden.",
            },
            {
                "id": 12,
                "Cilt_Kaynak": "Masnavi, Vol 1, p. 380 (via Hakikat.com)",
                "Konu_Tema": "Transmission of Muhammadan Light Like a Candle",
                "Tercume_Eden": "Veled Izbudak",
                "Metin": "Mustafa said: 'Blessed is he who sees my face, and blessed is he who sees the one who saw my face.' He who sees a candle lit from another candle truly has seen the original candle. Thus, if that candle's light is transferred to a hundred candles, whoever sees the last one is considered to have seen the first candle. Whether you take the light from the last candle or the original candle of the soul, there is no difference.",
                "Aciklama_Serh": "Explains how the Prophet's (pbuh) light is passed down through ages from heart to heart among saints like lighting one candle from another. Whoever sees a perfect master of his era spiritually sees the light of the Prophet.",
            },
        ],
    },
}

# Aktif Dil Verilerini Seç
t = TRANSLATIONS[selected_lang]

# Uygulama Verilerini Yükle
df_quotes = pd.DataFrame(t["quotes"])

# --- ARAYÜZ (UI) BAŞLIĞI ---
st.markdown(
    f'<div class="main-title">{t["page_title"]}</div>', unsafe_allow_html=True
)
st.markdown(
    f'<div class="sub-title">{t["sub_title"]}</div>', unsafe_allow_html=True
)

# SEKME YAPISI (TABS)
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [t["tab1"], t["tab2"], t["tab3"], t["tab4"], t["tab5"]]
)

# ==========================================
# SEKME 1: İKTİBASLAR VE ŞERHLER
# ==========================================
with tab1:
    st.subheader(t["tab1"])

    # Kenar Çubuğu Filtreleri
    st.sidebar.markdown("---")
    st.sidebar.header(t["sidebar_filter"])

    temalar = [t["all_themes"]] + list(df_quotes["Konu_Tema"].unique())
    selected_tema = st.sidebar.selectbox(t["theme_select"], temalar)

    search_keyword = st.sidebar.text_input(t["search_input"])

    # Filtreleme Mantığı
    filtered_df = df_quotes.copy()

    if selected_tema != t["all_themes"]:
        filtered_df = filtered_df[filtered_df["Konu_Tema"] == selected_tema]

    if search_keyword:
        filtered_df = filtered_df[
            filtered_df["Metin"].str.contains(search_keyword, case=False, na=False)
            | filtered_df["Aciklama_Serh"].str.contains(
                search_keyword, case=False, na=False
            )
            | filtered_df["Cilt_Kaynak"].str.contains(
                search_keyword, case=False, na=False
            )
        ]

    st.markdown(f"*{t['record_count']}* {len(filtered_df)} / {len(df_quotes)}")
    st.markdown("---")

    if len(filtered_df) == 0:
        st.warning(t["no_record"])
    else:
        for idx, row in filtered_df.iterrows():
            st.markdown(
                f"""
                <div class="quote-card">
                    <div>
                        <span class="quote-ref">📌 {row['Cilt_Kaynak']}</span>
                        <span class="quote-theme">🏷️ {row['Konu_Tema']}</span>
                    </div>
                    <div class="quote-text">
                        "{row['Metin']}"
                    </div>
                    <div class="analysis-box">
                        <b>{t['analysis_label']}</b><br>
                        {row['Aciklama_Serh']}
                    </div>
                    <div style="font-size:0.8rem; color:#888; margin-top:8px;">
                        {t['translation_label']} {row['Tercume_Eden']}
                    </div>
                </div>
            """,
                unsafe_allow_html=True,
            )

# ==========================================
# SEKME 2: HAYATI VE BİYOGRAFİSİ
# ==========================================
with tab2:
    st.subheader(t["bio_title"])

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(
            f"""
        <div class="bio-card">
            <h4>{t['id_card']}</h4>
            <ul>
                <li><b>{t['bio_name']}</b> Muhammed b. Muhammed b. Hüseyin el-Belhî</li>
                <li><b>{t['bio_title_lbl']}</b> Mevlânâ, Rûmî, Hüdavendigâr</li>
                <li><b>{t['bio_dob']}</b> 30 Eylül 1207 / Sep 30, 1207</li>
                <li><b>{t['bio_pob']}</b> Belh (Balkh)</li>
                <li><b>{t['bio_dod']}</b> 17 Aralık 1273 / Dec 17, 1273</li>
                <li><b>{t['bio_pod']}</b> Konya, Türkiye</li>
                <li><b>{t['bio_day']}</b> Şeb-i Arûs</li>
                <li><b>{t['bio_father']}</b> Bahaeddin Veled</li>
                <li><b>{t['bio_guides']}</b> Şems-i Tebrizî, S. Burhaneddin</li>
            </ul>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(t["bio_text"])

# ==========================================
# SEKME 3: YAŞADIĞI DÖNEM VE TARİHÇE
# ==========================================
with tab3:
    st.subheader(t["history_title"])
    st.markdown(t["history_text"])

# ==========================================
# SEKME 4: ESERLERİ
# ==========================================
with tab4:
    st.subheader(t["books_title"])

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"### {t['manzum']}")
        st.markdown(t["books_desc"])

    with col_b:
        st.markdown(f"### {t['mensur']}")
        st.markdown(t["books_desc2"])

# ==========================================
# SEKME 5: HUKUKİ YASAL UYARI VE KULLANIM ŞARTLARI
# ==========================================
with tab5:
    st.subheader(t["legal_title"])
    st.markdown(t["legal_content"], unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# UYKU MODU BİLGİLENDİRME BİLEŞENİ (SIDEBAR) & ALT BİLGİ (FOOTER)
# -----------------------------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.info(t["sidebar_info"])

st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #7F8C8D; font-size: 0.88rem; line-height: 1.6;'>
        {t['footer_text']}<br><br>
        <span style='font-size: 0.78rem; color: #95A5A6;'>
            {t['footer_legal']}
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)