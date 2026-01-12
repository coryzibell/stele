#!/usr/bin/env python3
"""
Generate dataset variants for benchmark testing.
Same structure, different content to avoid prompt cache contamination.
"""

import json
from pathlib import Path

# Variant configurations: (theme, domain, first_names, last_names)
VARIANTS = {
    "a": {
        "domain": "foodmail.io",
        "firsts": [
            "pepper", "ginger", "basil", "sage", "olive", "clove", "maple", "hazel",
            "honey", "cinnamon", "saffron", "thyme", "rosemary", "vanilla", "cocoa",
            "nutmeg", "almond", "pecan", "walnut", "cashew", "pistachio", "mango",
            "papaya", "kiwi", "lemon", "lime", "berry", "cherry", "plum", "peach",
            "apricot", "fig", "date", "grape", "melon", "grapefruit", "tangerine",
            "clementine", "kumquat", "lychee", "guava", "coconut", "pineapple",
            "banana", "apple", "pear", "quince", "persimmon", "pomegranate", "raisin",
            "currant", "elderberry", "mulberry", "boysenberry", "gooseberry", "cranberry",
            "blueberry", "raspberry", "strawberry", "blackberry", "lingonberry", "acai",
            "dragonfruit", "starfruit", "passionfruit", "tamarind", "jackfruit", "durian",
            "rambutan", "mangosteen", "soursop", "cherimoya", "plantain", "breadfruit",
            "avocado", "tomato", "cucumber", "zucchini", "squash", "pumpkin", "carrot",
            "parsnip", "turnip", "radish", "beet", "potato", "yam", "cassava", "taro",
            "onion", "garlic", "shallot", "leek", "chive", "scallion", "fennel", "celery",
            "rhubarb", "asparagus", "artichoke",
        ],
        "lasts": [
            "crumble", "tart", "crisp", "compote", "reduction", "glaze", "coulis",
            "puree", "preserve", "marmalade", "chutney", "relish", "pickle", "brine",
            "cure", "smoke", "roast", "braise", "saute", "blanch", "poach", "simmer",
            "steam", "grill", "sear", "caramelize", "deglaze", "flambe", "julienne",
            "brunoise", "chiffonade", "mince", "dice", "slice", "wedge", "segment",
            "zest", "peel", "core", "seed", "pit", "hull", "trim", "pith", "rind",
            "flesh", "pulp", "juice", "extract", "essence", "infusion", "steep",
            "blend", "whisk", "fold", "cream", "whip", "beat", "knead", "proof",
            "rise", "bake", "broil", "toast", "char", "crust", "crumb", "dust",
            "drizzle", "garnish", "plate", "portion", "serve", "present", "pair",
            "balance", "layer", "stack", "wrap", "roll", "stuff", "fill", "coat",
            "dip", "dredge", "bread", "batter", "fry", "deepfry", "panfry", "stirfry",
            "wok", "griddle", "plancha", "tandoor", "rotisserie", "sous_vide", "confit",
            "cure", "age", "ferment", "culture",
        ],
    },
    "b": {
        "domain": "colorverse.net",
        "firsts": [
            "crimson", "scarlet", "ruby", "garnet", "vermillion", "coral", "salmon",
            "peach", "apricot", "tangerine", "amber", "gold", "honey", "marigold",
            "saffron", "mustard", "lemon", "canary", "chartreuse", "lime", "mint",
            "sage", "olive", "emerald", "jade", "teal", "cyan", "turquoise", "aqua",
            "azure", "cerulean", "cobalt", "sapphire", "indigo", "violet", "lavender",
            "lilac", "mauve", "plum", "magenta", "fuchsia", "rose", "blush", "pink",
            "cerise", "maroon", "burgundy", "wine", "mahogany", "chestnut", "sienna",
            "umber", "ochre", "rust", "copper", "bronze", "brass", "pewter", "silver",
            "platinum", "chrome", "steel", "iron", "slate", "charcoal", "onyx", "jet",
            "obsidian", "ebony", "midnight", "raven", "ink", "ash", "smoke", "fog",
            "mist", "pearl", "ivory", "cream", "bone", "vanilla", "snow", "frost",
            "glacier", "arctic", "winter", "cloud", "cotton", "chalk", "eggshell",
            "linen", "sand", "taupe", "khaki", "beige", "camel", "fawn", "buff",
            "wheat", "flax", "ecru",
        ],
        "lasts": [
            "shade", "tint", "tone", "hue", "saturation", "value", "chroma",
            "gradient", "spectrum", "prism", "palette", "swatch", "pigment", "dye",
            "stain", "wash", "glaze", "patina", "finish", "sheen", "luster", "gleam",
            "shimmer", "sparkle", "glitter", "glow", "radiance", "luminance", "brilliance",
            "flash", "flare", "beam", "ray", "streak", "stripe", "band", "ribbon",
            "swirl", "spiral", "wave", "ripple", "pool", "splash", "drip", "pour",
            "flood", "wash", "fade", "blend", "merge", "mix", "meld", "fuse",
            "layer", "overlap", "contrast", "complement", "harmony", "discord", "clash",
            "pop", "punch", "burst", "bloom", "blossom", "flow", "shift", "morph",
            "transform", "transmute", "evolve", "emerge", "surface", "depth", "dimension",
            "texture", "pattern", "motif", "design", "scheme", "theme", "mood", "vibe",
            "aura", "essence", "spirit", "soul", "heart", "core", "center", "focus",
            "accent", "highlight", "shadow", "contrast", "balance", "weight", "density",
            "opacity", "transparency", "clarity",
        ],
    },
    "c": {
        "domain": "animalnet.org",
        "firsts": [
            "falcon", "hawk", "eagle", "osprey", "kite", "harrier", "buzzard",
            "owl", "raven", "crow", "magpie", "jay", "finch", "sparrow", "wren",
            "robin", "thrush", "warbler", "swift", "swallow", "martin", "heron",
            "egret", "crane", "stork", "ibis", "pelican", "cormorant", "gannet",
            "albatross", "petrel", "puffin", "guillemot", "tern", "gull", "skua",
            "penguin", "kiwi", "emu", "ostrich", "cassowary", "peacock", "pheasant",
            "quail", "partridge", "grouse", "turkey", "duck", "goose", "swan",
            "wolf", "fox", "coyote", "jackal", "hyena", "lion", "tiger", "leopard",
            "jaguar", "cheetah", "panther", "cougar", "lynx", "bobcat", "ocelot",
            "bear", "panda", "badger", "wolverine", "otter", "marten", "weasel",
            "ferret", "mink", "stoat", "mongoose", "meerkat", "raccoon", "coati",
            "deer", "elk", "moose", "caribou", "antelope", "gazelle", "ibex",
            "chamois", "bison", "buffalo", "yak", "ox", "bull", "ram", "goat",
            "sheep", "llama", "alpaca", "camel", "horse", "zebra", "donkey",
        ],
        "lasts": [
            "paw", "claw", "talon", "hoof", "horn", "antler", "tusk", "fang",
            "tooth", "beak", "bill", "snout", "muzzle", "whisker", "bristle", "fur",
            "pelt", "hide", "coat", "mane", "tail", "plume", "feather", "wing",
            "fin", "scale", "shell", "carapace", "spine", "quill", "barb", "frill",
            "crest", "crown", "tuft", "ruff", "collar", "stripe", "spot", "patch",
            "blaze", "marking", "band", "ring", "mask", "saddle", "blanket", "cape",
            "mantle", "hood", "brow", "ridge", "hump", "pouch", "sac", "gland",
            "organ", "muscle", "sinew", "tendon", "bone", "rib", "skull", "jaw",
            "limb", "leg", "arm", "shoulder", "hip", "knee", "elbow", "ankle",
            "wrist", "digit", "toe", "pad", "sole", "heel", "track", "print",
            "trail", "path", "route", "range", "territory", "domain", "realm", "haunt",
            "den", "lair", "nest", "burrow", "warren", "lodge", "holt", "sett",
            "roost", "perch", "aerie", "eyrie", "rookery", "colony", "herd", "pack",
            "pride", "troop", "flock",
        ],
    },
    "d": {
        "domain": "cityscape.co",
        "firsts": [
            "tokyo", "kyoto", "osaka", "seoul", "beijing", "shanghai", "mumbai",
            "delhi", "bangkok", "hanoi", "manila", "jakarta", "singapore", "kuala",
            "sydney", "melbourne", "auckland", "wellington", "perth", "brisbane",
            "cairo", "lagos", "nairobi", "cape", "casablanca", "tunis", "algiers",
            "dakar", "accra", "addis", "london", "paris", "berlin", "rome", "madrid",
            "barcelona", "lisbon", "amsterdam", "brussels", "vienna", "prague",
            "budapest", "warsaw", "stockholm", "oslo", "copenhagen", "helsinki",
            "moscow", "kiev", "athens", "istanbul", "dubai", "doha", "riyadh",
            "tehran", "karachi", "dhaka", "colombo", "kathmandu", "taipei", "hong",
            "macau", "havana", "mexico", "bogota", "lima", "santiago", "buenos",
            "sao", "rio", "caracas", "quito", "montevideo", "asuncion", "la_paz",
            "new_york", "los_angeles", "chicago", "houston", "phoenix", "philadelphia",
            "san_antonio", "san_diego", "dallas", "san_jose", "austin", "jacksonville",
            "fort_worth", "columbus", "charlotte", "seattle", "denver", "boston",
            "nashville", "detroit", "portland", "memphis", "atlanta", "miami",
            "phoenix", "minneapolis", "cleveland", "tampa", "baltimore", "oakland",
        ],
        "lasts": [
            "avenue", "boulevard", "street", "lane", "road", "drive", "way",
            "court", "place", "circle", "terrace", "plaza", "square", "park",
            "garden", "grove", "meadow", "field", "hill", "ridge", "valley",
            "canyon", "cliff", "bluff", "point", "cape", "bay", "cove", "harbor",
            "port", "pier", "dock", "wharf", "quay", "bridge", "crossing", "junction",
            "station", "terminal", "depot", "hub", "center", "complex", "tower",
            "building", "block", "quarter", "district", "ward", "borough", "precinct",
            "zone", "sector", "area", "region", "territory", "province", "county",
            "state", "nation", "realm", "domain", "empire", "kingdom", "republic",
            "union", "federation", "commonwealth", "colony", "outpost", "settlement",
            "village", "town", "city", "metropolis", "megacity", "suburb", "exurb",
            "downtown", "uptown", "midtown", "waterfront", "riverfront", "lakefront",
            "beachfront", "oceanfront", "skyline", "horizon", "vista", "panorama",
            "view", "scene", "landscape", "cityscape", "streetscape", "nightscape",
            "soundscape", "dreamscape", "mindscape", "escape",
        ],
    },
    "e": {
        "domain": "cosmicmail.space",
        "firsts": [
            "nova", "nebula", "pulsar", "quasar", "neutron", "proton", "photon",
            "electron", "positron", "neutrino", "muon", "tau", "boson", "higgs",
            "gluon", "meson", "baryon", "hadron", "lepton", "fermion", "quark",
            "plasma", "corona", "aurora", "solar", "lunar", "stellar", "cosmic",
            "galactic", "orbital", "radial", "axial", "polar", "equator", "meridian",
            "zenith", "nadir", "apex", "vertex", "vector", "tensor", "matrix",
            "quantum", "atomic", "nuclear", "fusion", "fission", "particle", "wave",
            "field", "force", "energy", "mass", "matter", "antimatter", "dark",
            "light", "bright", "dim", "faint", "vivid", "intense", "brilliant",
            "radiant", "luminous", "glowing", "blazing", "burning", "flaming", "fiery",
            "ember", "spark", "flash", "burst", "flare", "pulse", "beacon", "signal",
            "echo", "ripple", "tremor", "quake", "surge", "swell", "tide", "current",
            "flow", "stream", "jet", "beam", "ray", "shaft", "column", "pillar",
            "tower", "spire", "needle", "point", "edge", "blade", "arc", "curve",
            "spiral", "helix", "vortex", "cyclone",
        ],
        "lasts": [
            "drift", "shift", "spin", "orbit", "transit", "eclipse", "occult",
            "phase", "cycle", "period", "epoch", "era", "age", "eon", "instant",
            "moment", "second", "minute", "hour", "day", "night", "dawn", "dusk",
            "twilight", "midnight", "noon", "morning", "evening", "season", "year",
            "decade", "century", "millennium", "infinity", "eternity", "forever",
            "always", "never", "sometimes", "often", "rarely", "seldom", "once",
            "twice", "thrice", "many", "few", "some", "all", "none", "every",
            "each", "both", "either", "neither", "other", "another", "same", "different",
            "similar", "opposite", "parallel", "perpendicular", "tangent", "secant",
            "chord", "radius", "diameter", "circumference", "perimeter", "area", "volume",
            "surface", "plane", "sphere", "cube", "cone", "cylinder", "pyramid",
            "prism", "polyhedron", "polygon", "triangle", "square", "pentagon", "hexagon",
            "heptagon", "octagon", "nonagon", "decagon", "circle", "ellipse", "parabola",
            "hyperbola", "asymptote", "limit", "bound", "threshold", "horizon", "frontier",
            "boundary", "border", "edge",
        ],
    },
}

# Role rotation pattern (extracted from original)
ROLE_PATTERN = ["admin", "user", "moderator", "user"]

# Active pattern (extracted from original - positions that are false, 1-indexed)
# Looking at the data: 4, 7, 10, 14, 17, 20, 24, 27, 30...
# Pattern: every 3-4 positions, specifically at positions where (i % 10) in {4, 7, 0}
# Actually simpler: false at positions 4, 7, 10, 14, 17, 20, 24, 27, 30...
# That's: 4, 7, 10, then +4, +3, +3, +4, +3, +3...
# Let me just hardcode the logic from the original


def get_active(index):
    """Return active status for 1-indexed position."""
    # Based on original pattern analysis
    # False at: 4, 7, 10, 14, 17, 20, 24, 27, 30, 34, 37, 40...
    # Cycle of 10: false at positions 4, 7, 10 (mod 10 = 4, 7, 0)
    mod = index % 10
    return mod not in {4, 7, 0}


def get_role(index):
    """Return role for 1-indexed position."""
    return ROLE_PATTERN[(index - 1) % len(ROLE_PATTERN)]


def generate_user(index, variant_config):
    """Generate a single user entry."""
    firsts = variant_config["firsts"]
    lasts = variant_config["lasts"]
    domain = variant_config["domain"]

    first = firsts[(index - 1) % len(firsts)]
    last = lasts[(index - 1) % len(lasts)]

    name = f"{first}_{last}"
    email = f"{first}.{last}@{domain}"

    return {
        "id": index,
        "name": name,
        "email": email,
        "role": get_role(index),
        "active": get_active(index),
    }


def generate_dataset(count, variant_key):
    """Generate a dataset with the given count and variant."""
    config = VARIANTS[variant_key]
    users = [generate_user(i, config) for i in range(1, count + 1)]
    return {"users": users}


def main():
    base_path = Path(__file__).parent
    sizes = [10, 50, 100, 500]
    variant_keys = ["a", "b", "c", "d", "e"]

    for size in sizes:
        size_dir = base_path / str(size)
        size_dir.mkdir(exist_ok=True)

        for variant in variant_keys:
            dataset = generate_dataset(size, variant)
            output_path = size_dir / f"variant-{variant}.json"

            with open(output_path, "w") as f:
                json.dump(dataset, f, indent=2)
                f.write("\n")

            print(f"Generated {output_path}")

    print(f"\nGenerated {len(sizes) * len(variant_keys)} dataset variants.")


if __name__ == "__main__":
    main()
