# ניסוי v2: סט צפוף ומבחן שרשרת

**למה:** בניסוי הראשון (`experiment/`) כל המודלים הגיעו לתקרה (כמעט 100%), ולכן הוא לא יכול להבדיל בין פרוזה ל-CL.
כאן המסמכים ארוכים וצפופים (כ-18 הצהרות בתרחיש, ישויות דומות, מקורות חופפים, מספרים קרובים),
והשאלות דורשות שליפה, ספירה והשוואה. בנוסף יש מבחן שרשרת: כמה מידע שורד כשהוא עובר דרך שלוש הודעות.

## קבצים
| קובץ | תפקיד |
|---|---|
| `docs-nl.md`, `docs-cl.md` | המסמכים בלבד, בלי שאלות (לשרשרת) |
| `questions.md` | 36 השאלות (זהות בשני המסלולים) |
| `track-nl.md`, `track-cl.md` | מסמכים + שאלות, להרצה ישירה |
| `scenarios/` | מקורות: `dNN.cl`, `dNN.nl.md` |
| `results/` | תשובות סופיות של כל הרצה |
| `relay/` | הודעות ביניים של השרשרת |
| `relay-budget.txt` | תקרת אורך הודעה בשרשרת: 3300 תווים |

## כללים
- **הקפאה:** אסור לשנות את `SPEC.md`, `lexicon.json` או קבצי `experiment/v2/` כל עוד הרצות נמשכות. שינוי באמצע פוסל את ההשוואה.
- כל הרצה בצ'אט חדש, בלי היסטוריה. `<MODEL>` הוא שם המודל באותיות קטנות בלי רווחים, אחיד בכל ההרצות של אותו מודל. `<N>` הוא מספר ההרצה.
- מומלץ 3 הרצות לפחות לכל מודל ולכל מסלול.
- המסמכים נוצרו מטבלת עובדות אחת, והשאלות והתשובות נגזרות ממנה (ונבדקו מול ה-CL המפורסר). מפתח התשובות אינו בריפו.

## הרצה ישירה
מסלול NL:
```
You are a participant in a reading-comprehension experiment.

1. Read ONLY these files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/track-nl.md

2. Do not open any other file or page in the repository, do not search the web, and do not use any prior knowledge of this project.

3. Answer every question (d01.q1 through d04.q9) with exactly one letter A-E, based only on the documents. Choose E only if the documents truly do not contain the answer.

4. Create the file experiment/v2/results/<MODEL>__nl__run<N>.md in the repository stodio-dev/- with exactly these lines:
model: <MODEL>
track: nl
run: <N>
d01.q1: <letter>
... (one line per question, up to d04.q9)

5. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

מסלול CL:
```
You are a participant in a reading-comprehension experiment.

1. Read ONLY these files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/track-cl.md
   https://raw.githubusercontent.com/stodio-dev/-/main/SPEC.md
   https://raw.githubusercontent.com/stodio-dev/-/main/lexicon.json
The documents in track-cl.md are written in CL, a compact language defined by SPEC.md and lexicon.json.

2. Do not open any other file or page in the repository, do not search the web, and do not use any prior knowledge of this project.

3. Answer every question (d01.q1 through d04.q9) with exactly one letter A-E, based only on the documents. Choose E only if the documents truly do not contain the answer.

4. Create the file experiment/v2/results/<MODEL>__cl__run<N>.md in the repository stodio-dev/- with exactly these lines:
model: <MODEL>
track: cl
run: <N>
d01.q1: <letter>
... (one line per question, up to d04.q9)

5. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

## שרשרת
שלושה צ'אטים לכל תנאי ולכל הרצה, **ברצף**: כל צ'אט קורא את מה שהקודם כתב לריפו. אחרי דחיפה של שלב, מומלץ לחכות כדקה
לפני הפעלת הבא (מטמון של `raw.githubusercontent.com`); אם הקובץ עדיין לא נגיש, מנסים שוב. אותו מודל בשלושת השלבים.

**תקרת אורך (3300 תווים) היא לחץ דחיסה מכוון.** היא 60% מאורך מסמכי ה-NL (5546 תווים),
בעוד מסמכי ה-CL באורך 3547 תווים (63% מה-NL). במסלול NL ההודעה חייבת לוותר על כ-41% מהתוכן;
במסלול CL המסמכים חורגים מהתקרה ב-247 תווים בלבד (כ-7%), כלומר נדרשת הקטנה קלה. לכן המבחן בודק **דחיסות מידע בערוץ בגודל קבוע ודריפט לאורכו**,
ולא השוואה בין שני מסלולים שדחוסים באותו יחס. התקרה נקבעה לפני שנראו תוצאות כלשהן.

### שרשרת NL, שלב 1
```
You are hop 1 in a 3-step relay experiment (relay-nl).

1. Read ONLY these files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/docs-nl.md

2. Do not open any other file or page, do not search the web, and do not use prior knowledge of this project.
3. Write a handoff message in plain English for the next AI in a relay. That AI will NOT see the original documents and will later have to answer detailed questions about them; you will not see the questions. Preserve as much accurate, specific information as possible: who said what, how certain they were, when, numbers, scope, what is unknown. Do not add anything that is not in your source.
4. The message body must not exceed 3300 characters (spaces included). If it is longer, shorten it before writing the file.
5. Create the file experiment/v2/relay/<MODEL>__relay-nl__run<N>__hop1.md in the repository stodio-dev/- with exactly these lines, then the message:
model: <MODEL>
condition: relay-nl
run: <N>
hop: 1
---
<message>

6. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

### שרשרת NL, שלב 2
```
You are hop 2 in a 3-step relay experiment (relay-nl).

1. Read ONLY these files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/relay/<MODEL>__relay-nl__run<N>__hop1.md

2. Do not open any other file or page, do not search the web, and do not use prior knowledge of this project.
3. Write a handoff message in plain English for the next AI in a relay. That AI will NOT see the original documents and will later have to answer detailed questions about them; you will not see the questions. Preserve as much accurate, specific information as possible: who said what, how certain they were, when, numbers, scope, what is unknown. Do not add anything that is not in your source.
4. The message body must not exceed 3300 characters (spaces included). If it is longer, shorten it before writing the file.
5. Create the file experiment/v2/relay/<MODEL>__relay-nl__run<N>__hop2.md in the repository stodio-dev/- with exactly these lines, then the message:
model: <MODEL>
condition: relay-nl
run: <N>
hop: 2
---
<message>

6. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

### שרשרת NL, שלב סופי
```
You are the final participant in a 3-step relay experiment (relay-nl).

1. Read ONLY these files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/relay/<MODEL>__relay-nl__run<N>__hop2.md
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/questions.md

2. Do not open any other file or page, do not search the web, and do not use prior knowledge of this project. The first file is a handoff message that passed through two earlier AIs; it is your only source of facts.
3. Answer every question (d01.q1 through d04.q9) with exactly one letter A-E, based only on the handoff message. Choose E only if the message truly does not contain the answer.
4. Create the file experiment/v2/results/<MODEL>__relay-nl__run<N>.md in the repository stodio-dev/- with exactly these lines:
model: <MODEL>
track: relay-nl
run: <N>
d01.q1: <letter>
... (one line per question, up to d04.q9)

5. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

### שרשרת CL, שלב 1
```
You are hop 1 in a 3-step relay experiment (relay-cl).

1. Read ONLY these files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/docs-cl.md
   https://raw.githubusercontent.com/stodio-dev/-/main/SPEC.md
   https://raw.githubusercontent.com/stodio-dev/-/main/lexicon.json

2. Do not open any other file or page, do not search the web, and do not use prior knowledge of this project.
3. Write a handoff message in CL only (no prose), following SPEC.md and lexicon.json for the next AI in a relay. That AI will NOT see the original documents and will later have to answer detailed questions about them; you will not see the questions. Preserve as much accurate, specific information as possible: who said what, how certain they were, when, numbers, scope, what is unknown. Do not add anything that is not in your source.
4. The message body must not exceed 3300 characters (spaces included). If it is longer, shorten it before writing the file.
5. Create the file experiment/v2/relay/<MODEL>__relay-cl__run<N>__hop1.md in the repository stodio-dev/- with exactly these lines, then the message:
model: <MODEL>
condition: relay-cl
run: <N>
hop: 1
---
<message>

6. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

### שרשרת CL, שלב 2
```
You are hop 2 in a 3-step relay experiment (relay-cl).

1. Read ONLY these files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/relay/<MODEL>__relay-cl__run<N>__hop1.md
   https://raw.githubusercontent.com/stodio-dev/-/main/SPEC.md
   https://raw.githubusercontent.com/stodio-dev/-/main/lexicon.json

2. Do not open any other file or page, do not search the web, and do not use prior knowledge of this project.
3. Write a handoff message in CL only (no prose), following SPEC.md and lexicon.json for the next AI in a relay. That AI will NOT see the original documents and will later have to answer detailed questions about them; you will not see the questions. Preserve as much accurate, specific information as possible: who said what, how certain they were, when, numbers, scope, what is unknown. Do not add anything that is not in your source.
4. The message body must not exceed 3300 characters (spaces included). If it is longer, shorten it before writing the file.
5. Create the file experiment/v2/relay/<MODEL>__relay-cl__run<N>__hop2.md in the repository stodio-dev/- with exactly these lines, then the message:
model: <MODEL>
condition: relay-cl
run: <N>
hop: 2
---
<message>

6. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

### שרשרת CL, שלב סופי
```
You are the final participant in a 3-step relay experiment (relay-cl).

1. Read ONLY these files:
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/relay/<MODEL>__relay-cl__run<N>__hop2.md
   https://raw.githubusercontent.com/stodio-dev/-/main/SPEC.md
   https://raw.githubusercontent.com/stodio-dev/-/main/lexicon.json
   https://raw.githubusercontent.com/stodio-dev/-/main/experiment/v2/questions.md

2. Do not open any other file or page, do not search the web, and do not use prior knowledge of this project. The first file is a handoff message that passed through two earlier AIs; it is your only source of facts.
3. Answer every question (d01.q1 through d04.q9) with exactly one letter A-E, based only on the handoff message. Choose E only if the message truly does not contain the answer.
4. Create the file experiment/v2/results/<MODEL>__relay-cl__run<N>.md in the repository stodio-dev/- with exactly these lines:
model: <MODEL>
track: relay-cl
run: <N>
d01.q1: <letter>
... (one line per question, up to d04.q9)

5. Commit and push only that file to branch main. If the push is rejected, pull with rebase and push again. Do not modify any other file.
```

## ציון
אצל מפעיל הניסוי, עם מפתח v2 מחוץ לריפו:
```
python3 experiment/score.py /path/to/answer-key-v2.json experiment/v2/results --out REPORT-v2.md
```
המסלולים בדוח: `nl`, `cl`, `relay-nl`, `relay-cl`. הדוח בודק גם אורך הודעות הביניים ב-`relay/` מול התקרה.

## מגבלות ידועות
- הפרוזה נוצרה מתבניות (כמה ניסוחים לכל סוג הצהרה) ולא נכתבה ביד, ולכן היא אחידה וחד-משמעית יותר מפרוזה אנושית.
  זה עשוי להקל על מסלול NL ולהמעיט בקושי שלו.
- 36 שאלות בלבד; הפרש קטן אינו מובהק. חוזרים על הרצות.
- התקרה בשרשרת מיטיבה עם CL מעצם תכנונה (ראו לעיל). זו שאלה על דחיסות, לא על "מי מבין טוב יותר".
- בשרשרת CL, מודל עשוי פשוט להעתיק את מסמכי ה-CL כמות שהם. זה בדיוק מה שהשפה אמורה לאפשר, ולכן זו לא "בעיה".
- הריפו ציבורי והמודלים יכולים לכתוב אליו: ייתכן זיהום (קריאת קבצים אחרים, או הודעות ביניים של הרצות אחרות). הפרומפטים אוסרים זאת ואי אפשר לאכוף.
