---
title: "واژه‌نامه و شیوه‌نامهٔ ترجمه"
summary: "مرجع اصطلاحات فنی، نام شخصیت‌ها و قواعد نگارشی نسخهٔ فارسی."
language: "fa"
---

# واژه‌نامه و شیوه‌نامهٔ ترجمه

نسخهٔ فارسی ترجمه‌ای وفادار و ویراسته است: همهٔ ادعاهای فنی، مثال‌ها،
پیامدهای روایی و محدودیت‌ها حفظ می‌شوند، اما جمله‌ها مطابق نثر طبیعی فارسی
بازنویسی می‌شوند.

## اصطلاحات canonical

| اصطلاح اصلی | صورت فارسی |
|---|---|
| prompt | پرامپت |
| prompt engineering | مهندسی پرامپت |
| language model | مدل زبانی |
| context | context با توضیح فارسی هنگام اشاره به مفهوم فنی |
| grounding | `grounding` |
| abstention | `abstention` |
| calibration | `calibration` |
| requirements | نیازمندی‌ها |
| output contract | قرارداد خروجی |
| schema | `schema` |
| dataset | `dataset` |
| fixture | fixture |
| evaluator | `evaluator` |
| pipeline | `pipeline` |
| instruction hierarchy | سلسله‌مراتب دستورها |
| prompt injection | تزریق پرامپت |
| template | `template` |
| rendering | `render` |
| dispatch | `dispatch` |
| workflow | workflow |
| checkpoint | checkpoint |
| idempotency | idempotency |
| variance | `variance` |
| generate-then-select | generate-then-select |
| context window | پنجرهٔ کانتکست |
| truncation | کوتاه‌سازی |
| token budget | بودجهٔ `token` |
| provenance | provenance |
| context engineering | `context engineering` |
| context package | `context package` |
| context assembly | `context assembly` |
| retrieval / RAG | `retrieval` / `RAG` |
| chunk / citation | `chunk` / `citation` |
| memory / state | `memory` / `state` |
| tool / permission | `tool` / `permission` |
| authorisation / capability | `authorisation` / `capability` |
| agent / termination | `agent` / `termination` |
| goal version | `goal version` |
| hand-off | `hand-off` |
| envelope / acknowledgement | `envelope` / `acknowledgement` |
| rubric / anchor / criterion | `rubric` / `anchor` / `criterion` |
| disqualifier / adjudication | `disqualifier` / `adjudication` |
| regression gate / protected tag | `regression gate` / `protected tag` |
| trust boundary / quarantine | `trust boundary` / `quarantine` |
| approval / approver | `approval` / `approver` |
| request digest | `request digest` |
| telemetry / SLO / drift | `telemetry` / `SLO` / `drift` |
| canary / rollback | `canary` / `rollback` |
| control selection / hard invariant | `control selection` / `hard invariant` |
| database constraint / access control | `database constraint` / `access control` |
| human judgement / least privilege | `human judgement` / `least privilege` |
| residual risk | `residual risk` |

## اصل انتخاب واژه

وابستگی واژه به موضوع، نه صرفاً انگلیسی‌بودن آن، شکل نمایش را تعیین می‌کند.
نام یک موجودیت پایدار در قرارداد، آزمایش، یادگیری ماشین یا معماری سامانه با
حروف لاتین حفظ می‌شود و در همهٔ کاربردهای نثری توضیح فارسی hover دارد. برای
مثال، `case` در این کتاب یک ورودی مستقل آزمایش است و با «مورد آزمایشی» یکسان
نیست که صرفاً در نثر عمومی به نمونه‌ای اشاره کند.

واژه‌های عادی که معادل فارسی دقیق و روان دارند ترجمه می‌شوند. `production`
به‌صورت «عملیاتی»، `application` به‌صورت «سامانه»، `test` به‌صورت «آزمون»،
`source` به‌صورت «منبع» و `output` به‌صورت «خروجی» نوشته می‌شود. فهرست مرکزی
تعریف‌های hover در `includes/fa-abbreviations.md` منبع حقیقت واژه‌های لاتین
مجاز است.

## نام‌های روایی

| نام اصلی | صورت فارسی |
|---|---|
| Tahmures | تهمورث |
| The First Scribe | دبیر نخست |
| Keeper of Scripts | نگهبان دبیره‌ها |
| The Archivist | بایگان |
| The Gatekeeper | دروازه‌بان |
| The Messenger | پیام‌رسان |
| Mirror Div | دیو آینه |
| Literal Div | دیو لفظ‌گرا |
| Wandering Div | دیو سرگردان |
| Many-Voiced Council | شورای چندصدا |
| mechanical scribes | دبیران مکانیکی |

## قواعد نگارشی

- در نثر از ی و ک فارسی، نیم‌فاصله و نشانه‌گذاری فارسی استفاده می‌شود.
- عددهای نثری فارسی‌اند؛ نسخه‌ها، شناسه‌ها، مسیرها، commandها و کد با نویسه‌های
  ASCII باقی می‌مانند.
- اصطلاح فنی لاتین در نثر بدون backtick نوشته می‌شود تا تعریف فارسی hover
  برای آن فعال باشد؛ مانند Python، case و fixture.
- شناسه، کلید JSON، مقدار enum، مسیر، command و هر متن ماشین‌خوان دقیق داخل
  backtick می‌ماند و tooltip نمی‌گیرد.
- پیش از پسوند فارسی متصل به اصطلاح لاتین نیم‌فاصله می‌آید؛ مانند case‌ها و
  fixture‌های.
- blockهای اجرایی Python، Go، Bash و JSON با منبع انگلیسی یکسان می‌مانند.
- عنوان و اطلاعات کتاب‌شناختی منابع به زبان انتشار اصلی حفظ می‌شود.
- هیچ روایت آموزشی به‌عنوان ترجمه، اقتباس یا بازسازی *شاهنامه* معرفی نمی‌شود.

[English source glossary context](/project-charter/)
