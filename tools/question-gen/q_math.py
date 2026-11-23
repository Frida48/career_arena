"""Riyaziyyat sual bankı: 9, 10, 11-ci siniflər.

- 9 və 11-ci sinif: bütün suallar çətin; 10-cu sinif: orta və çətin.
- 11-ci sinifdə suallar çoxaddımlıdır: düstura qoymazdan əvvəl ara hesablama tələb olunur.
- Hər sinfin sualları fərqlidir (mətnlər siniflər arasında təkrarlanmır).
- «Orta qiymət və moda» (stat-avg) 11-ci sinifdə yoxdur.
- Hər sualın cavabı iki dəfə hesablanır: düsturla (a) və müstəqil üsulla (chk — sadalama, koordinat,
  ədədi yoxlama). Uyğun gəlməsə generator dayanır (mx.check).
- Variantlar oxşardır: tipik səhvlərdən və düzgün cavaba yaxın qiymətlərdən qurulur, ədədi qiyməti eyni olan
  iki variant ola bilməz (məs. √12 və 2√3).
- Həndəsə suallarının bir hissəsində SVG çertyoj var (JSON-da «image» sahəsi).

İşə salmaq:  python3 q_math.py
"""
from mbuild import build
from quiz import save_grade
import m_num
import m_alg
import m_geo
import m_stat

SEED = 2026
ORDER = ["num-real", "num-frac", "num-pow", "num-abs", "num-pct",
         "alg-eq", "alg-sys", "alg-quad", "alg-prog", "alg-func",
         "geo-basic", "geo-poly", "geo-circle", "geo-trig",
         "stat-avg", "stat-prob"]

ALL = {}
for mod in (m_num, m_alg, m_geo, m_stat):
    ALL.update(mod.TOPICS)


def main():
    used = set()  # bütün siniflər üzrə mətnlər — siniflərin sualları fərqli olsun
    for g in (9, 10, 11):
        topics = {}
        for tid in ORDER:
            tpls = ALL[tid].get(g)
            if not tpls:
                continue
            topics[tid] = build(g, tid, tpls, SEED, used)
        save_grade(g, "math", topics)


if __name__ == "__main__":
    main()
