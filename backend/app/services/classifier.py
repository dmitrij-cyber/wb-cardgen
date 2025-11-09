# Very light-weight heuristic classifier (MVP). Replace with ML later.
from collections import defaultdict

KEYWORDS = {
    "Одежда": ["футболка","кофта","платье","юбка","брюки","куртка","носки","джинсы","рубашка"],
    "Обувь": ["кроссовки","ботинки","сандалии","туфли","кеды"],
    "Аксессуары": ["сумка","ремень","кошелёк","очки","часы","рюкзак"],
    "Электроника": ["наушники","часы умные","смартфон","powerbank","колонка","планшет"],
    "Дом и кухня": ["чехол","сковорода","нож","подушка","простыня","полотенце","органайзер"],
    "Красота": ["косметичка","расчёска","щетка","маска","крем"],
}

def classify(title: str):
    title_l = title.lower()
    scores = defaultdict(int)
    for cat, words in KEYWORDS.items():
        for w in words:
            if w in title_l:
                scores[cat] += 1
    if scores:
        cat = max(scores, key=lambda k: scores[k])
        top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:3]
        top3 = [c for c,_ in top]
        return cat, 0.7, top3
    return "Прочее", 0.3, ["Прочее"]
