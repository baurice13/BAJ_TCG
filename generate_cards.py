import os
import re
import json

IMAGE_DIR = "images"
pattern = re.compile(r"^(\d{3})(.+)\.(png|webp|jpg)$", re.IGNORECASE)

db = {
    "common": [],
    "rare": [],
    "epic": [],
    "legendary": []
}

if not os.path.exists(IMAGE_DIR):
    print(f"Erreur : le dossier '{IMAGE_DIR}' n'existe pas.")
    exit()

for file in sorted(os.listdir(IMAGE_DIR)):
    match = pattern.match(file)
    if match:
        card_id = match.group(1)       # ex: "001"
        card_name = match.group(2)     # ex: "Kamayosh"
        num = int(card_id)

        card_data = {
            "id": card_id,
            "name": card_name,
            "emoji": "🎺",
            "image": f"{IMAGE_DIR}/{file}"
        }

        # Attribution selon tes règles exactes
        if (1 <= num <= 148) or num == 222:
            db["common"].append(card_data)
        elif 149 <= num <= 198:
            db["rare"].append(card_data)
        elif 199 <= num <= 218:
            db["epic"].append(card_data)
        elif 219 <= num <= 221:
            db["legendary"].append(card_data)

total = sum(len(cards) for cards in db.values())

with open("cards_data.js", "w", encoding="utf-8") as f:
    f.write("const CARDS_DB = " + json.dumps(db, ensure_ascii=False, indent=4) + ";\n")

print(f"Succès : {total} cartes générées dans cards_data.js !")
print(f"- Communes : {len(db['common'])}")
print(f"- Rares : {len(db['rare'])}")
print(f"- Épiques : {len(db['epic'])}")
print(f"- Légendaires : {len(db['legendary'])}")
