"""
Ministry-style bilingual website (Arabic / English).

Run it:
    pip install flask
    python app.py
Then open http://127.0.0.1:5000
"""

from flask import Flask, render_template, redirect, url_for, abort, request

app = Flask(__name__)

# ---------------------------------------------------------------------------
# Content. In a real project this would come from a database or a CMS.
# Every text has an "ar" and an "en" version.
# ---------------------------------------------------------------------------

LANGUAGES = {
    "ar": {"name": "العربية", "dir": "rtl"},
    "en": {"name": "English", "dir": "ltr"},
}

UI = {
    "ar": {
        "site_name": "وزارة التعاون الدولي",
        "nav_home": "الرئيسية",
        "nav_about": "عن الوزارة",
        "nav_news": "الأخبار",
        "nav_reports": "التقارير",
        "nav_contact": "اتصل بنا",
        "hero_title": "شراكات دولية من أجل تنمية اقتصادية مستدامة",
        "hero_text": "نعمل مع شركاء التنمية حول العالم لتمويل مشروعات تخدم المواطن المصري.",
        "hero_cta": "تعرّف على مشروعاتنا",
        "stats_title": "أرقام رئيسية",
        "news_title": "آخر الأخبار",
        "news_all": "كل الأخبار",
        "read_more": "اقرأ المزيد",
        "contact_title": "اتصل بنا",
        "contact_name": "الاسم",
        "contact_email": "البريد الإلكتروني",
        "contact_message": "الرسالة",
        "contact_send": "إرسال الرسالة",
        "contact_sent": "تم استلام رسالتك. شكرًا لتواصلك معنا.",
        "address": "٨ شارع عدلي، القاهرة، مصر",
        "footer_rights": "جميع الحقوق محفوظة",
        "back": "رجوع",
    },
    "en": {
        "site_name": "Ministry of International Cooperation",
        "nav_home": "Home",
        "nav_about": "About",
        "nav_news": "News",
        "nav_reports": "Reports",
        "nav_contact": "Contact",
        "hero_title": "International partnerships for sustainable economic development",
        "hero_text": "We work with development partners worldwide to finance projects that serve people in Egypt.",
        "hero_cta": "See our projects",
        "stats_title": "Key figures",
        "news_title": "Latest news",
        "news_all": "All news",
        "read_more": "Read more",
        "contact_title": "Contact us",
        "contact_name": "Name",
        "contact_email": "Email",
        "contact_message": "Message",
        "contact_send": "Send message",
        "contact_sent": "Your message was received. Thank you for writing to us.",
        "address": "8 Adly Street, Cairo, Egypt",
        "footer_rights": "All rights reserved",
        "back": "Back",
    },
}

STATS = [
    {"value": "9.8", "unit": {"ar": "مليار دولار", "en": "billion USD"},
     "label": {"ar": "تمويلات تنموية", "en": "development financing"}},
    {"value": "27", "unit": {"ar": "", "en": ""},
     "label": {"ar": "شريك تنمية", "en": "development partners"}},
    {"value": "377", "unit": {"ar": "", "en": ""},
     "label": {"ar": "مشروعًا جاريًا", "en": "ongoing projects"}},
]

NEWS = [
    {
        "slug": "green-financing-forum",
        "date": "2026-09-10",
        "sector": {"ar": "التمويل الأخضر", "en": "Green financing"},
        "title": {
            "ar": "انطلاق منتدى التمويل الأخضر بمشاركة ١٢ دولة",
            "en": "Green financing forum opens with twelve countries taking part",
        },
        "summary": {
            "ar": "ناقش المنتدى آليات تمويل مشروعات الطاقة المتجددة ومياه الشرب.",
            "en": "The forum discussed financing mechanisms for renewable energy and clean water projects.",
        },
        "body": {
            "ar": "استضافت الوزارة منتدى التمويل الأخضر لبحث سبل توسيع التمويل المناخي، "
                  "وناقش المشاركون محفظة المشروعات القائمة وآليات إشراك القطاع الخاص.",
            "en": "The ministry hosted the green financing forum to explore ways of widening climate "
                  "finance. Participants reviewed the current project portfolio and discussed how the "
                  "private sector can take part.",
        },
    },
    {
        "slug": "annual-report-2025",
        "date": "2026-07-22",
        "sector": {"ar": "التقارير", "en": "Reports"},
        "title": {
            "ar": "إصدار التقرير السنوي لعام ٢٠٢٥",
            "en": "The 2025 annual report is published",
        },
        "summary": {
            "ar": "يرصد التقرير محفظة التعاون الدولي وتوزيعها على القطاعات والمحافظات.",
            "en": "The report sets out the international cooperation portfolio by sector and governorate.",
        },
        "body": {
            "ar": "يعرض التقرير السنوي توزيع التمويلات على قطاعات النقل والطاقة والصحة والتعليم، "
                  "ويقدّم مؤشرات متابعة لكل مشروع.",
            "en": "The annual report breaks down financing across transport, energy, health and "
                  "education, and gives progress indicators for each project.",
        },
    },
    {
        "slug": "water-programme-signed",
        "date": "2026-05-04",
        "sector": {"ar": "المياه", "en": "Water"},
        "title": {
            "ar": "توقيع اتفاق لتطوير شبكات المياه في الصعيد",
            "en": "Agreement signed to upgrade water networks in Upper Egypt",
        },
        "summary": {
            "ar": "يستهدف البرنامج خدمة أكثر من مليون نسمة في أربع محافظات.",
            "en": "The programme will serve more than a million people across four governorates.",
        },
        "body": {
            "ar": "يشمل الاتفاق تجديد محطات المعالجة ومد شبكات جديدة، على أن يبدأ التنفيذ مطلع العام المقبل.",
            "en": "The agreement covers renovating treatment plants and laying new networks, with work "
                  "starting early next year.",
        },
    },
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def check_lang(lang):
    """Reject any language that is not defined above."""
    if lang not in LANGUAGES:
        abort(404)


@app.context_processor
def inject_globals():
    """Makes these available inside every template without passing them each time."""
    lang = request.view_args.get("lang", "ar") if request.view_args else "ar"
    if lang not in LANGUAGES:
        lang = "ar"
    return {
        "lang": lang,
        "t": UI[lang],
        "direction": LANGUAGES[lang]["dir"],
        "languages": LANGUAGES,
        "other_lang": "en" if lang == "ar" else "ar",
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def root():
    return redirect(url_for("home", lang="ar"))


@app.route("/<lang>/")
def home(lang):
    check_lang(lang)
    return render_template("index.html", stats=STATS, news=NEWS[:3])


@app.route("/<lang>/news/")
def news_list(lang):
    check_lang(lang)
    return render_template("news.html", news=NEWS)


@app.route("/<lang>/news/<slug>/")
def news_detail(lang, slug):
    check_lang(lang)
    article = next((n for n in NEWS if n["slug"] == slug), None)
    if article is None:
        abort(404)
    return render_template("news_detail.html", article=article)


@app.route("/<lang>/contact/", methods=["GET", "POST"])
def contact(lang):
    check_lang(lang)
    sent = False
    if request.method == "POST":
        # A real site would validate, store, or email this.
        print("New message:", request.form.get("name"), request.form.get("email"))
        sent = True
    return render_template("contact.html", sent=sent)


if __name__ == "__main__":
    app.run(debug=True)