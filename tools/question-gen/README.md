# Sual bankının generatoru

`src/data/questions/*.json` faylları bu qovluqdakı skriptlərlə yaradılır. Bütün suallar DİM buraxılış imtahanı formatında yazılmış **orijinal** suallardır (DİM materiallarından köçürülməyib).

| Skript | Nə yaradır |
| --- | --- |
| `math9.py` | 9-cu sinif riyaziyyat — suallar şablonlardan kodla yaradılır, cavablar hesablanır |
| `az9.py` | 9-cu sinif Azərbaycan dili — əl ilə yazılmış suallar |
| `en9.py` | 9-cu sinif ingilis dili — əl ilə yazılmış suallar (Reading üçün orijinal mətnlər) |
| `validate.py` | hər bölmədə 30 sual, unikal id, 5 fərqli variant, cavab indeksi |

```bash
cd tools/question-gen
python3 math9.py && python3 az9.py && python3 en9.py
python3 validate.py
```

Python 3.10+ lazımdır, əlavə paket tələb olunmur. Riyaziyyat generatoru sabit `seed` ilə işləyir, ona görə hər dəfə eyni suallar çıxır.

## Sual formatı

- `type: "single"` — `options` (5 variant) və `correctIndex` (0–4)
- `type: "open"` — `answer` (rəqəm və ya ifadə, mətn kimi)
- Reading suallarında `passage` sahəsi var.

Tiplər: `src/data/questions/index.ts`.
