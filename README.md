# BAJ_TCG
site de tcg pour Telegram
Voici le fichier `README.md` complet et documenté, prêt à être placé à la racine de ton dépôt GitHub pour guider le projet et tout futur développeur.

---

```markdown
# 🎺 TCG La Band'à Joe — Telegram Mini App (TMA)

Jeu de cartes à collectionner (TCG / Gacha) 100 % Serverless conçu pour être exécuté nativement dans l'écosystème Telegram sous forme de **Telegram Mini App (TMA)** ou directement dans un navigateur moderne.

---

## 📁 Architecture du Dépôt

Le projet repose sur une architecture sans backend ("zero-backend"), hébergée directement via **GitHub Pages**.

```text
├── index.html          # Application complète (UI, logique gacha, shaders foil, stats)
├── cards_data.js       # Base de données externe des 222 cartes (objet CARDS_DB)
├── images/             # Dossier contenant les 222 illustrations (format 630x880)
│   ├── 001Kamayosh.png
│   ├── 149Cuzco.png
│   ├── 199NDT.png
│   └── 220BABAJ.png
└── README.md           # Documentation technique du projet

```

---

## ⚙️ Spécifications Techniques

### 1. Stockage & Persistance des Données

* **Clé de sauvegarde :** `tma_gacha_v1`
* **Mécanisme :**
1. Utilisation prioritaire de l'API cloud Telegram : `window.Telegram.WebApp.CloudStorage`.
2. Fallback automatique sur `window.localStorage` en cas d'exécution hors Telegram ou d'échec réseau.


* **Structure de l'objet d'état (`state`) :**
```json
{
  "packs": 6,
  "lastUpdate": 1711370000000,
  "inventory": {
    "001": 2,
    "149": 1
  },
  "stats": {
    "packsOpened": 14,
    "cardsDrawn": 42,
    "firstOpenedAt": 1711369000000
  }
}

```



> ⚠️ **Alerte Développeur (Plafond 4 Ko) :**
> Telegram impose une limite stricte de **4 096 octets** par clé dans `CloudStorage`.
> L'inventaire actuel (222 cartes) consomme environ 1,8 Ko. Si le jeu dépasse les **400 à 450 cartes uniques**, il faudra compacter le stockage (ex: tableau d'identifiants ou bitfield) ou segmenter les clés (`tma_gacha_v1_set1`, `tma_gacha_v1_set2`).

---

### 2. Économie & Système d'Énergie

* **Boosters max en réserve :** 6 boosters.
* **Taux de régénération :** 1 booster toutes les 10 minutes (`10 * 60 * 1000` ms).
* **Composition d'un pack :** 3 cartes tirées séquentiellement.

---

### 3. Moteur de Tirage & Probabilités

Le tirage implémente une logique par emplacement (**Slot-based RNG**) pour garantir un équilibre entre progression fluide et préservation de la rareté des cartes fortes :

| Emplacement dans le booster | Commune (◆) | Rare (◆◆) | Épique (◆◆★) | Légendaire (◆◆★★) |
| --- | --- | --- | --- | --- |
| **Cartes 1 & 2** (Slots 0 & 1) | **82.0 %** | **16.9 %** | **1.0 %** | **0.1 %** |
| **Carte 3** (Slot 2 — "Carte Rare") | **60.0 %** | **28.0 %** | **11.0 %** | **1.0 %** |

---

### 4. Rendu Visuel & Effets Graphiques

* **Format des cartes :** Ratio officiel TCG $630 \times 880$ (`aspect-ratio: 630 / 880`).
* **Intégrité graphique :** Aucun rognage CSS (`border-radius: 0` sur l'image) afin de préserver les bordures noires, numéros et symboles de rareté d'origine.
* **Performance :** Attribut `loading="lazy"` actif sur les images de la grille pour minimiser l'empreinte mémoire initiale.
* **Effet Foil / Holographique interactif :**
* Appliqué exclusivement sur les cartes **Épiques** et **Légendaires**.
* Coordonnées dynamiques via CSS Variables (`--foil-x`, `--foil-y`).
* Piloté en temps réel par :
* Les événements tactiles (`pointermove`).
* L'API Gyroscope mobile (`DeviceOrientationEvent` sur `gamma` et `beta`).





---

## 🛠️ Outils Développeur & Commandes URL (Cheats)

Des commandes administratives permettent de tester l'application sans console, via le paramètre Telegram `startapp` ou les paramètres URL classiques :

| Commande | URL Telegram (TMA) | URL Navigateur standard | Action |
| --- | --- | --- | --- |
| **Recharger l'énergie** | `t.me/BOT/app?startapp=boosters` | `https://site.io/?startapp=boosters` | Remet les boosters à 6/6 |
| **Donner une carte** | `t.me/BOT/app?startapp=give_001` | `https://site.io/?startapp=give_001` | Attribue 1 exemplaire de la carte (format 3 chiffres) |
| **Reset complet** | `t.me/BOT/app?startapp=reset` | `https://site.io/?startapp=reset` | Purge intégrale de la sauvegarde (inventaire + stats) |

---

## 📖 Guide de Contribution pour le Prochain Développeur

### Ajouter de nouvelles cartes

1. Ajouter les illustrations dans le répertoire `images/` en respectant la nomenclature : `IDNomDeLaCarte.png` (ex : `223Saxophone.png`).
2. Mettre à jour `cards_data.js` en déclarant la nouvelle carte dans la catégorie correspondante (`common`, `rare`, `epic`, `legendary`) :
```javascript
{
    "id": "223",
    "name": "Saxophone",
    "emoji": "🎷",
    "image": "images/223Saxophone.png"
}

```


3. L'application recalcule automatiquement le total des cartes et met à jour les barres de progression au lancement suivant.

### Modifier les probabilités de tirage

Ouvrir `index.html` et ajuster la fonction `drawCardBySlot(slotIndex)` :

* Modifier les seuils numériques du test `roll` (valeur entre 0 et 100).
* Veiller à ce que la somme des tranches soit strictement égale à 100.

### Déploiement et liaison Telegram

1. Commiter et pousser les modifications sur la branche principale (`main`).
2. Vérifier que GitHub Pages est actif dans **Settings > Pages** (Source : `Deploy from a branch` -> `/root`).
3. Dans Telegram, ouvrir **[@BotFather](https://t.me/BotFather?utm_source=gemini)** :
* `/myapps` > Sélectionner l'application.
* `Edit App` > `Edit URL` > Renseigner l'adresse HTTPS fournie par GitHub Pages.



```

```
