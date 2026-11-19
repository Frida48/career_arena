# Sual bankının generatoru

`src/data/questions/grade{9,10,11}-{math,az,en}.json` faylları bu qovluqdakı skriptlərlə yaradılır. Bütün suallar orijinaldır və orta-çətin səviyyədədir.

Quruluş: **sinif → mövzu → 3 quiz × 20 sual**. İstisna Reading-dir: **3 quiz × 10 sual**, hər quiz bir mətn.

| Fayl | Nə edir |
| --- | --- |
| `q_math.py` | Riyaziyyat, 16 mövzu. Şablonlardan kodla yaradılır, bütün cavablar hesablanır |
| `q_az.py` | Azərbaycan dili, 8 mövzu. Söz/cümlə bankları + `az_morph.py` qaydaları (ahəng, hallar, feil formaları) |
| `q_en.py` | İngilis dili, 5 mövzu. Feil cədvəli ilə zaman/şərt/məchul növ, söz yaradıcılığı və frazal feil bankları |
| `en_passages.py` | Reading mətnləri (hər sinif üçün 3 mətn × 10 sual) |
| `quiz.py` | Ümumi çərçivə: 60 unikal sual → 3 quiz (çətinlik qarışıq paylanır) |
| `common.py` | Formatlama, variantların qarışdırılması, Azərbaycan şəkilçiləri (3-cü, 6-cı, 2-yə…) |
| `validate.py` | Say, unikal id, 5 fərqli variant, cavab indeksi, çətinlik və təkrarların yoxlanması |

```bash
cd tools/question-gen
python3 q_math.py && python3 q_az.py && python3 q_en.py
python3 validate.py
```

Python 3.10+ lazımdır, əlavə paket tələb olunmur. Generatorlar sabit `seed` ilə işləyir, ona görə hər dəfə eyni suallar çıxır.

## Sual formatı

```json
{ "grade": 10, "subject": "math", "topics": [ { "topicId": "alg-quad", "quizzes": [[ { "id": "...", "difficulty": "hard", "text": "...", "type": "single", "options": ["…5 variant…"], "correctIndex": 2, "explanation": "..." } ]] } ] }
```

- `type: "single"` — `options` (5 variant) və `correctIndex` (0–4)
- `type: "open"` — `answer` (rəqəm və ya ifadə, mətn kimi)
- Reading suallarında `passage` sahəsi var.

Mövzu id-ləri `src/data/catalog.ts`-dəki ilə eynidir. Loader: `src/data/questions/index.ts`.
