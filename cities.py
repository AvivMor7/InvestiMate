import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class City:
    def __init__(self, english_name, hebrew_name, avg_rent=0, avg_selling_price=0):
        self.english_name = english_name
        self.hebrew_name = hebrew_name
        self.avg_rent = avg_rent
        self.avg_selling_price = avg_selling_price

    def __repr__(self):
        return (f"City(English Name: {self.english_name}, "
                f"Hebrew Name: {self.hebrew_name}, "
                f"Avg Rent: {self.avg_rent}, "
                f"Avg Selling Price: {self.avg_selling_price})")
        
def loadCities():
    cities = []
    for english_name, hebrew_name in cities_dict.items():
        city = City(english_name=english_name, hebrew_name=hebrew_name)
        cities.append(city)
    return cities

cities_dict = {
    "Acre": "עכו-ישראל",
    "Afula": "עפולה-ישראל",
    "Ashdod": "אשדוד-ישראל",
    "Ashkelon": "אשקלון-ישראל",
    "Arad": "ערד-ישראל",
    "AloneiHaBashan": "אלוני-הבשן-ישראל",
    "BatYam": "בת-ים-ישראל",
    "Beersheba": "באר-שבע-ישראל",
    "BneiYehuda": "בני-יהודה-ישראל",
    "Dimona": "דימונה-ישראל",
    "Eilat": "אילת-ישראל",
    "Gedera": "גדרה-ישראל",
    "Givataim": "גבעתיים-ישראל",
    "Haifa": "חיפה-ישראל",
    "HatzorHaGlilit": "חצור-הגלילית-ישראל",
    "Herzliya": "הרצליה-ישראל",
    "HodHaSharon": "הוד-השרון-ישראל",
    "Holon": "חולון-ישראל",
    "Jerusalem": "ירושלים-ישראל",
    "Kanaf": "כנף-ישראל",
    "Katzrin": "קצרין-ישראל",
    "KfarYona": "כפר-יונה-ישראל",
    "KfarSaba": "כפר-סבא-ישראל",
    "KfarVradim": "כפר-ורדים-ישראל",
    "KfarTabur": "כפר-תבור-ישראל",
    "KiryatAta": "קרית-אתא-ישראל",
    "KiryatBialik": "קרית-ביאליק-ישראל",
    "KiryatShmona": "קרית-שמונה-ישראל",
    "KiryatTivon": "קרית-טבעון-ישראל",
    "KritGat": "קרית-גת-ישראל",
    "KiryatMotzkin": "קרית-מוצקין-ישראל",
    "Nahariya": "נהריה-ישראל",
    "MaaleGamla": "מעלה-גמלא-ישראל",
    "MaalotTarshiha": "מעלות-תרשיחא-ישראל",
    "MigdalHaEmek": "מגדל-העמק-ישראל",
    "Safed": "צפת-ישראל",
    "Sderot": "שדרות-ישראל",
    "Shlomi": "שלומי-ישראל",
    "Netanya": "נתניה-ישראל",
    "Netivot": "נתיבות-ישראל",
    "NesZiyona": "נס-ציונה-ישראל",
    "NofHaGalil": "נוף-הגליל-ישראל",
    "Metula": "מטולה-ישראל",
    "Raanana": "רעננה-ישראל",
    "RamatHasharon": "רמת-השרון-ישראל",
    "RamatGan": "רמת-גן-ישראל",
    "RamatYishai": "רמת-ישי-ישראל",
    "Ramot": "רמות-ישראל",
    "Rehovot": "רחובות-ישראל",
    "RishonLezion": "ראשון-לציון-ישראל",
    "RoshHaayin": "ראש-העין-ישראל",
    "RoshPina": "ראש-פינה-ישראל",
    "TelAviv": "תל-אביב-יפו-ישראל",
    "Tveriya": "טבריה-ישראל",
    "Ilaniya": "אילניה-ישראל",
    "Odem": "אודם-ישראל",
    "Ofakim": "אופקים-ישראל",
    "Yavne": "יבנה-ישראל",
    "Yavneel": "יבנאל-ישראל",
    "Yeruham": "ירוחם-ישראל",
    "YokneamIllit": "יוקנעם-עילית-ישראל"
}
