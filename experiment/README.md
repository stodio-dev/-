# ניסוי הבנה: פרוזה מול CL

**שאלה:** האם מודל שקורא את אותו מידע ב-CL טועה פחות (או יותר) ממודל שקורא אותו בפרוזה? (סיכון R5 ב-`CHAT_HISTORY.md`)

## מה בתיקייה
| קובץ | תפקיד |
|---|---|
| `track-nl.md` | 8 תרחישים בפרוזה + 32 שאלות (מסלול NL) |
| `track-cl.md` | אותם 8 תרחישים ב-CL + אותן 32 שאלות (מסלול CL) |
| `scenarios/` | מקורות התרחישים (`sNN.cl`, `sNN.nl.md`), בלי שאלות |
| `results/` | כאן כל מודל כותב את התשובות שלו |
| `score.py` | חישוב ציונים מול מפתח התשובות |

מפתח התשובות **לא נמצא בריפו** (הריפו ציבורי). הוא נמסר למפעיל הניסוי בנפרד, ו-`.gitignore` חוסם העלאה בטעות.

## איך מריצים
כל הרצה: **צ'אט חדש** (בלי היסטוריה), מודל אחד, מסלול אחד. מומלץ **3 הרצות לפחות** לכל מודל ולכל מסלול. `<model>` הוא שם המודל באותיות קטנות בלי רווחים (למשל `claude-sonnet-5-5`), ו-`<N>` מספר ההרצה.

### פרומפט למסלול NL
```
You are a participant in a reading-comprehension experiment.
1. Read ONLY this file: https://raw.githubusercontent.com/stodio-dev/-/main/experiment/track-nl.md
2. Do not open any other file or page in the repository, do not search the web, and do not use any prior knowledge of this project.
3. Answer every question (s01.q1 through s08.q4) with exactly one letter A-E, based only on the documents in that file. Choose E only if the documents truly do not contain the answer.
4. Create the file experiment/results/<model>__nl__run<N>.md in the repository stodio-dev/- with exactly these lines:
model: <your model name>
track: nl
run: <N>
s01.q1: <letter>
s01.q2: <letter>
... (one line per question, up to s08.q4)
5. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

### פרומפט למסלול CL
```
You are a participant in a reading-comprehension experiment.
1. Read ONLY these three files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/track-cl.md
   https://raw.githubusercontent.com/stodio-dev/-/main/SPEC.md
   https://raw.githubusercontent.com/stodio-dev/-/main/lexicon.json
   The documents in track-cl.md are written in CL, a compact language defined by SPEC.md and lexicon.json.
2. Do not open any other file or page in the repository, do not search the web, and do not use any prior knowledge of this project.
3. Answer every question (s01.q1 through s08.q4) with exactly one letter A-E, based only on the documents in track-cl.md. Choose E only if the documents truly do not contain the answer.
4. Create the file experiment/results/<model>__cl__run<N>.md in the repository stodio-dev/- with exactly these lines:
model: <your model name>
track: cl
run: <N>
s01.q1: <letter>
s01.q2: <letter>
... (one line per question, up to s08.q4)
5. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

## ציון
אצל מפעיל הניסוי, עם מפתח התשובות מחוץ לריפו:
```
python3 experiment/score.py /path/to/answer-key.json experiment/results --out REPORT.md
```
הדוח כולל דיוק לכל מודל ומסלול, הפרש CL פחות NL לאותו מודל, דיוק לפי קטגוריה וגודל קלט (היוריסטי). תשובה חסרה, פגומה או סותרת נחשבת שגויה.

## מגבלות ידועות
- כל החומר נכתב על ידי מחבר אחד (הסוכן שבנה את השפה), ולכן ייתכנה הטיה בניסוח גרסת הפרוזה. מומלץ שמישהו אחר ינסח מחדש את הפרוזה לפחות בחלק מהתרחישים.
- 32 שאלות הן מדגם קטן. הפרש של כמה נקודות אחוז אינו מובהק; לכן חוזרים על הרצות.
- הריפו ציבורי והמודלים המשתתפים יכולים לכתוב אליו, לכן ייתכן זיהום: מודל שיסקור את הריפו ימצא את `SPEC.md` וקבצים נוספים גם במסלול NL. הפרומפטים אוסרים זאת, אבל לא ניתן לאכוף.
- הניסוי מודד הבנה של מסמך אחד. הוא לא מודד דריפט בשרשרת העברה בין מודלים (מבחן שרשרת מתוכנן כשלב ב').
- גודל הקלט במסלול CL כולל את `SPEC.md` ואת `lexicon.json`; במסלול NL אין עלות כזו. ההשוואה הכלכלית דורשת ספירת טוקנים אמיתית מה-API.
- חלק מהתרחישים בודקים במכוון נקודות שהשפה לא מגדירה היטב (`dur` ב-s05, אישור קבלה ב-s03; ראו R10, R11). טעות שם היא ממצא על השפה, לא על המודל.
