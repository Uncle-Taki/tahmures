---
title: "بخش چهار — ارزیابی، امنیت و عملیات"
summary: "ارزیابی، ایمن‌سازی، بهره‌برداری و محدودکردن مسئولانهٔ سامانه‌های مدل زبانی."
language: "fa"
---

# بخش چهار — ارزیابی، امنیت و محیط عملیاتی

بخش چهارم رشد تهمورث را از طراح سامانه به evaluator، نگهبان، operator و
آموزگار کامل می‌کند. او rubric و regression gate می‌سازد، trust boundary را
حفظ می‌کند، approval را به درخواست دقیق می‌بندد، drift را با telemetry
نسخه‌دار می‌بیند و تشخیص می‌دهد کدام requirement باید با سازوکاری غیر از
زبان enforce شود.

1. [ارزیابی و معیارنامه‌ها](19-evaluation-and-rubrics.md)
2. [آزمون رگرسیون برای سامانه‌های مبتنی بر پرامپت](20-regression-testing-for-prompted-systems.md)
3. [تزریق پرامپت و مرزهای اعتماد](21-prompt-injection-and-trust-boundaries.md)
4. [تأییدها، قابلیت‌ها و اقدام‌های پیامددار](22-approvals-capabilities-and-consequential-action.md)
5. [عملیات محیط تولید و رانش](23-production-operations-and-drift.md)
6. [فراتر از پرامپت: انتخاب سازوکار کنترل مناسب](24-beyond-prompting-choosing-the-right-control.md)

همهٔ manifest‌ها، dataset‌ها، fixture‌ها و implementation‌های Python و Go همان
دارایی‌های canonical انگلیسی‌اند. نتیجه‌ها فقط رفتار case‌های ثبت‌شده را
نشان می‌دهند و ادعایی جهان‌شمول دربارهٔ model یا provider نیستند.
