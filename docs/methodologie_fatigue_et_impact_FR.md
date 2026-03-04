# Methodologie complete de verification de la resistance en fatigue et a l'impact des structures mecaniques soudees

**Reference du document :** WF-METH-001 Rev.0
**Normes applicables :** IIW XIII-2259-15 (2024), EN 1993-1-8/1-9, EN 1999-1-3, BS 7608:2014, BS 7910:2019, ISO 5817:2023, DNV-RP-C203, ASME KD-10
**Domaine d'application :** Toutes les structures mecaniques soudees en acier et aluminium soumises a des chargements de fatigue et/ou d'impact

---

## TABLE DES MATIERES

- [PARTIE I — CADRE GENERAL](#partie-i--cadre-general)
  - [1. Domaine d'application et objectifs](#1-domaine-dapplication-et-objectifs)
  - [2. References normatives](#2-references-normatives)
  - [3. Terminologie et definitions](#3-terminologie-et-definitions)
  - [4. Processus global de verification](#4-processus-global-de-verification)
- [PARTIE II — VERIFICATION DE LA RESISTANCE EN FATIGUE](#partie-ii--verification-de-la-resistance-en-fatigue)
  - [5. Phase 1 : Collecte des donnees et classification](#5-phase-1--collecte-des-donnees-et-classification)
  - [6. Phase 2 : Selection de la methode d'evaluation](#6-phase-2--selection-de-la-methode-devaluation)
  - [7. Phase 3 : Selection de la courbe S-N et de la norme](#7-phase-3--selection-de-la-courbe-s-n-et-de-la-norme)
  - [8. Phase 4 : Chaine de modificateurs — Facteurs de correction](#8-phase-4--chaine-de-modificateurs--facteurs-de-correction)
  - [9. Phase 5 : Calcul d'endommagement et criteres d'acceptation](#9-phase-5--calcul-dendommagement-et-criteres-dacceptation)
  - [10. Cas particuliers en fatigue](#10-cas-particuliers-en-fatigue)
- [PARTIE III — VERIFICATION DE LA RESISTANCE A L'IMPACT](#partie-iii--verification-de-la-resistance-a-limpact)
  - [11. Phase 1 : Caracterisation dynamique du materiau](#11-phase-1--caracterisation-dynamique-du-materiau)
  - [12. Phase 2 : Evaluation de la rupture des joints soudes sous impact](#12-phase-2--evaluation-de-la-rupture-des-joints-soudes-sous-impact)
  - [13. Phase 3 : Evaluation de l'absorption d'energie](#13-phase-3--evaluation-de-labsorption-denergie)
- [PARTIE IV — INTEGRATION EF](#partie-iv--integration-ef)
  - [14. Extraction des donnees EF pour la fatigue](#14-extraction-des-donnees-ef-pour-la-fatigue)
  - [15. Extraction des donnees EF pour l'impact](#15-extraction-des-donnees-ef-pour-limpact)
- [PARTIE V — EVALUATION COMBINEE ET RAPPORT](#partie-v--evaluation-combinee-et-rapport)
  - [16. Scenarios combines fatigue + impact](#16-scenarios-combines-fatigue--impact)
  - [17. Exigences de rapport](#17-exigences-de-rapport)
- [PARTIE VI — ARBRES DE DECISION ET REFERENCE RAPIDE](#partie-vi--arbres-de-decision-et-reference-rapide)
  - [18. Arbre de decision principal — Quelle methode utiliser](#18-arbre-de-decision-principal--quelle-methode-utiliser)
  - [19. Tableaux de reference rapide](#19-tableaux-de-reference-rapide)
  - [20. Liste de controle pour la verification complete](#20-liste-de-controle-pour-la-verification-complete)
- [ANNEXES](#annexes)
  - [Annexe A : Catalogue des classes FAT](#annexe-a--catalogue-des-classes-fat)
  - [Annexe B : Resume de la base de donnees materiaux](#annexe-b--resume-de-la-base-de-donnees-materiaux)
  - [Annexe C : Resume des formules](#annexe-c--resume-des-formules)
  - [Annexe D : Exemples d'application](#annexe-d--exemples-dapplication)

---

# PARTIE I — CADRE GENERAL

## 1. Domaine d'application et objectifs

### 1.1 Objet

Ce document etablit une **methodologie d'ingenierie generique, systematique et reproductible** pour verifier :

1. **La resistance en fatigue** des joints et composants soudes sous chargement cyclique
2. **La resistance a l'impact** des structures soudees sous chargement dynamique/crash

La methodologie est applicable a **tout type de structure mecanique soudee**, y compris mais sans s'y limiter :

- Caisse en blanc et chassis automobile
- Boitiers de batteries pour vehicules electriques et cadres structuraux
- Cadres de reservoirs a hydrogene et recipients sous pression
- Renforts structuraux et absorbeurs de choc
- Structures offshore et de genie civil
- Equipements industriels et sous pression

### 1.2 Conditions d'applicabilite

Cette methodologie s'applique lorsque **TOUTES** les conditions suivantes sont remplies :

| Condition | Plage |
|-----------|-------|
| Materiau | Acier de construction (limite d'elasticite 210–1500 MPa) ou alliages d'aluminium corroyes |
| Methode d'assemblage | Soudage a l'arc (MIG/MAG, TIG), soudage laser, soudage par friction-malaxage (FSW), soudage par resistance par points |
| Temperature | -40 °C a +300 °C (acier), -40 °C a +150 °C (aluminium) |
| Chargement | Cyclique (fatigue), impact dynamique (crash), ou combine |
| Duree de vie | Finie (10³ a 10⁹ cycles) ou infinie (limite d'endurance) |
| Site d'amorcage de fissure | Pied de cordon, racine de soudure, ou metal de base adjacent a la soudure |

### 1.3 Exclusions

Cette methodologie ne couvre **PAS** :

- Les composants moules ou forges (sans soudure)
- L'interaction fluage-fatigue (T > 300 °C pour l'acier, T > 150 °C pour l'aluminium)
- La fatigue des boulons ou le collage structural
- La fatigue des materiaux non metalliques
- Le chargement par explosion/souffle (vitesse de deformation > 10⁴ /s)

---

## 2. References normatives

| Norme | Titre | Application dans cette methodologie |
|-------|-------|-------------------------------------|
| IIW XIII-2259-15 (2024) | Recommandations pour le dimensionnement en fatigue des joints et composants soudes, 3e edition | **Reference principale fatigue** : courbes S-N, classes FAT, methodes d'evaluation |
| EN 1993-1-9 | Eurocode 3 — Fatigue des structures en acier | Courbes S-N alternatives, coefficients partiels de securite |
| EN 1999-1-3 | Eurocode 9 — Fatigue des structures en aluminium | Courbes S-N et classes FAT specifiques a l'aluminium |
| EN 1993-1-8 | Eurocode 3 — Calcul des assemblages | Resistance des soudures, criteres de rupture statique et a l'impact |
| BS 7608:2014 | Dimensionnement en fatigue des structures en acier | Classification alternative des details (classes B–W1) |
| BS 7910:2019 | Evaluation des defauts dans les structures metalliques | Mecanique de la rupture, facteurs de geometrie, facteurs Mk |
| ISO 5817:2023 | Qualite des soudures — Joints soudes par fusion | Niveaux de qualite B/C/D, limites des imperfections |
| DNV-RP-C203 | Dimensionnement en fatigue des structures offshore | Facteurs de dimensionnement en fatigue pour applications marines/offshore |
| ASME KD-10 | Fatigue des reservoirs a hydrogene | Facteurs de reduction pour fragilisation par l'hydrogene |
| ASTM E1049-85 | Comptage par la methode Rainflow | Decomposition des chargements a amplitude variable |
| IIW-2259-15 HFMI (2024) | Traitement HFMI pour l'amelioration de la tenue en fatigue | Facteurs d'amelioration par traitement post-soudage |

---

## 3. Terminologie et definitions

| Terme | Symbole | Definition |
|-------|---------|------------|
| Etendue de contrainte | Δσ | σ_max − σ_min [MPa] |
| Contrainte moyenne | σ_m | (σ_max + σ_min) / 2 [MPa] |
| Rapport de contrainte | R | σ_min / σ_max |
| Amplitude de contrainte | σ_a | Δσ / 2 [MPa] |
| Classe FAT | FAT | Resistance en fatigue caracteristique a N = 2×10⁶ cycles [MPa] |
| Courbe S-N | — | Relation entre Δσ et N (courbe de Wohler) |
| Point de rupture de pente | N_knee | Point de transition sur la courbe S-N bilineaire (10⁷ pour IIW) |
| Endommagement cumule | D | Somme d'endommagement de Palmgren-Miner (rupture a D ≥ 1,0) |
| Facteur d'augmentation dynamique | DIF | σ_dynamique / σ_statique |
| Vitesse de deformation | ε̇ | Taux de variation de la deformation [1/s] |
| Gorge de soudure | a | Epaisseur de gorge efficace de la soudure d'angle [mm] |
| Contrainte au point chaud | σ_hs | Contrainte structurale extrapolee au pied de cordon [MPa] |
| Contrainte d'entaille | σ_notch | Contrainte maximale au pied de cordon avec rayon de reference [MPa] |
| Absorption specifique d'energie | SEA | Energie absorbee par unite de masse [J/kg] |
| Efficacite de force d'ecrasement | CFE | P_moyen / P_max (rapport de la force moyenne a la force maximale) |

---

## 4. Processus global de verification

La verification complete d'une structure soudee suit ce processus directeur :

```
DEBUT
  │
  ├──► ETAPE 1 : Identifier le type de chargement
  │      ├── Chargement cyclique uniquement ?  ──────► ALLER A LA PARTIE II (Fatigue)
  │      ├── Impact/crash uniquement ?          ──────► ALLER A LA PARTIE III (Impact)
  │      └── Combine ?                          ──────► ALLER A LA PARTIE V (Combine)
  │
  ├──► ETAPE 2 : Collecter les donnees d'entree (Section 5)
  │      ├── Proprietes du materiau
  │      ├── Geometrie du joint et type de soudure
  │      ├── Spectre de chargement ou conditions d'impact
  │      └── Conditions environnementales
  │
  ├──► ETAPE 3 : Selectionner la methode d'evaluation (Section 6)
  │      └── Utiliser l'arbre de decision (Section 18)
  │
  ├──► ETAPE 4 : Appliquer la procedure specifique a la methode
  │      └── Suivre la section correspondante dans la Partie II ou III
  │
  ├──► ETAPE 5 : Appliquer les facteurs de correction (Section 8)
  │
  ├──► ETAPE 6 : Verifier les criteres d'acceptation (Section 9)
  │
  └──► ETAPE 7 : Documenter et rapporter (Section 17)
```

**Principe : Chaque verification doit produire un resultat binaire — CONFORME ou NON CONFORME — avec une marge de securite quantifiee.**

---

# PARTIE II — VERIFICATION DE LA RESISTANCE EN FATIGUE

## 5. Phase 1 : Collecte des donnees et classification

Avant tout calcul, l'ingenieur doit collecter et classifier systematiquement toutes les donnees d'entree. Des donnees manquantes ou mal classifiees sont la source principale d'erreurs dans l'evaluation en fatigue.

### 5.1 Donnees materiaux

**Parametres requis :**

| Parametre | Symbole | Unites | Source |
|-----------|---------|--------|--------|
| Famille de materiau | — | — | Plan / specification |
| Designation de la nuance | — | — | EN 10025, EN 10338, EN 10268, etc. |
| Limite d'elasticite | R_y (ou R_p0.2) | MPa | Certificat matiere ou minimum normatif |
| Resistance a la traction | R_m (ou S_u) | MPa | Certificat matiere ou minimum normatif |
| Module de Young | E | MPa | 210 000 (acier), 70 000 (aluminium) |

**Regle de decision pour la famille de materiau :**
- Si le metal de base est un acier au carbone, un acier allie ou un acier inoxydable → **Materiau = ACIER**
- Si le metal de base est un alliage d'aluminium corroye (series 2xxx, 5xxx, 6xxx, 7xxx) → **Materiau = ALUMINIUM**
- Autres materiaux → hors du domaine d'application de cette methodologie

### 5.2 Geometrie du joint et classification de la soudure

Classifier le joint selon le tableau de decision suivant :

| Observation | Classification → TypeSoudure |
|-------------|------------------------------|
| Deux toles assemblees bout a bout, pleine penetration | **BOUT A BOUT (BUTT)** |
| Soudure triangulaire reliant des elements superposes ou perpendiculaires | **ANGLE (FILLET)** |
| Deux toles assemblees a angle droit avec soudures bout a bout a pleine penetration des deux cotes | **CRUCIFORME (CRUCIFORM)** |
| Deux toles superposees avec soudures d'angle | **A RECOUVREMENT (LAP)** |
| Tole soudee perpendiculairement a une autre tole (soudure d'angle simple ou double) | **EN T (T_JOINT)** |
| Raidisseur longitudinal ou transversal | **RAIDISSEUR (STIFFENER)** |
| Soudure par point par resistance (pas de metal d'apport, pas de cordon visible) | **POINT (SPOT)** |
| Soudure bout a bout laser (cordon etroit, penetration profonde) | **BOUT A BOUT LASER (LASER_BUTT)** |
| Soudure d'angle laser | **ANGLE LASER (LASER_FILLET)** |
| Soudure par friction-malaxage (procede a l'etat solide, sans metal d'apport) | **FSW BOUT A BOUT (FSW_BUTT)** |

**Parametres geometriques supplementaires a enregistrer :**

| Parametre | Symbole | Quand requis |
|-----------|---------|--------------|
| Epaisseur de la tole | t | Toujours |
| Gorge de la soudure | a | Angle, cruciforme, recouvrement, en T |
| Profondeur de penetration | p | Soudures a penetration partielle |
| Longueur de l'attachement | L | Raidisseurs, attachements longitudinaux |
| Longueur de soudure | L_w | Verifications de rupture de soudure |
| Desalignement axial | e_axial | Si desalignement observe ou suspecte |
| Desalignement angulaire | e_angular | Si desalignement observe ou suspecte |

### 5.3 Classification du chargement

**Etape 1 — Determiner la nature du chargement :**

| Question | Si OUI → | Si NON → |
|----------|----------|----------|
| La charge est-elle repetee cycliquement ? | Chargement de fatigue | Continuer |
| La charge est-elle un evenement soudain unique (crash, chute, explosion) ? | Chargement d'impact | Continuer |
| La charge est-elle une vibration aleatoire (decrite par une DSP) ? | Fatigue vibratoire | Continuer |
| La charge agit-elle simultanement dans plusieurs directions ? | Chargement multiaxial | Chargement uniaxial |

**Etape 2 — Pour le chargement de fatigue, classifier l'amplitude :**

| Condition | Classification | Approche d'evaluation |
|-----------|---------------|----------------------|
| Δσ est constant tout au long de la duree de vie | **Amplitude Constante (AC)** | Lecture directe sur la courbe S-N |
| Δσ varie par blocs ou aleatoirement | **Amplitude Variable (AV)** | Endommagement cumule de Palmgren-Miner |
| Charge decrite par une DSP dans le domaine frequentiel | **Aleatoire / Vibration** | Methode de Dirlik ou bande etroite |

**Etape 3 — Pour le chargement de fatigue, classifier la directionnalite :**

| Condition | Classification | Approche d'evaluation |
|-----------|---------------|----------------------|
| Une seule composante de contrainte (σ ou τ) agit sur la soudure | **Uniaxial** | Courbe S-N standard |
| Les contraintes normales (σ) et de cisaillement (τ) agissent simultanement | **Multiaxial** | Gough-Pollard / Findley / MWCM |
| Les composantes de contrainte sont en phase (rapport σ/τ constant) | **Proportionnel** | Gough-Pollard (plus simple) |
| Les composantes de contrainte sont dephasees (rapport σ/τ variable) | **Non proportionnel** | Findley / MWCM (necessaire) |

**Etape 4 — Determiner le type de charge sur la soudure :**

| Contrainte dominante a la soudure | Classification → TypeCharge |
|-----------------------------------|----------------------------|
| Traction/compression axiale perpendiculaire ou le long de la soudure | **TRACTION (TENSION)** |
| Contrainte induite par la flexion (gradient lineaire dans l'epaisseur) | **FLEXION (BENDING)** |
| Cisaillement dans le plan le long de la gorge de soudure | **CISAILLEMENT (SHEAR)** |
| Combinaison des precedents | **COMBINE (COMBINED)** |

### 5.4 Conditions environnementales

Enregistrer l'environnement de service :

| Parametre | Options | Effet |
|-----------|---------|-------|
| Atmosphere | Air, eau de mer (corrosion libre), eau de mer (protection cathodique), industrielle | Facteur de reduction de corrosion |
| Temperature | Temperature de service [°C] | Facteur de reduction de temperature |
| Hydrogene | Pression d'hydrogene [bar] (si applicable) | Facteur de fragilisation par l'hydrogene |
| Cryogenique | Temperature < -40 °C ? | Risque de transition ductile-fragile |

### 5.5 Donnees de qualite de soudure

Enregistrer la qualite observee ou specifiee :

| Parametre | Options | Source |
|-----------|---------|--------|
| Specification du niveau de qualite | B (meilleur), C (intermediaire), D (minimum) | Plan ou specification selon ISO 5817 |
| Imperfections observees | Caniveau, porosite, manque de fusion, desalignement, manque de penetration, exces de metal fondu | Rapport d'inspection (visuel, CND) |
| Traitement post-soudage | Aucun, HFMI, refusion TIG, meulage, martelage, grenaillage | Specification de fabrication |
| Traitement thermique post-soudage (TTPS) | Oui/Non, temperature, duree de maintien | Specification de fabrication |
| Procede de soudage | MIG/MAG, TIG, laser, FSW, point par resistance, hybride laser | Specification de fabrication |

### 5.6 Exigences de consequence et de securite

| Parametre | Options |
|-----------|---------|
| Classe de consequence | Faible, Normale, Elevee |
| Niveau d'inspection | Aucun, periodique, continu |
| Norme de conception | IIW, Eurocode 3, Eurocode 9, BS 7608, DNV |
| Probabilite de survie requise | 97,7% (standard), 99%, 99,9% |

---

## 6. Phase 2 : Selection de la methode d'evaluation

C'est la decision la plus critique dans la verification en fatigue. Une methode inadaptee conduit a des resultats incorrects. Utiliser la **logique de decision** suivante, en procedant de haut en bas :

### 6.1 Arbre de decision pour la selection de la methode principale

```
DEBUT : Disposez-vous de resultats EF ?
  │
  ├── OUI, avec maillage fin au pied de cordon (element ≤ r_ref/4)
  │     └──► Pouvez-vous modeliser la soudure avec un rayon de reference r_ref = 1 mm ?
  │           ├── OUI ──► METHODE DE LA CONTRAINTE D'ENTAILLE EFFECTIVE (Section 6.4)
  │           └── NON ──► Continuer vers la question du point chaud
  │
  ├── OUI, avec maillage grossier/moyen (element ≈ t)
  │     └──► Pouvez-vous extraire les contraintes de surface aux distances prescrites du pied de cordon ?
  │           ├── OUI ──► METHODE DE LA CONTRAINTE AU POINT CHAUD (Section 6.3)
  │           └── NON ──► METHODE DE LA CONTRAINTE NOMINALE avec contraintes EF (Section 6.2)
  │
  └── NON (calcul manuel ou EF simple)
        └──► Pouvez-vous calculer la contrainte nominale a la section de la soudure ?
              ├── OUI ──► Le detail de soudure correspond-il a une entree du catalogue IIW ?
              │     ├── OUI ──► METHODE DE LA CONTRAINTE NOMINALE (Section 6.2)
              │     └── NON ──► Methode POINT CHAUD ou ENTAILLE requise (besoin d'EF)
              └── NON ──► Geometrie complexe — EF necessaire, puis revenir a l'arbre
```

**Verifications supplementaires (appliquees apres la selection principale) :**

```
Le chargement est-il MULTIAXIAL (σ et τ combines) ?
  ├── OUI ──► Utiliser l'evaluation MULTIAXIALE EN PLUS de la methode principale (Section 10.1)
  └── NON ──► Continuer avec la methode principale

Existe-t-il une FISSURE connue ou supposee ?
  ├── OUI ──► Utiliser la MECANIQUE DE LA RUPTURE (Section 10.3) au lieu de ou en plus de l'approche S-N
  └── NON ──► Continuer avec l'approche S-N

La soudure est-elle a penetration partielle et la rupture en racine est-elle possible ?
  ├── OUI ──► Verifier la FATIGUE EN RACINE (Section 10.2) en plus de la fatigue en pied
  └── NON ──► Continuer avec la fatigue en pied uniquement

Le chargement est-il une vibration aleatoire (entree DSP) ?
  ├── OUI ──► Utiliser la methode de FATIGUE VIBRATOIRE (Section 10.4)
  └── NON ──► Continuer avec l'approche dans le domaine temporel

Disposez-vous d'un acier a haute resistance (R_y > 355 MPa) avec des contraintes residuelles connues ?
  ├── OUI ──► Envisager la METHODE 4R (Section 10.5) pour un traitement plus precis de la contrainte moyenne
  └── NON ──► La correction de contrainte moyenne standard est suffisante
```

### 6.2 Methode de la contrainte nominale

**Quand l'utiliser :**
- Le detail de soudure peut etre clairement identifie dans le catalogue de classes FAT de l'IIW (ou BS 7608)
- Les contraintes nominales peuvent etre calculees par la theorie des poutres ou un EF simple (loin des discontinuites)
- La geometrie structurale correspond a un detail catalogue sans modification significative
- Conception preliminaire ou verification lorsque les EF ne sont pas encore disponibles

**Quand NE PAS l'utiliser :**
- Geometrie complexe ne correspondant a aucun detail catalogue
- Les gradients de contrainte sont trop raides pour definir une contrainte « nominale » significative
- Plusieurs concentrateurs de contrainte interagissent pres de la soudure

**Procedure :**

```
1. Calculer l'etendue de contrainte nominale :
      Δσ_nom = σ_max - σ_min [MPa]
      (a partir des efforts de section : Δσ = ΔF/A + ΔM·y/I pour traction + flexion combines)

2. Selectionner la classe FAT dans le catalogue IIW :
      → En fonction du TypeSoudure + TypeCharge + materiau
      → Voir l'Annexe A pour le catalogue complet

3. Appliquer la chaine de modificateurs (Section 8) pour obtenir FAT_conception

4. Calculer le nombre de cycles admissibles :
      N_admissible = (FAT_conception / Δσ_nom)^m × 2×10⁶

5. Verifier l'acceptation :
      N_admissible ≥ N_requis → CONFORME
      OU : Δσ_nom ≤ FAT_conception × (2×10⁶ / N_requis)^(1/m) → CONFORME
```

### 6.3 Methode de la contrainte au point chaud

**Quand l'utiliser :**
- Des resultats EF sont disponibles avec un maillage adequat dans la zone du pied de cordon
- Le gradient de contrainte pres de la soudure est significatif et ne peut etre capture par la contrainte nominale
- Le detail de soudure est de type standard mais la geometrie a des proportions non couvertes exactement par le catalogue de contrainte nominale
- L'extrapolation de type a (surface de tole) ou de type b (bord de tole) peut etre appliquee

**Quand NE PAS l'utiliser :**
- La rupture en racine est le mode critique (la methode du point chaud ne traite que les ruptures en pied)
- La soudure est au bord libre sans surface de tole pour l'extrapolation
- Le maillage grossier ne permet pas l'extraction de contrainte aux distances prescrites

**Procedure :**

```
1. Extraire les contraintes de surface des EF aux distances prescrites du pied de cordon :

   TYPE A (surface de tole, perpendiculaire a la soudure) :
     Lineaire :    σ_hs = 1,67 × σ(0,4t) - 0,67 × σ(1,0t)
     Quadratique : σ_hs = 2,52 × σ(0,4t) - 2,24 × σ(0,9t) + 0,72 × σ(1,4t)

   TYPE B (le long du bord de tole, le long du pied de cordon) :
     σ_hs = 3 × σ(5mm) - 3 × σ(15mm) + σ(25mm)

2. Selectionner la classe FAT du point chaud :
     Soudure d'angle non porteuse : FAT 100
     Soudure d'angle porteuse :     FAT 90

3. Appliquer la chaine de modificateurs (Section 8) pour obtenir FAT_conception

4. Calculer le nombre de cycles admissibles a partir de la courbe S-N :
     N_admissible = (FAT_conception / Δσ_hs)^m × 2×10⁶

5. Verification : N_admissible ≥ N_requis → CONFORME
```

**Quelle extrapolation choisir :**

| Situation | Utiliser |
|-----------|---------|
| Soudure sur surface de tole, taille de maille ≈ t | Type A, Lineaire (2 points) |
| Soudure sur surface de tole, maillage fin (≤ 0,4t) | Type A, Quadratique (3 points) |
| Soudure au bord de tole ou le long d'un bord libre | Type B (distances fixes) |

### 6.4 Methode de la contrainte d'entaille effective

**Quand l'utiliser :**
- Un maillage EF fin est disponible (taille d'element ≈ r_ref/4 = 0,25 mm)
- La geometrie de la soudure est complexe et ne peut etre classifiee par le catalogue de contrainte nominale
- L'evaluation de la rupture en pied et en racine de soudure est necessaire
- Une haute precision est requise pour les composants critiques
- Toles epaisses (t ≥ 5 mm) pour le r_ref standard, ou toles minces avec r_ref de micro-support

**Quand NE PAS l'utiliser :**
- Toles minces (t < 5 mm) sauf si le r_ref de micro-support = 0,05 mm est utilise
- Lorsqu'un maillage EF grossier est la seule option
- Pour la conception preliminaire (inutilement complexe)

**Procedure :**

```
1. Modeliser la soudure avec le rayon de reference :
     Standard (t ≥ 5 mm) : r_ref = 1,0 mm au pied et/ou a la racine
     Tole mince (t < 5 mm) : r_ref = 0,05 mm

2. Lancer le calcul EF et extraire la contrainte principale maximale a l'entaille :
     Δσ_entaille = σ_max,entaille - σ_min,entaille

3. Utiliser la classe FAT universelle :
     Acier :     FAT 225
     Aluminium : FAT 71

4. Appliquer la chaine de modificateurs (Section 8) pour obtenir FAT_conception
     NOTE : La correction d'epaisseur N'EST PAS appliquee (geometrie explicitement modelisee)
     NOTE : Le km de qualite de soudure N'EST PAS applique (geometrie explicite)

5. Calculer le nombre de cycles admissibles :
     N_admissible = (FAT_conception / Δσ_entaille)^m × 2×10⁶

6. Verification : N_admissible ≥ N_requis → CONFORME
```

### 6.5 Comparaison et resume de selection des methodes

| Critere | Contrainte nominale | Contrainte au point chaud | Contrainte d'entaille effective |
|---------|--------------------|--------------------------|---------------------------------|
| Complexite | Faible | Moyenne | Elevee |
| EF requis ? | Non (optionnel) | Oui | Oui (maillage fin) |
| Exigence de maillage | N/A | Element ≈ t | Element ≈ r_ref/4 |
| Catalogue de details requis ? | Oui | Partiellement | Non |
| Capture la geometrie locale ? | Non | Partiellement | Oui |
| Rupture en racine ? | Non | Non | Oui |
| Application typique | Conception preliminaire, details standards | Verification basee sur EF | Composants critiques, geometrie complexe |
| Conservatisme | Variable (selon la correspondance au catalogue) | Modere | Moins conservatif (plus precis) |

---

## 7. Phase 3 : Selection de la courbe S-N et de la norme

### 7.1 Decision de selection de la norme

```
Quel est le code de conception applicable a votre projet ?

  ├── Structures europeennes en acier (batiments, ponts, grues)
  │     └──► EN 1993-1-9 (Eurocode 3)
  │
  ├── Structures europeennes en aluminium
  │     └──► EN 1999-1-3 (Eurocode 9)
  │
  ├── Pratique britannique pour les structures en acier
  │     └──► BS 7608:2014
  │
  ├── Structures offshore / marines
  │     └──► DNV-RP-C203
  │
  ├── International / automobile / mecanique generale
  │     └──► IIW XIII-2259-15 (2024)  ← DEFAUT RECOMMANDE
  │
  └── Aucune exigence de code specifique
        └──► IIW XIII-2259-15 (2024)  ← DEFAUT RECOMMANDE
```

### 7.2 Parametres des courbes S-N par norme

#### IIW (Defaut — Recommande)

| Parametre | Acier | Aluminium |
|-----------|-------|-----------|
| Cycles de reference (N_ref) | 2 × 10⁶ | 2 × 10⁶ |
| Pente m₁ (sous le coude) | 3,0 | 3,376 |
| Pente m₂ (au-dessus du coude, AV uniquement) | 5,0 | 5,376 |
| Point de coude (N_coude) | 10⁷ | 10⁷ |
| Coupure (N_coupure) | 10⁹ | 10⁹ |
| Amplitude constante : sous la contrainte du coude | Duree de vie infinie | Duree de vie infinie |
| Amplitude variable : sous la contrainte du coude | Continue avec m₂ | Continue avec m₂ |

**Equation S-N :**
```
Region 1 (N ≤ N_coude) :
    N = (FAT / Δσ)^m₁ × N_ref

Region 2 (N_coude < N ≤ N_coupure, amplitude variable uniquement) :
    N = (Δσ_coude / Δσ)^m₂ × N_coude
    ou Δσ_coude = FAT × (N_ref / N_coude)^(1/m₁)
```

#### Eurocode 3 (EN 1993-1-9)

| Parametre | Valeur |
|-----------|--------|
| Pente m₁ | 3,0 |
| Pente m₂ | 5,0 |
| Point de coude | 5 × 10⁶ (plus tot que l'IIW) |
| Coupure | 10⁸ (plus bas que l'IIW) |

#### BS 7608:2014

| Classe de detail | Pente m | Contrainte de reference S_ref [MPa] |
|-----------------|---------|--------------------------------------|
| B | 4,0 | 100 |
| C | 3,5 | 78 |
| D | 3,0 | 53 |
| E | 3,0 | 47 |
| F | 3,0 | 40 |
| F2 | 3,0 | 35 |
| G | 3,0 | 29 |
| W1 | 3,0 | 25 |

Coupure : 10⁸ cycles

#### Eurocode 9 (EN 1999-1-3 — Aluminium)

| Parametre | Valeur |
|-----------|--------|
| Pente m₁ | 3,4 (la plupart des details) ou 4,3 (FAT 32, 28, 25) |
| Pente m₂ | 5,4 |
| Point de coude | 5 × 10⁶ |
| Coupure | 10⁸ |

### 7.3 Regle de decision : Quelle courbe S-N pour votre cas

```
SI materiau = aluminium
    SI norme = eurocode9 → Utiliser la courbe Eurocode 9 (m₁=3,4, coude a 5e6)
    SINON → Utiliser la courbe IIW aluminium (m₁=3,376, coude a 1e7)

SI materiau = acier
    SI norme = eurocode3 → Utiliser la courbe Eurocode 3 (m₁=3, coude a 5e6, coupure 1e8)
    SI norme = bs7608 → Utiliser la courbe BS 7608 (m variable selon la classe)
    SI norme = dnv → Utiliser la courbe IIW + DFF DNV sur la duree de vie
    SINON → Utiliser la courbe IIW acier (m₁=3, coude a 1e7, coupure 1e9)

SI chargement = amplitude_constante
    → La courbe S-N se termine au point de coude (duree de vie infinie en dessous)
    → Exception : un environnement corrosif supprime la limite d'endurance

SI chargement = amplitude_variable
    → La courbe S-N se prolonge au-dela du coude avec la pente m₂
    → La coupure s'applique (pas d'endommagement sous la contrainte de coupure)
```

---

## 8. Phase 4 : Chaine de modificateurs — Facteurs de correction

La classe FAT « brute » doit etre ajustee par une chaine de facteurs de correction avant utilisation. **Tous les facteurs applicables sont multiplies entre eux** pour obtenir la classe FAT de conception effective :

```
FAT_conception = FAT_base × f_epaisseur × f_environnement × f_traitement × f_procede × f_qualite / (γ_Mf × γ_Ff) × f_survie
```

**Appliquer les modificateurs dans l'ordre suivant. Chaque modificateur n'est applique QUE lorsque la condition correspondante est remplie :**

### 8.1 Correction d'epaisseur

**Quand appliquer :** Epaisseur de tole t > 25 mm (epaisseur de reference t_ref = 25 mm)

**Quand NE PAS appliquer :**
- Methode de la contrainte d'entaille effective (geometrie explicitement modelisee)
- Chargement en cisaillement sur les soudures d'angle (exposant = 0)
- t ≤ 25 mm (facteur = 1,0)

**Formule :**
```
f_epaisseur = (t_ref / t_eff)^n    pour t_eff > t_ref
f_epaisseur = 1,0                   pour t_eff ≤ t_ref

t_ref = 25 mm
```

**Exposant n par type de soudure et charge :**

| Type de soudure | Traction/Flexion | Cisaillement |
|----------------|-----------------|--------------|
| Bout a bout | 0,2 | 0,1 |
| Cruciforme | 0,3 | — |
| En T | 0,2 | — |
| Angle | 0,1 | 0,0 |
| Recouvrement | 0,1 | 0,0 |
| Raidisseur | 0,2 | — |

### 8.2 Correction environnementale

**Quand appliquer :** L'environnement de service N'EST PAS de l'air sec a temperature ambiante

**Facteur de corrosion (f_corrosion) :**

| Environnement | Acier | Aluminium |
|---------------|-------|-----------|
| Air (sec ou modere) | 1,0 | 1,0 |
| Eau de mer, corrosion libre | 0,7 | 0,6 |
| Eau de mer, protection cathodique | 0,85 | 0,8 |
| Atmosphere industrielle | 0,9 | 0,85 |
| Hydrogene gazeux | 0,5 | 0,9 |

**Facteur de temperature (f_temperature) :**

| Materiau | Condition | Facteur |
|----------|-----------|---------|
| Acier | T ≤ 100 °C | 1,0 |
| Acier | 100 < T ≤ 300 °C | 1,0 − 0,0015 × (T − 100) |
| Acier | T > 300 °C | **Hors domaine** (regime de fluage) |
| Aluminium | T ≤ 50 °C | 1,0 |
| Aluminium | 50 < T ≤ 150 °C | 1,0 − 0,003 × (T − 50) |
| Aluminium | T > 150 °C | **Hors domaine** |

**Facteur de fragilisation par l'hydrogene (f_hydrogene) :**
```
f_H2 = 1 / (1 + 0,002 × p)    [acier uniquement, p en bar]
f_H2 = 1,0                      [aluminium, non affecte]
```

**Facteur cryogenique (f_cryo) :**
```
T < -40 °C (acier au carbone/faiblement allie) : f_cryo = 0,8
T < -40 °C (acier inoxydable austenitique ou aluminium) : f_cryo = 1,0
T ≥ -40 °C : f_cryo = 1,0
```

**Facteur environnemental combine :**
```
f_environnement = f_corrosion × f_temperature × f_H2 × f_cryo
```

**Regle speciale :** Dans les environnements d'eau de mer (libre ou PC), la limite d'endurance est **supprimee** — la courbe S-N continue avec la pente m₁ indefiniment (pas de point de coude).

### 8.3 Amelioration par traitement post-soudage

**Quand appliquer :** Un traitement post-soudage a ete realise et verifie

**Amelioration en nombre de paliers FAT (sequence FAT standard IIW : 36, 40, 45, 50, 56, 63, 71, 80, 90, 100, 112, 125, 140, 160) :**

| Traitement | Paliers d'amelioration | Conditions / Notes |
|------------|----------------------|-------------------|
| Aucun | 0 | Etat brut de soudage (reference) |
| Meulage | +1 | Lissage de la surface au pied de cordon |
| Refusion TIG | +2 | Refusion du pied de cordon pour un profil plus lisse |
| Grenaillage de precontrainte | +2 | Introduction de contraintes residuelles de compression |
| Martelage | +2 a +3 | Amelioration dependante de la limite d'elasticite |
| **HFMI** | **+4 a +8** | **IIW 2024 dependant de la limite d'elasticite :** voir tableau ci-dessous |

**Tableau d'amelioration HFMI (IIW-2259-15, 2024) :**

| Limite d'elasticite R_y [MPa] | Paliers d'amelioration |
|-------------------------------|----------------------|
| 235 – 355 | +4 |
| 355 – 550 | +6 |
| 550 – 750 | +8 |
| 750 – 1300 | +8 (plafonne) |

**Exemple :** FAT 71 avec HFMI sur acier R_y = 500 MPa :
- Amelioration +6 paliers : 71 → 80 → 90 → 100 → 112 → 125 → 140
- Resultat : FAT 140

**Restrictions importantes :**
- L'amelioration par traitement post-soudage n'est valable QUE pour la rupture en pied de cordon
- La rupture en racine N'EST PAS amelioree par les traitements de surface
- La qualite du traitement doit etre verifiee par inspection

### 8.4 Facteur de procede de soudage

**Quand appliquer :** Le procede de soudage differe du MIG/MAG (procede de reference)

| Procede | Facteur (sur FAT) |
|---------|-------------------|
| MIG/MAG | 1,00 (reference) |
| TIG | 1,10 (meilleure geometrie du pied) |
| Laser | 1,10 – 1,20 (ZAT etroite) |
| FSW | 1,30 (etat solide, pas de defauts) |
| Hybride laser | 1,15 |

### 8.5 Qualite de soudure et desalignement

**Ajustement de la classe FAT selon le niveau de qualite (ISO 5817) :**

Au lieu d'appliquer un facteur, selectionner la classe FAT de base selon le niveau de qualite atteint :

| Niveau de qualite | Bout a bout | Angle | Cruciforme | En T | Recouvrement |
|-------------------|-------------|-------|------------|------|--------------|
| B (le plus eleve) | FAT 112 | FAT 90 | FAT 80 | FAT 80 | FAT 71 |
| C (intermediaire) | FAT 90 | FAT 71 | FAT 63 | FAT 63 | FAT 56 |
| D (minimum) | FAT 71 | FAT 56 | FAT 50 | FAT 50 | FAT 45 |

**Facteur de majoration de contrainte par desalignement (k_m) :**

Si un desalignement axial ou angulaire est present, la contrainte appliquee est augmentee :

```
Axial :    k_m,axial = 1 + e/t
Angulaire : k_m,angulaire = 1 + c × (e/t)
    ou c = 1,5 (extremites encastrees) ou 3,0 (extremites articulees)

Combine : k_m = k_m,axial × k_m,angulaire

Contrainte effective : σ_eff = σ_nom × k_m
```

**Quand appliquer :** La methode de la contrainte nominale est utilisee ET le desalignement a ete mesure ou suppose a partir des tolerances. Pour la methode de la contrainte d'entaille, le desalignement doit etre modelise explicitement dans les EF.

### 8.6 Correction de contrainte moyenne

**Quand appliquer :** Le chargement a une contrainte moyenne non nulle ET le joint est detensionnement (TTPS)

**Regle de decision pour le choix de la methode :**

```
SI le joint est brut de soudage (pas de TTPS) :
    → Pas de correction de contrainte moyenne necessaire (hypothese IIW : les contraintes
      residuelles sont deja a la limite d'elasticite, donc l'effet du rapport R est negligeable)
    → f(R) = 1,0

SI le joint est detensionnement (TTPS) :
    → Appliquer le facteur d'amelioration IIW f(R) :
        R < -1 :        f(R) = 1,6
        -1 ≤ R ≤ 0,5 :  f(R) = -0,4R + 1,2
        R > 0,5 :       f(R) = 1,0

    OU appliquer l'une des methodes classiques :
        Goodman :   Δσ_eq = Δσ / (1 - σ_m/S_u)     [la plus courante]
        Gerber :    Δσ_eq = Δσ / (1 - (σ_m/S_u)²)   [moins conservatif]
        Soderberg : Δσ_eq = Δσ / (1 - σ_m/R_y)       [le plus conservatif]
```

**Guide de selection :**
- **IIW f(R) :** Recommande pour les joints soudes ; utiliser quand le rapport R est connu
- **Goodman :** Usage general ; conservatif pour la plupart des cas
- **Gerber :** A utiliser quand Goodman est trop conservatif et que des donnees d'essai le justifient
- **Soderberg :** A utiliser pour les composants critiques pour la securite necessitant un conservatisme maximal

### 8.7 Prise en compte des contraintes residuelles

**Etat brut de soudage (par defaut) :**
```
σ_res = R_y (limite d'elasticite)    [hypothese conservative IIW]
→ Pas de benefice de correction de contrainte moyenne (rapport R au pire cas deja suppose)
```

**Apres TTPS :**
```
Fraction de contrainte residuelle restante :
    f_relaxation = exp(-k × (T - 200) × √t_maintien)

ou :
    k = 0,004 (constante empirique)
    T = temperature de TTPS [°C] (doit etre > 200 °C pour tout relachement)
    t_maintien = duree de maintien [heures]

σ_res,finale = σ_res,initiale × f_relaxation

Relaxation typique :
    550 °C, 1 heure → ~70% de relaxation
    600 °C, 1 heure → ~80% de relaxation
    620 °C, 2 heures → ~90% de relaxation
```

**Sous chargement cyclique (relaxation) :**
```
Apres le premier cycle : σ_res = max(0, R_y - σ_max)    [si plasticite]
Poursuite du cyclage : σ_res(N) = σ_res(1) × (1 - 0,1 × log₁₀(N))
```

### 8.8 Coefficients de securite

**Coefficient partiel de securite sur la resistance (γ_Mf) :**

*Norme IIW :*

| Consequence \ Inspection | Periodique | Continue | Aucune |
|-------------------------|------------|---------|--------|
| Faible | 1,00 | 1,00 | 1,00 |
| Normale | 1,15 | 1,00 | 1,25 |
| Elevee | 1,30 | 1,15 | 1,40 |

*Eurocode 3 :*

| Consequence | γ_Mf |
|-------------|-------|
| Faible | 1,00 |
| Normale | 1,15 |
| Elevee | 1,35 |

**Facteur de dimensionnement en fatigue DNV (DFF) :**

| Consequence \ Inspection | Periodique | Aucune |
|-------------------------|------------|--------|
| Faible | 1,0 | 2,0 |
| Normale | 2,0 | 3,0 |
| Elevee | 3,0 | 10,0 |

Applique comme : N_conception = N_calcule / DFF (reduit la duree de vie admissible)

**Coefficient partiel de charge (γ_Ff) :** 1,0 pour toutes les normes (charges supposees deja ponderees)

**Ajustement de la probabilite de survie :**
```
Les courbes IIW sont caracteristiques a 97,7% de survie (moyenne − 2σ)
Ecart-type en log₁₀(N) = 0,2 pour les joints soudes

Pour une probabilite differente :
    f_survie = 10^(-Δz × 0,2 / m)
    ou Δz = z(cible) - 2,0

Courant :
    97,7% → f_survie = 1,000 (reference)
    99,0% → f_survie ≈ 0,957
    99,9% → f_survie ≈ 0,869
```

**Effet combine sur la classe FAT :**
```
FAT_conception = FAT_base × f_survie / (γ_Mf × γ_Ff)
```

### 8.9 Chaine complete de modificateurs — Tableau recapitulatif

Appliquer les facteurs suivants **dans l'ordre**. Si un facteur ne s'applique pas (condition non remplie), le fixer a 1,0 :

| # | Facteur | Symbole | Applique a | Condition d'application |
|---|---------|---------|-----------|------------------------|
| 1 | Correction d'epaisseur | f_ep | Classe FAT | t > 25 mm ET pas methode entaille |
| 2 | Correction environnementale | f_env | Classe FAT | Environnement ≠ air a 20°C |
| 3 | Traitement post-soudage | f_tps | Classe FAT (paliers) | Traitement applique |
| 4 | Procede de soudage | f_proc | Classe FAT | Procede ≠ MIG/MAG |
| 5 | Desalignement | k_m | Contrainte appliquee | Desalignement present |
| 6 | Correction de contrainte moyenne | f(R) ou equivalent | Contrainte appliquee | Joint detensionnement, R ≠ 0 |
| 7 | Coefficient partiel de securite (resistance) | 1/γ_Mf | Classe FAT | Toujours (γ_Mf ≥ 1,0) |
| 8 | Coefficient partiel de charge | 1/γ_Ff | Etendue de contrainte | Toujours (typiquement 1,0) |
| 9 | Probabilite de survie | f_surv | Classe FAT | Cible ≠ 97,7% |

```
Contrainte effective :  Δσ_eff = Δσ_nom × k_m × γ_Ff / f(R)
FAT effective :         FAT_eff = FAT_base × f_ep × f_env × f_tps × f_proc × f_surv / γ_Mf
```

---

## 9. Phase 5 : Calcul d'endommagement et criteres d'acceptation

### 9.1 Chargement a amplitude constante

**Procedure :**

```
1. Calculer l'etendue de contrainte effective : Δσ_eff (apres corrections)
2. Calculer la classe FAT effective : FAT_eff (apres tous les modificateurs)
3. Calculer le nombre de cycles admissibles :

   N_admissible = (FAT_eff / Δσ_eff)^m × 2×10⁶

4. Verifier la duree de vie infinie :
   SI Δσ_eff < Δσ_coude ET chargement a amplitude constante ET l'environnement ne supprime pas la limite d'endurance :
       → N_admissible = ∞ → CONFORME (duree de vie infinie)

   ou Δσ_coude = FAT_eff × (2×10⁶ / N_coude)^(1/m₁)

5. Verifier la duree de vie finie :
   SI N_admissible ≥ N_requis → CONFORME
   SI N_admissible < N_requis → NON CONFORME

6. Calculer le coefficient de securite :
   CS = (N_admissible / N_requis)^(1/m)
       → CS > 1,0 → CONFORME
       → CS ≤ 1,0 → NON CONFORME
```

### 9.2 Chargement a amplitude variable

**Procedure (endommagement cumule de Palmgren-Miner) :**

```
1. Decomposer l'historique de chargement en blocs d'etendue de contrainte :
   - A partir d'un spectre mesure : utiliser le COMPTAGE RAINFLOW (ASTM E1049-85)
   - A partir d'un spectre de conception : utiliser des blocs de charge predefinis {(Δσ_i, n_i)}

2. Pour chaque bloc i :
   a. Calculer la contrainte effective : Δσ_i,eff (appliquer desalignement, contrainte moyenne)
   b. Calculer les cycles admissibles a partir de la courbe S-N :
      - Si Δσ_i,eff ≥ Δσ_coude :     N_i = (FAT_eff / Δσ_i,eff)^m₁ × N_ref
      - Si Δσ_coude > Δσ_i,eff ≥ Δσ_coupure : N_i = (Δσ_coude / Δσ_i,eff)^m₂ × N_coude
      - Si Δσ_i,eff < Δσ_coupure :   N_i = ∞ (pas de contribution a l'endommagement)
   c. Calculer l'endommagement partiel : D_i = n_i / N_i

3. Sommer l'endommagement cumule :
   D_total = Σ D_i

4. Verifier l'acceptation :
   D_total < D_limite → CONFORME
   D_total ≥ D_limite → NON CONFORME

   ou D_limite :
     Structures courantes :           D_limite = 1,0
     Structures critiques pour la securite : D_limite = 0,5

5. Calculer l'etendue de contrainte equivalente a amplitude constante :
   Δσ_eq = [Σ(n_i × Δσ_i,eff^m) / Σn_i]^(1/m)
   (utile pour la comparaison et le rapport)
```

### 9.3 Resume des criteres d'acceptation

| Critere | Condition CONFORME | Notes |
|---------|-------------------|-------|
| Amplitude constante, duree de vie finie | N_admissible ≥ N_requis | OU CS ≥ 1,0 |
| Amplitude constante, duree de vie infinie | Δσ_eff < Δσ_coude | Uniquement si la limite d'endurance existe |
| Amplitude variable | D_total < D_limite | D_limite = 1,0 (normal) ou 0,5 (critique) |
| Multiaxial (Gough-Pollard) | (Δσ/Δσ_R)² + (Δτ/Δτ_R)² < 1 | Critere d'interaction |
| Multiaxial (Findley) | FP / FP_limite < 1 | Critere du plan critique |
| Mecanique de la rupture | a_finale < a_critique a N_requis | La fissure ne doit pas atteindre la taille critique |
| Fatigue en racine | N_admissible,racine ≥ N_requis | Verification separee pour la rupture en racine |

---

## 10. Cas particuliers en fatigue

### 10.1 Fatigue multiaxiale

**Quand necessaire :** Les contraintes normales (σ) et de cisaillement (τ) combinees agissent simultanement sur la soudure.

**Etape 1 — Determiner la proportionnalite :**

```
SI les historiques temporels de σ(t) et τ(t) sont disponibles :
    Calculer le rapport : ρ(t) = τ(t) / σ(t)
    SI coefficient de variation de ρ(t) < 0,1 → PROPORTIONNEL
    SINON → NON PROPORTIONNEL

SI seules les valeurs de crete sont connues :
    SI σ et τ atteignent leurs maxima simultanement → supposer PROPORTIONNEL
    SI ils sont dephases → NON PROPORTIONNEL
```

**Etape 2 — Selectionner le critere multiaxial :**

| Type de chargement | Critere recommande |
|-------------------|--------------------|
| Proportionnel | **Gough-Pollard** (recommande IIW) |
| Non proportionnel, modere | **Methode de la courbe de Wohler modifiee (MWCM)** |
| Non proportionnel, composants critiques | **Plan critique de Findley** |

**Etape 3 — Appliquer le critere selectionne :**

**Gough-Pollard (Proportionnel) :**
```
Verification : (Δσ / Δσ_R)² + (Δτ / Δτ_R)² ≤ 1,0

ou :
    Δσ_R = FAT_σ × (N_ref / N)^(1/m)    [etendue de contrainte normale admissible]
    Δτ_R = FAT_τ × (N_ref / N)^(1/m)    [etendue de contrainte de cisaillement admissible]

SI FAT_τ n'est pas specifie : FAT_τ = FAT_σ / √3

Taux d'utilisation = √((Δσ/Δσ_R)² + (Δτ/Δτ_R)²)
CONFORME si taux d'utilisation < 1,0
```

**Plan critique de Findley (Non proportionnel) :**
```
Pour chaque angle de plan θ de 0° a 180° :
    τ_a(θ) = amplitude de contrainte de cisaillement sur le plan
    σ_n,max(θ) = contrainte normale maximale sur le plan

    FP(θ) = τ_a(θ) + k × σ_n,max(θ)

Trouver θ_critique ou FP est maximal.

Parametre materiau k = 0,2 a 0,4 pour les joints soudes (typiquement 0,3)

Taux d'utilisation = FP(θ_critique) / FP_admissible
CONFORME si taux d'utilisation < 1,0
```

**MWCM (Non proportionnel) :**
```
Etendue de contrainte equivalente :
    Δσ_eq = √(Δσ² + 3 × Δτ²)    [critere energetique de von Mises]

Rapport de biaxialite : ρ = Δτ / Δσ (ou τ_a / σ_a)

Pente S-N modifiee : m_eff = 3,0 + 2,0 × min(ρ, 1,0)

Evaluer par rapport a la courbe S-N avec la pente m_eff
```

### 10.2 Fatigue en racine (soudures a penetration partielle)

**Quand verifier :** La soudure est une soudure d'angle a penetration partielle et la fissuration depuis la racine est geometriquement possible.

**Regle d'identification :**
```
SI type de soudure = ANGLE ou EN T ou RECOUVREMENT ou CRUCIFORME
    ET penetration < epaisseur de tole (penetration partielle)
    → La verification de fatigue en racine est OBLIGATOIRE en plus de la verification en pied
```

**Procedure :**

```
1. Calculer le facteur de concentration de contrainte en racine :
   FCC_racine = 1 + 2 × √((t - p) / (2 × a))
   ou :
       t = epaisseur de tole [mm]
       p = profondeur de penetration [mm]
       a = gorge de soudure [mm]

   Pour la flexion : FCC_flexion = FCC_traction × 0,85

2. Calculer la contrainte d'entaille en racine :
   σ_racine = σ_nominale × FCC_racine × min(t / a_eff, 3,0)
   ou a_eff = a + p

3. Utiliser la classe FAT en racine :
   Acier :     FAT 200
   Aluminium : FAT 71

4. Calculer N_admissible pour la racine :
   N_admissible,racine = (FAT_racine / Δσ_racine)^m × N_ref

5. Comparer avec le resultat en pied :
   Emplacement critique = min(N_admissible,pied, N_admissible,racine)
   Indiquer quel emplacement gouverne
```

**Important :** Les traitements de surface post-soudage (HFMI, meulage, etc.) N'AMELIORENT PAS la duree de vie en fatigue en racine.

### 10.3 Mecanique de la rupture (MLER)

**Quand utiliser :**
- Une fissure ou un defaut est connu (suite a une inspection ou suppose)
- Evaluation de l'aptitude au service d'un composant avec des defauts detectes
- Estimation de la duree de vie residuelle apres detection d'une fissure
- Verification de la duree de vie lorsque l'approche S-N est insuffisante

**Procedure :**

```
1. Definir les parametres de fissure initiaux :
   a₀ = profondeur de fissure initiale [mm]
       → Si connue par inspection : utiliser la valeur mesuree
       → Si supposee (conception) : a₀ = 0,1 a 0,5 mm (typique pour les joints soudes)
   a_c = profondeur de fissure critique [mm]
       → A partir de la tenacite : a_c = (K_Ic / (Y × σ_max))² / π
       → Ou par exigence structurale (ex. traversee = epaisseur de tole t)

2. Selectionner les parametres de la loi de Paris :

   | Environnement | Materiau | C [mm/cycle] | m |
   |---------------|----------|-------------|---|
   | Air | Acier | 5,21 × 10⁻¹³ | 3,0 |
   | Eau de mer (libre) | Acier | 1,30 × 10⁻¹² | 3,0 |
   | Eau de mer (PC) | Acier | (utiliser valeurs air) | 3,0 |
   | Air | Aluminium | 1,59 × 10⁻¹¹ | 3,06 |

3. Selectionner les facteurs de geometrie et de majoration de soudure :

   Facteur de geometrie Y(a/t) :
       Fissure de bord :   Y = ajustement polynomial (BS 7910)
       Fissure traversante : Y = 1,0
       Fissure de surface : Y = 1,12 / √Q (semi-elliptique)

   Facteur de majoration de soudure Mk(a/t) :
       Bout a bout en T :  Mk = 0,51 × (a/t)^(-0,31)
       Cruciforme :        Mk = 0,50 × (a/t)^(-0,29)
       Recouvrement :      Mk = 0,45 × (a/t)^(-0,25)
       Angle :             Mk = 0,48 × (a/t)^(-0,30)

4. Etendue du facteur d'intensite de contrainte :
   ΔK = Y × Mk × Δσ × √(π × a)

5. Integrer la propagation de fissure :
   da/dN = C × (ΔK - ΔK_seuil)^m    [seuil inclus]

   ΔK_seuil (seuil) :
       Acier : 63 MPa√mm (~2 MPa√m)
       Aluminium : 30 MPa√mm (~1 MPa√m)

   Integration numerique : Euler explicite de a₀ a a_c
   → Compter le nombre total de cycles N_total

6. Acceptation :
   N_total ≥ N_requis → CONFORME (la fissure n'atteint pas la taille critique pendant la duree de vie)
   N_total < N_requis → NON CONFORME
```

### 10.4 Fatigue vibratoire (domaine frequentiel)

**Quand utiliser :** Le chargement est une vibration aleatoire decrite par une Densite Spectrale de Puissance (DSP) plutot qu'un historique temporel.

**Procedure :**

```
1. Obtenir la DSP : G(f) [MPa²/Hz] en fonction de la frequence f [Hz]
   (a partir de donnees mesurees, de specifications d'essai ou d'EF)

2. Calculer les moments spectraux :
   m_n = ∫ f^n × G(f) df    pour n = 0, 1, 2, 4

3. Calculer les parametres de bande passante :
   Facteur d'irregularite : γ = m₂ / √(m₀ × m₄)
   Taux de cretes attendu :  E_P = √(m₄ / m₂) [cretes/seconde]
   Taux de zeros attendu :   E_0 = √(m₂ / m₀) [passages par zero/seconde]

4. Selectionner la methode selon la bande passante :

   SI γ > 0,99 :
       → Approximation BANDE ETROITE (conservative, simple)
       D = E_0 × T × (2√(2m₀))^m × Γ(1 + m/2) / C_sn
       ou C_sn = FAT^m × N_ref

   SI γ < 0,99 :
       → METHODE DE DIRLIK (la plus precise pour les processus gaussiens a large bande)
       Calculer la PDF de Dirlik p(S) et integrer :
       D = E_P × T × ∫ S^m × p(S) dS / C_sn

   ALTERNATIVEMENT :
       → CORRECTION DE WIRSCHING-LIGHT (correction de la bande etroite)
       ε = √(1 - γ²)    [parametre de bande passante]
       λ = a(m) + (1 - a(m)) × (1 - ε)^b(m)
       a(m) = 0,926 - 0,033m
       b(m) = 1,587m - 2,323
       D_corrige = λ × D_bande_etroite

5. Duree : T = duree totale d'exposition [secondes]

6. Acceptation :
   D < D_limite → CONFORME
```

**Guide de selection de la methode :**

| Bande passante (γ) | Methode recommandee | Notes |
|--------------------|--------------------|----|
| γ > 0,99 | Bande etroite | Simple, conservatif |
| 0,7 < γ < 0,99 | Wirsching-Light | Bonne correction pour bande passante moderee |
| γ < 0,7 | Dirlik | Necessaire pour les processus a large bande |

### 10.5 Methode 4R (correction avancee de contrainte moyenne)

**Quand utiliser :**
- Acier a haute resistance (R_y > 355 MPa) ou les corrections de contrainte moyenne standard peuvent etre imprecises
- Etat de contrainte residuelle connu (mesure ou donnees TTPS disponibles)
- Precision maximale requise pour les composants critiques

**Procedure :**

```
1. Determiner les contraintes locales (correction de Neuber) :
   SI σ_elastique ≤ R_y :
       σ_locale = σ_elastique
   SI σ_elastique > R_y :
       σ_locale = R_y (limitee a la limite d'elasticite)
       ε_locale = σ_elastique² / (E × R_y)

2. Inclure la contrainte residuelle :
   σ_max,locale = σ_max,neuber + σ_res (limite a R_y)
   σ_min,locale = σ_min,neuber + σ_res

3. Rapport de contrainte local :
   R_local = σ_min,locale / σ_max,locale

4. Sensibilite a la contrainte moyenne :
   M = 0,00035 × R_m - 0,1    (borne ≥ 0)

5. Etendue de contrainte equivalente :
   Δσ_eq = Δσ × (1 - M × R_local) / (1 + M)

6. Evaluer par rapport a la courbe maitresse :
   Acier :     FAT 200 (r_ref = 1mm, R_local = 0)
   Aluminium : FAT 71
```

---

# PARTIE III — VERIFICATION DE LA RESISTANCE A L'IMPACT

## 11. Phase 1 : Caracterisation dynamique du materiau

### 11.1 Quand l'evaluation d'impact est-elle requise ?

```
SI l'une des conditions suivantes est remplie :
    - Le composant est dans un chemin de charge de crash
    - La specification de conception inclut un cas de charge d'impact/crash
    - La vitesse de deformation en service depasse 1 /s
    - La duree de chargement dynamique < 100 ms
→ L'evaluation d'impact est OBLIGATOIRE
```

### 11.2 Selection du modele de vitesse de deformation

**Regle de decision :**

```
SI seuls les effets de vitesse de deformation sont necessaires (pas de thermique ni d'ecrouissage) :
    → Utiliser le modele de COWPER-SYMONDS (plus simple, suffisant pour la plupart des cas de crash)

SI les effets thermiques sont significatifs (echauffement adiabatique, impact a grande vitesse) :
    → Utiliser le modele de JOHNSON-COOK (capture vitesse de deformation + temperature + ecrouissage)

SI le materiau est un acier de construction courant :
    → Cowper-Symonds est le choix par defaut

SI une simulation haute fidelite est necessaire (balistique, formage) :
    → Johnson-Cook avec couplage thermique
```

### 11.3 Modele de Cowper-Symonds

**Formule :**
```
DIF = 1 + (ε̇ / D)^(1/q)
σ_dynamique = σ_statique × DIF

ou :
    ε̇ = vitesse de deformation [1/s]
    D, q = constantes materiaux
```

**Parametres materiaux :**

| Nuance | D [1/s] | q | Application typique |
|--------|---------|---|---------------------|
| DC04 | 40,4 | 5,0 | Emboutissage profond, panneaux de carrosserie |
| DP600 | 100,0 | 4,73 | Renforts structuraux |
| DP780 | 200,0 | 4,5 | Montants B, impact lateral |
| DP980 | 300,0 | 4,0 | Composants de cage de securite |
| HSLA340 | 80,0 | 4,8 | Chassis, berceaux |
| HSLA420 | 120,0 | 4,5 | Traverses |
| 22MnB5 | 802,0 | 3,585 | Composants emboutis a chaud |
| S355J2 | 40,4 | 5,0 | Acier de construction (genie civil/general) |
| 316L | 100,0 | 10,0 | Inoxydable (haute sensibilite a la vitesse) |
| 6061-T6 | 6500,0 | 4,0 | Structures aluminium |
| 6082-T6 | 6500,0 | 4,0 | Profiles aluminium |
| 5083-H111 | 6500,0 | 4,0 | Aluminium marine |
| 5754-O | 6500,0 | 4,0 | Aluminium automobile |
| 7075-T6 | 6500,0 | 4,0 | Aluminium aeronautique |

**Vitesses de deformation typiques par application :**

| Scenario | Vitesse de deformation [1/s] | Notes |
|----------|------------------------------|-------|
| Essai quasi-statique | 10⁻⁴ a 10⁻² | Essai de traction standard |
| Chargement sismique | 10⁻² a 1 | Reponse aux seismes |
| Crash automobile | 1 a 500 | Impact frontal/lateral/arriere |
| Crash a grande vitesse | 500 a 1000 | Collision a grande vitesse |
| Explosion/souffle | 1000 a 10⁴ | Hors domaine |

### 11.4 Modele de Johnson-Cook

**Formule :**
```
σ = (A + B × εₚⁿ) × (1 + C × ln(ε̇ / ε̇₀)) × (1 - T*ᵐ)

ou :
    T* = (T - T_ref) / (T_fusion - T_ref)    [temperature homologue]
    εₚ = deformation plastique
    ε̇₀ = vitesse de deformation de reference (typiquement 1,0 /s)
    T_ref = temperature de reference (typiquement 293 K)
```

**Decomposition en trois termes :**

| Terme | Formule | Signification physique |
|-------|---------|----------------------|
| Ecrouissage | (A + B × εₚⁿ) | La contrainte augmente avec la deformation plastique |
| Vitesse de deformation | (1 + C × ln(ε̇/ε̇₀)) | La contrainte augmente avec la vitesse de chargement |
| Adoucissement thermique | (1 − T*ᵐ) | La contrainte diminue avec l'elevation de temperature |

**Quand utiliser chaque terme :**
- Analyse statique a temperature ambiante : Terme 1 uniquement (courbe σ-ε pure)
- Crash a temperature ambiante : Termes 1 + 2 (limite d'elasticite dependante de la vitesse)
- Impact a grande vitesse avec echauffement adiabatique : Les trois termes
- Formage a chaud (emboutissage a chaud) : Termes 1 + 3 (pas d'effet de vitesse necessaire)

**Pour l'evaluation de crash a temperature ambiante :**
```
Limite d'elasticite dynamique a 0,2% :
    σ_y,dyn = (A + B × 0,002ⁿ) × (1 + C × ln(ε̇ / ε̇₀))
```

### 11.5 Criteres d'acceptation pour le materiau dynamique

```
Calculer :
    DIF = σ_dynamique / σ_statique
    σ_dynamique = σ_statique × DIF

Verification :
    SI le DIF est anormalement eleve (> 3 pour l'acier, > 2 pour l'aluminium) :
        → Verifier l'hypothese de vitesse de deformation ; peut indiquer une erreur dans l'estimation de la charge

Utilisation en conception :
    → Utiliser σ_dynamique comme limite d'elasticite dans toutes les verifications d'impact subsequentes
    → σ_dynamique remplace σ_statique dans les formules de rupture de soudure et les calculs d'energie
```

---

## 12. Phase 2 : Evaluation de la rupture des joints soudes sous impact

### 12.1 Quand l'evaluation de rupture de soudure est-elle requise ?

```
SI la structure contient des soudures dans le chemin de charge de crash
    ET la soudure est soumise a des efforts significatifs pendant l'impact
→ La verification de rupture de soudure est OBLIGATOIRE

La verification assure que les soudures ne rompent pas ou ne se dechirent pas pendant l'evenement de crash.
```

### 12.2 Selection de la methode

```
SI les efforts resultants sur la soudure sont connus (des EF ou du calcul manuel) :
    → Utiliser la verification BASEE SUR LES EFFORTS (plus simple, Section 12.3)

SI les composantes de contrainte dans le plan de gorge de la soudure sont connues (EF detailles) :
    → Utiliser la verification BASEE SUR LES CONTRAINTES (EN 1993-1-8, Section 12.4)

SI les deux sont disponibles :
    → Utiliser BASEE SUR LES CONTRAINTES (plus rigoureuse) et verifier avec BASEE SUR LES EFFORTS
```

### 12.3 Verification de rupture de soudure basee sur les efforts

**Procedure :**

```
1. Determiner les efforts sur la soudure :
   F_n = effort normal sur la soudure [N] (perpendiculaire a l'axe de la soudure)
   F_s = effort de cisaillement sur la soudure [N] (parallele a l'axe de la soudure)

2. Calculer la section de soudure :
   A_s = a × L_s [mm²]
   ou a = epaisseur de gorge, L_s = longueur effective de soudure

3. Calculer les contraintes :
   σ_n = F_n / A_s [MPa]
   τ = F_s / A_s [MPa]

4. Calculer la contrainte equivalente (von Mises) :
   σ_eq = √(σ_n² + τ²) [MPa]

5. Calculer la contrainte admissible :
   σ_admissible = f_u / γ_Mw [MPa]
   ou :
       f_u = resistance a la traction du metal de soudure [MPa]
       γ_Mw = coefficient partiel de securite (defaut 1,25)

6. Calculer le taux d'utilisation :
   U = σ_eq / σ_admissible

7. CONFORME si U < 1,0 ; NON CONFORME si U ≥ 1,0
```

### 12.4 Verification de rupture de soudure basee sur les contraintes (EN 1993-1-8)

**Procedure :**

```
1. Determiner les composantes de contrainte dans le plan de gorge de la soudure :
   σ_⊥ = contrainte normale perpendiculaire a la gorge de soudure [MPa]
   τ_⊥ = contrainte de cisaillement perpendiculaire a la gorge (dans le plan de gorge) [MPa]
   τ_∥ = contrainte de cisaillement parallele a l'axe de la soudure [MPa]

2. Verifier le critere 1 (contrainte combinee) :
   σ_eq = √(σ_⊥² + 3 × (τ_⊥² + τ_∥²)) [MPa]
   σ_admissible,1 = f_u / (β_w × γ_Mw)
   U_1 = σ_eq / σ_admissible,1

3. Verifier le critere 2 (limite de contrainte normale) :
   σ_admissible,2 = 0,9 × f_u / γ_Mw
   U_2 = |σ_⊥| / σ_admissible,2

4. Taux d'utilisation gouvernant :
   U = max(U_1, U_2)

5. CONFORME si U < 1,0 ; NON CONFORME si U ≥ 1,0
```

**Valeurs des parametres :**

| Parametre | Valeur | Notes |
|-----------|--------|-------|
| β_w | 0,8 | Aciers de construction courants (S235–S460) |
| β_w | 0,85 | Aciers inoxydables austenitiques |
| β_w | 1,0 | Conservatif (si nuance d'acier inconnue) |
| γ_Mw | 1,25 | Coefficient de securite standard |
| γ_Mw | 1,0 | Pour les situations de calcul accidentelles/crash (l'Eurocode le permet) |

**Pour les situations de calcul accidentelles (crash) :**
- L'Eurocode autorise γ_Mw = 1,0 (coefficient partiel supprime pour les actions accidentelles)
- Cependant, les exigences specifiques au projet ou a l'entreprise peuvent toujours imposer γ_Mw > 1,0

### 12.5 Resistance de soudure dynamique vs. statique

```
SI la verification de rupture de soudure utilise les proprietes dynamiques du materiau :
    → Utiliser f_u,dynamique = f_u × DIF_ultime
    → Ou DIF_ultime est le facteur d'augmentation dynamique pour la resistance a la traction
    → ATTENTION : le DIF pour la resistance a la traction est plus faible que le DIF pour la limite d'elasticite
    → Approche conservative : utiliser f_u statique (NE PAS augmenter pour la vitesse de deformation)
```

**Recommandation :** Utiliser le f_u **statique** pour les verifications de rupture de soudure, sauf si des donnees d'essai dynamiques sont disponibles pour le metal de soudure specifique. Ceci est conservatif car :
1. Le metal de soudure peut ne pas beneficier autant du durcissement par vitesse de deformation que le metal de base
2. Les defauts de soudure peuvent reduire la ductilite dynamique
3. La vitesse de deformation dans la soudure peut differer de la vitesse de deformation globale

---

## 13. Phase 3 : Evaluation de l'absorption d'energie

### 13.1 Quand l'evaluation de l'absorption d'energie est-elle requise ?

```
SI le composant est concu pour absorber l'energie de crash (zone de deformation, boitier de crash, zone de froissement)
    OU la specification de conception inclut une absorption d'energie minimale
    OU les performances effort-deplacement sont specifiees
→ L'evaluation de l'absorption d'energie est OBLIGATOIRE
```

### 13.2 Indicateurs et formules

| Indicateur | Symbole | Formule | Unites | Objectif |
|------------|---------|---------|--------|----------|
| Energie totale | E | ∫ F(δ) dδ | J | ≥ specification |
| Absorption specifique d'energie | SEA | E / m | J/kg | Plus eleve = meilleur |
| Force moyenne | P_m | E / Δδ_total | N | ≥ specification |
| Force de crete | P_max | max(F) | N | ≤ specification |
| Efficacite de force d'ecrasement | CFE | P_m / P_max | — | 0,6–0,8 typique, plus eleve = meilleur |

### 13.3 Procedure

```
1. Obtenir les donnees effort-deplacement :
   - A partir de la simulation EF de crash
   - A partir d'un essai de crash physique
   - A partir de la specification de conception (courbe synthetique)

2. Calculer tous les indicateurs :
   E = ∫ F(δ) dδ  (integration trapezoidale)
   P_m = E / δ_max
   P_max = max(F)
   CFE = P_m / P_max
   SEA = E / m_composant  (si la masse est connue)

3. Verifier par rapport aux exigences :

   | Type d'exigence | Critere | CONFORME si |
   |----------------|---------|-------------|
   | Energie minimale | E ≥ E_requis | L'energie totale satisfait la specification |
   | Force de crete maximale | P_max ≤ P_max,admissible | Protection des occupants/charge utile |
   | SEA minimale | SEA ≥ SEA_cible | Conception efficace en poids |
   | CFE minimale | CFE ≥ CFE_cible | Ecrasement progressif stable |
```

### 13.4 Guide d'interpretation

| Plage CFE | Interpretation | Structure typique |
|-----------|---------------|-------------------|
| < 0,4 | Effondrement instable, pics de force aigus | Monocoque sans declencheurs |
| 0,4 – 0,6 | Stabilite moderee | Tubes d'ecrasement simples |
| 0,6 – 0,8 | Bon ecrasement progressif | Boitiers de crash bien concus |
| > 0,8 | Excellente efficacite d'absorption | Tubes multi-cellules ou remplis de mousse |

---

# PARTIE IV — INTEGRATION EF

## 14. Extraction des donnees EF pour la fatigue

### 14.1 Exigences EF par methode d'evaluation

| Methode | Type d'element | Taille d'element | Sortie requise | Localisation de la contrainte |
|---------|---------------|-----------------|-----------------|-------------------------------|
| Contrainte nominale | Coque ou solide | Grossier (≥ 2t) | Efforts de section ou contrainte en champ lointain | Loin de la soudure |
| Contrainte au point chaud | Coque ou solide | ≈ t × t | Contrainte de surface a 0,4t, 1,0t (Type A) ou 5/15/25 mm (Type B) | Surface, perpendiculaire au pied de cordon |
| Contrainte d'entaille | Solide uniquement | ≈ r_ref/4 (≈0,25 mm) | Contrainte principale maximale a l'entaille | Au pied/racine de cordon modelise avec r_ref |
| Mecanique de la rupture | Solide uniquement | Fin en pointe de fissure | K ou integrale J | Zone de pointe de fissure |

### 14.2 Traitement du tenseur de contraintes

Lorsque les EF fournissent le tenseur de contraintes complet (σ_xx, σ_yy, σ_zz, τ_xy, τ_yz, τ_xz), extraire la mesure de contrainte pertinente :

```
Contrainte equivalente de von Mises :
    σ_VM = √(0,5 × ((σ_xx-σ_yy)² + (σ_yy-σ_zz)² + (σ_zz-σ_xx)² + 6×(τ_xy²+τ_yz²+τ_xz²)))

Contrainte principale maximale :
    Valeurs propres du tenseur de contraintes → σ₁ ≥ σ₂ ≥ σ₃
    Utiliser σ₁ pour la fatigue si la fissure s'ouvre perpendiculairement a σ₁

Contrainte dans le repere local de la soudure :
    Transformer le tenseur de contraintes dans les axes locaux de la soudure :
    → σ_⊥ (perpendiculaire a la soudure), τ_⊥ (cisaillement dans le plan), τ_∥ (le long de la soudure)
    → Requis pour la verification de rupture de soudure EN 1993-1-8
```

**Quelle mesure de contrainte utiliser :**

| Methode d'evaluation | Mesure de contrainte |
|---------------------|---------------------|
| Methode de la contrainte nominale | Contrainte nominale (a partir des efforts de section, pas la contrainte EF aux elements pres de la soudure) |
| Methode du point chaud | Contrainte principale maximale en surface, perpendiculaire a la soudure |
| Methode de la contrainte d'entaille | Contrainte principale maximale a l'entaille |
| Fatigue multiaxiale | Composantes σ et τ separement |
| Rupture de soudure (EN 1993-1-8) | σ_⊥, τ_⊥, τ_∥ dans les coordonnees de la gorge de soudure |

### 14.3 Extraction du point chaud a partir des EF

```
1. Identifier l'emplacement du pied de cordon dans le modele EF
2. Definir le chemin de contrainte perpendiculaire au pied de cordon (Type A) ou le long du pied de cordon (Type B)
3. Extraire la contrainte de surface aux distances prescrites :
   Type A : 0,4t, 1,0t (lineaire) ou 0,4t, 0,9t, 1,4t (quadratique)
   Type B : 5 mm, 15 mm, 25 mm
4. Appliquer la formule d'extrapolation (Section 6.3)
5. Resultat : etendue de contrainte au point chaud Δσ_hs
```

### 14.4 Solveurs EF supportes

| Solveur | Lecteur | Format de fichier | Notes |
|---------|---------|-------------------|-------|
| Abaqus | AbaqusResultsReader | .odb, .dat | Sortie standard Abaqus |
| LS-DYNA | LSDynaResultsReader | ASCII d3plot, binout | Simulation de crash |
| Nastran | NastranResultsReader | .f06, .pch | Lineaire/non-lineaire |
| CSV generique | GenericCSVReader | .csv | Export de tout solveur |

---

## 15. Extraction des donnees EF pour l'impact

### 15.1 Sorties EF requises pour l'evaluation d'impact

| Sortie | Utilisation | Localisation d'extraction |
|--------|-------------|--------------------------|
| Vitesse de deformation plastique ε̇ | Calcul de la limite d'elasticite dynamique | Element a la soudure ou section critique |
| Efforts sur la soudure | Verification de rupture de soudure | Efforts de section a l'interface de soudure |
| Courbe effort-deplacement | Absorption d'energie | Reponse globale ou de section |
| Tenseur de contrainte a la soudure | Verification de soudure basee sur les contraintes | Elements dans la gorge de soudure |
| Force de contact | Verification de la force de crete | Interface entre l'impacteur et la structure |

### 15.2 Vitesse de deformation a partir des EF

```
SI les EF fournissent directement la vitesse de deformation (LS-DYNA, Abaqus Explicit) :
    → Utiliser la vitesse de deformation maximale a l'emplacement concerne

SI les EF fournissent un historique deformation-temps :
    → ε̇ = Δε / Δt au pas de temps concerne
    → Utiliser la vitesse de deformation de crete pour le calcul de la limite d'elasticite dynamique

SI les EF ne fournissent pas la vitesse de deformation :
    → Estimer a partir de la vitesse d'impact et de la geometrie de la structure :
    → ε̇ ≈ v_impact / L_structure [1/s]
    → Ceci est approximatif ; les EF sont preferes
```

---

# PARTIE V — EVALUATION COMBINEE ET RAPPORT

## 16. Scenarios combines fatigue + impact

### 16.1 Quand l'evaluation combinee s'applique-t-elle ?

```
SI le composant est soumis AUX DEUX :
    - Chargement cyclique de fatigue pendant le service (ex. vibrations de roulage, cycles de pression)
    - Un ou plusieurs evenements d'impact (ex. crash, chute)
→ L'evaluation combinee est OBLIGATOIRE

Exemples typiques :
    - Boitier de batterie VE : fatigue par vibrations de roulage + crash en collision
    - Cadre de reservoir a hydrogene : cyclage en pression + impact accidentel
    - Composants de chassis : fatigue par charges de route + integrite crash
```

### 16.2 Procedure d'evaluation combinee

```
ETAPE 1 : Realiser l'evaluation en fatigue (Partie II)
    → Resultat : N_admissible ou D_total et CONFORME/NON CONFORME

ETAPE 2 : Realiser l'evaluation d'impact (Partie III)
    → Resultat : Taux d'utilisation de la soudure, absorption d'energie, et CONFORME/NON CONFORME

ETAPE 3 : Verifier l'interaction :
    a. SI la fatigue se produit AVANT un impact potentiel :
       → L'endommagement par fatigue peut avoir propage des fissures qui reduisent la resistance a l'impact
       → Approche conservative : reduire f_u de (1 - D_total) pour la verification de rupture de soudure
       → OU : utiliser la mecanique de la rupture pour estimer la taille de fissure au moment de l'impact

    b. SI l'impact se produit AVANT le service en fatigue :
       → L'impact peut introduire des contraintes residuelles, des distorsions geometriques ou des micro-fissures
       → Approche conservative : supposer une fissure initiale a₀ = 1 mm pour la mecanique de la rupture
       → Ou utiliser une classe FAT reduite (un palier en dessous)

    c. SI les deux se produisent simultanement ou en alternance :
       → Traiter comme la combinaison la plus severe
       → Appliquer les deux verifications independamment avec les hypotheses les plus defavorables

ETAPE 4 : Verdict global :
    CONFORME uniquement si les verifications en fatigue ET en impact sont conformes individuellement
    ET les effets d'interaction sont pris en compte
```

---

## 17. Exigences de rapport

### 17.1 Contenu minimum du rapport

Chaque rapport de verification en fatigue et/ou en impact doit contenir :

| Section | Contenu |
|---------|---------|
| **1. Identification du projet** | Nom du projet, reference du composant, auteur, date, revision |
| **2. Domaine d'application** | Ce qui est verifie, cas de charge, criteres d'acceptation |
| **3. Donnees materiaux** | Nuance, limite d'elasticite, resistance a la traction, module, source (certificat / norme) |
| **4. Description du joint** | Type de soudure, geometrie (t, a, p), procede, niveau de qualite |
| **5. Description du chargement** | Type de charge, etendues de contrainte, rapport R ou spectre, nombre de cycles |
| **6. Conditions environnementales** | Temperature, atmosphere, hydrogene (si applicable) |
| **7. Justification du choix de methode** | Pourquoi cette methode a ete choisie (reference a l'arbre de decision Section 6) |
| **8. Norme et courbe S-N** | Quelle norme, quels parametres de courbe S-N |
| **9. Chaine de modificateurs** | Chaque facteur applique, sa valeur et sa justification |
| **10. Resultats de calcul** | N_admissible, D_total, coefficient de securite, taux d'utilisation |
| **11. Verdict CONFORME/NON CONFORME** | Resultat binaire clair avec marge quantifiee |
| **12. Hypotheses et limitations** | Toute simplification, conservatisme ou limitation |
| **13. References** | Normes, specifications, rapports references |

### 17.2 Formats de rapport

Deux formats sont supportes :

- **Rapport PDF** (livrable formel) : Genere via la classe `FatigueReport`. Inclut page de garde, tableaux formates, graphiques integres (courbes S-N, diagrammes de Haigh, propagation de fissure).
- **Rapport HTML** (revue interactive) : Genere via `HTMLReportGenerator`. Inclut des graphiques interactifs, des tableaux filtrables.

---

# PARTIE VI — ARBRES DE DECISION ET REFERENCE RAPIDE

## 18. Arbre de decision principal — Quelle methode utiliser

### 18.1 Organigramme complet de selection de methode

```
╔══════════════════════════════════════════════════════════════════════╗
║                VERIFICATION DE STRUCTURE SOUDEE                      ║
║                COMMENCER ICI                                          ║
╚══════════════════════════════════════════════════════════════════════╝
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  ┌──────────┐         ┌──────────┐         ┌──────────────┐
  │ FATIGUE  │         │  IMPACT  │         │  COMBINE     │
  │ charg.   │         │  charg.  │         │  fatigue +   │
  │ (cyclique)│        │ (crash)  │         │  impact      │
  └────┬─────┘         └────┬─────┘         └──────┬───────┘
       │                    │                      │
       ▼                    ▼                      ▼
  ┌──────────────┐   ┌──────────────┐    Faire LES DEUX branches
  │ Uniaxial ou  │   │ Materiau     │    independamment, puis
  │ multiaxial ? │   │ dynamique    │    verifier l'interaction
  └──┬───────┬───┘   │ (Sec. 11)   │    (Section 16)
     │       │        └──────┬──────┘
     ▼       ▼               │
  ┌─────┐ ┌───────┐    ┌────┴────────┐
  │ UNI │ │ MULTI │    │ Rupture     │
  │     │ │ AXIAL │    │ soudure     │
  └──┬──┘ └───┬───┘    │ (Sec. 12)  │
     │        │         └──────┬──────┘
     ▼        ▼               │
  ┌────────┐ Voir 10.1  ┌────┴──────┐
  │ EF     │             │ Absorption│
  │ dispo? │             │ d'energie │
  └─┬────┬─┘             │ (Sec. 13) │
    │    │                └───────────┘
    ▼    ▼
  OUI   NON
    │    │
    ▼    ▼
  ┌────┐ ┌────────────┐
  │Mail│ │ Peut-on    │
  │fin │ │ calculer   │
  │?   │ │ σ nominal ?│
  └┬─┬─┘ └──┬─────┬───┘
   │ │      ▼     ▼
   │ │    OUI    NON
   │ │     │     │
   ▼ ▼     ▼     ▼
  ┌──┐ ┌──┐ ┌───────┐ ┌──────────┐
  │r=│ │t │ │CONTR. │ │ EF       │
  │1 │ │×t│ │NOMIN. │ │ necessai-│
  │mm│ │  │ │       │ │ res →    │
  └┬─┘ └┬─┘ └───────┘ │ revenir  │
   │    │              └──────────┘
   ▼    ▼
ENTAILLE PT CHAUD
```

### 18.2 Matrice de decision basee sur le chargement

| Chargement | Amplitude | Directionnalite | Methode |
|------------|-----------|----------------|---------|
| Cyclique | Constante | Uniaxial | Nominale / Pt chaud / Entaille + lecture directe S-N |
| Cyclique | Variable | Uniaxial | Meme methode + endommagement Palmgren-Miner |
| Cyclique | Constante | Multiaxial, proportionnel | Methode principale + Gough-Pollard |
| Cyclique | Constante | Multiaxial, non proportionnel | Methode principale + Findley / MWCM |
| Cyclique | Variable | Multiaxial | Methode principale + Miner + critere multiaxial |
| Vibration aleatoire | Entree DSP | Uniaxial | Fatigue vibratoire (Dirlik / bande etroite) |
| Vibration aleatoire | Entree DSP | Multiaxial | Avance (hors portee standard) |
| Impact | Evenement unique | — | Cowper-Symonds/J-C + rupture soudure + energie |
| Mixte | Fatigue + impact | — | Les deux evaluations + interaction |

### 18.3 Matrice de decision par configuration de soudure

| Type de soudure | Mode de rupture principal | Methode recommandee | Verif. racine necessaire ? |
|-----------------|--------------------------|--------------------|-----------------------------|
| Bout a bout, pleine penetration | Fissure en pied | Nominale (si cataloguee) ou pt chaud | Non |
| Bout a bout, penetration partielle | Pied ou racine | Entaille ou nominale + verif. racine | OUI |
| Angle, non porteuse | Fissure en pied | Nominale ou pt chaud (FAT 80) | Non |
| Angle, porteuse | Pied ou racine | Nominale + verif. racine | OUI |
| Cruciforme, pleine penetration | Fissure en pied | Nominale ou pt chaud | Non |
| Cruciforme, partielle | Pied ou racine | Nominale + verif. racine | OUI |
| Recouvrement | Pied ou racine | Nominale (FAT 45–71) + verif. racine | OUI |
| En T | Fissure en pied | Nominale ou pt chaud | Depend de la penetration |
| Raidisseur | Fissure en pied | Nominale (FAT selon longueur) | Non |
| Point | Bord du noyau | Methodes speciales (hors portee standard) | N/A |
| Bout a bout laser | Pied ou racine | Contrainte d'entaille (cordon etroit) | Possible |
| FSW bout a bout | Cote en retrait | Nominale + facteur de procede | Non |

---

## 19. Tableaux de reference rapide

### 19.1 Recherche rapide des classes FAT (Acier, IIW)

| Detail de soudure | FAT Traction | FAT Flexion |
|-------------------|-------------|-------------|
| Metal de base, surface laminee | 160 | 160 |
| Metal de base, bords decoupes a la flamme | 140 | 140 |
| Bout a bout transversal, meule, CND | 125 | 125 |
| Bout a bout transversal, meule | 112 | 112 |
| Bout a bout transversal, brut de soudage (2 cotes) | 100 | 100 |
| Bout a bout transversal, 1 cote, pleine pen. | 90 | 90 |
| Bout a bout transversal, sur latte support | 71 | 71 |
| Angle non porteuse, transversale | 80 | 80 |
| Angle porteuse, longitudinale | 71 | 71 |
| Cruciforme, pleine penetration en K | 90 | 90 |
| Cruciforme, soudure d'angle porteuse | 71 | 71 |
| Cruciforme, penetration partielle | 63 | 63 |
| Recouvrement, soudures d'angle | 45–63 | 45–63 |

### 19.2 Reference rapide des facteurs environnementaux

| Condition | Facteur acier | Facteur aluminium |
|-----------|--------------|-------------------|
| Air, 20°C | 1,0 | 1,0 |
| Eau de mer (libre) | 0,7 | 0,6 |
| Eau de mer (PC) | 0,85 | 0,8 |
| Industriel | 0,9 | 0,85 |
| Hydrogene (50 bar) | 0,91 | 1,0 |
| Hydrogene (200 bar) | 0,71 | 1,0 |
| Hydrogene (350 bar) | 0,59 | 1,0 |
| 150°C (acier) | 0,925 | N/A |
| 200°C (acier) | 0,85 | N/A |
| 300°C (acier) | 0,70 | N/A |
| 100°C (aluminium) | N/A | 0,85 |
| -50°C (acier au carbone) | 0,8 | 1,0 |

### 19.3 Reference rapide des coefficients de securite

| Norme | Consequence | Inspection | γ_Mf |
|-------|------------|------------|------|
| IIW | Normale | Periodique | 1,15 |
| IIW | Elevee | Aucune | 1,40 |
| EC3 | Normale | — | 1,15 |
| EC3 | Elevee | — | 1,35 |
| DNV | Normale | Periodique | DFF = 2,0 |
| DNV | Elevee | Aucune | DFF = 10,0 |

---

## 20. Liste de controle pour la verification complete

Utiliser cette liste de controle pour s'assurer qu'aucune etape n'est oubliee :

### 20.1 Liste de controle de verification en fatigue

- [ ] **Donnees materiaux** collectees (nuance, R_y, R_m, E, famille de materiau)
- [ ] **Classification de la soudure** completee (TypeSoudure, geometrie : t, a, p, L)
- [ ] **Chargement classifie** (AC/AV, uniaxial/multiaxial, type de charge)
- [ ] **Contrainte calculee** (nominale, point chaud ou entaille)
- [ ] **Methode d'evaluation selectionnee** et justifiee (arbre de decision Section 6)
- [ ] **Classe FAT selectionnee** (catalogue ou tableau de niveau de qualite)
- [ ] **Courbe S-N et norme selectionnees** (Section 7)
- [ ] **Correction d'epaisseur** appliquee (si t > 25 mm)
- [ ] **Correction environnementale** appliquee (si environnement non-air)
- [ ] **Traitement post-soudage** pris en compte (si applique)
- [ ] **Facteur de procede de soudage** applique (si non-MIG/MAG)
- [ ] **Desalignement** pris en compte (si present)
- [ ] **Correction de contrainte moyenne** appliquee (si TTPS et R ≠ 0)
- [ ] **Coefficients de securite** appliques (γ_Mf, γ_Ff, probabilite de survie)
- [ ] **Endommagement calcule** (N_admissible pour AC, D_total pour AV)
- [ ] **Fatigue en racine verifiee** (si penetration partielle)
- [ ] **Multiaxial verifie** (si σ + τ combines)
- [ ] **CONFORME/NON CONFORME determine** avec marge de securite quantifiee
- [ ] **Rapport genere** avec toutes les sections requises

### 20.2 Liste de controle de verification a l'impact

- [ ] **Donnees materiaux** collectees (y compris parametres Cowper-Symonds ou J-C)
- [ ] **Vitesse de deformation estimee** (des EF ou de la vitesse d'impact)
- [ ] **Modele de vitesse de deformation selectionne** (Cowper-Symonds ou Johnson-Cook)
- [ ] **Limite d'elasticite dynamique calculee** (DIF × σ_statique)
- [ ] **Efforts/contraintes de soudure** determines (des EF)
- [ ] **Verification de rupture de soudure** effectuee (basee sur les efforts et/ou les contraintes)
- [ ] **Absorption d'energie** calculee (si applicable : E, SEA, P_m, P_max, CFE)
- [ ] **Tous les criteres satisfaits** (utilisation < 1, energie ≥ spec, P_max ≤ spec)
- [ ] **CONFORME/NON CONFORME determine** pour chaque critere
- [ ] **Rapport genere** avec toutes les sections requises

### 20.3 Liste de controle d'evaluation combinee

- [ ] Evaluation en fatigue completee → CONFORME/NON CONFORME
- [ ] Evaluation d'impact completee → CONFORME/NON CONFORME
- [ ] Effets d'interaction consideres (Section 16.2)
- [ ] Verdict global : CONFORME uniquement si les deux sont conformes ET l'interaction est acceptable

---

# ANNEXES

## Annexe A : Catalogue des classes FAT

Le catalogue complet des classes FAT est maintenu dans les fichiers de donnees de l'outil :
- Acier : `src/weldfatigue/fatigue/data/fat_catalog_steel.json`
- Aluminium : `src/weldfatigue/fatigue/data/fat_catalog_aluminum.json`

Consulter IIW XIII-2259-15 (2024) Tableaux 4.1–4.8 pour le catalogue complet avec illustrations.

## Annexe B : Resume de la base de donnees materiaux

### Nuances d'acier

| Nuance | Norme | R_y [MPa] | R_m [MPa] | E [GPa] | CS D [1/s] | CS q |
|--------|-------|-----------|-----------|---------|----------|------|
| DC04 | EN 10130 | 210 | 310 | 210 | 40,4 | 5,0 |
| DP600 | EN 10338 | 350 | 600 | 210 | 100,0 | 4,73 |
| DP780 | EN 10338 | 480 | 780 | 210 | 200,0 | 4,5 |
| DP980 | EN 10338 | 600 | 980 | 210 | 300,0 | 4,0 |
| HSLA340 | EN 10268 | 340 | 410 | 210 | 80,0 | 4,8 |
| HSLA420 | EN 10268 | 420 | 480 | 210 | 120,0 | 4,5 |
| 22MnB5 | EN 10083 | 1000 | 1500 | 210 | 802,0 | 3,585 |
| S355J2 | EN 10025 | 355 | 510 | 210 | 40,4 | 5,0 |
| 316L | EN 10088 | 220 | 520 | 200 | 100,0 | 10,0 |

### Nuances d'aluminium

| Nuance | Norme | R_y [MPa] | R_m [MPa] | E [GPa] | CS D [1/s] | CS q |
|--------|-------|-----------|-----------|---------|----------|------|
| 6061-T6 | EN 573 | 276 | 310 | 70 | 6500 | 4,0 |
| 6082-T6 | EN 573 | 260 | 310 | 70 | 6500 | 4,0 |
| 5083-H111 | EN 573 | 165 | 275 | 70 | 6500 | 4,0 |
| 5754-O | EN 573 | 100 | 190 | 70 | 6500 | 4,0 |
| 7075-T6 | EN 573 | 503 | 572 | 72 | 6500 | 4,0 |

## Annexe C : Resume des formules

### C.1 Relation S-N fondamentale
```
N = (FAT / Δσ)^m × N_ref

Δσ = FAT × (N_ref / N)^(1/m)

N_ref = 2 × 10⁶ (IIW)
```

### C.2 Endommagement de Palmgren-Miner
```
D = Σ(n_i / N_i)

Rupture : D ≥ D_limite (1,0 standard, 0,5 critique pour la securite)
```

### C.3 Etendue de contrainte equivalente
```
Δσ_eq = [Σ(n_i × Δσ_i^m) / Σn_i]^(1/m)
```

### C.4 Extrapolation au point chaud
```
Type A lineaire :    σ_hs = 1,67 × σ(0,4t) - 0,67 × σ(1,0t)
Type A quadratique : σ_hs = 2,52 × σ(0,4t) - 2,24 × σ(0,9t) + 0,72 × σ(1,4t)
Type B :             σ_hs = 3 × σ(5mm) - 3 × σ(15mm) + σ(25mm)
```

### C.5 Correction d'epaisseur
```
f(t) = (25 / t)^n    pour t > 25 mm
```

### C.6 Limite d'elasticite dynamique de Cowper-Symonds
```
σ_dyn = σ_statique × [1 + (ε̇ / D)^(1/q)]
```

### C.7 Contrainte d'ecoulement de Johnson-Cook
```
σ = (A + B × εₚⁿ) × (1 + C × ln(ε̇/ε̇₀)) × (1 - T*ᵐ)
```

### C.8 Rupture de soudure (EN 1993-1-8)
```
Critere 1 : √(σ_⊥² + 3(τ_⊥² + τ_∥²)) ≤ f_u / (β_w × γ_Mw)
Critere 2 : |σ_⊥| ≤ 0,9 × f_u / γ_Mw
```

### C.9 Propagation de fissure par la loi de Paris
```
da/dN = C × (ΔK)^m
ΔK = Y × Mk × Δσ × √(π × a)
```

### C.10 Interaction de Gough-Pollard
```
(Δσ / Δσ_R)² + (Δτ / Δτ_R)² ≤ 1
```

### C.11 Moments spectraux de Dirlik
```
m_n = ∫ f^n × G(f) df    (n = 0, 1, 2, 4)
γ = m₂ / √(m₀ × m₄)     [facteur d'irregularite]
```

### C.12 Indicateurs d'absorption d'energie
```
E = ∫ F dδ
SEA = E / m
P_m = E / δ_max
CFE = P_m / P_max
```

## Annexe D : Exemples d'application

### D.1 Exemple : Fatigue a amplitude constante d'une soudure bout a bout

**Donnees :**
- Materiau : S355J2 (R_y = 355 MPa, R_m = 510 MPa)
- Type de soudure : Bout a bout transversal, brut de soudage deux cotes
- Chargement : Traction a amplitude constante, Δσ = 80 MPa, R = 0,1
- Duree de vie de conception : N = 2 × 10⁶ cycles
- Environnement : Air, 20 °C
- Niveau de qualite : C
- Epaisseur de tole : 12 mm
- Pas de traitement post-soudage
- Consequence : Normale, inspection periodique

**Solution :**

```
Etape 1 : Selection de la classe FAT
    Niveau de qualite C, bout a bout → FAT 90 (du tableau, Section 8.5)

Etape 2 : Chaine de modificateurs
    Epaisseur : t = 12 mm < 25 mm → f_ep = 1,0
    Environnement : Air, 20°C → f_env = 1,0
    Traitement : Aucun → f_tps = 1,0 (pas d'amelioration)
    Procede : MIG/MAG → f_proc = 1,0
    Contrainte moyenne : Brut de soudage → f(R) = 1,0 (pas de correction selon IIW)
    Desalignement : Non specifie → k_m = 1,0
    Coeff. de securite : Consequence normale, periodique → γ_Mf = 1,15
    Coeff. de charge : γ_Ff = 1,0
    Survie : 97,7% → f_surv = 1,0

    FAT_conception = 90 × 1,0 × 1,0 × 1,0 × 1,0 × 1,0 / 1,15 = 78,3 MPa

Etape 3 : Calcul du nombre de cycles admissibles
    N_admissible = (78,3 / 80)^3 × 2×10⁶ = 1,87 × 10⁶ cycles

Etape 4 : Verification
    N_admissible = 1,87 × 10⁶ < N_requis = 2 × 10⁶

    → NON CONFORME (marginal)

Etape 5 : Coefficient de securite
    CS = (1,87 × 10⁶ / 2 × 10⁶)^(1/3) = 0,977
    CS < 1,0 → Confirme NON CONFORME

Recommandation :
    → Ameliorer la qualite au niveau B (FAT 112) ou appliquer un traitement HFMI
    → Avec qualite B : FAT_conception = 112/1,15 = 97,4 MPa
      N_admissible = (97,4/80)^3 × 2×10⁶ = 3,60 × 10⁶ → CONFORME (CS = 1,22)
```

### D.2 Exemple : Evaluation d'impact d'une soudure de boitier de crash

**Donnees :**
- Materiau : DP600 (R_y = 350 MPa, R_m = 600 MPa)
- Cowper-Symonds : D = 100 /s, q = 4,73
- Vitesse de deformation a la soudure : 200 /s
- Soudure : Soudure d'angle, a = 4 mm, L = 80 mm
- Effort normal sur la soudure : 40 000 N
- Effort de cisaillement sur la soudure : 25 000 N
- Contrainte admissible (metal de soudure) : 480 MPa

**Solution :**

```
Etape 1 : Limite d'elasticite dynamique
    DIF = 1 + (200 / 100)^(1/4,73) = 1 + 2^0,211 = 1 + 1,159 = 2,159
    σ_y,dyn = 350 × 2,159 = 755,7 MPa

Etape 2 : Verification de rupture de soudure (basee sur les efforts)
    A_s = 4 × 80 = 320 mm²
    σ_n = 40000 / 320 = 125,0 MPa
    τ = 25000 / 320 = 78,1 MPa
    σ_eq = √(125² + 78,1²) = 147,4 MPa
    σ_admissible = 480 / 1,25 = 384 MPa    (statique, conservatif)
    U = 147,4 / 384 = 0,384

    → CONFORME (taux d'utilisation = 38,4%, marge significative)
```

---

## Historique du document

| Revision | Date | Description |
|----------|------|-------------|
| Rev.0 | 2026-03-02 | Publication initiale — methodologie complete |

---

*Ce document methodologique est base sur l'outil WeldFatigue (v0.1.0) et s'aligne sur toutes les methodes d'evaluation, facteurs de correction et normes implementes. Chaque etape de cette methodologie correspond a une fonction ou une classe dans le code source, assurant une tracabilite complete entre la procedure documentee et son implementation informatique.*
