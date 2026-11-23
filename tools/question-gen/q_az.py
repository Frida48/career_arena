"""Azərbaycan dili sual bankı: 9, 10, 11-ci siniflər × 18 mövzu × 90 sual (3 quiz × 30 sual).

Bölmələr: Fonetika (səs və hərf — fonetik təhlil, orfoqrafiya — transkripsiyadan yazılış), Leksika (sinonim, antonim,
omonim; frazeologizmlər), Əsas nitq hissələri (6), Köməkçi nitq hissələri (5), Sintaksis (cümlə üzvləri, mürəkkəb cümlə),
Durğu işarələri.
- 9-cu sinif: çətin (2 şərt); 10-cu sinif: orta və çətin (2–3 şərt); 11-ci sinif: çox çətin (3–4 şərt).
- Hər sualda şərt 5 variantın hamısında işarələrə/qaydalara görə yenidən yoxlanır: düz bir variant ödəməlidir.
- Hər sinfin sualları ayrıdır (öz korpusu, mətn + variantlar siniflər arasında təkrarlanmır).

İşə salmaq:  python3 q_az.py
"""
from azbuild import build
from quiz import save_grade
import az_phon
import az_lex
import az_pos
import az_synt

SEED = 2026
ORDER = ["aze-sound", "aze-orth", "aze-syn", "aze-idiom",
         "aze-isim", "aze-sifet", "aze-say", "aze-evez", "aze-feil", "aze-zerf",
         "aze-qosma", "aze-bag", "aze-edat", "aze-modal", "aze-nida",
         "aze-member", "aze-complex", "aze-punct"]
ALL = {}
for d in (az_phon.PHON_TOPICS, az_lex.LEX_TOPICS, az_pos.POS_TOPICS, az_synt.SYNT_TOPICS):
    ALL.update(d)


def main():
    used = set()
    for g in (9, 10, 11):
        topics = {tid: build(g, tid, ALL[tid][g], SEED, used) for tid in ORDER}
        save_grade(g, "az", topics)


if __name__ == "__main__":
    main()
