from storage import get_countries

data = get_countries()

if data:
    print("✅ API OK")
    print("Nb:", len(data["data"]))
    print("First:", data["data"][0])
else:
    print("❌ API KO")
