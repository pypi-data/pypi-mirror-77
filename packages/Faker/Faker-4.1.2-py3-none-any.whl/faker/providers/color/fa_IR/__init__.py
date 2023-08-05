from collections import OrderedDict

from .. import Provider as ColorProvider


class Provider(ColorProvider):
    # https://www.seyedrezabazyar.com/fa/name-and-code-of-colors/
    # https://bit.ly/353BBiY
    all_colors = OrderedDict((
        ("نیلی محو", "#F0F8FF"),
        ("بژ تیره", "#FAEBD7"),
        ("فیروزه‌ای", "#00FFFF"),
        ("یشمی", "#7FFFD4"),
        ("لاجوردی", "#F0FFFF"),
        ("بژ", "#F5F5DC"),
        ("کرم", "#FFE4C4"),
        ("مشکی", "#000000"),
        ("کاهگلی", "#FFEBCD"),
        ("آبی", "#0000FF"),
        ("آبی-بنفش سیر", "#8A2BE2"),
        ("قهوه‌ای", "#A52A2A"),
        ("خاکی", "#DEB887"),
        ("آبی لجنی", "#5F9EA0"),
        ("سبز روشن", "#7FFF00"),
        ("شوکولاتی", "#D2691E"),
        ("مرجانی", "#FF7F50"),
        ("آبی کدر", "#6495ED"),
        ("کاهی", "#FFF8DC"),
        ("زرشکی", "#DC143C"),
        ("فیروزه‌ای", "#00FFFF"),
        ("سرمه‌ای", "#00008B"),
        ("سبز کبریتی تیره", "#008B8B"),
        ("ماشی سیر", "#B8860B"),
        ("خاکستری سیر", "#A9A9A9"),
        ("سبز آووکادو", "#006400"),
        ("ماشی", "#BDB76B"),
        ("مخملی", "#8B008B"),
        ("زیتونی سیر", "#556B2F"),
        ("نارنجی سیر", "#FF8C00"),
        ("ارکیده بنفش", "#9932CC"),
        ("عنابی تند", "#8B0000"),
        ("قهوه‌ایِ حنایی", "#E9967A"),
        ("سبز دریایی تیره", "#8FBC8F"),
        ("آبی دودی", "#483D8B"),
        ("لجنی تیره", "#2F4F4F"),
        ("فیروزه‌ای سیر", "#00CED1"),
        ("بنفش باز", "#9400D3"),
        ("شفقی", "#FF1493"),
        ("آبی کمرنگ", "#00BFFF"),
        ("دودی", "#696969"),
        ("نیلی", "#1E90FF"),
        ("شرابی", "#B22222"),
        ("پوست پیازی", "#FFFAF0"),
        ("شویدی", "#228B22"),
        ("سرخابی", "#FF00FF"),
        ("خاکستری مات", "#DCDCDC"),
        ("سفید بنفشه", "#F8F8FF"),
        ("کهربایی باز", "#FFD700"),
        ("خردلی", "#DAA520"),
        ("خاکستری", "#808080"),
        ("سبز", "#008000"),
        ("مغزپسته‌ای کمرنگ", "#ADFF2F"),
        ("یشمی محو", "#F0FFF0"),
        ("سرخابی", "#FF69B4"),
        ("جگری", "#CD5C5C"),
        ("نیلی سیر", "#4B0082"),
        ("استخوانی", "#FFFFF0"),
        ("خاکی روشن", "#F0E68C"),
        ("نیلی کمرنگ", "#E6E6FA"),
        ("صورتی مات", "#FFF0F5"),
        ("مغزپسته‌ای پررنگ", "#7CFC00"),
        ("شیرشکری", "#FFFACD"),
        ("آبی کبریتی", "#ADD8E6"),
        ("بژ تیره", "#F08080"),
        ("آبی آسمانی", "#E0FFFF"),
        ("لیمویی روشن", "#FAFAD2"),
        ("خاکستری روشن", "#D3D3D3"),
        ("سبز روشن", "#90EE90"),
        ("صورتی روشن", "#FFB6C1"),
        ("کرم نارنجی", "#FFA07A"),
        ("سبز کبریتی روشن", "#20B2AA"),
        ("آبی آسمانی روشن", "#87CEFA"),
        ("سربی", "#778899"),
        ("بنفش مایل به آبی", "#B0C4DE"),
        ("شیری", "#FFFFE0"),
        ("مغزپسته‌ای روشن", "#00FF00"),
        ("سبز چمنی", "#32CD32"),
        ("كتانی", "#FAF0E6"),
        ("سرخ آبی", "#FF00FF"),
        ("آلبالویی", "#800000"),
        ("سبز دریایی", "#66CDAA"),
        ("آبی سیر", "#0000CD"),
        ("ارکیده سیر", "#BA55D3"),
        ("سرخ آبی سیر", "#9370DB"),
        ("خزه‌ای", "#3CB371"),
        ("آبی متالیک روشن", "#7B68EE"),
        ("یشمی سیر", "#00FA9A"),
        ("فیروزه‌ای تیره", "#48D1CC"),
        ("ارغوانی", "#C71585"),
        ("آبی نفتی", "#191970"),
        ("سفید نعنائی", "#F5FFFA"),
        ("بژ", "#FFE4E1"),
        ("هلویی", "#FFE4B5"),
        ("کرم سیر", "#FFDEAD"),
        ("لاجوردی", "#000080"),
        ("بژ روشن", "#FDF5E6"),
        ("زیتونی", "#808000"),
        ("سبز ارتشی", "#6B8E23"),
        ("نارنجی", "#FFA500"),
        ("قرمز-نارنجی", "#FF4500"),
        ("ارکیده", "#DA70D6"),
        ("نخودی", "#EEE8AA"),
        ("سبز کمرنگ", "#98FB98"),
        ("فیروزه‌ای کدر", "#AFEEEE"),
        ("شرابی روشن", "#DB7093"),
        ("هلویی روشن", "#FFEFD5"),
        ("هلویی پررنگ", "#FFDAB9"),
        ("بادامی سیر", "#CD853F"),
        ("صورتی", "#FFC0CB"),
        ("بنفش کدر", "#DDA0DD"),
        ("آبی کبریتی روشن", "#B0E0E6"),
        ("بنفش", "#800080"),
        ("قرمز", "#FF0000"),
        ("بادمجانی", "#BC8F8F"),
        ("فیروزه‌ای فسفری", "#4169E1"),
        ("کاکائویی", "#8B4513"),
        ("سالمحناییِ روشنوني", "#FA8072"),
        ("هلویی سیر", "#F4A460"),
        ("خزه‌ای پررنگ", "#2E8B57"),
        ("صدفی", "#FFF5EE"),
        ("قهوه‌ای متوسط", "#A0522D"),
        ("طوسی", "#C0C0C0"),
        ("آبی آسمانی", "#87CEEB"),
        ("آبی فولادی", "#6A5ACD"),
        ("سربی تیره", "#708090"),
        ("صورتی محو", "#FFFAFA"),
        ("یشمی کمرنگ", "#00FF7F"),
        ("نیلی متالیک", "#4682B4"),
        ("برنزه کدر", "#D2B48C"),
        ("سبز دودی", "#008080"),
        ("بادمجانی روشن", "#D8BFD8"),
        ("قرمز گوجه‌ای", "#FF6347"),
        ("سبز دریایی روشن", "#40E0D0"),
        ("بنفش روشن", "#EE82EE"),
        ("گندمی", "#F5DEB3"),
        ("سفید", "#FFFFFF"),
        ("خاکستری محو", "#F5F5F5"),
        ("زرد", "#FFFF00"),
        ("سبز لجنی", "#9ACD32"),
    ))

    safe_colors = (
        "سیاه", "عنابی", "سبز", "آبی کاربنی", "زیتونی",
        "بنفش", "سبز دودی", "آهکی", "آبی", "نقره‌ای",
        "خاکستری", "زرد", "ارغوانی", "فیروزه‌ای", "سفید",
    )
