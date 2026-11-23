"""Azərbaycan dili · işarələnmiş sadə cümlə korpusu (hər sinif üçün ayrıca).

Yazılış: söz{NH[.növ][:hal]|ÜZV}. Çoxsözlü vahidlər alt xətlə yazılır: heç_kim, ehtimal_ki, ya_da.
Nitq hissələri (NH):
  İ — isim (hal: a adlıq, y yiyəlik, yö yönlük, t təsirlik, yer yerlik, ç çıxışlıq)
  S — sifət
  Say — say (.mq miqdar, .sr sıra, .kəsr kəsr, .tx təxmini)
  Ə — əvəzlik (.şəxs, .işarə, .sual, .təyini, .qayıdış, .qm qeyri-müəyyən, .inkar); hal göstərilə bilər
  F — feilin təsriflənən forması; FS — feili sifət; FB — feili bağlama; Məs — məsdər
  Z — zərf (.tərz, .zaman, .yer, .kəm kəmiyyət, .məqsəd)
  Q — qoşma (:hal — idarə etdiyi hal)
  B — bağlayıcı (.tbsz tabesizlik)
  Əd — ədat; Mod — modal söz; N — nida
Cümlə üzvləri: M mübtəda, X xəbər, Tvs vasitəsiz tamamlıq, Tvl vasitəli tamamlıq, Ty təyin, Zr zərflik,
  - üzv deyil (köməkçi nitq hissələri, modal sözlər, nida, müraciət), ? mübahisəli (belə cümlələr üzv suallarında işlənmir).
Şərtlər: feili sifət, feili bağlama və məsdər tərkiblərinin daxilindəki sözlər tərkibin bütövlükdə daşıdığı üzvlə
işarələnir (məktəb qrammatikasında tərkib bir üzv sayılır). Qoşma qoşulduğu sözlə birlikdə bir üzv olur.
"""
import re

RAW = {
    9: """
Dünən{Z.zaman|Zr} biz{Ə.şəxs|M} qədim{S|Ty} qalaya{İ:yö|Zr} qədər{Q:yö|Zr} piyada{Z.tərz|Zr} getdik{F|X}.
Əlbəttə{Mod|-}, sən{Ə.şəxs|M} bu{Ə.işarə|Ty} kitabı{İ:t|Tvs} oxumalısan{F|X}.
Ay{N|-} uşaqlar{İ:a|-}, dərhal{Z.zaman|Zr} sinfə{İ:yö|Zr} qayıdın{F|X}!
Anam{İ:a|M} bazardan{İ:ç|Zr} beş{Say.mq|Ty} alma{İ:a|Tvs} aldı{F|X}.
Yeddinci{Say.sr|Ty} sinfin{İ:y|Ty} şagirdləri{İ:a|M} muzeyə{İ:yö|Zr} getdilər{F|X}.
Qardaşım{İ:a|M} məktəbdən{İ:ç|Zr} sonra{Q:ç|Zr} kitabxanaya{İ:yö|Zr} gedir{F|X}.
O{Ə.şəxs|M}, dostu{İ:a|Tvl} ilə{Q:a|Tvl} parkda{İ:yer|Zr} gəzirdi{F|X}.
Əli{İ:a|M} ilə{B.tbsz|-} Vəli{İ:a|M} bu{Ə.işarə|Ty} məktəbdə{İ:yer|Zr} oxuyurlar{F|X}.
Həmin{Ə.işarə|Ty} axşam{İ:a|Zr} güclü{S|Ty} külək{İ:a|M} əsdi{F|X}.
Kim{Ə.sual|M} bu{Ə.işarə|Ty} məktubu{İ:t|Tvs} yazıb{F|X}?
Hər{Ə.təyini|Ty} şagird{İ:a|M} öz{Ə.qayıdış|Ty} dəftərini{İ:t|Tvs} götürdü{F|X}.
Heç_kim{Ə.inkar|M} bu{Ə.işarə|Ty} tapmacanı{İ:t|Tvs} tapmadı{F|X}.
Kimsə{Ə.qm|M} qapını{İ:t|Tvs} yavaşca{Z.tərz|Zr} döydü{F|X}.
Biz{Ə.şəxs|M} yay{İ:a|Ty} tətilində{İ:yer|Zr} dənizə{İ:yö|Zr} getdik{F|X}.
Nənəm{İ:a|M} nəvələrinə{İ:yö|Tvl} maraqlı{S|Ty} nağıllar{İ:a|Tvs} danışırdı{F|X}.
Təəssüf_ki{Mod|-}, qatar{İ:a|M} vaxtında{İ:yer|Zr} gəlmədi{F|X}.
Oxuyan{FS|Ty} uşaq{İ:a|M} başını{İ:t|Tvs} kitabdan{İ:ç|Zr} qaldırdı{F|X}.
Qız{İ:a|M} gülə-gülə{FB|Zr} otağa{İ:yö|Zr} girdi{F|X}.
Dərsə{İ:yö|Zr} gecikməmək{Məs|Zr} üçün{Q:a|Zr} evdən{İ:ç|Zr} erkən{Z.zaman|Zr} çıxdım{F|X}.
Yağış{İ:a|Zr} yağanda{FB|Zr} uşaqlar{İ:a|M} evə{İ:yö|Zr} qaçdılar{F|X}.
Axı{Əd|-} sən{Ə.şəxs|M} bunu{Ə.işarə:t|Tvs} bilirdin{F|X}.
Hətta{Əd|-} kiçik{S|Ty} uşaqlar{İ:a|M} bu{Ə.işarə|Ty} mahnını{İ:t|Tvs} bilirdi{F|X}.
Yalnız{Əd|-} Leyla{İ:a|M} tapşırığı{İ:t|Tvs} vaxtında{İ:yer|Zr} bitirdi{F|X}.
Qoy{Əd|-} uşaqlar{İ:a|M} həyətdə{İ:yer|Zr} oynasınlar{F|X}.
Ura{N|-}, komandamız{İ:a|M} kuboku{İ:t|Tvs} qazandı{F|X}!
Afərin{N|-}, sən{Ə.şəxs|M} bütün{Ə.təyini|Ty} tapmacaları{İ:t|Tvs} tapdın{F|X}!
Şübhəsiz{Mod|-}, bu{Ə.işarə|Ty} il{İ:a|Zr} məhsul{İ:a|M} bol{S|X} olacaq{F|X}.
Bu{Ə.işarə|Ty} kitabı{İ:t|Tvs} mənə{Ə.şəxs:yö|Tvl} dostum{İ:a|M} bağışladı{F|X}.
Siz{Ə.şəxs|M} nə{Ə.sual|Tvs} oxuyursunuz{F|X}?
Neçə{Ə.sual|Ty} şagird{İ:a|M} yarışa{İ:yö|Tvl} qatıldı{F|X}?
Üçdə_bir{Say.kəsr|Ty} hissəni{İ:t|Tvs} qardaşıma{İ:yö|Tvl} verdim{F|X}.
Beş-altı{Say.tx|Ty} quş{İ:a|M} budağa{İ:yö|Zr} qondu{F|X}.
Yarım{Say.kəsr|Ty} çörəyi{İ:t|Tvs} quşlara{İ:yö|Tvl} verdi{F|X}.
Axşamüstü{Z.zaman|Zr} səmada{İ:yer|Zr} parlaq{S|Ty} ulduzlar{İ:a|M} göründü{F|X}.
Bağçada{İ:yer|Zr} qırmızı{S|Ty} və{B.tbsz|-} sarı{S|Ty} güllər{İ:a|M} açmışdı{F|X}.
Müəllim{İ:a|M} lövhəyə{İ:yö|Zr} iki{Say.mq|Ty} misal{İ:a|Tvs} yazdı{F|X}.
O{Ə.şəxs|M}, quş{İ:a|Zr} kimi{Q:a|Zr} oxuyur{F|X}.
Atam{İ:a|M} işdən{İ:ç|Zr} gec{Z.zaman|Zr} qayıtdı{F|X}.
Biz{Ə.şəxs|M} dənizə{İ:yö|Zr} doğru{Q:yö|Zr} irəlilədik{F|X}.
Uşaqlar{İ:a|M} meşəyə{İ:yö|Zr} tərəf{Q:yö|Zr} qaçdılar{F|X}.
Səhərdən{İ:ç|Zr} bəri{Q:ç|Zr} yağış{İ:a|M} yağır{F|X}.
Bu{Ə.işarə|Ty} hədiyyəni{İ:t|Tvs} sənin{Ə.şəxs:y|Tvl} üçün{Q:y|Tvl} almışam{F|X}.
Doğrudan_da{Mod|-}, bu{Ə.işarə|Ty} film{İ:a|M} maraqlıdır{S|X}.
Deməli{Mod|-}, siz{Ə.şəxs|M} sabah{Z.zaman|Zr} Bakıya{İ:yö|Zr} gedirsiniz{F|X}.
Gəncə{İ:a|M} qədim{S|Ty} şəhərdir{İ:a|X}.
Sən{Ə.şəxs|M} ya{B.tbsz|-} çay{İ:a|Tvs}, ya_da{B.tbsz|-} şirə{İ:a|Tvs} iç{F|X}.
Həm{B.tbsz|-} atam{İ:a|M}, həm_də{B.tbsz|-} anam{İ:a|M} bu{Ə.işarə|Ty} xəbərə{İ:yö|Tvl} sevindi{F|X}.
Nə{B.tbsz|-} qar{İ:a|M}, nə_də{B.tbsz|-} yağış{İ:a|M} yağdı{F|X}.
Biz{Ə.şəxs|M} əvvəlcə{Z.zaman|Zr} dərsimizi{İ:t|Tvs} oxuduq{F|X}, sonra{Z.zaman|Zr} oynadıq{F|X}.
Dərsdən{İ:ç|Zr} əvvəl{Q:ç|Zr} müəllim{İ:a|M} jurnalı{İ:t|Tvs} yoxladı{F|X}.
Ancaq{Əd|-} sən{Ə.şəxs|M} mənə{Ə.şəxs:yö|Tvl} inanırsan{F|X}.
O{Ə.işarə|Ty} kitabı{İ:t|Tvs} rəfə{İ:yö|Zr} qoy{F|X}.
O{Ə.şəxs|M}, kitabı{İ:t|Tvs} rəfə{İ:yö|Zr} qoydu{F|X}.
Uşaqlar{İ:a|M} yuxarı{Z.yer|Zr} qalxdılar{F|X}.
Babam{İ:a|M} bizə{Ə.şəxs:yö|Tvl} iki{Say.mq|Ty} quzu{İ:a|Tvs} bağışladı{F|X}.
Ah{N|-}, mən{Ə.şəxs|M} açarı{İ:t|Tvs} evdə{İ:yer|Zr} unutmuşam{F|X}!
Ey{N|-} dostlar{İ:a|-}, bura{Ə.işarə|Zr} gəlin{F|X}!
Vay{N|-}, stəkan{İ:a|M} sındı{F|X}!
Of{N|-}, mən{Ə.şəxs|M} yoruldum{F|X}.
Əhsən{N|-}, siz{Ə.şəxs|M} bu{Ə.işarə|Ty} yarışı{İ:t|Tvs} uddunuz{F|X}!
Qardaşım{İ:a|M} və{B.tbsz|-} bacım{İ:a|M} kinoya{İ:yö|Zr} getdilər{F|X}.
Mən{Ə.şəxs|M} çay{İ:a|Tvs} və{B.tbsz|-} peçenye{İ:a|Tvs} aldım{F|X}.
Sabah{Z.zaman|Zr} yaxud{B.tbsz|-} birigün{Z.zaman|Zr} Bakıya{İ:yö|Zr} gedəcəyik{F|X}.
Atam{İ:a|M} qəzet{İ:a|Tvs} və{B.tbsz|-} jurnal{İ:a|Tvs} oxuyur{F|X}.
Məhz{Əd|-} sən{Ə.şəxs|M} bu{Ə.işarə|Ty} işi{İ:t|Tvs} bacararsan{F|X}.
Bəs{Əd|-} siz{Ə.şəxs|M} sabah{Z.zaman|Zr} gəlmirsiniz{F|X}?
Qoy{Əd|-} Anar{İ:a|M} bu{Ə.işarə|Ty} şeiri{İ:t|Tvs} oxusun{F|X}.
Hətta{Əd|-} babam{İ:a|M} kompüterdə{İ:yer|Zr} oynayırdı{F|X}.
Səkkiz{Say.mq|Ty} şagird{İ:a|M} olimpiadaya{İ:yö|Tvl} qatıldı{F|X}.
Üçüncü{Say.sr|Ty} cərgədə{İ:yer|Zr} iki{Say.mq|Ty} boş{S|Ty} yer{İ:a|M} qalmışdı{F|X}.
Gülümsəyən{FS|Ty} qız{İ:a|M} əlini{İ:t|Tvs} yellədi{F|X}.
Kitab{İ:a|Tvs} oxumağı{Məs:t|Tvs} sevirəm{F|X}.
Evə{İ:yö|Zr} çatanda{FB|Zr} anam{İ:a|M} məni{Ə.şəxs:t|Tvs} qarşıladı{F|X}.
Sınan{FS|Ty} oyuncağı{İ:t|Tvs} atam{İ:a|M} düzəltdi{F|X}.
Bəlkə{Mod|-}, biz{Ə.şəxs|M} sabah{Z.zaman|Zr} dənizə{İ:yö|Zr} gedək{F|X}.
Yəqin{Mod|-}, qonaqlar{İ:a|M} yorulublar{F|X}.
Biz{Ə.şəxs|M} axşama{İ:yö|Zr} qədər{Q:yö|Zr} oynadıq{F|X}.
Uşaqlar{İ:a|M} ucadan{Z.tərz|Zr} güldülər{F|X}.
Gözəl{S|Ty} və{B.tbsz|-} geniş{S|Ty} otaqda{İ:yer|Zr} qonaqlar{İ:a|M} oturmuşdular{F|X}.
""",
    10: """
Gələn{FS|Ty} həftə{İ:a|Zr} sinfimiz{İ:a|M} təbiət{İ:a|Ty} muzeyinə{İ:yö|Zr} gedəcək{F|X}.
Yəqin{Mod|-}, siz{Ə.şəxs|M} bu{Ə.işarə|Ty} xəbəri{İ:t|Tvs} dünən{Z.zaman|Zr} eşitmisiniz{F|X}.
Kitabxanadan{İ:ç|Ty} götürdüyüm{FS|Ty} kitabları{İ:t|Tvs} vaxtında{İ:yer|Zr} qaytardım{F|X}.
Ucadan{Z.tərz|Ty} gülən{FS|Ty} uşaqlar{İ:a|M} müəllimi{İ:t|Zr} görüb{FB|Zr} susdular{F|X}.
Xoşbəxtlikdən{Mod|-}, yaralı{S|Ty} quşu{İ:t|Tvs} vaxtında{İ:yer|Zr} həkimə{İ:yö|Tvl} çatdırdıq{F|X}.
Uşaq{İ:a|M} vazanı{İ:t|Tvs} bilərəkdən{Z.məqsəd|Zr} sındırmamışdı{F|X}.
Səkkizinci{Say.sr|Ty} mərtəbədə{İ:yer|Ty} yaşayan{FS|Ty} qonşumuz{İ:a|M} hər{Ə.təyini|Ty} səhər{İ:a|Zr} parkda{İ:yer|Zr} qaçır{F|X}.
Üç-dörd{Say.tx|Ty} günə{İ:yö|Zr} qədər{Q:yö|Zr} işimizi{İ:t|Tvs} bitirəcəyik{F|X}.
Tortun{İ:y|Ty} dörddə_birini{Say.kəsr:t|Tvs} qonaqlara{İ:yö|Tvl} verdik{F|X}.
Ay{N|-} qızım{İ:a|-}, bu{Ə.işarə|Ty} sözləri{İ:t|Tvs} kimdən{Ə.sual:ç|Tvl} eşitdin{F|X}?
Bu{Ə.işarə|Ty} məktubu{İ:t|Tvs} özüm{Ə.qayıdış|M} yazacağam{F|X}.
Heç_nə{Ə.inkar|Zr} demədən{FB|Zr} otaqdan{İ:ç|Zr} çıxdı{F|X}.
Kimsə{Ə.qm|M} həyətdə{İ:yer|Zr} ucadan{Z.tərz|Zr} mahnı{İ:a|Tvs} oxuyurdu{F|X}.
Hansı{Ə.sual|Ty} şəhərdə{İ:yer|Zr} doğulmusan{F|X}?
Oxumaq{Məs|M} insanı{İ:t|Tvs} zənginləşdirir{F|X}.
Mən{Ə.şəxs|M} üzməyi{Məs:t|Tvs} yayda{İ:yer|Zr} öyrəndim{F|X}.
Dostcasına{Z.tərz|Ty} gülümsəyən{FS|Ty} satıcı{İ:a|M} bizə{Ə.şəxs:yö|Tvl} təzə{S|Ty} meyvə{İ:a|Tvs} uzatdı{F|X}.
Ehtimal_ki{Mod|-}, qonaqlar{İ:a|M} axşama{İ:yö|Zr} kimi{Q:yö|Zr} gələcəklər{F|X}.
Biz{Ə.şəxs|M} çayın{İ:y|Ty} sahili{İ:a|Zr} ilə{Q:a|Zr} xeyli{Z.kəm|Zr} getdik{F|X}.
Qardaşım{İ:a|M} məktubu{İ:t|Tvs} qələm{İ:a|Tvl} ilə{Q:a|Tvl} yazdı{F|X}.
Anam{İ:a|M} ilə{B.tbsz|-} atam{İ:a|M} toya{İ:yö|Zr} getdilər{F|X}.
Ən{Əd|-} çətin{S|Ty} sualları{İ:t|Tvs} hətta{Əd|-} kiçik{S|Ty} qardaşım{İ:a|M} tapdı{F|X}.
Məhz{Əd|-} bu{Ə.işarə|Ty} kənddə{İ:yer|Zr} böyük{S|Ty} şair{İ:a|M} doğulub{F|X}.
Bəs{Əd|-} sən{Ə.şəxs|M} hara{Ə.sual|Zr} gedirsən{F|X}?
Of{N|-}, bu{Ə.işarə|Ty} çanta{İ:a|M} ağırdır{S|X}!
Ey{N|-} gənclər{İ:a|-}, Vətəni{İ:t|Tvs} sevin{F|X}!
Əhsən{N|-}! Bu{Ə.işarə|Ty} rəsmi{İ:t|Tvs} kim{Ə.sual|M} çəkib{F|X}?
Dərslərini{İ:t|Zr} oxumadan{FB|Zr} oynamağa{Məs:yö|Zr} getdi{F|X}.
Qatar{İ:a|Zr} stansiyaya{İ:yö|Zr} çatan_kimi{FB|Zr} sərnişinlər{İ:a|M} vaqonlardan{İ:ç|Zr} düşdülər{F|X}.
Yarışa{İ:yö|Tvl} on_səkkiz{Say.mq|Ty} komanda{İ:a|M} qatıldı{F|X}.
Uşaq{İ:a|M} şirniyyatı{İ:t|Tvs} gizlicə{Z.tərz|Zr} yedi{F|X}.
Biz{Ə.şəxs|M} dağın{İ:y|Ty} zirvəsinə{İ:yö|Zr} doğru{Q:yö|Zr} yuxarı{Z.yer|Zr} qalxdıq{F|X}.
Yağışa{İ:yö|Zr} görə{Q:yö|Zr} oyun{İ:a|M} dayandırıldı{F|X}.
Bacım{İ:a|M} məndən{Ə.şəxs:ç|Tvl} kitab{İ:a|Tvs} istədi{F|X}.
Həm{B.tbsz|-} riyaziyyatı{İ:t|Tvs}, həm_də{B.tbsz|-} fizikanı{İ:t|Tvs} sevirəm{F|X}.
Ya{B.tbsz|-} sabah{Z.zaman|Zr}, ya_da{B.tbsz|-} birigün{Z.zaman|Zr} gələcəyəm{F|X}.
Sözsüz{Mod|-}, sizin{Ə.şəxs:y|Ty} əməyiniz{İ:a|M} qiymətləndiriləcək{F|X}.
Bir_sözlə{Mod|-}, hamı{Ə.təyini|M} məmnun{S|X} qaldı{F|X}.
Qəhrəmancasına{Z.tərz|Ty} vuruşan{FS|Ty} əsgərlər{İ:a|M} düşməni{İ:t|Tvs} geri{Z.yer|Zr} oturtdular{F|X}.
O{Ə.şəxs|M}, ikinci{Say.sr|Ty} dəfə{İ:a|Zr} bu{Ə.işarə|Ty} şəhərə{İ:yö|Zr} gəlir{F|X}.
Biz{Ə.şəxs|M} stansiyada{İ:yer|Zr} qatarı{İ:t|Tvs} xeyli{Z.kəm|Zr} gözlədik{F|X}.
Səndən{Ə.şəxs:ç|?} başqa{Q:ç|?} hamı{Ə.təyini|M} gəldi{F|X}.
Ah{N|-}, köhnə{S|Ty} dostumu{İ:t|Tvs} uzun{S|Ty} müddət{İ:a|Zr} görmədim{F|X}!
Ura{N|-}, bayram{İ:a|M} gəldi{F|X}!
Vay{N|-}, buzlu{S|Ty} yolda{İ:yer|Zr} maşın{İ:a|M} sürüşdü{F|X}!
Ay{N|-} Leyla{İ:a|-}, pəncərəni{İ:t|Tvs} bağla{F|X}!
Bağda{İ:yer|Zr} alma{İ:a|M}, armud{İ:a|M} və{B.tbsz|-} heyva{İ:a|M} yetişmişdi{F|X}.
Həm{B.tbsz|-} oxuyur{F|X}, həm_də{B.tbsz|-} işləyir{F|X}.
Sən{Ə.şəxs|M} ya{B.tbsz|-} rəsm{İ:a|Tvs}, ya_da{B.tbsz|-} musiqi{İ:a|Tvs} seç{F|X}.
Yalnız{Əd|-} zəhmət{İ:a|M} insanı{İ:t|Tvs} ucaldır{F|X}.
Axı{Əd|-} biz{Ə.şəxs|M} bu{Ə.işarə|Ty} yolu{İ:t|Tvs} tanımırıq{F|X}.
Qoy{Əd|-} hamı{Ə.təyini|M} bu{Ə.işarə|Ty} həqiqəti{İ:t|Tvs} bilsin{F|X}.
Bu{Ə.işarə|M}, lap{Əd|-} yeni{S|Ty} maşındır{İ:a|X}.
Biz{Ə.şəxs|M} iki-üç{Say.tx|Ty} saat{İ:a|Zr} gözlədik{F|X}.
Onuncu{Say.sr|Ty} sinfin{İ:y|Ty} şagirdləri{İ:a|M} teatra{İ:yö|Zr} getdilər{F|X}.
Əlbəttə{Mod|-}, biz{Ə.şəxs|M} sizə{Ə.şəxs:yö|Tvl} inanırıq{F|X}.
Təəssüf_ki{Mod|-}, mən{Ə.şəxs|M} toya{İ:yö|Zr} getmədim{F|X}.
Atam{İ:a|M} mənim{Ə.şəxs:y|Tvl} üçün{Q:y|Tvl} velosiped{İ:a|Tvs} aldı{F|X}.
Biz{Ə.şəxs|M} sizdən{Ə.şəxs:ç|Zr} sonra{Q:ç|Zr} gəldik{F|X}.
Yazılmış{FS|Ty} məktubu{İ:t|Tvs} poçta{İ:yö|Zr} apardım{F|X}.
Danışmaq{Məs|M} asandır{S|X}.
Mahnı{İ:a|Zr} oxuya-oxuya{FB|Zr} işləyirdi{F|X}.
Sərnişinlər{İ:a|M} avtobusa{İ:yö|Zr} dalbadal{Z.tərz|Zr} mindilər{F|X}.
""",
    11: """
Şübhəsiz{Mod|-}, kitabxanadan{İ:ç|Ty} götürdüyümüz{FS|Ty} nadir{S|Ty} əlyazmaları{İ:t|Tvs} sabah{Z.zaman|Zr} geri{Z.yer|Zr} qaytaracağıq{F|X}.
Ay{N|-} müəllim{İ:a|-}, dünən{Z.zaman|Ty} sizin{Ə.şəxs:y|Ty} danışdığınız{FS|Ty} hadisəni{İ:t|Tvs} heç_kim{Ə.inkar|M} unutmayacaq{F|X}.
Ehtimal_ki{Mod|-}, iki{Say.mq|Ty} həftədən{İ:ç|Ty} sonra{Q:ç|Ty} başlayacaq{FS|Ty} müsabiqədə{İ:yer|Zr} on_iki{Say.mq|Ty} ölkənin{İ:y|Ty} təmsilçiləri{İ:a|M} yarışacaq{F|X}.
Dağların{İ:y|Ty} ətəyində{İ:yer|Ty} yerləşən{FS|Ty} bu{Ə.işarə|Ty} kiçik{S|Ty} kənddə{İ:yer|Zr} qədim{S|Ty} adətlər{İ:a|M} yaşadılır{F|X}.
Təəssüf_ki{Mod|-}, ötən{FS|Ty} il{İ:a|Ty} əkdiyimiz{FS|Ty} fidanların{İ:y|Ty} üçdə_biri{Say.kəsr|M} quruyub{F|X}.
Ey{N|-} gənclər{İ:a|-}, ata-babalarımızdan{İ:ç|Ty} qalan{FS|Ty} bu{Ə.işarə|Ty} müqəddəs{S|Ty} torpağı{İ:t|Tvs} göz{İ:a|Ty} bəbəyi{İ:a|Zr} kimi{Q:a|Zr} qoruyun{F|X}!
Gülə-gülə{FB|Ty} içəri{Z.yer|Ty} girən{FS|Ty} qızlar{İ:a|M} müəllimi{İ:t|Zr} görcək{FB|Zr} susdular{F|X}.
Məncə{Mod|-}, bu{Ə.işarə|Ty} məsələni{İ:t|Tvs} yalnız{Əd|-} siz{Ə.şəxs|M} bizə{Ə.şəxs:yö|Tvl} anladarsınız{F|X}.
Fəhlələr{İ:a|M} səhərdən{İ:ç|Zr} axşama{İ:yö|Zr} qədər{Q:yö|Zr} dayanmadan{FB|Zr} işlədilər{F|X}.
Doğrudan_da{Mod|-}, sevdiyi{FS|Ty} işi{İ:t|Ty} görən{FS|Ty} insan{İ:a|M} yorulmur{F|X}.
Nənəmin{İ:y|Ty} bişirdiyi{FS|Ty} plovun{İ:y|Ty} ətri{İ:a|M} bütün{Ə.təyini|Ty} evə{İ:yö|Zr} yayılmışdı{F|X}.
Afərin{N|-}, sən{Ə.şəxs|M} yarışda{İ:yer|Zr} birinci{Say.sr|Ty} yeri{İ:t|Tvs} tutdun{F|X}!
Kimin{Ə.sual:y|Ty} əlyazmasını{İ:t|Tvs} muzeyə{İ:yö|Tvl} verdiniz{F|X}?
Hər_kəs{Ə.təyini|M} öz{Ə.qayıdış|Ty} fikrini{İ:t|Tvs} yazsın{F|X}.
Axı{Əd|-} siz{Ə.şəxs|M} bu{Ə.işarə|Ty} kitabı{İ:t|Tvs} oxumamısınız{F|X}.
Qoy{Əd|-} gələcək{FS|Ty} nəsillər{İ:a|M} bu{Ə.işarə|Ty} qəhrəmanlığı{İ:t|Tvs} unutmasınlar{F|X}.
Bəlkə{Mod|-}, biz{Ə.şəxs|M} son{S|Ty} qatara{İ:yö|Tvl} çatmayacağıq{F|X}.
Görünür{Mod|-}, yağış{İ:a|M} səhərə{İ:yö|Zr} kimi{Q:yö|Zr} dayanmayacaq{F|X}.
Vay{N|-}, pəncərənin{İ:y|Ty} şüşəsi{İ:a|M} küləkdən{İ:ç|Zr} sındı{F|X}!
Qardaşım{İ:a|M} həm{B.tbsz|-} rəssam{İ:a|X}, həm_də{B.tbsz|-} musiqiçidir{İ:a|X}.
Nə{B.tbsz|-} atam{İ:a|M}, nə_də{B.tbsz|-} anam{İ:a|M} bu{Ə.işarə|Ty} xəbəri{İ:t|Tvs} eşitmişdi{F|X}.
Mən{Ə.şəxs|M} səni{Ə.şəxs:t|Tvs} öz{Ə.qayıdış|Ty} qardaşım{İ:a|Zr} kimi{Q:a|Zr} sevirəm{F|X}.
Doğma{S|Ty} yurduna{İ:yö|Ty} qayıdan{FS|Ty} qaçqınlar{İ:a|M} müharibədən{İ:ç|Zr} sonra{Q:ç|Zr} yeni{S|Ty} evlər{İ:a|Tvs} tikdilər{F|X}.
Babam{İ:a|M} təkbaşına{Z.tərz|Tvs} dağa{İ:yö|Tvs} çıxmağı{Məs:t|Tvs} sevirdi{F|X}.
Uşaqlar{İ:a|M} sakitcə{Z.tərz|Zr} nağılı{İ:t|Tvs} dinləyirdilər{F|X}.
Bayram{İ:a|Ty} süfrəsinin{İ:y|Ty} başında{İ:yer|Zr} uşaqlar{İ:a|M} yan-yana{Z.tərz|Zr} oturmuşdular{F|X}.
Xalqımızın{İ:y|Ty} yetirdiyi{FS|Ty} dahi{S|Ty} şəxsiyyətlər{İ:a|M} dünya{İ:a|Ty} mədəniyyətinə{İ:yö|Tvl} böyük{S|Ty} töhfələr{İ:a|Tvs} veriblər{F|X}.
Beşinci{Say.sr|Ty} sinifdən{İ:ç|Zr} bəri{Q:ç|Zr} Anar{İ:a|M} şahmat{İ:a|Ty} dərnəyinə{İ:yö|Zr} gedir{F|X}.
Kiçik{S|Ty} qardaşımdan{İ:ç|?} savayı{Q:ç|?} hamı{Ə.təyini|M} imtahandan{İ:ç|?} keçdi{F|X}.
Uzun{S|Ty} illər{İ:a|Ty} xaricdə{İ:yer|Ty} yaşayan{FS|Ty} alim{İ:a|M} doğma{S|Ty} Vətənə{İ:yö|Zr} qayıtdı{F|X}.
Tələbələr{İ:a|M} mühazirəni{İ:t|Zr} dinləyə-dinləyə{FB|Zr} qeydlər{İ:a|Tvs} aparırdılar{F|X}.
Əlbəttə{Mod|-}, ana{İ:a|M} dilini{İ:t|M} qorumaq{Məs|M} vətəndaşlıq{İ:a|Ty} borcudur{İ:a|X}.
Ay{N|-} bala{İ:a|-}, kitablarını{İ:t|Tvs} rəfə{İ:yö|Zr} yığ{F|X}.
Gördüyünüz_kimi{Mod|-}, bütün{Ə.təyini|Ty} sənədlər{İ:a|M} hazırdır{S|X}.
Rəqib{İ:a|M} topu{İ:t|Tvs} qəsdən{Z.məqsəd|Zr} kənara{İ:yö|Zr} vurdu{F|X}.
Bu{Ə.işarə|Ty} işi{İ:t|Tvs} üç{Say.mq|Ty} nəfər{İ:a|M} bir{Say.mq|Ty} həftəyə{İ:yö|Zr} gördü{F|X}.
Biz{Ə.şəxs|M} qatarı{İ:t|Tvs} stansiyada{İ:yer|Zr} xeyli{Z.kəm|Zr} gözlədik{F|X}.
Ura{N|-}, uzun{S|Ty} illər{İ:a|Ty} gözlədiyimiz{FS|Ty} qələbə{İ:a|M} gəldi{F|X}!
Ah{N|-}, gəncliyimdə{İ:yer|Zr} bu{Ə.işarə|Ty} imkanlar{İ:a|M} olsaydı{F|X}!
Ey{N|-} Vətən{İ:a|-}, sənin{Ə.şəxs:y|Ty} hər{Ə.təyini|Ty} qarış{İ:a|Ty} torpağın{İ:a|M} müqəddəsdir{S|X}!
Əhsən{N|-}, bu{Ə.işarə|Ty} çətin{S|Ty} yarışda{İ:yer|Zr} hamını{Ə.təyini:t|Tvs} qabaqladın{F|X}!
Of{N|-}, bu{Ə.işarə|Ty} bitib-tükənməyən{FS|Ty} yol{İ:a|M} məni{Ə.şəxs:t|Tvs} yordu{F|X}!
Şairin{İ:y|Ty} şeirləri{İ:a|M} həm{B.tbsz|-} ölkəmizdə{İ:yer|Zr}, həm_də{B.tbsz|-} xaricdə{İ:yer|Zr} sevilir{F|X}.
Gənclər{İ:a|M} nə{B.tbsz|-} çətinlikdən{İ:ç|Tvl}, nə_də{B.tbsz|-} yorğunluqdan{İ:ç|Tvl} qorxurdular{F|X}.
Muzeydə{İ:yer|Zr} qədim{S|Ty} qılınclar{İ:a|M}, qalxanlar{İ:a|M} və{B.tbsz|-} zirehlər{İ:a|M} nümayiş_etdirilir{F|X}.
Siz{Ə.şəxs|M} ya{B.tbsz|-} tarixi{S|Ty} romanı{İ:t|Tvs}, ya_da{B.tbsz|-} elmi{S|Ty} əsəri{İ:t|Tvs} təhlil_edin{F|X}.
Hətta{Əd|-} ən{Əd|-} təcrübəli{S|Ty} alpinistlər{İ:a|M} bu{Ə.işarə|Tvl} zirvəyə{İ:yö|Tvl} qalxmaqdan{Məs:ç|Tvl} çəkinirdilər{F|X}.
Məhz{Əd|-} bu{Ə.işarə|Ty} hadisədən{İ:ç|Zr} sonra{Q:ç|Zr} onun{Ə.şəxs:y|Ty} həyatı{İ:a|M} dəyişdi{F|X}.
Bəs{Əd|-} siz{Ə.şəxs|M} hansı{Ə.sual|Ty} universitetə{İ:yö|Zr} sənəd{İ:a|Tvs} vermisiniz{F|X}?
Yarışda{İ:yer|Zr} iyirmi_yeddi{Say.mq|Ty} ölkənin{İ:y|Ty} idmançıları{İ:a|M} iştirak_etdi{F|X}.
Kitabın{İ:y|Ty} üçüncü{Say.sr|Ty} fəslini{İ:t|Tvs} iki-üç{Say.tx|Ty} dəfə{İ:a|Zr} oxudum{F|X}.
Deməli{Mod|-}, bütün{Ə.təyini|Ty} çətinliklər{İ:a|M} arxada{İ:yer|Zr} qaldı{F|X}.
Karvan{İ:a|M} dənizə{İ:yö|Zr} sarı{Q:yö|Zr} irəliləyirdi{F|X}.
Nağılı{İ:t|Zr} dinləyərkən{FB|Zr} uşaqlar{İ:a|M} bir-bir{Z.tərz|Zr} yatdılar{F|X}.
Alim{İ:a|M} bu{Ə.işarə|Ty} problemi{İ:t|Tvs} təkbaşına{Z.tərz|Zr} araşdırdı{F|X}.
Sinfimizin{İ:y|Ty} ən{Əd|-} çalışqan{S|Ty} şagirdi{İ:a|M} beşdə_dörd{Say.kəsr|Ty} hissəni{İ:t|Tvs} təkbaşına{Z.tərz|Zr} həll_etdi{F|X}.
""",
}

TOK = re.compile(r"(\S+?)\{([^}|]+)\|([^}]+)\}")


class Tok:
    __slots__ = ("w", "pos", "sub", "case", "role")

    def __init__(self, w, tag, role):
        self.w = w.replace("_", " ")
        m = re.match(r"^([^.:]+)(?:\.([^:]+))?(?::(.+))?$", tag)
        self.pos, self.sub, self.case = m.group(1), m.group(2), m.group(3)
        self.role = role


POS_ALL = {"İ", "S", "Say", "Ə", "F", "FS", "FB", "Məs", "Z", "Q", "B", "Əd", "Mod", "N"}
ROLES = {"M", "X", "Tvs", "Tvl", "Ty", "Zr", "-", "?"}


class Sent:
    def __init__(self, raw, grade):
        self.grade = grade
        self.toks = [Tok(w, t, r) for w, t, r in TOK.findall(raw)]
        self.text = TOK.sub(lambda m: m.group(1), raw).replace("_", " ").strip()
        for t in self.toks:
            if t.pos not in POS_ALL or t.role not in ROLES:
                raise ValueError(f"naməlum işarə: {t.w} {t.pos} {t.role} — {self.text}")
        self.doubt = any(t.role == "?" for t in self.toks)
        self.words = [t.w.lower() for t in self.toks]

    def n(self, pos, sub=None, case=None, role=None):
        return sum(1 for t in self.toks if t.pos == pos and (sub is None or t.sub == sub)
                   and (case is None or t.case == case) and (role is None or t.role == role))

    def roles(self):
        return {t.role for t in self.toks}

    def role_pos(self, role):
        return {t.pos for t in self.toks if t.role == role}


def load():
    out = {}
    for g, raw in RAW.items():
        lines = [ln.strip() for ln in raw.strip().splitlines() if ln.strip()]
        out[g] = [Sent(ln, g) for ln in lines]
        # sintaksis yoxlaması: hər sözün işarəsi var
        for s, ln in zip(out[g], lines):
            plain = re.sub(r"\{[^}]*\}", "", ln)
            words = re.findall(r"[A-Za-zÇçƏəĞğİıÖöŞşÜü_\-]+", plain)
            if len(words) != len(s.toks):
                raise ValueError(f"işarəsiz söz: {ln}")
    return out


CORPUS = load()
