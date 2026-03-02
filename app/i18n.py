"""Internationalization (i18n) support for the Streamlit UI.

Provides French / English translations. Technical terms universally known
in English by francophone engineers are kept as-is (FAT class, S-N curve,
von Mises, Palmgren-Miner, Cowper-Symonds, Johnson-Cook, Hot-Spot, DIF,
SEA, CFE, Rainflow, Goodman, Gerber, Soderberg, IIW, FEA, etc.).
"""

import streamlit as st

# ---------------------------------------------------------------------------
# Translation dictionaries
# ---------------------------------------------------------------------------

TRANSLATIONS: dict[str, dict[str, str]] = {
    # ── Main / Global ──────────────────────────────────────────────────────
    "app_subtitle": {
        "en": "Fatigue & Shock Validation Tool for Welded Automobile Assemblies",
        "fr": "Outil de validation en fatigue et choc pour assemblages automobiles soudés",
    },
    "main_title": {
        "en": "WeldFatigue - Fatigue & Shock Validation",
        "fr": "WeldFatigue - Validation fatigue et choc",
    },
    "main_subtitle": {
        "en": "Validation Tool for Welded Automobile Metal Assemblies",
        "fr": "Outil de validation pour assemblages métalliques automobiles soudés",
    },
    "main_description": {
        "en": (
            "This tool implements IIW (International Institute of Welding) standardized methods\n"
            "for assessing the **fatigue resistance** and **shock/crash resistance** of welded\n"
            "joints used in automotive clean energy components."
        ),
        "fr": (
            "Cet outil implémente les méthodes normalisées de l'IIW (International Institute of Welding)\n"
            "pour évaluer la **résistance en fatigue** et la **résistance au choc/crash** des joints\n"
            "soudés utilisés dans les composants automobiles d'énergie propre."
        ),
    },
    "available_modules": {
        "en": "Available Modules",
        "fr": "Modules disponibles",
    },
    "navigate_sidebar": {
        "en": "Navigate using the sidebar pages:",
        "fr": "Naviguez à l'aide des pages dans la barre latérale :",
    },
    "page": {
        "en": "Page",
        "fr": "Page",
    },
    "description": {
        "en": "Description",
        "fr": "Description",
    },
    "mod_material_db": {
        "en": "Browse and compare automotive steel & aluminum grades",
        "fr": "Parcourir et comparer les nuances d'acier et d'aluminium automobiles",
    },
    "mod_fatigue": {
        "en": "IIW methods, multiaxial, fracture mechanics, vibration fatigue, weld quality",
        "fr": "Méthodes IIW, multiaxial, mécanique de la rupture, fatigue vibratoire, qualité de soudure",
    },
    "mod_shock": {
        "en": "Dynamic material properties and weld failure criteria",
        "fr": "Propriétés dynamiques des matériaux et critères de rupture de soudure",
    },
    "mod_fea": {
        "en": "Import and process FEA simulation results",
        "fr": "Importer et traiter les résultats de simulation FEA",
    },
    "mod_report": {
        "en": "Generate PDF/HTML assessment reports",
        "fr": "Générer des rapports d'évaluation PDF/HTML",
    },
    "applicable_standards": {
        "en": "Applicable Standards",
        "fr": "Normes applicables",
    },
    "target_applications": {
        "en": "Target Applications",
        "fr": "Applications visées",
    },
    "ev_battery": {
        "en": "EV Battery Enclosures",
        "fr": "Boîtiers de batteries VE",
    },
    "h2_tank": {
        "en": "Hydrogen Tank Frames",
        "fr": "Châssis de réservoirs hydrogène",
    },
    "structural_reinforcements": {
        "en": "Structural Reinforcements",
        "fr": "Renforts structurels",
    },
    "welded_chassis": {
        "en": "Welded Chassis Components",
        "fr": "Composants de châssis soudés",
    },

    # ── Sidebar / Common ──────────────────────────────────────────────────
    "language": {
        "en": "Language",
        "fr": "Langue",
    },
    "configuration": {
        "en": "Configuration",
        "fr": "Configuration",
    },
    "filters": {
        "en": "Filters",
        "fr": "Filtres",
    },
    "material_family": {
        "en": "Material Family",
        "fr": "Famille de matériaux",
    },
    "material_grade": {
        "en": "Material Grade",
        "fr": "Nuance de matériau",
    },
    "all": {
        "en": "All",
        "fr": "Tous",
    },
    "steel": {
        "en": "steel",
        "fr": "steel",  # keep technical DB key
    },
    "aluminum": {
        "en": "aluminum",
        "fr": "aluminum",  # keep technical DB key
    },

    # ── Material Database Page ─────────────────────────────────────────────
    "material_database": {
        "en": "Material Database",
        "fr": "Base de données matériaux",
    },
    "min_yield_strength": {
        "en": "Min Yield Strength [MPa]",
        "fr": "Limite d'élasticité min [MPa]",
    },
    "max_yield_strength": {
        "en": "Max Yield Strength [MPa]",
        "fr": "Limite d'élasticité max [MPa]",
    },
    "available_grades": {
        "en": "Available Grades",
        "fr": "Nuances disponibles",
    },
    "material_detail_view": {
        "en": "Material Detail View",
        "fr": "Détail du matériau",
    },
    "select_grade_details": {
        "en": "Select a grade for details",
        "fr": "Sélectionnez une nuance pour plus de détails",
    },
    "mechanical_properties": {
        "en": "Mechanical Properties",
        "fr": "Propriétés mécaniques",
    },
    "yield_strength": {
        "en": "Yield Strength",
        "fr": "Limite d'élasticité",
    },
    "ultimate_strength": {
        "en": "Ultimate Strength",
        "fr": "Résistance à la traction",
    },
    "youngs_modulus": {
        "en": "Young's Modulus",
        "fr": "Module d'Young",
    },
    "elongation": {
        "en": "Elongation",
        "fr": "Allongement à la rupture",
    },
    "strain_rate_params_cs": {
        "en": "Strain Rate Parameters (Cowper-Symonds)",
        "fr": "Paramètres de taux de déformation (Cowper-Symonds)",
    },
    "weld_haz_properties": {
        "en": "Weld / HAZ Properties",
        "fr": "Propriétés soudure / ZAT",
    },
    "weld_process": {
        "en": "Weld Process",
        "fr": "Procédé de soudage",
    },
    "haz_width": {
        "en": "HAZ Width",
        "fr": "Largeur ZAT",
    },
    "haz_yield_factor": {
        "en": "HAZ Yield Factor",
        "fr": "Facteur de limite d'élasticité ZAT",
    },
    "haz_uts_factor": {
        "en": "HAZ UTS Factor",
        "fr": "Facteur UTS ZAT",
    },

    # ── Fatigue Analysis Page ──────────────────────────────────────────────
    "fatigue_assessment": {
        "en": "Fatigue Assessment",
        "fr": "Évaluation en fatigue",
    },
    "assessment_method": {
        "en": "Assessment Method",
        "fr": "Méthode d'évaluation",
    },
    "nominal_stress": {
        "en": "Nominal Stress",
        "fr": "Nominal Stress",  # IIW term
    },
    "hotspot_stress": {
        "en": "Hot-Spot Stress",
        "fr": "Hot-Spot Stress",  # IIW term
    },
    "notch_stress": {
        "en": "Notch Stress",
        "fr": "Notch Stress",  # IIW term
    },
    "weld_type": {
        "en": "Weld Type",
        "fr": "Type de soudure",
    },
    "load_type": {
        "en": "Load Type",
        "fr": "Type de chargement",
    },
    "fat_class": {
        "en": "FAT Class",
        "fr": "Classe FAT",
    },
    "recommended": {
        "en": "Recommended",
        "fr": "Recommandé",
    },
    "mean_stress_correction": {
        "en": "Mean Stress Correction",
        "fr": "Correction de contrainte moyenne",
    },
    "variable_amplitude_loading": {
        "en": "Variable Amplitude Loading",
        "fr": "Chargement à amplitude variable",
    },
    "single_load_block": {
        "en": "Single Load Block",
        "fr": "Bloc de chargement unique",
    },
    "variable_amplitude_miner": {
        "en": "Variable Amplitude (Miner)",
        "fr": "Amplitude variable (Miner)",
    },
    "sn_curve_explorer": {
        "en": "S-N Curve Explorer",
        "fr": "Explorateur de courbe S-N",
    },
    "fat_class_catalog": {
        "en": "FAT Class Catalog",
        "fr": "Catalogue de classes FAT",
    },
    "single_block_assessment": {
        "en": "Single Load Block Assessment",
        "fr": "Évaluation pour un bloc de chargement unique",
    },
    "stress_range": {
        "en": "Stress Range [MPa]",
        "fr": "Étendue de contrainte [MPa]",
    },
    "number_of_cycles": {
        "en": "Number of Cycles",
        "fr": "Nombre de cycles",
    },
    "mean_stress": {
        "en": "Mean Stress [MPa]",
        "fr": "Contrainte moyenne [MPa]",
    },
    "run_assessment": {
        "en": "Run Assessment",
        "fr": "Lancer l'évaluation",
    },
    "result": {
        "en": "Result",
        "fr": "Résultat",
    },
    "allowable_cycles": {
        "en": "Allowable Cycles",
        "fr": "Cycles admissibles",
    },
    "damage_ratio": {
        "en": "Damage Ratio",
        "fr": "Taux d'endommagement",
    },
    "safety_factor": {
        "en": "Safety Factor",
        "fr": "Facteur de sécurité",
    },
    "miner_assessment": {
        "en": "Variable Amplitude - Palmgren-Miner",
        "fr": "Amplitude variable - Palmgren-Miner",
    },
    "enter_load_spectrum": {
        "en": "Enter the load spectrum (stress range and cycles per block):",
        "fr": "Entrez le spectre de chargement (étendue de contrainte et cycles par bloc) :",
    },
    "number_load_blocks": {
        "en": "Number of load blocks",
        "fr": "Nombre de blocs de chargement",
    },
    "block_stress_range": {
        "en": "Block {i} - Stress Range [MPa]",
        "fr": "Bloc {i} - Étendue de contrainte [MPa]",
    },
    "block_cycles": {
        "en": "Block {i} - Cycles",
        "fr": "Bloc {i} - Cycles",
    },
    "run_miner_assessment": {
        "en": "Run Miner Assessment",
        "fr": "Lancer l'évaluation Miner",
    },
    "miner_result": {
        "en": "Miner Result",
        "fr": "Résultat Miner",
    },
    "total_damage": {
        "en": "Total Damage D",
        "fr": "Endommagement total D",
    },
    "critical_block": {
        "en": "Critical Block",
        "fr": "Bloc critique",
    },
    "block_n": {
        "en": "Block {n}",
        "fr": "Bloc {n}",
    },
    "knee_point_stress": {
        "en": "Knee point stress",
        "fr": "Contrainte au point d'inflexion",
    },
    "cutoff_stress_va": {
        "en": "Cut-off stress (VA)",
        "fr": "Contrainte de coupure (VA)",
    },
    "iiw_fat_class_catalog": {
        "en": "IIW FAT Class Catalog",
        "fr": "Catalogue IIW des classes FAT",
    },
    "material": {
        "en": "Material",
        "fr": "Matériau",
    },
    "no_details_found": {
        "en": "No details found for this material.",
        "fr": "Aucun détail trouvé pour ce matériau.",
    },

    # ── Shock Analysis Page ────────────────────────────────────────────────
    "crash_shock_assessment": {
        "en": "Crash / Shock Assessment",
        "fr": "Évaluation crash / choc",
    },
    "strain_rate_model": {
        "en": "Strain Rate Model",
        "fr": "Modèle de taux de déformation",
    },
    "dynamic_material_properties": {
        "en": "Dynamic Material Properties",
        "fr": "Propriétés dynamiques du matériau",
    },
    "weld_failure_check": {
        "en": "Weld Failure Check",
        "fr": "Vérification de rupture de soudure",
    },
    "energy_absorption": {
        "en": "Energy Absorption",
        "fr": "Absorption d'énergie",
    },
    "strain_rate": {
        "en": "Strain Rate [1/s]",
        "fr": "Taux de déformation [1/s]",
    },
    "temperature": {
        "en": "Temperature [K]",
        "fr": "Température [K]",
    },
    "results": {
        "en": "Results",
        "fr": "Résultats",
    },
    "static_yield": {
        "en": "Static Yield",
        "fr": "Limite d'élasticité statique",
    },
    "dynamic_yield": {
        "en": "Dynamic Yield",
        "fr": "Limite d'élasticité dynamique",
    },
    "flow_curves_jc": {
        "en": "Flow Curves (Johnson-Cook)",
        "fr": "Courbes d'écoulement (Johnson-Cook)",
    },
    "true_stress_vs_plastic_strain": {
        "en": "True Stress vs Plastic Strain at Various Strain Rates",
        "fr": "Contrainte vraie vs déformation plastique à différents taux de déformation",
    },
    "plastic_strain": {
        "en": "Plastic strain",
        "fr": "Déformation plastique",
    },
    "true_stress": {
        "en": "True stress [MPa]",
        "fr": "Contrainte vraie [MPa]",
    },
    "criterion": {
        "en": "Criterion",
        "fr": "Critère",
    },
    "force_based": {
        "en": "Force-based",
        "fr": "Basé sur les efforts",
    },
    "stress_based_en1993": {
        "en": "Stress-based (EN 1993-1-8)",
        "fr": "Basé sur les contraintes (EN 1993-1-8)",
    },
    "normal_force": {
        "en": "Normal Force [N/mm]",
        "fr": "Effort normal [N/mm]",
    },
    "shear_force": {
        "en": "Shear Force [N/mm]",
        "fr": "Effort tranchant [N/mm]",
    },
    "weld_throat": {
        "en": "Weld Throat [mm]",
        "fr": "Gorge de soudure [mm]",
    },
    "weld_length": {
        "en": "Weld Length [mm]",
        "fr": "Longueur de soudure [mm]",
    },
    "allowable_stress": {
        "en": "Allowable Stress [MPa]",
        "fr": "Contrainte admissible [MPa]",
    },
    "check_weld": {
        "en": "Check Weld",
        "fr": "Vérifier la soudure",
    },
    "equivalent_stress": {
        "en": "Equivalent Stress",
        "fr": "Contrainte équivalente",
    },
    "allowable": {
        "en": "Allowable",
        "fr": "Admissible",
    },
    "utilization": {
        "en": "Utilization",
        "fr": "Taux d'utilisation",
    },
    "sigma_perp": {
        "en": "Sigma perp [MPa]",
        "fr": "Sigma perp [MPa]",
    },
    "tau_perp": {
        "en": "Tau perp [MPa]",
        "fr": "Tau perp [MPa]",
    },
    "tau_parallel": {
        "en": "Tau parallel [MPa]",
        "fr": "Tau parallèle [MPa]",
    },
    "fu_uts": {
        "en": "fu (UTS of weaker part) [MPa]",
        "fr": "fu (UTS de la pièce la plus faible) [MPa]",
    },
    "check_weld_stress": {
        "en": "Check Weld (stress)",
        "fr": "Vérifier la soudure (contrainte)",
    },
    "energy_absorption_analysis": {
        "en": "Energy Absorption Analysis",
        "fr": "Analyse d'absorption d'énergie",
    },
    "upload_or_enter_fd_data": {
        "en": "Upload or enter force-displacement data:",
        "fr": "Télécharger ou saisir les données force-déplacement :",
    },
    "input_method": {
        "en": "Input Method",
        "fr": "Méthode de saisie",
    },
    "manual_sample": {
        "en": "Manual (sample data)",
        "fr": "Manuel (données exemple)",
    },
    "upload_csv": {
        "en": "Upload CSV",
        "fr": "Télécharger CSV",
    },
    "component_mass": {
        "en": "Component Mass [kg]",
        "fr": "Masse du composant [kg]",
    },
    "total_energy": {
        "en": "Total Energy",
        "fr": "Énergie totale",
    },
    "peak_force": {
        "en": "Peak Force",
        "fr": "Force maximale",
    },
    "upload_fd_csv": {
        "en": "Upload force-displacement CSV",
        "fr": "Télécharger le CSV force-déplacement",
    },

    # ── FEA Post-Processing Page ───────────────────────────────────────────
    "fea_postprocessing": {
        "en": "FEA Result Processing",
        "fr": "Traitement des résultats FEA",
    },
    "file_format": {
        "en": "File Format",
        "fr": "Format de fichier",
    },
    "stress_operations": {
        "en": "Stress Operations",
        "fr": "Opérations sur les contraintes",
    },
    "plate_thickness": {
        "en": "Plate Thickness [mm]",
        "fr": "Épaisseur de tôle [mm]",
    },
    "upload_fea_file": {
        "en": "Upload FEA results file",
        "fr": "Télécharger le fichier de résultats FEA",
    },
    "loaded_rows": {
        "en": "Loaded {n} rows, {m} columns",
        "fr": "{n} lignes chargées, {m} colonnes",
    },
    "parsed_nodes": {
        "en": "Parsed {n} nodes",
        "fr": "{n} nœuds analysés",
    },
    "computed_stress_results": {
        "en": "Computed Stress Results",
        "fr": "Résultats de contrainte calculés",
    },
    "vm_stress_distribution": {
        "en": "Von Mises Stress Distribution",
        "fr": "Distribution de la contrainte von Mises",
    },
    "hotspot_extraction": {
        "en": "Hot-Spot Stress Extraction",
        "fr": "Extraction de la contrainte Hot-Spot",
    },
    "hotspot_explanation": {
        "en": "Define the weld toe location and path direction for extrapolation.",
        "fr": "Définissez la position du pied de cordon et la direction du chemin pour l'extrapolation.",
    },
    "weld_toe_node": {
        "en": "Weld Toe Node ID",
        "fr": "ID du nœud au pied de cordon",
    },
    "path_direction": {
        "en": "Path Direction",
        "fr": "Direction du chemin",
    },
    "hotspot_type": {
        "en": "Hot-Spot Type",
        "fr": "Type Hot-Spot",
    },
    "extract_hotspot": {
        "en": "Extract Hot-Spot Stress",
        "fr": "Extraire la contrainte Hot-Spot",
    },
    "hotspot_stress_label": {
        "en": "Hot-Spot Stress",
        "fr": "Contrainte Hot-Spot",
    },
    "no_stress_tensor": {
        "en": "No stress tensor columns found. Expected: sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_xz",
        "fr": "Aucune colonne de tenseur de contrainte trouvée. Attendu : sigma_xx, sigma_yy, sigma_zz, tau_xy, tau_yz, tau_xz",
    },
    "error_parsing": {
        "en": "Error parsing file: {e}",
        "fr": "Erreur lors de l'analyse du fichier : {e}",
    },
    "parser_optional": {
        "en": "Parser for {fmt} is available via the [solvers] optional dependency.",
        "fr": "Le parseur pour {fmt} est disponible via la dépendance optionnelle [solvers].",
    },
    "upload_to_start": {
        "en": "Upload an FEA results file to get started.",
        "fr": "Téléchargez un fichier de résultats FEA pour commencer.",
    },
    "expected_csv_format": {
        "en": "Expected CSV Format",
        "fr": "Format CSV attendu",
    },

    # ── Report Generation Page ─────────────────────────────────────────────
    "report_generation": {
        "en": "Report Generation",
        "fr": "Génération de rapport",
    },
    "report_settings": {
        "en": "Report Settings",
        "fr": "Paramètres du rapport",
    },
    "include_sections": {
        "en": "Include Sections",
        "fr": "Sections à inclure",
    },
    "cover_page": {
        "en": "Cover Page",
        "fr": "Page de garde",
    },
    "material_data": {
        "en": "Material Data",
        "fr": "Données matériau",
    },
    "fatigue_results": {
        "en": "Fatigue Results",
        "fr": "Résultats de fatigue",
    },
    "sn_curves": {
        "en": "S-N Curves",
        "fr": "Courbes S-N",
    },
    "haigh_diagram": {
        "en": "Haigh Diagram",
        "fr": "Diagramme de Haigh",
    },
    "crash_results": {
        "en": "Crash Results",
        "fr": "Résultats de crash",
    },
    "energy_metrics": {
        "en": "Energy Metrics",
        "fr": "Métriques d'énergie",
    },
    "output_format": {
        "en": "Output Format",
        "fr": "Format de sortie",
    },
    "project_information": {
        "en": "Project Information",
        "fr": "Informations du projet",
    },
    "project_name": {
        "en": "Project Name",
        "fr": "Nom du projet",
    },
    "default_project_name": {
        "en": "Battery Enclosure Weld Assessment",
        "fr": "Évaluation de soudure de boîtier de batterie",
    },
    "author": {
        "en": "Author",
        "fr": "Auteur",
    },
    "date": {
        "en": "Date",
        "fr": "Date",
    },
    "component": {
        "en": "Component",
        "fr": "Composant",
    },
    "results_data": {
        "en": "Results Data",
        "fr": "Données de résultats",
    },
    "results_auto_include": {
        "en": "Results from the Fatigue and Shock analysis pages will be included automatically if available in the session state.",
        "fr": "Les résultats des pages d'analyse de fatigue et de choc seront inclus automatiquement s'ils sont disponibles dans la session.",
    },
    "fatigue_results_available": {
        "en": "Fatigue results: Available",
        "fr": "Résultats de fatigue : Disponibles",
    },
    "fatigue_results_not_computed": {
        "en": "Fatigue results: Not yet computed (go to Fatigue Analysis page)",
        "fr": "Résultats de fatigue : Pas encore calculés (allez à la page Fatigue Analysis)",
    },
    "generate_report": {
        "en": "Generate Report",
        "fr": "Générer le rapport",
    },
    "download_pdf": {
        "en": "Download PDF Report",
        "fr": "Télécharger le rapport PDF",
    },
    "download_html": {
        "en": "Download HTML Report",
        "fr": "Télécharger le rapport HTML",
    },
    "pdf_generated": {
        "en": "PDF report generated!",
        "fr": "Rapport PDF généré !",
    },
    "html_generated": {
        "en": "HTML report generated!",
        "fr": "Rapport HTML généré !",
    },
    "preview_report": {
        "en": "Preview Report",
        "fr": "Aperçu du rapport",
    },

    # ── Components ─────────────────────────────────────────────────────────
    "sidebar_subtitle": {
        "en": "Fatigue & Shock Validation Tool\nfor Welded Automobile Assemblies",
        "fr": "Outil de validation fatigue et choc\npour assemblages automobiles soudés",
    },
    "status": {
        "en": "Status",
        "fr": "Statut",
    },
    "allowable_n": {
        "en": "Allowable N",
        "fr": "N admissible",
    },
    "upload_fea_results": {
        "en": "Upload FEA results",
        "fr": "Télécharger les résultats FEA",
    },
    "loaded_csv_rows": {
        "en": "Loaded {n} rows from CSV",
        "fr": "{n} lignes chargées depuis le CSV",
    },
    "parser_optional_ext": {
        "en": "Parser for {fmt} files is available as an optional extension.",
        "fr": "Le parseur pour les fichiers {fmt} est disponible en tant qu'extension optionnelle.",
    },
    "weld_assessment": {
        "en": "Weld Fatigue Assessment",
        "fr": "Évaluation de fatigue des soudures",
    },

    # ── Display labels for dropdown values ─────────────────────────────────
    # Material families
    "family_steel": {
        "en": "Steel",
        "fr": "Acier",
    },
    "family_aluminum": {
        "en": "Aluminum",
        "fr": "Aluminium",
    },

    # Weld types
    "weld_butt": {
        "en": "Butt",
        "fr": "Bout à bout",
    },
    "weld_fillet": {
        "en": "Fillet",
        "fr": "Cordon d'angle",
    },
    "weld_cruciform": {
        "en": "Cruciform",
        "fr": "Cruciforme",
    },
    "weld_t_joint": {
        "en": "T-joint",
        "fr": "Joint en T",
    },
    "weld_lap": {
        "en": "Lap",
        "fr": "Joint à recouvrement",
    },
    "weld_stiffener": {
        "en": "Stiffener",
        "fr": "Raidisseur",
    },

    # Load types
    "load_tension": {
        "en": "Tension",
        "fr": "Traction",
    },
    "load_bending": {
        "en": "Bending",
        "fr": "Flexion",
    },
    "load_shear": {
        "en": "Shear",
        "fr": "Cisaillement",
    },

    # Mean stress correction labels
    "msc_none": {
        "en": "None",
        "fr": "Aucune",
    },

    # Material database table columns
    "col_name": {
        "en": "Name",
        "fr": "Nom",
    },
    "col_standard": {
        "en": "Standard",
        "fr": "Norme",
    },
    "col_family": {
        "en": "Family",
        "fr": "Famille",
    },
    "col_yield": {
        "en": "Yield [MPa]",
        "fr": "Re [MPa]",
    },
    "col_uts": {
        "en": "UTS [MPa]",
        "fr": "Rm [MPa]",
    },
    "col_e": {
        "en": "E [MPa]",
        "fr": "E [MPa]",
    },
    "col_density": {
        "en": "Density [kg/m3]",
        "fr": "Densité [kg/m³]",
    },
    "col_elongation": {
        "en": "Elongation [%]",
        "fr": "Allongement [%]",
    },

    # FAT catalog columns
    "col_detail_num": {
        "en": "Detail #",
        "fr": "Détail n°",
    },
    "col_description": {
        "en": "Description",
        "fr": "Description",
    },

    # FEA columns
    "col_node_id": {
        "en": "Node ID",
        "fr": "ID nœud",
    },
    "principal_stresses": {
        "en": "Principal Stresses",
        "fr": "Contraintes principales",
    },
    "max_shear": {
        "en": "Max Shear",
        "fr": "Cisaillement max",
    },
    "hydrostatic": {
        "en": "Hydrostatic",
        "fr": "Hydrostatique",
    },

    # ── Plot labels ────────────────────────────────────────────────────────
    "plot_sn_title": {
        "en": "S-N Curve - FAT {fat} ({mat})",
        "fr": "Courbe S-N - FAT {fat} ({mat})",
    },
    "plot_cycles_axis": {
        "en": "Number of cycles N",
        "fr": "Nombre de cycles N",
    },
    "plot_stress_range_axis": {
        "en": "Stress range [MPa]",
        "fr": "Étendue de contrainte [MPa]",
    },
    "plot_operating_point": {
        "en": "Operating point",
        "fr": "Point de fonctionnement",
    },
    "plot_knee_point": {
        "en": "Knee point",
        "fr": "Point d'inflexion",
    },
    "plot_haigh_title": {
        "en": "Haigh Diagram (Mean Stress Correction)",
        "fr": "Diagramme de Haigh (correction de contrainte moyenne)",
    },
    "plot_mean_stress_axis": {
        "en": "Mean stress [MPa]",
        "fr": "Contrainte moyenne [MPa]",
    },
    "plot_stress_amplitude_axis": {
        "en": "Stress amplitude [MPa]",
        "fr": "Amplitude de contrainte [MPa]",
    },
    "plot_point": {
        "en": "Point {i}",
        "fr": "Point {i}",
    },
    "plot_damage_title": {
        "en": "Damage Contribution per Load Block",
        "fr": "Contribution à l'endommagement par bloc de chargement",
    },
    "plot_stress_range_label": {
        "en": "Stress range",
        "fr": "Étendue de contrainte",
    },
    "plot_damage_ratio_axis": {
        "en": "Damage ratio (ni/Ni)",
        "fr": "Taux d'endommagement (ni/Ni)",
    },
    "plot_dynamic_yield_title": {
        "en": "Dynamic Yield vs Strain Rate - {name}",
        "fr": "Limite d'élasticité dynamique vs taux de déformation - {name}",
    },
    "plot_strain_rate_axis": {
        "en": "Strain rate [1/s]",
        "fr": "Taux de déformation [1/s]",
    },
    "plot_yield_stress_axis": {
        "en": "Yield stress [MPa]",
        "fr": "Limite d'élasticité [MPa]",
    },
    "plot_static_yield": {
        "en": "Static yield",
        "fr": "Limite élastique statique",
    },
    "plot_fd_title": {
        "en": "Force-Displacement Curve",
        "fr": "Courbe force-déplacement",
    },
    "plot_fd_trace": {
        "en": "Force-Displacement",
        "fr": "Force-déplacement",
    },
    "plot_displacement_axis": {
        "en": "Displacement [mm]",
        "fr": "Déplacement [mm]",
    },
    "plot_force_axis": {
        "en": "Force [N]",
        "fr": "Force [N]",
    },
    "plot_mean_annotation": {
        "en": "Mean: {v:.0f} N",
        "fr": "Moyenne : {v:.0f} N",
    },
    "plot_peak_annotation": {
        "en": "Peak: {v:.0f} N",
        "fr": "Max : {v:.0f} N",
    },

    # File format
    "csv_generic": {
        "en": "CSV (generic)",
        "fr": "CSV (générique)",
    },

    # ── Home page module cards ────────────────────────────────────────────
    "mod_material_db_title": {
        "en": "Material Database",
        "fr": "Base de matériaux",
    },
    "mod_fatigue_title": {
        "en": "Fatigue Analysis",
        "fr": "Analyse de fatigue",
    },
    "mod_shock_title": {
        "en": "Shock / Crash",
        "fr": "Choc / Crash",
    },
    "mod_fea_title": {
        "en": "FEA Post-Processing",
        "fr": "Post-traitement EF",
    },
    "mod_report_title": {
        "en": "Report Generation",
        "fr": "Génération de rapport",
    },
    "open_module": {
        "en": "Open",
        "fr": "Ouvrir",
    },

    # ── Session status ────────────────────────────────────────────────────
    "session_status": {
        "en": "Session Status",
        "fr": "État de la session",
    },
    "ready": {
        "en": "Ready",
        "fr": "Prêt",
    },
    "pending": {
        "en": "Pending",
        "fr": "En attente",
    },

    # ── Haigh diagram ─────────────────────────────────────────────────────
    "haigh_diagram": {
        "en": "Haigh Diagram",
        "fr": "Diagramme de Haigh",
    },
    "haigh_explanation": {
        "en": "The Haigh diagram shows the interaction between mean stress and stress amplitude. "
              "Operating points below the Goodman line (blue) are considered safe. "
              "The Gerber parabola (green dashed) is less conservative.",
        "fr": "Le diagramme de Haigh montre l'interaction entre la contrainte moyenne et l'amplitude de contrainte. "
              "Les points de fonctionnement sous la ligne de Goodman (bleue) sont considérés comme sûrs. "
              "La parabole de Gerber (verte pointillée) est moins conservatrice.",
    },

    # ── Rainflow ──────────────────────────────────────────────────────────
    "rainflow_from_signal": {
        "en": "Rainflow Counting from Signal",
        "fr": "Comptage Rainflow à partir du signal",
    },
    "rainflow_explanation": {
        "en": "Upload a time-domain stress signal (single column CSV). "
              "The rainflow algorithm (ASTM E1049-85) extracts the load spectrum automatically.",
        "fr": "Téléchargez un signal temporel de contrainte (CSV à une colonne). "
              "L'algorithme rainflow (ASTM E1049-85) extrait le spectre de chargement automatiquement.",
    },
    "spectrum_input_method": {
        "en": "Spectrum input method",
        "fr": "Méthode d'entrée du spectre",
    },
    "manual_spectrum": {
        "en": "Manual entry",
        "fr": "Saisie manuelle",
    },
    "from_time_signal": {
        "en": "From time signal (Rainflow)",
        "fr": "À partir du signal temporel (Rainflow)",
    },
    "upload_time_signal": {
        "en": "Upload stress signal (CSV, single column)",
        "fr": "Télécharger le signal de contrainte (CSV, colonne unique)",
    },
    "signal_column": {
        "en": "Signal column",
        "fr": "Colonne du signal",
    },
    "rainflow_bins": {
        "en": "Number of bins",
        "fr": "Nombre de classes",
    },
    "rainflow_spectrum": {
        "en": "Extracted Load Spectrum",
        "fr": "Spectre de chargement extrait",
    },
    "use_for_miner": {
        "en": "Use this spectrum for Miner assessment",
        "fr": "Utiliser ce spectre pour l'évaluation de Miner",
    },
    "spectrum_loaded": {
        "en": "Spectrum loaded! Configure settings and click 'Run Miner Assessment'.",
        "fr": "Spectre chargé ! Configurez les paramètres et cliquez sur 'Lancer l'évaluation Miner'.",
    },

    # ── Damage limit ──────────────────────────────────────────────────────
    "damage_limit": {
        "en": "Damage Limit (IIW)",
        "fr": "Limite d'endommagement (IIW)",
    },
    "damage_limit_help": {
        "en": "IIW recommends D=0.5 for safety-critical joints, D=1.0 for normal joints.",
        "fr": "L'IIW recommande D=0.5 pour les joints critiques, D=1.0 pour les joints normaux.",
    },

    # ── FEA → Fatigue integration ─────────────────────────────────────────
    "fea_result_available": {
        "en": "FEA Hot-Spot Result Available",
        "fr": "Résultat Hot-Spot EF disponible",
    },
    "fea_hotspot_detected": {
        "en": "Hot-spot stress: {stress} MPa (Type {hs_type})",
        "fr": "Contrainte hot-spot : {stress} MPa (Type {hs_type})",
    },
    "import_from_fea": {
        "en": "Import from FEA",
        "fr": "Importer depuis l'EF",
    },
    "hotspot_saved_to_session": {
        "en": "Hot-spot stress saved. Navigate to Fatigue Analysis to use it.",
        "fr": "Contrainte hot-spot sauvegardée. Allez à l'analyse de fatigue pour l'utiliser.",
    },
    "navigate_to_fatigue_hint": {
        "en": "Go to **Fatigue Analysis** in the sidebar to continue the assessment.",
        "fr": "Allez dans **Analyse de fatigue** dans la barre latérale pour continuer l'évaluation.",
    },
    "msc_not_applicable_for_method": {
        "en": "Mean stress correction is not applied for Hot-Spot / Notch Stress methods.",
        "fr": "La correction de contrainte moyenne n'est pas appliquée pour les méthodes Hot-Spot / Notch.",
    },

    # ── Report enhancements ───────────────────────────────────────────────
    "crash_results_available": {
        "en": "Shock/Crash results available",
        "fr": "Résultats choc/crash disponibles",
    },
    "crash_results_not_computed": {
        "en": "Shock/Crash results not yet computed",
        "fr": "Résultats choc/crash non encore calculés",
    },
    "fea_results_available": {
        "en": "FEA hot-spot results available",
        "fr": "Résultats hot-spot EF disponibles",
    },
    "fea_results_not_computed": {
        "en": "FEA hot-spot results not yet computed",
        "fr": "Résultats hot-spot EF non encore calculés",
    },
    "download_shock_html": {
        "en": "Download Shock Report (HTML)",
        "fr": "Télécharger le rapport choc (HTML)",
    },

    # ── Student help / method explanations ────────────────────────────────
    "method_explanation": {
        "en": "Method explanation",
        "fr": "Explication de la méthode",
    },
    "help_nominal": {
        "en": "**Nominal Stress Method** — Use beam/plate theory to compute the global stress, "
              "ignoring weld geometry. The FAT class accounts for the weld detail. "
              "Simplest IIW method, suitable for standard welded details.",
        "fr": "**Méthode de la contrainte nominale** — Utilise la théorie des poutres/plaques pour calculer "
              "la contrainte globale, sans tenir compte de la géométrie de la soudure. "
              "La classe FAT tient compte du détail. Méthode IIW la plus simple.",
    },
    "help_hotspot": {
        "en": "**Hot-Spot Stress Method** — Extrapolate surface stresses at IIW reference points "
              "(0.4t and 1.0t from weld toe). Accounts for structural geometry but not weld notch. "
              "Requires FEA results. Use FAT 100 (steel) or FAT 40 (aluminum).",
        "fr": "**Méthode de la contrainte au point chaud** — Extrapole les contraintes de surface aux points "
              "de référence IIW (0.4t et 1.0t du pied de soudure). Tient compte de la géométrie structurelle "
              "mais pas de l'entaille. Nécessite des résultats EF.",
    },
    "help_notch": {
        "en": "**Effective Notch Stress Method** — Include a 1 mm fictitious radius at the weld notch. "
              "Universal FAT class: FAT 225 (steel) / FAT 71 (aluminum). "
              "Most detailed method, requires a fine FEA mesh at the weld toe.",
        "fr": "**Méthode de la contrainte d'entaille effective** — Inclut un rayon fictif de 1 mm à l'entaille "
              "de la soudure. Classe FAT universelle : FAT 225 (acier) / FAT 71 (aluminium). "
              "Méthode la plus détaillée, nécessite un maillage EF fin au pied de soudure.",
    },
    "fat_class_guide": {
        "en": "FAT class guide",
        "fr": "Guide des classes FAT",
    },
    "fat_class_explanation": {
        "en": "The FAT class is the characteristic stress range (MPa) at 2 million cycles. "
              "Higher FAT = better fatigue resistance. "
              "Select the class matching your weld detail from the IIW catalog.",
        "fr": "La classe FAT est l'étendue de contrainte caractéristique (MPa) à 2 millions de cycles. "
              "FAT plus élevé = meilleure résistance à la fatigue. "
              "Sélectionnez la classe correspondant à votre détail de soudure dans le catalogue IIW.",
    },

    # ── Tooltips (help= parameter on widgets) ─────────────────────────────
    "help_stress_range": {
        "en": "The difference between max and min stress in the loading cycle (MPa).",
        "fr": "La différence entre la contrainte max et min dans le cycle de chargement (MPa).",
    },
    "help_mean_stress": {
        "en": "Average of max and min stress. Zero for fully reversed loading (R=-1).",
        "fr": "Moyenne des contraintes max et min. Zéro pour un chargement alternant symétrique (R=-1).",
    },
    "help_num_cycles": {
        "en": "Number of load cycles the component must endure.",
        "fr": "Nombre de cycles de chargement que le composant doit supporter.",
    },
    "help_weld_throat": {
        "en": "Effective throat thickness of the fillet weld (mm).",
        "fr": "Épaisseur de gorge efficace de la soudure d'angle (mm).",
    },

    # ── Engineering summary (fatigue single-block) ─────────────────────────
    "engineering_summary": {
        "en": "Engineering Summary",
        "fr": "Résumé d'ingénierie",
    },
    "stress_decomposition": {
        "en": "Stress Decomposition",
        "fr": "Décomposition des contraintes",
    },
    "sigma_max": {
        "en": "σ_max (Maximum stress)",
        "fr": "σ_max (Contrainte maximale)",
    },
    "sigma_min": {
        "en": "σ_min (Minimum stress)",
        "fr": "σ_min (Contrainte minimale)",
    },
    "stress_amplitude": {
        "en": "σ_a (Stress amplitude)",
        "fr": "σ_a (Amplitude de contrainte)",
    },
    "stress_ratio_r": {
        "en": "R (Stress ratio)",
        "fr": "R (Rapport de contrainte)",
    },
    "fatigue_limits": {
        "en": "Fatigue Limits & Margins",
        "fr": "Limites et marges de fatigue",
    },
    "max_allowable_stress": {
        "en": "Max allowable Δσ for {n} cycles",
        "fr": "Δσ admissible max pour {n} cycles",
    },
    "stress_margin": {
        "en": "Stress margin (allowable − applied)",
        "fr": "Marge de contrainte (admissible − appliqué)",
    },
    "remaining_life": {
        "en": "Remaining life",
        "fr": "Durée de vie restante",
    },
    "life_used_pct": {
        "en": "Life consumed",
        "fr": "Vie consommée",
    },
    "repetitions_to_failure": {
        "en": "Load repetitions to failure",
        "fr": "Répétitions de charge avant rupture",
    },
    "operating_region": {
        "en": "Operating region",
        "fr": "Zone de fonctionnement",
    },
    "above_knee": {
        "en": "Above knee point — finite life region (slope m={m})",
        "fr": "Au-dessus du point de coude — zone de vie finie (pente m={m})",
    },
    "below_knee_ca": {
        "en": "Below knee point — infinite life (constant amplitude endurance limit)",
        "fr": "Sous le point de coude — vie infinie (limite d'endurance en amplitude constante)",
    },
    "below_knee_va": {
        "en": "Below knee point — extended life region (slope m={m})",
        "fr": "Sous le point de coude — zone de vie prolongée (pente m={m})",
    },
    "cycles_unit": {
        "en": "cycles",
        "fr": "cycles",
    },
    "infinite": {
        "en": "Infinite",
        "fr": "Infini",
    },
    "loading_type_label": {
        "en": "Loading type",
        "fr": "Type de chargement",
    },
    "fully_reversed": {
        "en": "Fully reversed (R = −1)",
        "fr": "Alternant symétrique (R = −1)",
    },
    "pulsating_tension": {
        "en": "Pulsating tension (R ≈ 0)",
        "fr": "Traction pulsatoire (R ≈ 0)",
    },
    "tension_tension": {
        "en": "Tension-tension (0 < R < 1)",
        "fr": "Traction-traction (0 < R < 1)",
    },
    "compression_dominated": {
        "en": "Compression dominated (R > 1 or R < −1)",
        "fr": "Dominé par la compression (R > 1 ou R < −1)",
    },
    "general_loading": {
        "en": "General loading (R = {r:.3f})",
        "fr": "Chargement général (R = {r:.3f})",
    },
    "knee_point_stress_val": {
        "en": "Knee point stress: {v:.1f} MPa at {n:.0e} cycles",
        "fr": "Contrainte au coude : {v:.1f} MPa à {n:.0e} cycles",
    },

    # ── Engineering summary (Miner) ────────────────────────────────────────
    "miner_summary": {
        "en": "Miner Damage Summary",
        "fr": "Résumé d'endommagement Miner",
    },
    "remaining_damage_budget": {
        "en": "Remaining damage budget",
        "fr": "Budget d'endommagement restant",
    },
    "spectrum_repetitions": {
        "en": "Full spectrum repetitions to failure",
        "fr": "Répétitions du spectre complet avant rupture",
    },
    "block_contribution": {
        "en": "Block {i}: Δσ = {sr:.1f} MPa → D = {d:.4f} ({pct:.1f}%)",
        "fr": "Bloc {i} : Δσ = {sr:.1f} MPa → D = {d:.4f} ({pct:.1f}%)",
    },
    "damage_breakdown": {
        "en": "Damage Breakdown per Block",
        "fr": "Répartition de l'endommagement par bloc",
    },
    "most_damaging_block": {
        "en": "Most damaging: Block {i} ({pct:.1f}% of total damage)",
        "fr": "Plus endommageant : Bloc {i} ({pct:.1f}% de l'endommagement total)",
    },
    "equivalent_stress_range": {
        "en": "Equivalent constant-amplitude stress range",
        "fr": "Étendue de contrainte équivalente en amplitude constante",
    },

    # ── Engineering summary (shock) ────────────────────────────────────────
    "shock_summary": {
        "en": "Dynamic Properties Summary",
        "fr": "Résumé des propriétés dynamiques",
    },
    "yield_increase_abs": {
        "en": "Yield increase",
        "fr": "Augmentation de la limite élastique",
    },
    "yield_increase_pct": {
        "en": "Yield increase (%)",
        "fr": "Augmentation de la limite élastique (%)",
    },
    "weld_summary": {
        "en": "Weld Check Summary",
        "fr": "Résumé de la vérification de soudure",
    },
    "reserve_factor": {
        "en": "Reserve factor (1/utilization)",
        "fr": "Facteur de réserve (1/utilisation)",
    },
    "stress_margin_weld": {
        "en": "Stress margin",
        "fr": "Marge de contrainte",
    },
    "safety_margin_pct": {
        "en": "Safety margin",
        "fr": "Marge de sécurité",
    },
    "energy_summary": {
        "en": "Energy Absorption Summary",
        "fr": "Résumé de l'absorption d'énergie",
    },
    "mean_crush_force": {
        "en": "Mean crush force",
        "fr": "Force d'écrasement moyenne",
    },
    "energy_per_mm": {
        "en": "Energy absorbed per mm of stroke",
        "fr": "Énergie absorbée par mm de course",
    },
    "stroke_length": {
        "en": "Total stroke",
        "fr": "Course totale",
    },

    # ── Severity classification ────────────────────────────────────────────
    "severity_safe": {"en": "SAFE", "fr": "SÛR"},
    "severity_marginal": {"en": "MARGINAL", "fr": "MARGINAL"},
    "severity_critical": {"en": "CRITICAL", "fr": "CRITIQUE"},

    # ── Panel section labels ──────────────────────────────────────────────
    "section_stress_state": {"en": "STRESS STATE", "fr": "ÉTAT DE CONTRAINTE"},
    "section_fatigue_margins": {"en": "FATIGUE MARGINS", "fr": "MARGES DE FATIGUE"},
    "section_life_assessment": {"en": "LIFE ASSESSMENT", "fr": "ÉVALUATION DE DURÉE DE VIE"},
    "section_damage_budget": {"en": "DAMAGE BUDGET", "fr": "BUDGET D'ENDOMMAGEMENT"},
    "section_block_analysis": {"en": "BLOCK ANALYSIS", "fr": "ANALYSE PAR BLOC"},
    "section_weld_capacity": {"en": "WELD CAPACITY", "fr": "CAPACITÉ DE SOUDURE"},
    "section_energy_metrics": {"en": "ENERGY METRICS", "fr": "MÉTRIQUES D'ÉNERGIE"},
    "section_crush_performance": {"en": "CRUSH PERFORMANCE", "fr": "PERFORMANCE D'ÉCRASEMENT"},

    # ── New computed values (fatigue) ──────────────────────────────────────
    "endurance_ratio": {
        "en": "Endurance ratio",
        "fr": "Ratio d'endurance",
    },
    "overload_capacity": {
        "en": "Overload capacity",
        "fr": "Capacité de surcharge",
    },

    # ── Strain rate / DIF classification (shock) ──────────────────────────
    "strain_rate_regime": {
        "en": "Strain rate regime",
        "fr": "Régime de vitesse de déformation",
    },
    "regime_low": {"en": "Low (quasi-static)", "fr": "Faible (quasi-statique)"},
    "regime_medium": {"en": "Medium (dynamic)", "fr": "Moyen (dynamique)"},
    "regime_high": {"en": "High (impact)", "fr": "Élevé (impact)"},
    "regime_very_high": {"en": "Very high (blast)", "fr": "Très élevé (explosion)"},
    "dif_classification": {
        "en": "DIF classification",
        "fr": "Classification DIF",
    },
    "dif_minimal": {"en": "Minimal effect", "fr": "Effet minimal"},
    "dif_low": {"en": "Low increase", "fr": "Augmentation faible"},
    "dif_moderate": {"en": "Moderate increase", "fr": "Augmentation modérée"},
    "dif_high": {"en": "High increase", "fr": "Augmentation élevée"},
    "min_weld_throat": {
        "en": "Min. throat for PASS",
        "fr": "Gorge min. pour PASS",
    },

    # ── Energy efficiency rating ──────────────────────────────────────────
    "efficiency_rating": {
        "en": "Efficiency rating",
        "fr": "Classement d'efficacité",
    },
    "efficiency_excellent": {"en": "Excellent (CFE > 0.7)", "fr": "Excellent (CFE > 0.7)"},
    "efficiency_good": {"en": "Good (0.5 < CFE ≤ 0.7)", "fr": "Bon (0.5 < CFE ≤ 0.7)"},
    "efficiency_fair": {"en": "Fair (0.3 < CFE ≤ 0.5)", "fr": "Moyen (0.3 < CFE ≤ 0.5)"},
    "efficiency_poor": {"en": "Poor (CFE ≤ 0.3)", "fr": "Médiocre (CFE ≤ 0.3)"},

    # ── What-If calculator ────────────────────────────────────────────────
    "what_if_calculator": {
        "en": "What-If Calculator",
        "fr": "Calculateur hypothétique",
    },
    "what_if_stress_label": {
        "en": "Explore stress range",
        "fr": "Explorer l'étendue de contrainte",
    },

    # ── S-N curve info panel ──────────────────────────────────────────────
    "sn_curve_parameters": {
        "en": "S-N Curve Parameters",
        "fr": "Paramètres de la courbe S-N",
    },
    "slope_m1": {"en": "Slope m₁ (finite life)", "fr": "Pente m₁ (vie finie)"},
    "slope_m2": {"en": "Slope m₂ (extended life)", "fr": "Pente m₂ (vie prolongée)"},
    "knee_cycles": {"en": "Knee point cycles", "fr": "Cycles au point de coude"},
    "cutoff_cycles": {"en": "Cut-off cycles", "fr": "Cycles de coupure"},

    # ── Analysis Modes (Fatigue page) ─────────────────────────────────────
    "analysis_mode": {
        "en": "Analysis Mode",
        "fr": "Mode d'analyse",
    },
    "mode_standard": {
        "en": "Standard (IIW)",
        "fr": "Standard (IIW)",
    },
    "mode_multiaxial": {
        "en": "Multiaxial",
        "fr": "Multiaxial",
    },
    "mode_fracture": {
        "en": "Fracture Mechanics",
        "fr": "Mécanique de la rupture",
    },
    "mode_vibration": {
        "en": "Vibration Fatigue",
        "fr": "Fatigue vibratoire",
    },

    # ── Multiaxial Assessment ─────────────────────────────────────────────
    "multiaxial_params": {
        "en": "Multiaxial Parameters",
        "fr": "Paramètres multiaxiaux",
    },
    "multiaxial_desc": {
        "en": "Assess fatigue under combined normal and shear loading using "
              "IIW multiaxial methods (Gough-Pollard, Findley, MWCM).",
        "fr": "Évaluer la fatigue sous chargement combiné normal et cisaillement "
              "par les méthodes multiaxiales IIW (Gough-Pollard, Findley, MWCM).",
    },
    "loading": {
        "en": "Loading",
        "fr": "Chargement",
    },
    "method_info": {
        "en": "Method Information",
        "fr": "Informations sur la méthode",
    },
    "normal_stress_range": {
        "en": "Normal Stress Range (MPa)",
        "fr": "Étendue de contrainte normale (MPa)",
    },
    "normal_stress_range_help": {
        "en": "Peak-to-peak normal (axial/bending) stress range.",
        "fr": "Étendue de contrainte normale (axiale/flexion) crête à crête.",
    },
    "shear_stress_range": {
        "en": "Shear Stress Range (MPa)",
        "fr": "Étendue de contrainte de cisaillement (MPa)",
    },
    "shear_stress_range_help": {
        "en": "Peak-to-peak shear stress range.",
        "fr": "Étendue de contrainte de cisaillement crête à crête.",
    },
    "interaction_diagram": {
        "en": "Interaction Diagram",
        "fr": "Diagramme d'interaction",
    },
    "interaction_envelope": {
        "en": "Interaction Envelope",
        "fr": "Enveloppe d'interaction",
    },
    "operating_point": {
        "en": "Operating Point",
        "fr": "Point de fonctionnement",
    },
    "detailed_results": {
        "en": "Detailed Results",
        "fr": "Résultats détaillés",
    },
    "results": {
        "en": "Results",
        "fr": "Résultats",
    },

    # ── Fracture Mechanics ────────────────────────────────────────────────
    "crack_growth_params": {
        "en": "Crack Growth Parameters",
        "fr": "Paramètres de propagation de fissure",
    },
    "fracture_desc": {
        "en": "Paris law fatigue crack propagation analysis (IIW 4th method). "
              "Integrates crack growth from initial flaw size to critical size.",
        "fr": "Analyse de propagation de fissure par la loi de Paris (4ᵉ méthode IIW). "
              "Intègre la croissance de fissure de la taille initiale au défaut critique.",
    },
    "environment": {
        "en": "Environment",
        "fr": "Environnement",
    },
    "weld_geometry": {
        "en": "Weld Geometry",
        "fr": "Géométrie de soudure",
    },
    "geometry_loading": {
        "en": "Geometry & Loading",
        "fr": "Géométrie et chargement",
    },
    "initial_conditions": {
        "en": "Initial Conditions",
        "fr": "Conditions initiales",
    },
    "initial_crack_help": {
        "en": "Initial flaw depth detected or assumed.",
        "fr": "Profondeur de défaut initial détecté ou supposé.",
    },
    "critical_crack_help": {
        "en": "Crack size at which failure / instability occurs.",
        "fr": "Taille de fissure à laquelle la rupture / instabilité survient.",
    },
    "plate_thickness": {
        "en": "Plate Thickness",
        "fr": "Épaisseur de plaque",
    },
    "below_threshold_warning": {
        "en": "Initial ΔK is below threshold — no crack growth expected.",
        "fr": "ΔK initial en dessous du seuil — aucune propagation attendue.",
    },
    "crack_grows_critical": {
        "en": "CRACK GROWS TO CRITICAL SIZE",
        "fr": "FISSURE ATTEINT LA TAILLE CRITIQUE",
    },
    "crack_arrested": {
        "en": "CRACK ARRESTED (below threshold)",
        "fr": "FISSURE ARRÊTÉE (sous le seuil)",
    },
    "propagation_life": {
        "en": "Propagation Life (cycles)",
        "fr": "Durée de vie en propagation (cycles)",
    },
    "crack_growth_curve": {
        "en": "Crack Growth Curve",
        "fr": "Courbe de propagation de fissure",
    },

    # ── Vibration Fatigue ─────────────────────────────────────────────────
    "vibration_params": {
        "en": "Vibration Fatigue Parameters",
        "fr": "Paramètres de fatigue vibratoire",
    },
    "vibration_desc": {
        "en": "Frequency-domain fatigue analysis from Power Spectral Density (PSD) input. "
              "Computes Palmgren-Miner damage using Dirlik, narrow-band, and Wirsching-Light methods.",
        "fr": "Analyse de fatigue fréquentielle à partir de la densité spectrale de puissance (PSD). "
              "Calcule le dommage Palmgren-Miner par les méthodes Dirlik, bande étroite et Wirsching-Light.",
    },
    "duration_seconds": {
        "en": "Duration (seconds)",
        "fr": "Durée (secondes)",
    },
    "duration_help": {
        "en": "Total exposure duration in seconds.",
        "fr": "Durée totale d'exposition en secondes.",
    },
    "psd_input_mode": {
        "en": "PSD Input Mode",
        "fr": "Mode d'entrée PSD",
    },
    "psd_example": {
        "en": "Example PSD",
        "fr": "PSD exemple",
    },
    "psd_manual": {
        "en": "Manual Entry",
        "fr": "Saisie manuelle",
    },
    "psd_csv": {
        "en": "CSV Upload",
        "fr": "Import CSV",
    },
    "psd_example_info": {
        "en": "Using a flat PSD of 1.0 MPa²/Hz between 5 Hz and 500 Hz as a demonstration.",
        "fr": "Utilisation d'une PSD plate de 1.0 MPa²/Hz entre 5 Hz et 500 Hz en démonstration.",
    },
    "psd_manual_info": {
        "en": "Enter frequency and PSD values as comma-separated lines: `frequency, PSD_value`",
        "fr": "Entrez les valeurs fréquence et PSD séparées par des virgules : `fréquence, valeur_PSD`",
    },
    "psd_manual_label": {
        "en": "Frequency, PSD (one pair per line)",
        "fr": "Fréquence, PSD (une paire par ligne)",
    },
    "psd_need_points": {
        "en": "Need at least 2 data points.",
        "fr": "Au moins 2 points de données requis.",
    },
    "psd_parse_error": {
        "en": "Could not parse input. Use format: `frequency, PSD_value`",
        "fr": "Impossible de parser l'entrée. Utilisez le format : `fréquence, valeur_PSD`",
    },
    "psd_csv_upload": {
        "en": "Upload CSV (columns: frequency, PSD)",
        "fr": "Import CSV (colonnes : fréquence, PSD)",
    },
    "psd_csv_error": {
        "en": "CSV must have at least 2 columns (frequency, PSD).",
        "fr": "Le CSV doit avoir au moins 2 colonnes (fréquence, PSD).",
    },
    "psd_provide_input": {
        "en": "Provide PSD input data above, then run the assessment.",
        "fr": "Fournissez les données PSD ci-dessus, puis lancez l'évaluation.",
    },
    "psd_input_title": {
        "en": "Input Power Spectral Density",
        "fr": "Densité spectrale de puissance (entrée)",
    },
    "psd_freq_axis": {
        "en": "Frequency (Hz)",
        "fr": "Fréquence (Hz)",
    },
    "psd_value_axis": {
        "en": "PSD (MPa²/Hz)",
        "fr": "PSD (MPa²/Hz)",
    },
    "equivalent_stress": {
        "en": "Equivalent Stress (MPa)",
        "fr": "Contrainte équivalente (MPa)",
    },
    "peak_rate": {
        "en": "Expected Peak Rate (Hz)",
        "fr": "Taux de pics attendu (Hz)",
    },
    "irregularity_factor": {
        "en": "Irregularity Factor",
        "fr": "Facteur d'irrégularité",
    },
    "spectral_moments": {
        "en": "Spectral Moments & Bandwidth",
        "fr": "Moments spectraux et bande passante",
    },
    "damage_comparison": {
        "en": "Damage Comparison",
        "fr": "Comparaison des dommages",
    },
    "damage_by_method": {
        "en": "Damage Estimates by Method",
        "fr": "Estimations de dommage par méthode",
    },

    # ── Weld Quality (ISO 5817) ───────────────────────────────────────────
    "weld_quality_tab": {
        "en": "Weld Quality",
        "fr": "Qualité de soudure",
    },
    "weld_quality_desc": {
        "en": "Evaluate weld imperfections against ISO 5817:2023 quality levels (B, C, D), "
              "compute misalignment stress magnification factors (km), and determine "
              "the quality-adjusted FAT class.",
        "fr": "Évaluer les imperfections de soudure selon les niveaux de qualité ISO 5817:2023 (B, C, D), "
              "calculer les facteurs de majoration de contrainte par mésalignement (km) et déterminer "
              "la classe FAT ajustée en qualité.",
    },
    "quality_level": {
        "en": "ISO 5817 Quality Level",
        "fr": "Niveau de qualité ISO 5817",
    },
    "quality_level_help": {
        "en": "B = stringent (highest quality), D = moderate (lowest quality).",
        "fr": "B = strict (qualité maximale), D = modéré (qualité minimale).",
    },
    "weld_type_wq": {
        "en": "Weld Type",
        "fr": "Type de soudure",
    },
    "end_restraint": {
        "en": "End Restraint",
        "fr": "Condition d'appui",
    },
    "geometry_misalignment": {
        "en": "Geometry & Misalignment",
        "fr": "Géométrie et mésalignement",
    },
    "joint_length": {
        "en": "Joint Length",
        "fr": "Longueur du joint",
    },
    "axial_misalignment": {
        "en": "Axial Misalignment",
        "fr": "Mésalignement axial",
    },
    "angular_misalignment": {
        "en": "Angular Misalignment",
        "fr": "Mésalignement angulaire",
    },
    "imperfection_checks": {
        "en": "Imperfection Checks (ISO 5817)",
        "fr": "Vérification des imperfections (ISO 5817)",
    },
    "imperfection_intro": {
        "en": "Enter measured imperfection values. They will be compared against "
              "the limits for quality level **{ql}**.",
        "fr": "Entrez les valeurs d'imperfection mesurées. Elles seront comparées "
              "aux limites du niveau de qualité **{ql}**.",
    },
    "undercut_depth": {
        "en": "Undercut Depth",
        "fr": "Profondeur de caniveau",
    },
    "porosity_area": {
        "en": "Porosity Area",
        "fr": "Surface de porosité",
    },
    "excess_weld_metal": {
        "en": "Excess Weld Metal Height",
        "fr": "Hauteur de surépaisseur de soudure",
    },
    "incomplete_penetration": {
        "en": "Incomplete Penetration Depth",
        "fr": "Profondeur de pénétration incomplète",
    },
    "axial_mis_check": {
        "en": "Axial Misalignment (check)",
        "fr": "Mésalignement axial (vérification)",
    },
    "km_factors": {
        "en": "Misalignment Stress Magnification Factors",
        "fr": "Facteurs de majoration de contrainte par mésalignement",
    },
    "effective_fat_km": {
        "en": "Effective FAT (km-adjusted)",
        "fr": "FAT effectif (ajusté km)",
    },
    "imperfection_results": {
        "en": "Imperfection Check Results",
        "fr": "Résultats des vérifications d'imperfection",
    },
    "all_checks_pass": {
        "en": "ALL CHECKS PASS",
        "fr": "TOUTES LES VÉRIFICATIONS RÉUSSIES",
    },
    "some_checks_fail": {
        "en": "SOME CHECKS FAIL",
        "fr": "CERTAINES VÉRIFICATIONS ÉCHOUENT",
    },
    "quality_comparison": {
        "en": "Quality Level Comparison",
        "fr": "Comparaison des niveaux de qualité",
    },
    "fat_by_quality_level": {
        "en": "FAT Class by Quality Level",
        "fr": "Classe FAT par niveau de qualité",
    },
}


# ---------------------------------------------------------------------------
# Dropdown value mapping helpers
# ---------------------------------------------------------------------------

FAMILY_KEYS = ["steel", "aluminum"]
FAMILY_LABELS = {"steel": "family_steel", "aluminum": "family_aluminum"}

WELD_TYPE_KEYS = ["butt", "fillet", "cruciform", "t_joint", "lap", "stiffener"]
WELD_TYPE_LABELS = {
    "butt": "weld_butt", "fillet": "weld_fillet", "cruciform": "weld_cruciform",
    "t_joint": "weld_t_joint", "lap": "weld_lap", "stiffener": "weld_stiffener",
}

LOAD_TYPE_KEYS = ["tension", "bending", "shear"]
LOAD_TYPE_LABELS = {
    "tension": "load_tension", "bending": "load_bending", "shear": "load_shear",
}

MSC_KEYS = ["none", "goodman", "gerber", "soderberg"]
MSC_LABELS = {"none": "msc_none"}  # goodman/gerber/soderberg stay as-is (names)

# File format display (internal key → display label)
FILE_FORMAT_KEYS = ["CSV (generic)", "LS-DYNA (.k)", "Abaqus (.inp)", "Nastran (.bdf)"]
FILE_FORMAT_LABELS = {"CSV (generic)": "csv_generic"}


def format_file_format(key: str) -> str:
    """Translate a file-format key for display."""
    label_key = FILE_FORMAT_LABELS.get(key)
    return t(label_key) if label_key else key

# Column rename map for MaterialDatabase.to_dataframe()
DB_COLUMN_MAP = {
    "Name": "col_name",
    "Standard": "col_standard",
    "Family": "col_family",
    "Yield [MPa]": "col_yield",
    "UTS [MPa]": "col_uts",
    "E [MPa]": "col_e",
    "Density [kg/m3]": "col_density",
    "Elongation [%]": "col_elongation",
}


def format_family(key: str) -> str:
    """Translate a family key for display."""
    label_key = FAMILY_LABELS.get(key)
    return t(label_key) if label_key else key


def format_weld_type(key: str) -> str:
    """Translate a weld type key for display."""
    label_key = WELD_TYPE_LABELS.get(key)
    return t(label_key) if label_key else key


def format_load_type(key: str) -> str:
    """Translate a load type key for display."""
    label_key = LOAD_TYPE_LABELS.get(key)
    return t(label_key) if label_key else key


def format_msc(key: str) -> str:
    """Translate a mean-stress-correction key for display."""
    label_key = MSC_LABELS.get(key)
    return t(label_key) if label_key else key.capitalize()


def rename_db_columns(df) -> "pd.DataFrame":
    """Rename MaterialDatabase DataFrame columns to the active language."""
    col_map = {eng: t(i18n_key) for eng, i18n_key in DB_COLUMN_MAP.items()}
    # Also translate the Family *values* inside the column
    fam_col = col_map.get("Family", t("col_family"))
    renamed = df.rename(columns=col_map)
    if fam_col in renamed.columns:
        renamed[fam_col] = renamed[fam_col].map(
            lambda v: format_family(v) if isinstance(v, str) else v
        )
    return renamed


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------

def get_lang() -> str:
    """Return the current language from session state ('en' or 'fr')."""
    return st.session_state.get("lang", "fr")


def t(key: str, **kwargs) -> str:
    """Translate *key* to the active language.

    Supports ``{placeholder}`` substitutions via *kwargs*.
    Falls back to English if the key or language is missing.
    """
    lang = get_lang()
    entry = TRANSLATIONS.get(key, {})
    text = entry.get(lang, entry.get("en", key))
    if kwargs:
        text = text.format(**kwargs)
    return text


def language_selector():
    """Render a language selector in the sidebar and persist the choice."""
    langs = {"Français": "fr", "English": "en"}
    current = get_lang()
    default_index = 0 if current == "fr" else 1
    chosen_label = st.sidebar.selectbox(
        "🌐 Langue / Language",
        list(langs.keys()),
        index=default_index,
        key="_lang_selector",
    )
    st.session_state["lang"] = langs[chosen_label]
