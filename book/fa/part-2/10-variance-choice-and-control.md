---
title: "واریانس، انتخاب و کنترل"
slug: "variance-choice-and-control"
chapter: 10
part: "بخش دو — طراحی تعامل‌های مبتنی بر پرامپت"
summary: "variation پاسخ را از خطا و گزینه تولیدشده را از انتخاب متعلق به برنامه جدا کنید."
maturity: "draft"
last_reviewed: "2026-07-29"
narrative_episode: "شورای چندصدا"
learning_objectives:
  - "اندازه‌گیری diversity پاسخ در trial‌های تکراری"
  - "جداسازی گزینه generation از انتخاب قطعی"
  - "تعریف جای مناسب stability، diversity یا escalation"
prerequisites:
  - "فصل ۹"
language: "fa"
translation_of: "part-2/10-variance-choice-and-control.md"
source_sha256: "b13dced8da5ebbde6fe2276b074ef492ea33a2ff36f60447b0e781c429886f5d"
translation_status: "draft"
last_translated: "2026-07-30"
---

# واریانس، انتخاب و کنترل

[این فصل را به انگلیسی بخوانید](/part-2/10-variance-choice-and-control/)

## اهداف یادگیری

تغییرپذیری مشروع را از incorrectness جدا، فرض پنهان پشت پاسخ‌های مختلف
را آشکار و سیستم generate-then-select طراحی می‌کنید که سیاست نهایی را
برنامه، نه نثر تولیدشده، مالک است. تنوع، modal رفتار، قید
satisfaction و انتخاب پایداری را می‌سنجید.

## روایت تهمورث

*روایت پیش رو داستانی آموزشی و اصیل است که برای این کتاب نوشته شده؛ ترجمه،
اقتباس یا بازسازی بخشی از* شاهنامه *نیست.*

### صحنه

شورای چندصدا گرد میز دایره‌ای با شش بخش چوب رنگ‌شده نشست؛ هر بخش زمینی بود
که باید پیش از باران پاییز کشت می‌شد. تهمورث soil گزارش و seed موجودی
یکسانی را پیش سه دیو پشت پرده‌های جدا گذاشت. صداها فرق داشتند و همدیگر را
نمی‌شنیدند.

### درخواست

تهمورث درخواست را بی‌تغییر تکرار کرد: «برنامهٔ کشتی را انتخاب کنید که بهترین
حفاظت را از غلهٔ زمستان می‌کند.»

دیو نخست جو را در زمین شمالی کاشت چون آب کم می‌خواست. دومی گندم دیررس را
برای yield بیشتر در سال متوسط برگزید. سومی زمین را تقسیم و seed ذخیرهٔ سیل
کنار گذاشت. هر برنامه seed موجود و تاریخ نوشته‌شده را رعایت و توضیح
خوبی داشت. تهمورث دوباره پرسید؛ دیو نخست پاسخ خود را عوض کرد.

### نتیجهٔ غیرمنتظره

دبیر نخست دوازده trial و پنج برنامه ثبت کرد. adviserها frequency را vote
دانستند: پرتکرارترین باید بهترین باشد. اما مزیت آن برنامه از فرض ناگفتهٔ
بازشدن کانال شمالی می‌آمد. با قید دروازه‌بان—«به کانال وابسته نباش»—
برنامه نامعتبر شد.

یکی commandی برای پاسخ یکسان خواست؛ دیگری تغییرپذیری را مفید می‌دانست چون
alternative را آشکار کرده بود. تهمورث آزادی بیان دیوها را کم کرد. wording
تکراری‌تر شد، اما تساوی دو برنامه معتبر ماند.

دربار سه پرسش را یکی گرفته بود: چه planهایی ممکن‌اند، کدام سخت قید
را می‌گذرانند و kingdom کدام acceptable برنامه را ترجیح می‌دهد؟

### کشف

دبیر جدول تولید داد: دیوها گزینه و فرض می‌نوشتند، winner
اعلام نمی‌کردند. board جدا مجاز برنامه ID، سخت قید و ordering قطعی
داشت: نخست survival آستانه، سپس water، بعد expected yield و در پایان
پایدار ID برای tie-break.

برنامه وابسته به کانال بسته حذف و arithmetic را دبیرها دوباره محاسبه کردند.
اگر دو برنامه زیر سیاست برابر بودند گزارش همین را می‌گفت، نه اینکه تفاوتی
بسازد. alternativeها برای بازبینی ماندند.

تهمورث به ledger گفت: «صداها vote نبودند؛ search بودند.» شورا همچنان تغییرپذیری
داشت، تصمیم دیگر همراهش drift نمی‌کرد.

دبیر در هر row خط «دلیل for کنارگذاری» گذاشت. گزینه تنها با شکست‌خورده
قید یا قاعده صریح ناپدید می‌شد، نه با صدای کمتر persuasive.

برای آخرین آزمون، دبیر ترتیب نمایش سه برنامه را برعکس کرد و نام دیوها را از
لوح‌ها پوشاند. انتخاب همان ماند، زیرا دبیرها مقدار آب و خطر را از جدول
موجودی می‌خواندند، نه از فصاحت توضیح. سپس قید بقا را اندکی تغییر دادند؛ این
بار برنده عوض شد و گزارش دقیقاً نشان داد کدام آستانه علت تغییر بوده است.

تهمورث دریافت پایداری به معنای بی‌حسی در برابر واقعیت تازه نیست. تصمیم باید
در برابر واژه‌پردازی بی‌ربط ثابت و در برابر نیازمندی مرتبط پاسخ‌گو باشد. او
به‌جای خاموش‌کردن صداهای شورا، مرزی روشن میان آنچه صداها کشف می‌کردند و
آنچه قانون انتخاب می‌کرد کشید.

### از روایت تا مهندسی

واریانس مدل زبانی می‌تواند گزینهٔ مفید، ابهام پنهان یا اثر عادی نمونه‌گیری
را نشان دهد. قابلیت اعتماد یعنی مشخص کنیم تنوع کجا مطلوب است و سیاست صریح
برنامه کجا باید انتخابی پایدار و حسابرسی‌پذیر بسازد.

## مسئلهٔ مهندسی

تعامل یکسان ممکن است به‌سبب نمونه‌گیری، زیرساخت، تغییر ارائه‌دهنده و چند
ادامهٔ محتمل خروجی متفاوت دهد. تغییر خودکار خطا نیست: در ایده‌پردازی پاسخ
یکسان شاید از کاوش کم خبر دهد؛ در طبقه‌بندی سیاست، برچسب متغیر شاید
غیرقابل‌قبول باشد.

درخواست یک پاسخ، مجموعهٔ گزینه و قاعدهٔ انتخاب را در یک تولید پنهان می‌کند.
مدل هم می‌کاود و هم تصمیم می‌گیرد؛ پس معلوم نیست تغییر از گزینهٔ تازه،
تفسیر قید یا ترجیح ناسازگار آمده است. باید کنترل را تخصیص داد: مدل
گزینه‌های بدیل می‌سازد؛ کد قطعی، rubric صریح یا انسان مجاز طبق نیازمندی‌ها
انتخاب می‌کند.

## مدل ذهنی

چهار مرحله را جدا کنید:

```text
تولید candidate -> validation candidate -> امتیاز/مقایسه -> انتخاب/escalation
```

تولید پوشش می‌خواهد؛ اعتبارسنجی نامعتبر یا disallowed را حذف می‌کند؛
مقایسه criteria اعلام‌شده را اعمال می‌کند؛ انتخاب قاعده قطعی
یا داوری پاسخ‌گو دارد. اگر گزینه‌ها معلوم‌اند تولید لازم نیست.

سطح variance wording را بدون تغییر معنا عوض می‌کند؛ معنایی variance
ادعا، برنامه یا تصمیم را. unique رشته تعداد اندازه‌گیری ناقص اولی است؛
canonicalisation کار-specific یا معنایی label برای تحلیل معنادار لازم
است.

## مفاهیم اصلی

temperature و sampling parameter‌ها distribution را تغییر می‌دهند اما «پیچ
خلاقیت» universal نیستند. پیاده‌سازی ارائه‌دهنده متفاوت است و seed ثابت
یا temperature پایین تضمین determinism نیست. parameter و مدل هویت را
ثبت و رفتار مشاهده‌شده را بسنجید.

در repeated trial، `unique_response_count` تعداد متن متمایز،
`unique_response_ratio` نسبت آن به trial و `modal_response_rate` سهم متن
پرتکرار است. این‌ها descriptive هستند، نه quality score؛ پاسخ غلط تکراری
modal نرخ بالا دارد.

allowed-choice قرارداد جلوی ID ساخته‌شده را می‌گیرد، نه نقض قید
را. attribute را از قابل‌اعتماد داده اعتبارسنجی و محاسبات را در کد انجام دهید.
tie-break باید صریح باشد. پایدار ID reproducible اما شاید arbitrary؛ تصادفی
می‌تواند fair ولی منبع کنترل‌شده و audit‌شده بخواهد؛ انسان انتخاب برای تساوی
subjective یا پیامددار مناسب است. abstention، ارجاع یا «تحت criteria
فعلی برابر» پیامد معتبر است.

## الگوی پرامپت

برای کاوش:

```text
حداکثر چهار candidate واقعاً متفاوت تولید کن.
برای هر یک assumptionها و allowed candidate ID را بنویس.
winner انتخاب نکن.
```

برای مقایسه مدل-assisted:

```text
فقط candidateهای validateشده را با rubric supplied مقایسه کن.
observation هر criterion و evidence گمشده را برگردان.
application score را محاسبه و انتخاب خواهد کرد.
```

hidden reasoning نخواهید؛ شواهد و معیار قابل‌بررسی بخواهید.

## تلاش خام

«بهترین برنامه را بده» نیازمندی تعریف‌نشده، تولید، مقایسه و انتخاب
را مخلوط می‌کند. تکرار فراخوانی و گرفتن پاسخ پرتکرار، probability مدل را سیاست
محصول می‌کند؛ گرفتن پاسخ نخست ترتیب و sampling را mechanism تصمیم می‌کند.
self-reported score مدل نیز arithmetic و order-sensitive است. feature قابل‌اعتماد
و calculation قطعی را ترجیح دهید.

## تحلیل شکست

تغییرپذیری می‌تواند از نیازمندی مبهم، گزینه equivalent، sampling،
کانتکست ترتیب، مدل به‌روزرسانی، ابزار nondeterministic یا evaluator noise باشد.
اگر price بازیابی‌شده عوض شده، temperature مسئله را حل نمی‌کند. انتخاب
شکست شامل ID بیرون مجاز set، سخت قید نقض، تساوی ناپایدار،
ترجیح پنهان در ترتیب و شواهد مدل‌شده است. تنوع شکست شامل
near-duplicateهایی است که novel شمرده یا option اقلیت در voting زودهنگام
حذف می‌شود.

## طراحی بهبودیافته

نخست تعیین کنید consistency، کاوش یا هر دو در مرحله‌های جدا لازم است.
ورودی را pin، repeated trial اجرا و canonicalisation را مستند کنید. وقتی exact
متن گمراه‌کننده است پیامد معنایی label بزنید.

در generate-then-select تعداد و قالب گزینه را محدود، ID و قید
را اعتبارسنجی، score را از برنامه داده محاسبه، ردشده گزینه و دلیل
را ذخیره و تساوی قاعده ثابت یا ارجاع اجرا کنید. تولید و انتخاب
معیار را جدا گزارش کنید.

runner مخزن تنوع را به variant خلاصه افزوده است. evaluator
`allowed_choice`، ID plain یا فیلد JSON `selected` را می‌پذیرد و allowed-choice
نرخ و ترجیح پایداری می‌دهد. این آموزشی است؛ انتخاب واقعی دامنه
قید بررسی می‌خواهد.

## مثال حل‌شده

پشتیبانی سیستم یکی از policy‌های `answer`، `request_evidence` یا `escalate`
را پیشنهاد می‌کند. تولید می‌تواند چند پیام پیش‌نویس کند؛ انتخاب باید
به حساب وضعیت، شواهد و ریسک وابسته باشد. مدل ambiguity را نشان می‌دهد،
برنامه صلاحیت و شواهد الزامی را بررسی می‌کند. trial تکراری
می‌سنجد wording مختلف و سیاست ثابت است یا نه؛ اگر سیاست جابه‌جا شد پیش از
سرکوب sampling، نیازمندی و شواهد sensitivity را inspect کنید.

## آزمایش

```bash
python -m tahmures.cli run \
  --manifest experiments/manifests/ch10-variance-choice.json
go run ./examples/go/cmd/tahmures run \
  --manifest experiments/manifests/ch10-variance-choice.json
```

دو case در سه trial، single-answer و generate-select را مقایسه می‌کنند. fixture
اول planهای مجاز متفاوت و fixture دوم انتخاب JSON پایدار تحت قرارداد ترجیح
صریح می‌دهد. unique تعداد/ratio، modal نرخ، allowed-choice و پایداری را
ببینید. دو متن unique variant پایدار ناشی از پاسخ درست متفاوت per-case
است؛ تنوع درون case نیز مهم است.

## ارزیابی

تنوع را بر variant، case و معنایی label همراه قید satisfaction
و کار quality گزارش کنید. پایداری فقط جایی معیار است که ترجیح
پایدار وجود دارد؛ برای انتخاب equivalent، تساوی یا ارجاع درست را بسنجید.
با trial کافی confidence interval بدهید، اما سه recording synthetic را
distribution نخوانید. regression باید case تاریخی ناپایدار با trial تکراری
و provenance fixture داشته باشد.

## کارگاه پیاده‌سازی

### Python

```python
allowed = {"barley-a", "barley-b"}
candidates = [candidate for candidate in generated if candidate.id in allowed]
feasible = [item for item in candidates if item.water <= water_limit]
selected = min(feasible, key=lambda item: (item.risk, item.water, item.id))
```

مدل گزینه می‌سازد؛ برنامه داده آن را اعتبارسنجی و ترتیب می‌کند.

### Go

```go
sort.Slice(feasible, func(i, j int) bool {
    if feasible[i].Risk != feasible[j].Risk {
        return feasible[i].Risk < feasible[j].Risk
    }
    if feasible[i].Water != feasible[j].Water {
        return feasible[i].Water < feasible[j].Water
    }
    return feasible[i].ID < feasible[j].ID
})
selected := feasible[0]
```

در عملیاتی پیش از index، پیامد صریح no-گزینه برگردانید.

## حالت‌های شکست

repetition را truth، exact-رشته تنوع را conceptual تنوع و seed
را determinism تضمینی ندانید. انتخاب متکی بر ترتیب مدل، float تساوی ناپایدار
یا feature ساختهٔ خود گزینه خطرناک است. تنها winner را نگه‌داشتن شواهد
search و رد را پاک می‌کند.

## ملاحظات امنیتی

گزینه تولیدشده مجاز اقدام set را گسترش نمی‌دهد. ID را با برنامه
داده resolve و مجوز را پس از انتخاب recheck کنید. attacker شاید
توضیح یا معیار فیلد را دست‌کاری کند؛ متن persuasive نباید سخت
قید را کنار بزند. fairness اولویت و تساوی قاعده را بازبینی کنید؛
auditability سیاست را عادلانه نمی‌کند.

## ملاحظات عملیاتی

تنوع و انتخاب معیار را بر مدل/پرامپت نسخه نگه دارید و بر معنایی
drift، نه punctuation بی‌ضرر، alert کنید. repeated trial را عمدتاً در ارزیابی
بودجه‌بندی کنید. cache انتخاب ورودی باید با تغییر قید invalidate
شود و provenance گزینه برای reproduction بماند.

## بده‌بستان‌ها

گزینه بیشتر پوشش را بالا و هزینه، latency و بازبین load را زیاد
می‌کند. انتخاب قطعی reproducibility و احتمال ترجیح brittle
می‌آورد. انسان انتخاب nuance و نیز inconsistency/delay دارد. تغییرپذیری کم
برای classification مناسب و برای ideation مضر است. کاوش و کنترل را
knobهای مرحله‌های جدا بدانید.

در variance بازبینی واحد پایدار را نام ببرید: exact پاسخ، label canonical،
set واقعیت cited، سیاست انتخاب‌شده یا قید compliance. canonicalisation
را پیش از دیدن نتیجه تعریف کنید تا تغییرپذیری نامطلوب پنهان نشود. trial matrix
ورودی، بازیابی‌شده کانتکست، پرامپت/مدل نسخه و parameter را ثابت نگه می‌دارد؛
سه trial فقط mechanics گزارش را نشان می‌دهد.

یک factor را تغییر دهید: کانتکست equivalent را reorder، نام irrelevant را
عوض، شواهد را move یا sampling parameter را تغییر دهید. این metamorphic
آزمون sensitivity را بدون gold واحد نشان می‌دهد. planting سیاست نباید با
ترتیب field‌ها عوض شود مگر ترتیب ترجیح صریح باشد.

گزینه آزاد را پس از اعتبارسنجی به پایدار ID map کنید. دو توضیح
ممکن است یک برنامه و یک توضیح ترکیبی از planهای ناسازگار باشد. clustering
معنایی نیز evaluator ناقص دیگری است؛ raw پاسخ و mapping method را نگه
دارید.

سخت قید باید predicate روی feature قابل‌اعتماد باشد. اگر گزینه
مصرف آب را ده ادعا می‌کند، از design ساخت‌یافته محاسبه کنید. گزینه نباید
هم feature و هم proof قبولی را بسازد. soft ترجیح به scale، direction،
unit و sensitivity تحلیل نیاز دارد؛ رتبه‌بندی حساس به تغییر کوچک باید
«close فراخوانی» نمایش داده شود.

تساوی قاعده تصمیم محصول است: ID پایدار arbitrary، submission زودتر timing
bias، تصادفی نیازمند seed ثبت‌شده و منبع مصوب و انسان دارای bias است. گاهی
خروجی درست set گزینه‌های non-dominated و درخواست ترجیح stakeholder
است.

generator با آگاهی score formula شاید توضیح score-friendly تولید کند
بی‌آنکه property بهتر شود. در high-stakes معیار را از independent داده
حساب و ورودی generator/evaluator را جدا کنید. انتخابگر همیشه یک برنامه پایدار
می‌تواند باشد چون تولید برنامه امن را هرگز نمی‌یابد؛ گزینه پوشش،
رد نامعتبر و determinism روی fixed set را جدا بسنجید.

در انسان مقایسه، presentation ترتیب را تصادفی و rating فردی را حفظ کنید.
pairwise ممکن است چرخه A>B، B>C، C>A بدهد؛ handling ترجیح incomplete
را صریح کنید. بسته تصمیم immutable شامل case نسخه، گزینه ID، ردشده
و دلیل، قابل‌اعتماد feature، سیاست نسخه، تساوی نتیجه و actor مجاز است.
توضیح narrative جای بسته را نمی‌گیرد.

معنایی پیامد نرخ را در زمان پایش و rare برچسب را جدا کنید. امنیت
آزمون گزینه instruction-like، ID جعلی، extreme feature، تکراری ID و
توضیح بازبین-manipulating دارد. تولیدشده محتوا نمی‌تواند weight،
قید یا مجاز set را تغییر دهد.

عدم‌قطعیت irreducible را سند کنید. forecast و انسان مقدار با تولید
تکراری حل نمی‌شوند؛ سیستم mature alternative، فرض و sensitivity را
به شخص مجاز می‌دهد. evaluator هم vary می‌کند؛ نسخه را pin و agreement
نمونه‌ای میان methodها بسنجید.

معیار باید تصمیم سطح را نمایندگی کند: confusion matrix per زیرگروه
برای classification، top-k overlap برای رتبه‌بندی و canonical ادعا set برای
extraction. «high confidence» مدل probability guarantee نیست؛ یا بر labelled
داده calibrate کنید یا از سیاست حذف.

انتخاب feedback حلقه می‌سازد وقتی winner همهٔ observation آینده را می‌گیرد.
controlled کاوش governance اخلاقی و آماری می‌خواهد. multi-tenant سیاست
باید tenant-scoped باشد و cache کلید شامل tenant، سیاست و وضعیت نسخه.

توضیح derived خروجی است: گزینه و معیار رکورد تصمیم‌اند.
توضیح نباید دلیل تازه بسازد یا شکست‌خورده alternative را پنهان کند.
regression gate مرحله-specific باشد: generator خلاق شاید minimum تنوع
و امکان‌پذیری بخواهد؛ انتخابگر روی fixed گزینه exact پایداری.

مقایسهٔ modelها با pipeline برابر انجام می‌شود. هزینه شامل تولید ردشده،
زمان to first acceptable و بازبین load است. variance سیاست table برای هر
فیلد permitted تغییرپذیری، canonicalisation، trial sample، quality معیار،
انتخابگر مالک و ارجاع را مشخص و offline ارزیابی را از online وضعیت
متغیر جدا می‌کند.

پایداری آنلاین ممکن است pipeline گیرکرده باشد—همه fallback چون بازیابی
شکست‌خورده. انتخاب نرخ را با upstream health و abstention دلیل جفت کنید.
در high-consequence بسته‌ها را دوره‌ای replay و دامنه مالک قید و
توضیح را بازبینی کند. قطعی bug کاملاً تکرار می‌شود.

وقتی چند option واقعاً acceptable است انتخاب محدود user agency را بهتر از
tie-break پنهان نگه می‌دارد. تفاوت را از قابل‌اعتماد feature نشان و ترجیح
را بدون consent دائمی نکنید. کنترل یعنی منبع تغییرپذیری، حد انتخاب و
اختیار نهایی explicit شوند؛ consistency پیاده‌سازی شواهد است، نه
مشروعیت اخلاقی یا حقوقی.

## چه زمانی پرامپت پاسخ مسئله نیست

وقتی انتخاب و معیار معلوم است، قید solver، optimisation، رتبه‌بندی
کد یا سیاست engine را مستقیم اجرا کنید. lottery به randomness کنترل‌شده
و تصمیم ارزشی به انسان governance نیاز دارد. مدل نباید election، تصادفی
منبع یا مجوزدهی سیستم را با نثر شبیه‌سازی کند.

## تمرین‌ها

1. ده trial mock اجرا و exact و معنایی تنوع را مقایسه کنید.
2. allowed-choice قرارداد با پیامد تساوی صریح بسازید.
3. ترجیح پنهان یک درخواست «best» را به سیاست بدل کنید.
4. flow generate-then-select بسازید که مدل weight حساس را نبیند.
5. توضیح دهید modal-پاسخ نرخ بالا کجا نامطلوب است.

## خلاصهٔ فصل

پاسخ variance property مشاهده‌شده است، نه verdict. تعیین کنید گزینه
متنوع کجا مفید و سیاست پایدار کجا الزامی است. تولید، اعتبارسنجی،
مقایسه و انتخاب را جدا و تنوع را همراه quality و قید
بسنجید. اختیار را در قاعده قطعی برنامه یا داوری انسانی
پاسخ‌گو نگه دارید.

## روایت بعدی

وقتی تهمورث planی خواست که هیچ kingdom ندیده باشد، زیباترین پیشنهاد آب را
در کانال‌های نقره‌ای سربالایی فرستاد. نامهٔ باغبان پرسش سخت‌تری آورد: چه نوع
تازگی ارزش ساخته‌شدن دارد؟

<!-- next: ch11 -->

## منابع و مطالعهٔ بیشتر

- Dodge, Jesse, et al. 2020. “Fine-Tuning Pretrained Language Models: Weight
  Initializations, داده Orders, and Early Stopping.” arXiv:2002.06305.
- Amabile, Teresa M. 1996. *Creativity in کانتکست*. Boulder, CO: Westview
  Press.
- Montgomery, Douglas C. 2019. *Design and Analysis of Experiments*. 10th ed.
  Hoboken, NJ: Wiley.
