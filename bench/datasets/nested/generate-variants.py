#!/usr/bin/env python3
"""
Generate nested dataset variants for benchmark testing.
Same structure, different content to avoid prompt cache contamination.

Nesting levels:
- shallow: org -> departments (2 levels)
- medium: org -> departments -> teams (3 levels)
- deep: org -> departments -> teams -> members -> skills (4+ levels)
"""

import json
from pathlib import Path

# Variant configurations with themed names for orgs, departments, teams, people, skills
VARIANTS = {
    "a": {  # Food theme
        "org_prefix": "Culinary",
        "org_suffixes": ["Collective", "Kitchen", "Pantry", "Garden", "Market"],
        "headquarters": ["Bordeaux, France", "Tokyo, Japan", "Barcelona, Spain", "Bangkok, Thailand", "Lima, Peru"],
        "departments": [
            {"id": "bakery", "name": "Bakery Division", "budget": 4500000},
            {"id": "savory", "name": "Savory Arts", "budget": 5200000},
            {"id": "pastry", "name": "Pastry & Desserts", "budget": 3800000},
            {"id": "ferment", "name": "Fermentation Lab", "budget": 2100000},
        ],
        "heads": ["Pepper Crumble", "Ginger Tart", "Basil Crisp", "Sage Compote"],
        "teams": {
            "bakery": [
                {"id": "bread", "name": "Artisan Bread", "items": ["sourdough", "ciabatta", "baguette"]},
                {"id": "pastry_bake", "name": "Baked Pastries", "items": ["croissant", "danish", "brioche"]},
                {"id": "gluten_free", "name": "Gluten-Free", "items": ["rice_flour", "almond_flour", "buckwheat"]},
            ],
            "savory": [
                {"id": "grill", "name": "Grill Station", "items": ["charcoal", "wood_fire", "plancha"]},
                {"id": "sauce", "name": "Sauce Kitchen", "items": ["reduction", "emulsion", "stock"]},
            ],
            "pastry": [
                {"id": "chocolate", "name": "Chocolate Lab", "items": ["tempering", "ganache", "praline"]},
                {"id": "sugar", "name": "Sugar Work", "items": ["caramel", "pulled_sugar", "isomalt"]},
            ],
            "ferment": [
                {"id": "pickle", "name": "Pickle & Preserve", "items": ["lacto", "vinegar", "salt_cure"]},
            ],
        },
        "leads": ["Olive Glaze", "Clove Puree", "Maple Preserve", "Hazel Chutney", "Honey Relish",
                  "Cinnamon Brine", "Saffron Cure", "Thyme Smoke", "Rosemary Roast", "Vanilla Braise"],
        "members": [
            ("Nutmeg", "Saute"), ("Almond", "Blanch"), ("Pecan", "Poach"), ("Walnut", "Simmer"),
            ("Cashew", "Steam"), ("Pistachio", "Grill"), ("Mango", "Sear"), ("Papaya", "Caramelize"),
            ("Kiwi", "Deglaze"), ("Lemon", "Flambe"), ("Lime", "Julienne"), ("Berry", "Brunoise"),
            ("Cherry", "Chiffonade"), ("Plum", "Mince"), ("Peach", "Dice"),
        ],
        "roles": ["Sous Chef", "Line Cook", "Pastry Chef", "Prep Cook", "Garde Manger"],
        "skills": [
            ("knife_work", "sauteing", "braising"),
            ("tempering", "lamination", "fermentation"),
            ("emulsification", "reduction", "plating"),
            ("butchery", "filleting", "curing"),
            ("baking", "proofing", "shaping"),
        ],
        "proficiencies": ["apprentice", "commis", "chef_de_partie", "sous_chef", "executive"],
    },
    "b": {  # Color theme
        "org_prefix": "Chromatic",
        "org_suffixes": ["Studios", "Spectrum", "Palette", "Canvas", "Prism"],
        "headquarters": ["Florence, Italy", "Paris, France", "Amsterdam, Netherlands", "New York, USA", "Melbourne, Australia"],
        "departments": [
            {"id": "warm", "name": "Warm Tones Division", "budget": 4200000},
            {"id": "cool", "name": "Cool Spectrum", "budget": 4800000},
            {"id": "neutral", "name": "Neutral & Earth", "budget": 2900000},
            {"id": "vivid", "name": "Vivid & Neon", "budget": 3500000},
        ],
        "heads": ["Crimson Shade", "Scarlet Tint", "Ruby Tone", "Garnet Hue"],
        "teams": {
            "warm": [
                {"id": "red", "name": "Red Family", "items": ["vermillion", "coral", "salmon"]},
                {"id": "orange", "name": "Orange Spectrum", "items": ["tangerine", "amber", "apricot"]},
                {"id": "yellow", "name": "Yellow Suite", "items": ["gold", "honey", "marigold"]},
            ],
            "cool": [
                {"id": "blue", "name": "Blue Depths", "items": ["azure", "cerulean", "cobalt"]},
                {"id": "green", "name": "Green Range", "items": ["emerald", "jade", "sage"]},
            ],
            "neutral": [
                {"id": "gray", "name": "Gray Scale", "items": ["charcoal", "slate", "ash"]},
                {"id": "brown", "name": "Earth Tones", "items": ["sienna", "umber", "ochre"]},
            ],
            "vivid": [
                {"id": "neon", "name": "Neon Lab", "items": ["electric", "fluorescent", "phosphor"]},
            ],
        },
        "leads": ["Saffron Gradient", "Mustard Spectrum", "Lemon Prism", "Canary Palette", "Chartreuse Swatch",
                  "Lime Pigment", "Mint Dye", "Sage Stain", "Olive Wash", "Emerald Glaze"],
        "members": [
            ("Jade", "Patina"), ("Teal", "Finish"), ("Cyan", "Sheen"), ("Turquoise", "Luster"),
            ("Aqua", "Gleam"), ("Azure", "Shimmer"), ("Cerulean", "Sparkle"), ("Cobalt", "Glow"),
            ("Sapphire", "Radiance"), ("Indigo", "Luminance"), ("Violet", "Brilliance"), ("Lavender", "Flash"),
            ("Lilac", "Flare"), ("Mauve", "Beam"), ("Plum", "Ray"),
        ],
        "roles": ["Color Theorist", "Pigment Specialist", "Palette Designer", "Tint Analyst", "Shade Master"],
        "skills": [
            ("color_mixing", "saturation_control", "value_mapping"),
            ("gradient_design", "spectrum_analysis", "prism_work"),
            ("pigment_chemistry", "dye_formulation", "stain_application"),
            ("digital_color", "print_calibration", "screen_matching"),
            ("lighting_adjustment", "reflection_control", "absorption_analysis"),
        ],
        "proficiencies": ["student", "practitioner", "specialist", "master", "grandmaster"],
    },
    "c": {  # Animal theme
        "org_prefix": "Wildlife",
        "org_suffixes": ["Preserve", "Sanctuary", "Reserve", "Haven", "Territory"],
        "headquarters": ["Nairobi, Kenya", "Darwin, Australia", "Costa Rica", "Vancouver, Canada", "Hokkaido, Japan"],
        "departments": [
            {"id": "avian", "name": "Avian Division", "budget": 3800000},
            {"id": "mammal", "name": "Mammal Studies", "budget": 5500000},
            {"id": "marine", "name": "Marine Life", "budget": 4200000},
            {"id": "reptile", "name": "Reptile & Amphibian", "budget": 2400000},
        ],
        "heads": ["Falcon Paw", "Hawk Claw", "Eagle Talon", "Osprey Hoof"],
        "teams": {
            "avian": [
                {"id": "raptor", "name": "Raptor Research", "items": ["falcon", "hawk", "eagle"]},
                {"id": "songbird", "name": "Songbird Study", "items": ["finch", "sparrow", "wren"]},
                {"id": "waterfowl", "name": "Waterfowl Watch", "items": ["duck", "goose", "swan"]},
            ],
            "mammal": [
                {"id": "predator", "name": "Predator Tracking", "items": ["wolf", "lion", "tiger"]},
                {"id": "ungulate", "name": "Ungulate Research", "items": ["deer", "elk", "moose"]},
            ],
            "marine": [
                {"id": "cetacean", "name": "Cetacean Study", "items": ["whale", "dolphin", "porpoise"]},
                {"id": "pinniped", "name": "Pinniped Watch", "items": ["seal", "sea_lion", "walrus"]},
            ],
            "reptile": [
                {"id": "snake", "name": "Serpent Research", "items": ["cobra", "python", "viper"]},
            ],
        },
        "leads": ["Kite Horn", "Harrier Antler", "Buzzard Tusk", "Owl Fang", "Raven Tooth",
                  "Crow Beak", "Magpie Bill", "Jay Snout", "Finch Muzzle", "Sparrow Whisker"],
        "members": [
            ("Wren", "Bristle"), ("Robin", "Fur"), ("Thrush", "Pelt"), ("Warbler", "Hide"),
            ("Swift", "Coat"), ("Swallow", "Mane"), ("Martin", "Tail"), ("Heron", "Plume"),
            ("Egret", "Feather"), ("Crane", "Wing"), ("Stork", "Fin"), ("Ibis", "Scale"),
            ("Pelican", "Shell"), ("Cormorant", "Carapace"), ("Gannet", "Spine"),
        ],
        "roles": ["Field Researcher", "Behavioral Analyst", "Conservation Lead", "Habitat Specialist", "Migration Tracker"],
        "skills": [
            ("tracking", "observation", "documentation"),
            ("tranquilization", "tagging", "sampling"),
            ("habitat_assessment", "population_modeling", "genetic_analysis"),
            ("behavioral_coding", "vocalization_analysis", "movement_patterns"),
            ("conservation_planning", "habitat_restoration", "species_protection"),
        ],
        "proficiencies": ["trainee", "field_assistant", "researcher", "senior_researcher", "principal_investigator"],
    },
    "d": {  # City theme
        "org_prefix": "Metropolitan",
        "org_suffixes": ["Alliance", "Network", "Collective", "Coalition", "Union"],
        "headquarters": ["Singapore", "Dubai, UAE", "Copenhagen, Denmark", "Seoul, South Korea", "Toronto, Canada"],
        "departments": [
            {"id": "transit", "name": "Transit Systems", "budget": 8500000},
            {"id": "planning", "name": "Urban Planning", "budget": 6200000},
            {"id": "green", "name": "Green Spaces", "budget": 3400000},
            {"id": "smart", "name": "Smart City Tech", "budget": 5800000},
        ],
        "heads": ["Tokyo Avenue", "Kyoto Boulevard", "Osaka Street", "Seoul Lane"],
        "teams": {
            "transit": [
                {"id": "rail", "name": "Rail Network", "items": ["subway", "light_rail", "commuter"]},
                {"id": "bus", "name": "Bus Operations", "items": ["local", "express", "brt"]},
                {"id": "bike", "name": "Cycling Infrastructure", "items": ["lanes", "sharing", "parking"]},
            ],
            "planning": [
                {"id": "zoning", "name": "Zoning & Land Use", "items": ["residential", "commercial", "mixed"]},
                {"id": "housing", "name": "Housing Development", "items": ["affordable", "high_density", "sustainable"]},
            ],
            "green": [
                {"id": "parks", "name": "Parks & Recreation", "items": ["urban_parks", "greenways", "plazas"]},
                {"id": "urban_forest", "name": "Urban Forestry", "items": ["street_trees", "canopy", "native_species"]},
            ],
            "smart": [
                {"id": "iot", "name": "IoT Infrastructure", "items": ["sensors", "networks", "platforms"]},
            ],
        },
        "leads": ["Beijing Road", "Shanghai Drive", "Mumbai Way", "Delhi Court", "Bangkok Place",
                  "Hanoi Circle", "Manila Terrace", "Jakarta Plaza", "Singapore Square", "Kuala Park"],
        "members": [
            ("Sydney", "Garden"), ("Melbourne", "Grove"), ("Auckland", "Meadow"), ("Wellington", "Field"),
            ("Perth", "Hill"), ("Brisbane", "Ridge"), ("Cairo", "Valley"), ("Lagos", "Canyon"),
            ("Nairobi", "Cliff"), ("Cape", "Bluff"), ("London", "Point"), ("Paris", "Cape"),
            ("Berlin", "Bay"), ("Rome", "Cove"), ("Madrid", "Harbor"),
        ],
        "roles": ["Urban Planner", "Transit Engineer", "Policy Analyst", "Project Manager", "Community Liaison"],
        "skills": [
            ("gis_mapping", "traffic_modeling", "zoning_analysis"),
            ("stakeholder_engagement", "public_consultation", "community_outreach"),
            ("project_management", "budget_planning", "timeline_coordination"),
            ("sustainability_assessment", "environmental_review", "impact_analysis"),
            ("data_analytics", "smart_city_platforms", "iot_integration"),
        ],
        "proficiencies": ["junior", "associate", "senior", "principal", "director"],
    },
    "e": {  # Space theme
        "org_prefix": "Stellar",
        "org_suffixes": ["Expedition", "Consortium", "Initiative", "Foundation", "Institute"],
        "headquarters": ["Houston, USA", "Baikonur, Kazakhstan", "Kourou, French Guiana", "Tanegashima, Japan", "Bangalore, India"],
        "departments": [
            {"id": "propulsion", "name": "Propulsion Systems", "budget": 12000000},
            {"id": "navigation", "name": "Navigation & Guidance", "budget": 7500000},
            {"id": "habitat", "name": "Habitat Engineering", "budget": 5200000},
            {"id": "science", "name": "Space Science", "budget": 4800000},
        ],
        "heads": ["Nova Drift", "Nebula Shift", "Pulsar Spin", "Quasar Orbit"],
        "teams": {
            "propulsion": [
                {"id": "chemical", "name": "Chemical Propulsion", "items": ["liquid", "solid", "hybrid"]},
                {"id": "ion", "name": "Ion Propulsion", "items": ["hall_thruster", "gridded_ion", "pulsed_plasma"]},
                {"id": "experimental", "name": "Experimental Drives", "items": ["solar_sail", "nuclear_thermal", "em_drive"]},
            ],
            "navigation": [
                {"id": "orbital", "name": "Orbital Mechanics", "items": ["trajectory", "transfer", "rendezvous"]},
                {"id": "comms", "name": "Deep Space Comms", "items": ["dsn", "optical", "relay"]},
            ],
            "habitat": [
                {"id": "life_support", "name": "Life Support", "items": ["atmosphere", "water", "food"]},
                {"id": "radiation", "name": "Radiation Shielding", "items": ["passive", "active", "magnetic"]},
            ],
            "science": [
                {"id": "astronomy", "name": "Observational Astronomy", "items": ["optical", "radio", "infrared"]},
            ],
        },
        "leads": ["Neutron Transit", "Proton Eclipse", "Photon Occult", "Electron Phase", "Positron Cycle",
                  "Neutrino Period", "Muon Epoch", "Tau Era", "Boson Age", "Higgs Eon"],
        "members": [
            ("Gluon", "Instant"), ("Meson", "Moment"), ("Baryon", "Second"), ("Hadron", "Minute"),
            ("Lepton", "Hour"), ("Fermion", "Day"), ("Quark", "Night"), ("Plasma", "Dawn"),
            ("Corona", "Dusk"), ("Aurora", "Twilight"), ("Solar", "Midnight"), ("Lunar", "Noon"),
            ("Stellar", "Morning"), ("Cosmic", "Evening"), ("Galactic", "Season"),
        ],
        "roles": ["Mission Specialist", "Flight Engineer", "Systems Analyst", "Research Scientist", "Operations Lead"],
        "skills": [
            ("orbital_mechanics", "trajectory_planning", "rendezvous_ops"),
            ("propulsion_systems", "fuel_management", "thrust_vectoring"),
            ("life_support_maintenance", "eva_operations", "emergency_protocols"),
            ("telemetry_analysis", "data_processing", "mission_planning"),
            ("scientific_instrumentation", "experiment_design", "sample_analysis"),
        ],
        "proficiencies": ["candidate", "trainee", "certified", "veteran", "commander"],
    },
}


def generate_shallow(variant_key):
    """Generate shallow dataset: org -> departments (2 levels)."""
    v = VARIANTS[variant_key]

    departments = []
    for i, dept in enumerate(v["departments"]):
        departments.append({
            "id": dept["id"],
            "name": dept["name"],
            "budget": dept["budget"],
            "head": v["heads"][i % len(v["heads"])],
            "employee_count": 25 + (i * 30),
        })

    return {
        "organization": {
            "name": f"{v['org_prefix']} {v['org_suffixes'][0]}",
            "founded": 2010 + (ord(variant_key) - ord('a')),
            "departments": departments,
        }
    }


def generate_medium(variant_key):
    """Generate medium dataset: org -> departments -> teams (3 levels)."""
    v = VARIANTS[variant_key]

    departments = []
    lead_idx = 0
    for i, dept in enumerate(v["departments"]):
        teams_data = v["teams"].get(dept["id"], [])
        teams = []
        for team in teams_data:
            # Use items as tech_stack, regions, or channels depending on context
            items_key = "tech_stack" if dept["id"] in ["bakery", "propulsion", "warm"] else \
                        "regions" if dept["id"] in ["savory", "mammal", "transit"] else "channels"
            teams.append({
                "id": team["id"],
                "name": team["name"],
                "lead": v["leads"][lead_idx % len(v["leads"])],
                "members": 15 + (lead_idx * 5),
                items_key: team["items"],
            })
            lead_idx += 1

        departments.append({
            "id": dept["id"],
            "name": dept["name"],
            "budget": dept["budget"],
            "head": v["heads"][i % len(v["heads"])],
            "teams": teams,
        })

    return {
        "organization": {
            "name": f"{v['org_prefix']} {v['org_suffixes'][1]}",
            "founded": 2010 + (ord(variant_key) - ord('a')),
            "departments": departments,
        }
    }


def generate_deep(variant_key):
    """Generate deep dataset: org -> departments -> teams -> members -> skills (4+ levels)."""
    v = VARIANTS[variant_key]

    departments = []
    lead_idx = 0
    member_id = 1001

    for i, dept in enumerate(v["departments"][:2]):  # Limit to 2 departments for deep
        teams_data = v["teams"].get(dept["id"], [])[:2]  # Limit to 2 teams per dept
        teams = []

        for team in teams_data:
            members = []
            # Add 2-3 members per team
            num_members = 2 if lead_idx == 0 else 3
            for m in range(num_members):
                member_tuple = v["members"][(lead_idx + m) % len(v["members"])]
                member_name = f"{member_tuple[0]} {member_tuple[1]}"

                # Generate skills for this member
                skill_set = v["skills"][(lead_idx + m) % len(v["skills"])]
                years_exp = 3 + (m * 2)
                skills = []
                for s_idx, skill_name in enumerate(skill_set):
                    skills.append({
                        "name": skill_name,
                        "proficiency": v["proficiencies"][min(s_idx + m, len(v["proficiencies"]) - 1)],
                        "years": years_exp - s_idx if years_exp > s_idx else 1,
                    })

                members.append({
                    "id": member_id,
                    "name": member_name,
                    "role": v["roles"][m % len(v["roles"])],
                    "years_experience": years_exp,
                    "skills": skills,
                })
                member_id += 1

            teams.append({
                "id": team["id"],
                "name": team["name"],
                "lead": v["leads"][lead_idx % len(v["leads"])],
                "members": members,
            })
            lead_idx += 1

        departments.append({
            "id": dept["id"],
            "name": dept["name"],
            "budget": dept["budget"],
            "head": v["heads"][i % len(v["heads"])],
            "teams": teams,
        })

    return {
        "organization": {
            "name": f"{v['org_prefix']} {v['org_suffixes'][2]}",
            "founded": 2010 + (ord(variant_key) - ord('a')),
            "headquarters": v["headquarters"][ord(variant_key) - ord('a')],
            "departments": departments,
        }
    }


def main():
    base_path = Path(__file__).parent
    depths = ["shallow", "medium", "deep"]
    variant_keys = ["a", "b", "c", "d", "e"]
    generators = {
        "shallow": generate_shallow,
        "medium": generate_medium,
        "deep": generate_deep,
    }

    for depth in depths:
        depth_dir = base_path / depth
        depth_dir.mkdir(exist_ok=True)

        for variant in variant_keys:
            dataset = generators[depth](variant)
            output_path = depth_dir / f"variant-{variant}.json"

            with open(output_path, "w") as f:
                json.dump(dataset, f, indent=2)
                f.write("\n")

            print(f"Generated {output_path}")

    print(f"\nGenerated {len(depths) * len(variant_keys)} nested dataset variants.")


if __name__ == "__main__":
    main()
