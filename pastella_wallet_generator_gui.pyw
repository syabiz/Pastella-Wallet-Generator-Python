import os
import zlib
import time
import queue
import threading
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Dict, Any
from Crypto.Hash import keccak

# ============================================================
#  CONSTANTS & WORDLIST
# ============================================================
WORDLIST = [
    "abbey", "abducts", "ability", "ablaze", "abnormal", "abort", "abrasive", "absorb",
    "abyss", "academy", "aces", "aching", "acidic", "acoustic", "acquire", "across",
    "actress", "acumen", "adapt", "addicted", "adept", "adhesive", "adjust", "adopt",
    "adrenalin", "adult", "adventure", "aerial", "afar", "affair", "afield", "afloat",
    "afoot", "afraid", "after", "against", "agenda", "aggravate", "agile", "aglow",
    "agnostic", "agony", "agreed", "ahead", "aided", "ailments", "aimless", "airport",
    "aisle", "ajar", "akin", "alarms", "album", "alchemy", "alerts", "algebra",
    "alkaline", "alley", "almost", "aloof", "alpine", "already", "also", "altitude",
    "alumni", "always", "amaze", "ambush", "amended", "amidst", "ammo", "amnesty",
    "among", "amply", "amused", "anchor", "android", "anecdote", "angled", "ankle",
    "annoyed", "answers", "antics", "anvil", "anxiety", "anybody", "apart", "apex",
    "aphid", "aplomb", "apology", "apply", "apricot", "aptitude", "aquarium", "arbitrary",
    "archer", "ardent", "arena", "argue", "arises", "army", "around", "arrow",
    "arsenic", "artistic", "ascend", "ashtray", "aside", "asked", "asleep", "aspire",
    "assorted", "asylum", "athlete", "atlas", "atom", "atrium", "attire", "auburn",
    "auctions", "audio", "august", "aunt", "austere", "autumn", "avatar", "avidly",
    "avoid", "awakened", "awesome", "awful", "awkward", "awning", "awoken", "axes",
    "axis", "axle", "aztec", "azure", "baby", "bacon", "badge", "baffles",
    "bagpipe", "bailed", "bakery", "balding", "bamboo", "banjo", "baptism", "basin",
    "batch", "bawled", "bays", "because", "beer", "befit", "begun", "behind",
    "being", "below", "bemused", "benches", "berries", "bested", "betting", "bevel",
    "beware", "beyond", "bias", "bicycle", "bids", "bifocals", "biggest", "bikini",
    "bimonthly", "binocular", "biology", "biplane", "birth", "biscuit", "bite", "biweekly",
    "blender", "blip", "bluntly", "boat", "bobsled", "bodies", "bogeys", "boil",
    "boldly", "bomb", "border", "boss", "both", "bounced", "bovine", "bowling",
    "boxes", "boyfriend", "broken", "brunt", "bubble", "buckets", "budget", "buffet",
    "bugs", "building", "bulb", "bumper", "bunch", "business", "butter", "buying",
    "buzzer", "bygones", "byline", "bypass", "cabin", "cactus", "cadets", "cafe",
    "cage", "cajun", "cake", "calamity", "camp", "candy", "casket", "catch",
    "cause", "cavernous", "cease", "cedar", "ceiling", "cell", "cement", "cent",
    "certain", "chlorine", "chrome", "cider", "cigar", "cinema", "circle", "cistern",
    "citadel", "civilian", "claim", "click", "clue", "coal", "cobra", "cocoa",
    "code", "coexist", "coffee", "cogs", "cohesive", "coils", "colony", "comb",
    "cool", "copy", "corrode", "costume", "cottage", "cousin", "cowl", "criminal",
    "cube", "cucumber", "cuddled", "cuffs", "cuisine", "cunning", "cupcake", "custom",
    "cycling", "cylinder", "cynical", "dabbing", "dads", "daft", "dagger", "daily",
    "damp", "dangerous", "dapper", "darted", "dash", "dating", "dauntless", "dawn",
    "daytime", "dazed", "debut", "decay", "dedicated", "deepest", "deftly", "degrees",
    "dehydrate", "deity", "dejected", "delayed", "demonstrate", "dented", "deodorant", "depth",
    "desk", "devoid", "dewdrop", "dexterity", "dialect", "dice", "diet", "different",
    "digit", "dilute", "dime", "dinner", "diode", "diplomat", "directed", "distance",
    "ditch", "divers", "dizzy", "doctor", "dodge", "does", "dogs", "doing",
    "dolphin", "domestic", "donuts", "doorway", "dormant", "dosage", "dotted", "double",
    "dove", "down", "dozen", "dreams", "drinks", "drowning", "drunk", "drying",
    "dual", "dubbed", "duckling", "dude", "duets", "duke", "dullness", "dummy",
    "dunes", "duplex", "duration", "dusted", "duties", "dwarf", "dwelt", "dwindling",
    "dying", "dynamite", "dyslexic", "each", "eagle", "earth", "easy", "eating",
    "eavesdrop", "eccentric", "echo", "eclipse", "economics", "ecstatic", "eden", "edgy",
    "edited", "educated", "eels", "efficient", "eggs", "egotistic", "eight", "either",
    "eject", "elapse", "elbow", "eldest", "eleven", "elite", "elope", "else",
    "eluded", "emails", "ember", "emerge", "emit", "emotion", "empty", "emulate",
    "energy", "enforce", "enhanced", "enigma", "enjoy", "enlist", "enmity", "enough",
    "enraged", "ensign", "entrance", "envy", "epoxy", "equip", "erase", "erected",
    "erosion", "error", "eskimos", "espionage", "essential", "estate", "etched", "eternal",
    "ethics", "etiquette", "evaluate", "evenings", "evicted", "evolved", "examine", "excess",
    "exhale", "exit", "exotic", "exquisite", "extra", "exult", "fabrics", "factual",
    "fading", "fainted", "faked", "fall", "family", "fancy", "farming", "fatal",
    "faulty", "fawns", "faxed", "fazed", "feast", "february", "federal", "feel",
    "feline", "females", "fences", "ferry", "festival", "fetches", "fever", "fewest",
    "fiat", "fibula", "fictional", "fidget", "fierce", "fifteen", "fight", "films",
    "firm", "fishing", "fitting", "five", "fixate", "fizzle", "fleet", "flippant",
    "flying", "foamy", "focus", "foes", "foggy", "foiled", "folding", "fonts",
    "foolish", "fossil", "fountain", "fowls", "foxes", "foyer", "framed", "friendly",
    "frown", "fruit", "frying", "fudge", "fuel", "fugitive", "fully", "fuming",
    "fungal", "furnished", "fuselage", "future", "fuzzy", "gables", "gadget", "gags",
    "gained", "galaxy", "gambit", "gang", "gasp", "gather", "gauze", "gave",
    "gawk", "gaze", "gearbox", "gecko", "geek", "gels", "gemstone", "general",
    "geometry", "germs", "gesture", "getting", "geyser", "ghetto", "ghost", "giant",
    "giddy", "gifts", "gigantic", "gills", "gimmick", "ginger", "girth", "giving",
    "glass", "gleeful", "glide", "gnaw", "gnome", "goat", "goblet", "godfather",
    "goes", "goggles", "going", "goldfish", "gone", "goodbye", "gopher", "gorilla",
    "gossip", "gotten", "gourmet", "governing", "gown", "greater", "grunt", "guarded",
    "guest", "guide", "gulp", "gumball", "guru", "gusts", "gutter", "guys",
    "gymnast", "gypsy", "gyrate", "habitat", "hacksaw", "haggled", "hairy", "hamburger",
    "happens", "hashing", "hatchet", "haunted", "having", "hawk", "haystack", "hazard",
    "hectare", "hedgehog", "heels", "hefty", "height", "hemlock", "hence", "heron",
    "hesitate", "hexagon", "hickory", "hiding", "highway", "hijack", "hiker", "hills",
    "himself", "hinder", "hippo", "hire", "history", "hitched", "hive", "hoax",
    "hobby", "hockey", "hoisting", "hold", "honked", "hookup", "hope", "hornet",
    "hospital", "hotel", "hounded", "hover", "howls", "hubcaps", "huddle", "huge",
    "hull", "humid", "hunter", "hurried", "husband", "huts", "hybrid", "hydrogen",
    "hyper", "iceberg", "icing", "icon", "identity", "idiom", "idled", "idols",
    "igloo", "ignore", "iguana", "illness", "imagine", "imbalance", "imitate", "impel",
    "inactive", "inbound", "incur", "industrial", "inexact", "inflamed", "ingested", "initiate",
    "injury", "inkling", "inline", "inmate", "innocent", "inorganic", "input", "inquest",
    "inroads", "insult", "intended", "inundate", "invoke", "inwardly", "ionic", "irate",
    "iris", "irony", "irritate", "island", "isolated", "issued", "italics", "itches",
    "items", "itinerary", "itself", "ivory", "jabbed", "jackets", "jaded", "jagged",
    "jailed", "jamming", "january", "jargon", "jaunt", "javelin", "jaws", "jazz",
    "jeans", "jeers", "jellyfish", "jeopardy", "jerseys", "jester", "jetting", "jewels",
    "jigsaw", "jingle", "jittery", "jive", "jobs", "jockey", "jogger", "joining",
    "joking", "jolted", "jostle", "journal", "joyous", "jubilee", "judge", "juggled",
    "juicy", "jukebox", "july", "jump", "junk", "jury", "justice", "juvenile",
    "kangaroo", "karate", "keep", "kennel", "kept", "kernels", "kettle", "keyboard",
    "kickoff", "kidneys", "king", "kiosk", "kisses", "kitchens", "kiwi", "knapsack",
    "knee", "knife", "knowledge", "knuckle", "koala", "laboratory", "ladder", "lagoon",
    "lair", "lakes", "lamb", "language", "laptop", "large", "last", "later",
    "launching", "lava", "lawsuit", "layout", "lazy", "lectures", "ledge", "leech",
    "left", "legion", "leisure", "lemon", "lending", "leopard", "lesson", "lettuce",
    "lexicon", "liar", "library", "licks", "lids", "lied", "lifestyle", "light",
    "likewise", "lilac", "limits", "linen", "lion", "lipstick", "liquid", "listen",
    "lively", "loaded", "lobster", "locker", "lodge", "lofty", "logic", "loincloth",
    "long", "looking", "lopped", "lordship", "losing", "lottery", "loudly", "love",
    "lower", "loyal", "lucky", "luggage", "lukewarm", "lullaby", "lumber", "lunar",
    "lurk", "lush", "luxury", "lymph", "lynx", "lyrics", "macro", "madness",
    "magically", "mailed", "major", "makeup", "malady", "mammal", "maps", "masterful",
    "match", "maul", "maverick", "maximum", "mayor", "maze", "meant", "mechanic",
    "medicate", "meeting", "megabyte", "melting", "memoir", "menu", "merger", "mesh",
    "metro", "mews", "mice", "midst", "mighty", "mime", "mirror", "misery",
    "mittens", "mixture", "moat", "mobile", "mocked", "mohawk", "moisture", "molten",
    "moment", "money", "moon", "mops", "morsel", "mostly", "motherly", "mouth",
    "movement", "mowing", "much", "muddy", "muffin", "mugged", "mullet", "mumble",
    "mundane", "muppet", "mural", "musical", "muzzle", "myriad", "mystery", "myth",
    "nabbing", "nagged", "nail", "names", "nanny", "napkin", "narrate", "nasty",
    "natural", "nautical", "navy", "nearby", "necklace", "needed", "negative", "neither",
    "neon", "nephew", "nerves", "nestle", "network", "neutral", "never", "newt",
    "nexus", "nibs", "niche", "niece", "nifty", "nightly", "nimbly", "nineteen",
    "nirvana", "nitrogen", "nobody", "nocturnal", "nodes", "noises", "nomad", "noodles",
    "northern", "nostril", "noted", "nouns", "novelty", "nowhere", "nozzle", "nuance",
    "nucleus", "nudged", "nugget", "nuisance", "null", "number", "nuns", "nurse",
    "nutshell", "nylon", "oaks", "oars", "oasis", "oatmeal", "obedient", "object",
    "obliged", "obnoxious", "observant", "obtains", "obvious", "occur", "ocean", "october",
    "odds", "odometer", "offend", "often", "oilfield", "ointment", "okay", "older",
    "olive", "olympics", "omega", "omission", "omnibus", "onboard", "oncoming", "oneself",
    "ongoing", "onion", "online", "onslaught", "onto", "onward", "oozed", "opacity",
    "opened", "opposite", "optical", "opus", "orange", "orbit", "orchid", "orders",
    "organs", "origin", "ornament", "orphans", "oscar", "ostrich", "otherwise", "otter",
    "ouch", "ought", "ounce", "ourselves", "oust", "outbreak", "oval", "oven",
    "owed", "owls", "owner", "oxidant", "oxygen", "oyster", "ozone", "pact",
    "paddles", "pager", "pairing", "palace", "pamphlet", "pancakes", "paper", "paradise",
    "pastry", "patio", "pause", "pavements", "pawnshop", "payment", "peaches", "pebbles",
    "peculiar", "pedantic", "peeled", "pegs", "pelican", "pencil", "people", "pepper",
    "perfect", "pests", "petals", "phase", "pheasants", "phone", "phrases", "physics",
    "piano", "picked", "pierce", "pigment", "piloted", "pimple", "pinched", "pioneer",
    "pipeline", "pirate", "pistons", "pitched", "pivot", "pixels", "pizza", "playful",
    "pledge", "pliers", "plotting", "plus", "plywood", "poaching", "pockets", "podcast",
    "poetry", "point", "poker", "polar", "ponies", "pool", "popular", "portents",
    "possible", "potato", "pouch", "poverty", "powder", "pram", "present", "pride",
    "problems", "pruned", "prying", "psychic", "public", "puck", "puddle", "puffin",
    "pulp", "pumpkins", "punch", "puppy", "purged", "push", "putty", "puzzled",
    "pylons", "pyramid", "python", "queen", "quick", "quote", "rabbits", "racetrack",
    "radar", "rafts", "rage", "railway", "raking", "rally", "ramped", "randomly",
    "rapid", "rarest", "rash", "rated", "ravine", "rays", "razor", "react",
    "rebel", "recipe", "reduce", "reef", "refer", "regular", "reheat", "reinvest",
    "rejoices", "rekindle", "relic", "remedy", "renting", "reorder", "repent", "request",
    "reruns", "rest", "return", "reunion", "revamp", "rewind", "rhino", "rhythm",
    "ribbon", "richly", "ridges", "rift", "rigid", "rims", "ringing", "riots",
    "ripped", "rising", "ritual", "river", "roared", "robot", "rockets", "rodent",
    "rogue", "roles", "romance", "roomy", "roped", "roster", "rotate", "rounded",
    "rover", "rowboat", "royal", "ruby", "rudely", "ruffled", "rugged", "ruined",
    "ruling", "rumble", "runway", "rural", "rustled", "ruthless", "sabotage", "sack",
    "sadness", "safety", "saga", "sailor", "sake", "salads", "sample", "sanity",
    "sapling", "sarcasm", "sash", "satin", "saucepan", "saved", "sawmill", "saxophone",
    "sayings", "scamper", "scenic", "school", "science", "scoop", "scrub", "scuba",
    "seasons", "second", "sedan", "seeded", "segments", "seismic", "selfish", "semifinal",
    "sensible", "september", "sequence", "serving", "session", "setup", "seventh", "sewage",
    "shackles", "shelter", "shipped", "shocking", "shrugged", "shuffled", "shyness", "siblings",
    "sickness", "sidekick", "sieve", "sifting", "sighting", "silk", "simplest", "sincerely",
    "sipped", "siren", "situated", "sixteen", "sizes", "skater", "skew", "skirting",
    "skulls", "skydive", "slackens", "sleepless", "slid", "slower", "slug", "smash",
    "smelting", "smidgen", "smog", "smuggled", "snake", "sneeze", "sniff", "snout",
    "snug", "soapy", "sober", "soccer", "soda", "software", "soggy", "soil",
    "solved", "somewhere", "sonic", "soothe", "soprano", "sorry", "southern", "sovereign",
    "sowed", "soya", "space", "speedy", "sphere", "spiders", "splendid", "spout",
    "sprig", "spud", "spying", "square", "stacking", "stellar", "stick", "stockpile",
    "strained", "stunning", "stylishly", "subtly", "succeed", "suddenly", "suede", "suffice",
    "sugar", "suitcase", "sulking", "summon", "sunken", "superior", "surfer", "sushi",
    "suture", "swagger", "swept", "swiftly", "sWord", "swung", "syllabus", "symptoms",
    "syndrome", "syringe", "system", "taboo", "tacit", "tadpoles", "tagged", "tail",
    "taken", "talent", "tamper", "tanks", "tapestry", "tarnished", "tasked", "tattoo",
    "taunts", "tavern", "tawny", "taxi", "teardrop", "technical", "tedious", "teeming",
    "tell", "template", "tender", "tepid", "tequila", "terminal", "testing", "tether",
    "textbook", "thaw", "theatrics", "thirsty", "thorn", "threaten", "thumbs", "thwart",
    "ticket", "tidy", "tiers", "tiger", "tilt", "timber", "tinted", "tipsy",
    "tirade", "tissue", "titans", "toaster", "tobacco", "today", "toenail", "toffee",
    "together", "toilet", "token", "tolerant", "tomorrow", "tonic", "toolbox", "topic",
    "torch", "tossed", "total", "touchy", "towel", "toxic", "toyed", "trash",
    "trendy", "tribal", "trolling", "truth", "trying", "tsunami", "tubes", "tucks",
    "tudor", "tuesday", "tufts", "tugs", "tuition", "tulips", "tumbling", "tunnel",
    "turnip", "tusks", "tutor", "tuxedo", "twang", "tweezers", "twice", "twofold",
    "tycoon", "typist", "tyrant", "ugly", "ulcers", "ultimate", "umbrella", "umpire",
    "unafraid", "unbending", "uncle", "under", "uneven", "unfit", "ungainly", "unhappy",
    "union", "unjustly", "unknown", "unlikely", "unmask", "unnoticed", "unopened", "unplugs",
    "unquoted", "unrest", "unsafe", "until", "unusual", "unveil", "unwind", "unzip",
    "upbeat", "upcoming", "update", "upgrade", "uphill", "upkeep", "upload", "upon",
    "upper", "upright", "upstairs", "uptight", "upwards", "urban", "urchins", "urgent",
    "usage", "useful", "usher", "using", "usual", "utensils", "utility", "utmost",
    "utopia", "uttered", "vacation", "vague", "vain", "value", "vampire", "vane",
    "vapidly", "vary", "vastness", "vats", "vaults", "vector", "veered", "vegan",
    "vehicle", "vein", "velvet", "venomous", "verification", "vessel", "veteran", "vexed",
    "vials", "vibrate", "victim", "video", "viewpoint", "vigilant", "viking", "village",
    "vinegar", "violin", "vipers", "virtual", "visited", "vitals", "vivid", "vixen",
    "vocal", "vogue", "voice", "volcano", "vortex", "voted", "voucher", "vowels",
    "voyage", "vulture", "wade", "waffle", "wagtail", "waist", "waking", "wallets",
    "wanted", "warped", "washing", "water", "waveform", "waxing", "wayside", "weavers",
    "website", "wedge", "weekday", "weird", "welders", "went", "wept", "were",
    "western", "wetsuit", "whale", "when", "whipped", "whole", "wickets", "width",
    "wield", "wife", "wiggle", "wildly", "winter", "wipeout", "wiring", "wise",
    "withdrawn", "wives", "wizard", "wobbly", "woes", "woken", "wolf", "womanly",
    "wonders", "woozy", "worry", "wounded", "woven", "wrap", "wrist", "wrong",
    "yacht", "yahoo", "yanks", "yard", "yawning", "yearbook", "yellow", "yesterday",
    "yeti", "yields", "yodel", "yoga", "younger", "yoyo", "zapped", "zeal",
    "zebra", "zero", "zesty", "zigzags", "zinger", "zippers", "zodiac", "zombie",
    "zones", "zoom"
]
N = len(WORDLIST)

PAS_PREFIX_BYTES = bytes([0x84, 0x80, 0x66])
B58_CHARS = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
CN_BLOCK_SIZES = [0, 2, 3, 5, 6, 7, 9, 10, 11]

P = 2**255 - 19
L = 7237005577332262213973186563042994240857116359379907606001950938285454250989
D = (-121665) * pow(121666, -1, P) % P
GY = 4 * pow(5, -1, P) % P

# ============================================================
#  CRYPTO FUNCTIONS
# ============================================================
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    g, y, x = egcd(b % a, a)
    return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Inverse does not exist")
    return x % m

def recover_x(y, sign):
    x2 = (y*y - 1) * modinv(D * y*y + 1, P) % P
    if x2 == 0:
        return 0 if sign == 0 else None
    x = pow(x2, (P + 3) // 8, P)
    if (x*x - x2) % P != 0:
        x = x * pow(2, (P - 1) // 4, P) % P
    if (x*x - x2) % P != 0:
        return None
    if (x & 1) != sign:
        x = P - x
    return x

GX = recover_x(GY, 0)
G = (GX, GY, 1, GX * GY % P)

def point_add(P1, P2):
    A = (P1[1] - P1[0]) * (P2[1] - P2[0]) % P
    B = (P1[1] + P1[0]) * (P2[1] + P2[0]) % P
    C = 2 * P1[3] * P2[3] * D % P
    D_ = 2 * P1[2] * P2[2] % P
    E = (B - A) % P
    F = (D_ - C) % P
    G_ = (D_ + C) % P
    H = (B + A) % P
    return (E * F % P, H * G_ % P, F * G_ % P, E * H % P)

def point_mul(scalar, Pt):
    Q = (0, 1, 1, 0)
    scalar = scalar % L
    while scalar > 0:
        if scalar & 1:
            Q = point_add(Q, Pt)
        Pt = point_add(Pt, Pt)
        scalar >>= 1
    return Q

def point_compress(pt):
    zinv = modinv(pt[2], P)
    x = pt[0] * zinv % P
    y = pt[1] * zinv % P
    tmp = y | ((x & 1) << 255)
    return tmp.to_bytes(32, 'little')

def ed25519_scalar_to_public(seed32):
    s = int.from_bytes(seed32, 'little') % L
    pub_point = point_mul(s, G)
    return point_compress(pub_point)

def random_scalar():
    raw = os.urandom(64)
    s = int.from_bytes(raw, 'little') % L
    return s.to_bytes(32, 'little')

def cn_base58_encode(data):
    def encode_block(block):
        num = int.from_bytes(block, 'big')
        out_len = CN_BLOCK_SIZES[len(block)]
        res = ""
        for _ in range(out_len):
            num, idx = divmod(num, 58)
            res = B58_CHARS[idx] + res
        return res
    full_blocks = len(data) // 8
    last_bytes = len(data) % 8
    result = ""
    for i in range(full_blocks):
        result += encode_block(data[i*8:(i+1)*8])
    if last_bytes > 0:
        result += encode_block(data[full_blocks*8:])
    return result

def keccak256_bytes(data):
    k = keccak.new(digest_bits=256)
    k.update(data)
    return k.digest()

def derive_address(pubkey32):
    payload = PAS_PREFIX_BYTES + pubkey32
    checksum = keccak256_bytes(payload)[:4]
    final_data = payload + checksum
    return cn_base58_encode(final_data)

def seed_to_words24(seed):
    words = []
    for i in range(0, 32, 4):
        x = int.from_bytes(seed[i:i+4], 'little')
        w1 = x % N
        w2 = (x // N + w1) % N
        w3 = (x // N // N + w2) % N
        words.extend([WORDLIST[w1], WORDLIST[w2], WORDLIST[w3]])
    return words

def words24_to_seed(words24):
    seed = bytearray(32)
    for i in range(8):
        i1 = WORDLIST.index(words24[i*3])
        i2 = WORDLIST.index(words24[i*3+1])
        i3 = WORDLIST.index(words24[i*3+2])
        val = (i1 + N * ((i2 - i1 + N) % N) + N * N * ((i3 - i2 + N) % N)) & 0xFFFFFFFF
        seed[i*4:i*4+4] = val.to_bytes(4, 'little')
    return bytes(seed)

def checksum_word(words24):
    prefix = ''.join(w[:3] for w in words24).encode()
    crc = zlib.crc32(prefix) & 0xFFFFFFFF
    return words24[crc % 24]

def seed_to_mnemonic(seed):
    w24 = seed_to_words24(seed)
    w25 = checksum_word(w24)
    return ' '.join(w24 + [w25])

def validate_mnemonic(mnemonic):
    words = mnemonic.strip().lower().split()
    if len(words) != 25:
        return {'ok': False, 'msg': f'Must be 25 words (found {len(words)})'}
    bad = [w for w in words if w not in WORDLIST]
    if bad:
        return {'ok': False, 'msg': f'Unknown words: {", ".join(bad[:5])}'}
    w24 = words[:24]
    given = words[24]
    expected = checksum_word(w24)
    if given != expected:
        return {'ok': False, 'msg': f'Invalid checksum! 25th word should be "{expected}"'}
    return {'ok': True, 'msg': 'OK', 'w24': w24}

# ============================================================
#  WALLET CLASS
# ============================================================
class Wallet:
    def __init__(self, seed32):
        self.seed32   = seed32
        self.seed_hex  = seed32.hex()
        self.pubkey    = ed25519_scalar_to_public(seed32)
        self.pubkey_hex = self.pubkey.hex()
        self.address   = derive_address(self.pubkey)
        self.mnemonic  = seed_to_mnemonic(seed32)

    @classmethod
    def generate(cls):
        return cls(random_scalar())

    @classmethod
    def from_mnemonic(cls, mnemonic):
        val = validate_mnemonic(mnemonic)
        if not val['ok']:
            raise ValueError(val['msg'])
        seed = words24_to_seed(val['w24'])
        return cls(seed)

# ============================================================
#  DESIGN TOKENS  (Pastella-inspired dark theme)
# ============================================================
BG          = "#0f0e11"
BG2         = "#17141d"
CARD        = "#1c1922"
CARD2       = "#231f2d"
BORDER      = "#2d2940"
ACCENT      = "#ff8afb"
ACCENT2     = "#c45fe8"
ACCENT_DIM  = "#7a3a8a"
FG          = "#f0edf8"
FG2         = "#9b95b0"
FG3         = "#5c5672"
SUCCESS     = "#4ade80"
WARNING     = "#fbbf24"
ERROR       = "#f87171"
TERMINAL_BG = "#0a090d"
TERMINAL_FG = "#a8ffb0"

MONO   = ("Consolas", 9)
UI     = ("Segoe UI", 9)
UI_SB  = ("Segoe UI Semibold", 9)
UI_B   = ("Segoe UI Bold", 9)
UI_SM  = ("Segoe UI", 8)
TITLE  = ("Segoe UI Semibold", 11)
HEADER = ("Segoe UI Bold", 13)

# ============================================================
#  GUI APPLICATION
# ============================================================
class PastellaWalletApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pastella Wallet Generator")
        self.root.geometry("920x700")
        self.root.minsize(820, 600)
        self.root.resizable(True, True)
        self.root.configure(bg=BG)

        # Mining state
        self.mining_process  = None
        self.mining_thread   = None
        self.mining_queue    = queue.Queue()
        self.mining_running  = False

        # Vanity state
        self.vanity_running        = False
        self.vanity_start_time     = 0
        self.vanity_attempts       = 0
        self.vanity_max_attempts   = 0
        self.vanity_pattern        = ""
        self.vanity_case_sensitive = False
        self.vanity_position       = "start"
        self.vanity_stop_requested = False

        self._apply_ttk_styles()
        self._build_ui()

    # ──────────────────────────────────────────────────────────────
    #  TTK STYLE
    # ──────────────────────────────────────────────────────────────
    def _apply_ttk_styles(self):
        s = ttk.Style()
        s.theme_use('clam')
        s.configure('.',
            background=BG, foreground=FG, font=UI,
            fieldbackground=CARD2,
            selectbackground=ACCENT, selectforeground="#000",
            borderwidth=0, relief='flat')
        # Notebook
        s.configure('TNotebook', background=BG2, borderwidth=0, tabmargins=[0,0,0,0])
        s.configure('TNotebook.Tab', background=BG2, foreground=FG2,
                    padding=[20, 9], font=UI_SB, borderwidth=0)
        s.map('TNotebook.Tab',
              background=[('selected', CARD), ('active', CARD2)],
              foreground=[('selected', ACCENT), ('active', FG)])
        # Frames
        s.configure('TFrame', background=BG)
        # Labels
        s.configure('TLabel',        background=BG,   foreground=FG,   font=UI)
        s.configure('Dim.TLabel',    background=BG,   foreground=FG2,  font=UI)
        s.configure('Card.TLabel',   background=CARD, foreground=FG,   font=UI)
        s.configure('Card2.TLabel',  background=CARD2,foreground=FG,   font=UI)
        s.configure('CardDim.TLabel',background=CARD, foreground=FG2,  font=UI)
        s.configure('Success.TLabel',background=CARD, foreground=SUCCESS, font=UI_SB)
        # Progressbar
        s.configure('TProgressbar', background=ACCENT,
                    troughcolor=CARD2, borderwidth=0, thickness=5)
        # Scrollbar
        s.configure('TScrollbar', background=CARD2, troughcolor=BG2,
                    arrowcolor=FG3, borderwidth=0, arrowsize=12)
        s.map('TScrollbar', background=[('active', BORDER)])

    # ──────────────────────────────────────────────────────────────
    #  LAYOUT SCAFFOLDING
    # ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header
        hdr = tk.Frame(self.root, bg=BG2, height=54)
        hdr.pack(fill='x')
        hdr.pack_propagate(False)

        logo_f = tk.Frame(hdr, bg=BG2)
        logo_f.pack(side='left', padx=18, fill='y')

        # Dot
        c = tk.Canvas(logo_f, width=10, height=10, bg=BG2, highlightthickness=0)
        c.pack(side='left', anchor='center', padx=(0, 9))
        c.create_oval(0, 0, 10, 10, fill=ACCENT, outline='')

        tk.Label(logo_f, text="PASTELLA", bg=BG2, fg=FG,
                 font=("Segoe UI Bold", 14)).pack(side='left', anchor='center')
        tk.Label(logo_f, text=" WALLET", bg=BG2, fg=ACCENT,
                 font=("Segoe UI Bold", 14)).pack(side='left', anchor='center')

        tk.Label(hdr, text="by syabiz", bg=BG2, fg=FG3,
                 font=UI_SM).pack(side='right', padx=18, anchor='center')

        # Accent rule
        tk.Frame(self.root, bg=ACCENT, height=2).pack(fill='x')

        # Notebook
        self.nb = ttk.Notebook(self.root)
        self.nb.pack(fill='both', expand=True)

        self.tab_gen    = ttk.Frame(self.nb)
        self.tab_rec    = ttk.Frame(self.nb)
        self.tab_van    = ttk.Frame(self.nb)
        self.tab_mine   = ttk.Frame(self.nb)

        self.nb.add(self.tab_gen,  text="  ✦  Generate  ")
        self.nb.add(self.tab_rec,  text="  ↺  Recover   ")
        self.nb.add(self.tab_van,  text="  ◈  Vanity    ")
        self.nb.add(self.tab_mine, text="  ⛏  Mining    ")

        self._build_generate_tab()
        self._build_recover_tab()
        self._build_vanity_tab()
        self._build_mining_tab()

        # Status bar
        sb = tk.Frame(self.root, bg=BG2, height=28)
        sb.pack(fill='x', side='bottom')
        sb.pack_propagate(False)

        self._sdot = tk.Canvas(sb, width=8, height=8, bg=BG2, highlightthickness=0)
        self._sdot.pack(side='left', padx=(14, 6), anchor='center')
        self._sdot.create_oval(0, 0, 8, 8, fill=SUCCESS, outline='', tags='dot')

        self._svar = tk.StringVar(value="Ready")
        tk.Label(sb, textvariable=self._svar, bg=BG2, fg=FG2,
                 font=UI_SM).pack(side='left', anchor='center')

        tk.Label(sb, text="Pastella Network  •  Ed25519  •  CryptoNote Base58",
                 bg=BG2, fg=FG3, font=UI_SM).pack(side='right', padx=14)

    def _status(self, msg, kind='ok'):
        clr = {'ok': SUCCESS, 'warn': WARNING, 'error': ERROR}.get(kind, SUCCESS)
        self._svar.set(msg)
        self._sdot.itemconfig('dot', fill=clr)

    # ──────────────────────────────────────────────────────────────
    #  SHARED WIDGET HELPERS
    # ──────────────────────────────────────────────────────────────
    def _tab_header(self, parent, title, subtitle=''):
        f = tk.Frame(parent, bg=BG2)
        f.pack(fill='x')
        inner = tk.Frame(f, bg=BG2)
        inner.pack(fill='x', padx=16, pady=12)
        tk.Label(inner, text=title, bg=BG2, fg=FG, font=HEADER).pack(side='left', anchor='w')
        if subtitle:
            tk.Label(inner, text=f"   {subtitle}", bg=BG2, fg=FG3, font=UI_SM).pack(
                side='left', anchor='center', pady=2)
        tk.Frame(parent, bg=BORDER, height=1).pack(fill='x')

    def _accent_btn(self, parent, text, cmd, side='left', padx=0, pady=0):
        btn = tk.Button(parent, text=text,
                        bg=ACCENT, fg="#0b0b0f",
                        font=("Segoe UI Bold", 10),
                        relief='flat', bd=0, padx=4, pady=8,
                        activebackground=ACCENT2, activeforeground="#fff",
                        cursor='hand2', command=cmd)
        btn.pack(side=side, padx=padx, pady=pady)
        return btn

    def _danger_btn(self, parent, text, cmd, side='left', padx=0):
        btn = tk.Button(parent, text=text,
                        bg="#3d1a1a", fg=ERROR,
                        font=("Segoe UI Bold", 10),
                        relief='flat', bd=0, padx=4, pady=8,
                        activebackground="#5a2222", activeforeground=ERROR,
                        cursor='hand2', state='disabled', command=cmd)
        btn.pack(side=side, padx=padx)
        return btn

    def _ghost_btn(self, parent, text, cmd, side='left', padx=0):
        btn = tk.Button(parent, text=text,
                        bg=CARD2, fg=FG2, font=UI,
                        relief='flat', bd=0, padx=10, pady=8,
                        activebackground=BORDER, activeforeground=FG,
                        cursor='hand2', command=cmd)
        btn.pack(side=side, padx=padx)
        return btn

    def _styled_entry(self, parent, default='', width=None, mono=False):
        """Return (frame, entry) for a styled bordered entry."""
        outer = tk.Frame(parent, bg=BORDER)
        inner = tk.Frame(outer, bg=CARD2)
        inner.pack(fill='both', padx=1, pady=1)
        kw = dict(bg=CARD2, fg=FG, font=MONO if mono else UI,
                  insertbackground=ACCENT, relief='flat',
                  bd=0, highlightthickness=0)
        if width:
            kw['width'] = width
        e = tk.Entry(inner, **kw)
        e.insert(0, default)
        e.pack(fill='x', padx=8, pady=7)
        return outer, e

    def _readonly_field(self, parent, label, value, row, height=2, mono=True):
        """Full-width label + bordered readonly text + copy button row."""
        tk.Label(parent, text=label, bg=CARD, fg=FG2,
                 font=UI_SB).grid(row=row*2, column=0, columnspan=2,
                                   sticky='w', padx=14, pady=(10, 2))
        outer = tk.Frame(parent, bg=BORDER)
        outer.grid(row=row*2+1, column=0, columnspan=2,
                   sticky='ew', padx=14, pady=(0, 4))
        inner = tk.Frame(outer, bg=CARD2)
        inner.pack(fill='both', padx=1, pady=1)
        t = tk.Text(inner, height=height, wrap='word',
                    font=MONO if mono else UI,
                    bg=CARD2, fg=FG, insertbackground=ACCENT,
                    relief='flat', padx=10, pady=8, bd=0,
                    selectbackground=ACCENT2, selectforeground="#000")
        t.insert('1.0', value)
        t.config(state='disabled')
        t.pack(side='left', fill='both', expand=True)
        cp = tk.Button(inner, text="⎘",
                       bg=CARD2, fg=FG3, font=("Segoe UI", 12),
                       relief='flat', bd=0, padx=10, pady=4,
                       activebackground=CARD2, activeforeground=ACCENT,
                       cursor='hand2',
                       command=lambda v=value: self.copy_to_clip(v))
        cp.pack(side='right', fill='y')
        parent.columnconfigure(0, weight=1)
        return t

    def _card_frame(self, parent, padx=12, pady=6):
        outer = tk.Frame(parent, bg=BORDER)
        outer.pack(fill='x', padx=padx, pady=pady)
        inner = tk.Frame(outer, bg=CARD)
        inner.pack(fill='both', padx=1, pady=1, ipadx=2, ipady=2)
        return inner

    def copy_to_clip(self, text):
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self._status("Copied to clipboard ✓", 'ok')

    # ──────────────────────────────────────────────────────────────
    #  GENERATE TAB
    # ──────────────────────────────────────────────────────────────
    def _build_generate_tab(self):
        tab = self.tab_gen

        top = tk.Frame(tab, bg=BG2)
        top.pack(fill='x')
        inner_top = tk.Frame(top, bg=BG2)
        inner_top.pack(fill='x', padx=16, pady=12)
        tk.Label(inner_top, text="Generate a new wallet",
                 bg=BG2, fg=FG, font=HEADER).pack(side='left')
        self.gen_btn = self._accent_btn(inner_top,
                                        "  ✦  Generate New Wallet  ",
                                        self.generate_wallet, side='right')
        tk.Frame(tab, bg=BORDER, height=1).pack(fill='x')

        # Scrollable result area
        canvas = tk.Canvas(tab, bg=BG, highlightthickness=0, bd=0)
        vsb = ttk.Scrollbar(tab, orient='vertical', command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)
        vsb.pack(side='right', fill='y')
        canvas.pack(side='left', fill='both', expand=True)

        self._gen_frame = tk.Frame(canvas, bg=BG)
        win_id = canvas.create_window((0, 0), window=self._gen_frame, anchor='nw')

        self._gen_frame.bind('<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',
            lambda e: canvas.itemconfig(win_id, width=e.width))

        # Placeholder
        ph = tk.Frame(self._gen_frame, bg=BG)
        ph.pack(pady=70)
        tk.Label(ph, text="✦", bg=BG, fg=ACCENT_DIM, font=("Segoe UI", 40)).pack()
        tk.Label(ph, text='Click "Generate New Wallet" to create a new wallet',
                 bg=BG, fg=FG3, font=UI).pack(pady=6)

    def generate_wallet(self):
        try:
            wallet = Wallet.generate()
            self._show_generate_result(wallet)
            self._status("New wallet generated successfully ✓", 'ok')
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate wallet: {e}")
            self._status("Generation failed", 'error')

    def _show_generate_result(self, wallet: Wallet):
        for w in self._gen_frame.winfo_children():
            w.destroy()

        # ── Mnemonic grid ──────────────────────────────────────── #
        hdr_f = tk.Frame(self._gen_frame, bg=BG)
        hdr_f.pack(fill='x', padx=14, pady=(14, 6))
        tk.Label(hdr_f, text="Mnemonic Seed", bg=BG, fg=FG, font=TITLE).pack(side='left')
        tk.Label(hdr_f, text="  25 words  •  store safely, never share",
                 bg=BG, fg=FG3, font=UI_SM).pack(side='left', anchor='center', pady=2)

        grid_outer = tk.Frame(self._gen_frame, bg=BORDER)
        grid_outer.pack(fill='x', padx=14, pady=(0, 4))
        grid_card = tk.Frame(grid_outer, bg=CARD)
        grid_card.pack(fill='x', padx=1, pady=1, ipadx=10, ipady=10)

        words = wallet.mnemonic.split()
        for i, word in enumerate(words):
            ck = (i == 24)
            cbg = ACCENT if ck else CARD2
            cfg_txt = "#0b0b0f" if ck else FG
            num_fg  = "#0b0b0f" if ck else FG3
            cell = tk.Frame(grid_card, bg=cbg)
            cell.grid(row=i//5, column=i%5, sticky='ew', padx=3, pady=3)
            tk.Label(cell, text=f"{i+1}", bg=cbg, fg=num_fg,
                     font=("Consolas", 7), width=3, anchor='e').pack(
                side='left', padx=(5,2))
            tk.Label(cell, text=word, bg=cbg, fg=cfg_txt,
                     font=("Consolas", 9, 'bold'), anchor='w').pack(
                side='left', padx=(0,8), pady=6)

        for col in range(5):
            grid_card.columnconfigure(col, weight=1)

        # Copy mnemonic button
        cm_f = tk.Frame(self._gen_frame, bg=BG)
        cm_f.pack(fill='x', padx=14, pady=(4, 2))
        self._ghost_btn(cm_f, "⎘  Copy all 25 words",
                        lambda: self.copy_to_clip(wallet.mnemonic),
                        side='right')

        tk.Frame(self._gen_frame, bg=BORDER, height=1).pack(fill='x', padx=14, pady=6)

        # ── Key/address fields ─────────────────────────────────── #
        fc = tk.Frame(self._gen_frame, bg=CARD)
        fc.pack(fill='x', padx=14, pady=(0, 16))

        self._readonly_field(fc, "Wallet Address",       wallet.address,   0, height=2)
        self._readonly_field(fc, "Private Key (Seed Hex)", wallet.seed_hex, 1, height=2)
        self._readonly_field(fc, "Public Key",           wallet.pubkey_hex, 2, height=2)
        self._readonly_field(fc, "Mnemonic (full text)", wallet.mnemonic,   3, height=3)

        tk.Frame(self._gen_frame, bg=BG, height=16).pack()

    # ──────────────────────────────────────────────────────────────
    #  RECOVER TAB
    # ──────────────────────────────────────────────────────────────
    def _build_recover_tab(self):
        tab = self.tab_rec
        self._tab_header(tab, "Recover wallet from mnemonic")

        # Input card
        ic = self._card_frame(tab, pady=(12, 6))
        tk.Label(ic, text="Enter your 25-word mnemonic seed phrase:",
                 bg=CARD, fg=FG2, font=UI_SB).pack(anchor='w', padx=14, pady=(10, 4))

        ent_outer = tk.Frame(ic, bg=BORDER)
        ent_outer.pack(fill='x', padx=14, pady=(0, 6))
        ent_inner = tk.Frame(ent_outer, bg=CARD2)
        ent_inner.pack(fill='x', padx=1, pady=1)
        self.recover_entry = tk.Text(ent_inner, height=4, wrap='word',
                                     font=MONO, bg=CARD2, fg=FG,
                                     insertbackground=ACCENT,
                                     relief='flat', padx=10, pady=8, bd=0,
                                     selectbackground=ACCENT2, selectforeground="#000")
        self.recover_entry.pack(fill='x')

        tk.Label(ic, text="Separate words with spaces. Word 25 is the checksum.",
                 bg=CARD, fg=FG3, font=UI_SM).pack(anchor='w', padx=14, pady=(0, 8))

        btn_f = tk.Frame(ic, bg=CARD)
        btn_f.pack(fill='x', padx=14, pady=(0, 10))
        self._accent_btn(btn_f, "  ↺  Recover Wallet  ", self.recover_wallet)
        self._ghost_btn(btn_f, "Clear",
                        lambda: self.recover_entry.delete('1.0', 'end'), padx=8)

        tk.Frame(tab, bg=BORDER, height=1).pack(fill='x', padx=14, pady=(4, 0))

        self._rec_result = tk.Frame(tab, bg=BG)
        self._rec_result.pack(fill='both', expand=True)

    def recover_wallet(self):
        mnemonic = self.recover_entry.get('1.0', 'end-1c').strip()
        if not mnemonic:
            messagebox.showwarning("Empty", "Please enter a mnemonic")
            return
        try:
            wallet = Wallet.from_mnemonic(mnemonic)
            self._show_recover_result(wallet)
            self._status("Wallet recovered successfully ✓", 'ok')
        except ValueError as e:
            messagebox.showerror("Invalid Mnemonic", str(e))
            self._status("Recovery failed — invalid mnemonic", 'error')
        except Exception as e:
            messagebox.showerror("Error", f"Recovery failed: {e}")
            self._status("Recovery failed", 'error')

    def _show_recover_result(self, wallet: Wallet):
        for w in self._rec_result.winfo_children():
            w.destroy()

        banner = tk.Frame(self._rec_result, bg="#0d2e1a")
        banner.pack(fill='x', padx=14, pady=(10, 4))
        tk.Label(banner, text="  ✅  Checksum valid — 25 words accepted",
                 bg="#0d2e1a", fg=SUCCESS, font=UI_SB,
                 pady=9).pack(anchor='w', padx=10)

        fc = tk.Frame(self._rec_result, bg=CARD)
        fc.pack(fill='x', padx=14, pady=(0, 12))
        self._readonly_field(fc, "Wallet Address",         wallet.address,    0, height=2)
        self._readonly_field(fc, "Private Key (Seed Hex)", wallet.seed_hex,   1, height=2)
        self._readonly_field(fc, "Public Key",             wallet.pubkey_hex, 2, height=2)

    # ──────────────────────────────────────────────────────────────
    #  VANITY TAB
    # ──────────────────────────────────────────────────────────────
    def _build_vanity_tab(self):
        tab = self.tab_van
        self._tab_header(tab, "Vanity address search",
                         "Generate a wallet with a custom address pattern")

        # Config card
        cc = self._card_frame(tab, pady=(12, 4))

        def row_lbl(text, r):
            tk.Label(cc, text=text, bg=CARD, fg=FG2, font=UI_SB).grid(
                row=r, column=0, sticky='e', padx=(14, 10), pady=6)

        def row_entry(r, default='', width=None):
            outer = tk.Frame(cc, bg=BORDER)
            outer.grid(row=r, column=1, sticky='ew', padx=(0, 14), pady=6)
            inner = tk.Frame(outer, bg=CARD2)
            inner.pack(fill='both', padx=1, pady=1)
            kw = dict(bg=CARD2, fg=FG, font=MONO, insertbackground=ACCENT,
                      relief='flat', bd=0, highlightthickness=0)
            if width:
                kw['width'] = width
            e = tk.Entry(inner, **kw)
            e.insert(0, default)
            e.pack(fill='x', padx=8, pady=7)
            return e

        row_lbl("Pattern (base58, no 'PAS'):", 0)
        self.vanity_pattern_entry = row_entry(0, width=28)

        row_lbl("Max trials:", 1)
        self.vanity_max = row_entry(1, "100000", width=14)

        row_lbl("Case sensitive:", 2)
        self.vanity_case = tk.BooleanVar(value=False)
        cs = tk.Frame(cc, bg=CARD)
        cs.grid(row=2, column=1, sticky='w', padx=(0,14), pady=6)
        tk.Checkbutton(cs, variable=self.vanity_case, text="Yes",
                       bg=CARD, fg=FG, activebackground=CARD,
                       selectcolor=CARD2, font=UI).pack(side='left')

        row_lbl("Position:", 3)
        self.vanity_pos = tk.StringVar(value="start")
        pos = tk.Frame(cc, bg=CARD)
        pos.grid(row=3, column=1, sticky='w', padx=(0,14), pady=6)
        for val, lbl in [("start", "Start (after PAS)"), ("anywhere", "Anywhere")]:
            tk.Radiobutton(pos, text=lbl, variable=self.vanity_pos, value=val,
                           bg=CARD, fg=FG, activebackground=CARD,
                           selectcolor=CARD2, font=UI).pack(side='left', padx=(0, 14))

        cc.columnconfigure(1, weight=1)

        # Buttons
        bf = tk.Frame(tab, bg=BG)
        bf.pack(fill='x', padx=14, pady=(6, 8))
        self.vanity_start_btn = self._accent_btn(bf, "  ◈  Start Search  ", self.start_vanity)
        self.vanity_stop_btn  = self._danger_btn(bf, "  ◼  Stop  ", self.stop_vanity, padx=8)

        # Progress
        self._van_prog_frame = tk.Frame(tab, bg=BG)
        self._van_prog_frame.pack(fill='x', padx=14, pady=(0, 6))

        prog_outer = tk.Frame(self._van_prog_frame, bg=BORDER)
        prog_outer.pack(fill='x')
        prog_card  = tk.Frame(prog_outer, bg=CARD)
        prog_card.pack(fill='x', padx=1, pady=1, ipadx=14, ipady=12)

        stats = tk.Frame(prog_card, bg=CARD)
        stats.pack(fill='x', pady=(0, 8))
        for label, attr in [("ATTEMPTS", "vanity_attempts_label"),
                             ("SPEED (w/s)", "vanity_speed_label"),
                             ("ELAPSED", "vanity_elapsed_label")]:
            cell = tk.Frame(stats, bg=CARD2)
            cell.pack(side='left', padx=(0, 8))
            tk.Label(cell, text=label, bg=CARD2, fg=FG3, font=UI_SM,
                     padx=12, pady=4).pack(anchor='w')
            v = tk.Label(cell, text="0", bg=CARD2, fg=ACCENT,
                         font=("Consolas", 12, 'bold'), padx=12, pady=4)
            v.pack(anchor='w')
            setattr(self, attr, v)

        self.vanity_progress = ttk.Progressbar(prog_card, orient='horizontal',
                                               mode='determinate')
        self.vanity_progress.pack(fill='x', pady=(0, 6))
        self.vanity_current = tk.Label(prog_card, text="", bg=CARD, fg=FG3, font=("Consolas", 8))
        self.vanity_current.pack(anchor='w')

        self._van_prog_frame.pack_forget()

        # Result
        self._van_result = tk.Frame(tab, bg=BG)
        self._van_result.pack(fill='x', padx=14)

        tk.Frame(self._van_result, bg="#0d2e1a").pack(fill='x', pady=(0, 4))  # banner placeholder
        self._van_banner = tk.Label(self._van_result, text="  ✨  Match found!",
                                    bg="#0d2e1a", fg=SUCCESS, font=UI_SB, pady=9)
        # result fields
        rfc = tk.Frame(self._van_result, bg=CARD)
        rfc.pack(fill='x')

        def van_field(label, attr, row):
            tk.Label(rfc, text=label, bg=CARD, fg=FG2, font=UI_SB).grid(
                row=row*2, column=0, columnspan=2, sticky='w', padx=14, pady=(8, 2))
            outer = tk.Frame(rfc, bg=BORDER)
            outer.grid(row=row*2+1, column=0, columnspan=2,
                       sticky='ew', padx=14, pady=(0, 4))
            inner = tk.Frame(outer, bg=CARD2)
            inner.pack(fill='both', padx=1, pady=1)
            t = tk.Text(inner, height=2, wrap='word', font=MONO,
                        bg=CARD2, fg=FG, insertbackground=ACCENT,
                        relief='flat', padx=10, pady=8, bd=0)
            t.pack(side='left', fill='x', expand=True)
            tk.Button(inner, text="⎘",
                      bg=CARD2, fg=FG3, font=("Segoe UI", 12),
                      relief='flat', bd=0, padx=10, pady=4,
                      activebackground=CARD2, activeforeground=ACCENT,
                      cursor='hand2',
                      command=lambda tw=t: self.copy_to_clip(tw.get('1.0', 'end-1c'))
                      ).pack(side='right', fill='y')
            setattr(self, attr, t)
            rfc.columnconfigure(0, weight=1)

        van_field("Address",     "vanity_addr_text", 0)
        van_field("Mnemonic",    "vanity_mnem_text", 1)
        van_field("Private Key", "vanity_priv_text", 2)
        van_field("Public Key",  "vanity_pub_text",  3)

        self._van_result.pack_forget()

    def start_vanity(self):
        pattern = self.vanity_pattern_entry.get().strip()
        if not pattern:
            messagebox.showwarning("Empty pattern", "Please enter a pattern to search")
            return
        for ch in pattern:
            if ch not in B58_CHARS:
                messagebox.showerror("Invalid character",
                                     f"Character '{ch}' is not valid in base58")
                return
        try:
            max_att = int(self.vanity_max.get())
            if max_att <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid", "Max Trials must be a positive integer")
            return

        self.vanity_running        = True
        self.vanity_stop_requested = False
        self.vanity_start_time     = time.time()
        self.vanity_attempts       = 0
        self.vanity_max_attempts   = max_att
        self.vanity_pattern        = pattern
        self.vanity_case_sensitive = self.vanity_case.get()
        self.vanity_position       = self.vanity_pos.get()

        self.vanity_start_btn.config(state='disabled', bg=ACCENT_DIM)
        self.vanity_stop_btn.config(state='normal')
        self._van_prog_frame.pack(fill='x', padx=14, pady=(0, 6))
        self._van_result.pack_forget()
        self.vanity_progress['value'] = 0
        self.vanity_attempts_label.config(text="0")
        self.vanity_speed_label.config(text="0")
        self.vanity_elapsed_label.config(text="0s")
        self.vanity_current.config(text="Searching\u2026")
        self._status("Vanity search started\u2026", 'ok')

        self.root.after(100, self.vanity_search_batch)

    def stop_vanity(self):
        self.vanity_stop_requested = True
        self.vanity_running        = False
        self.vanity_start_btn.config(state='normal', bg=ACCENT)
        self.vanity_stop_btn.config(state='disabled')
        self._status("Vanity search stopped", 'warn')

    def vanity_search_batch(self):
        if not self.vanity_running or self.vanity_stop_requested:
            return

        for _ in range(10):
            if self.vanity_attempts >= self.vanity_max_attempts:
                self.stop_vanity()
                messagebox.showinfo("Finished",
                    f"Pattern not found in {self.vanity_max_attempts} attempts.")
                return
            if self.vanity_stop_requested:
                return

            self.vanity_attempts += 1
            try:
                seed = random_scalar()
                pub  = ed25519_scalar_to_public(seed)
                addr = derive_address(pub)
                after = addr[3:]
                hay = after if self.vanity_case_sensitive else after.lower()
                pat = self.vanity_pattern if self.vanity_case_sensitive else self.vanity_pattern.lower()

                if self.vanity_position == "start":
                    match = hay.startswith(pat)
                else:
                    match = pat in hay

                if match:
                    wallet = Wallet(seed)
                    for attr, val in [
                        ("vanity_addr_text", wallet.address),
                        ("vanity_mnem_text", wallet.mnemonic),
                        ("vanity_priv_text", wallet.seed_hex),
                        ("vanity_pub_text",  wallet.pubkey_hex),
                    ]:
                        t = getattr(self, attr)
                        t.config(state='normal')
                        t.delete('1.0', 'end')
                        t.insert('1.0', val)
                        t.config(state='disabled')

                    self._van_result.pack(fill='x', padx=14, pady=(0, 14))
                    self.stop_vanity()
                    self._status(f"\u2728 Match found after {self.vanity_attempts} attempts!", 'ok')
                    return
            except Exception as e:
                print(f"Vanity error: {e}")

        elapsed = time.time() - self.vanity_start_time
        speed   = int(self.vanity_attempts / elapsed) if elapsed > 0 else 0
        self.vanity_attempts_label.config(text=str(self.vanity_attempts))
        self.vanity_speed_label.config(text=str(speed))
        self.vanity_elapsed_label.config(text=f"{elapsed:.1f}s")
        self.vanity_progress['value'] = (self.vanity_attempts / self.vanity_max_attempts) * 100

        sample = random_scalar()
        self.vanity_current.config(
            text=f"Checking: {derive_address(ed25519_scalar_to_public(sample))}")

        if self.vanity_running and not self.vanity_stop_requested:
            self.root.after(10, self.vanity_search_batch)

    # ──────────────────────────────────────────────────────────────
    #  MINING TAB
    # ──────────────────────────────────────────────────────────────
    def _build_mining_tab(self):
        tab = self.tab_mine
        self._tab_header(tab, "XMRig Mining", "Mine PAS via the Pastella pool")

        # Config card
        cc = self._card_frame(tab, pady=(12, 4))

        def row_lbl(text, r):
            tk.Label(cc, text=text, bg=CARD, fg=FG2, font=UI_SB).grid(
                row=r, column=0, sticky='e', padx=(14, 10), pady=6)

        def row_entry(r, default='', width=None):
            outer = tk.Frame(cc, bg=BORDER)
            outer.grid(row=r, column=1, sticky='ew', padx=(0, 14), pady=6)
            inner = tk.Frame(outer, bg=CARD2)
            inner.pack(fill='both', padx=1, pady=1)
            kw = dict(bg=CARD2, fg=FG, font=MONO, insertbackground=ACCENT,
                      relief='flat', bd=0, highlightthickness=0)
            if width:
                kw['width'] = width
            e = tk.Entry(inner, **kw)
            e.insert(0, default)
            e.pack(fill='x', padx=8, pady=7)
            return e

        row_lbl("Pool URL:", 0);        self.pool_url    = row_entry(0, "pool.pastella.org")
        row_lbl("Port:", 1);            self.pool_port   = row_entry(1, "5555", width=10)
        row_lbl("Wallet Address:", 2);  self.wallet_addr = row_entry(2, "PAS1Dj6xgtVS56REDFbheSJe76ac44fq1dY4obnUgzSj2JGkVPGUDB")
        row_lbl("Worker Name:", 3);     self.worker_name = row_entry(3, "%COMPUTERNAME%", width=22)
        row_lbl("Threads:", 4);         self.threads     = row_entry(4, "2", width=6)
        cc.columnconfigure(1, weight=1)

        # Buttons
        bf = tk.Frame(tab, bg=BG)
        bf.pack(fill='x', padx=14, pady=(6, 8))
        self.mining_start_btn = self._accent_btn(bf, "  \u26cf  Start Mining  ", self.start_mining)
        self.mining_stop_btn  = self._danger_btn(bf, "  \u25fc  Stop Mining  ", self.stop_mining, padx=8)

        # Terminal output
        tl = tk.Frame(tab, bg=BG)
        tl.pack(fill='x', padx=14, pady=(0, 4))
        tk.Label(tl, text="Output", bg=BG, fg=FG2, font=UI_SB).pack(side='left')
        tk.Label(tl, text=" — xmrig stdout", bg=BG, fg=FG3, font=UI_SM).pack(side='left', pady=2)

        term_outer = tk.Frame(tab, bg=BORDER)
        term_outer.pack(fill='both', expand=True, padx=14, pady=(0, 12))
        term_inner = tk.Frame(term_outer, bg=TERMINAL_BG)
        term_inner.pack(fill='both', expand=True, padx=1, pady=1)

        self.mining_output = tk.Text(
            term_inner, font=("Consolas", 9),
            bg=TERMINAL_BG, fg=TERMINAL_FG,
            insertbackground=ACCENT, relief='flat',
            padx=12, pady=10, bd=0,
            selectbackground=ACCENT2, selectforeground="#000")
        msb = ttk.Scrollbar(term_inner, orient='vertical', command=self.mining_output.yview)
        self.mining_output.configure(yscrollcommand=msb.set)
        msb.pack(side='right', fill='y')
        self.mining_output.pack(side='left', fill='both', expand=True)

        self.check_mining_queue()

    def start_mining(self):
        pool   = self.pool_url.get().strip()
        port   = self.pool_port.get().strip()
        wallet = self.wallet_addr.get().strip()
        worker = self.worker_name.get().strip() or "%COMPUTERNAME%"
        thr    = self.threads.get().strip()

        if not pool or not port or not wallet:
            messagebox.showerror("Error", "Pool, port, and wallet must be filled")
            return

        base_dir   = os.path.dirname(os.path.abspath(__file__))
        xmrig_path = os.path.join(base_dir, "xmrig.exe")
        if not os.path.isfile(xmrig_path):
            messagebox.showerror("Error", "xmrig.exe not found in the same folder")
            return

        cmd = [xmrig_path, "-a", "rx/0", "-o", f"{pool}:{port}",
               "-u", wallet, "-p", worker, "-t", thr]
        try:
            self.mining_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                bufsize=1, universal_newlines=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            self.mining_running = True
            self.mining_start_btn.config(state='disabled', bg=ACCENT_DIM)
            self.mining_stop_btn.config(state='normal')
            self.mining_output.delete('1.0', 'end')
            self.mining_output.insert('end', "\u26cf Mining started\u2026\n")
            self._status("Mining started", 'ok')
            self.mining_thread = threading.Thread(target=self.read_mining_output, daemon=True)
            self.mining_thread.start()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start xmrig: {e}")
            self._status("Failed to start miner", 'error')

    def read_mining_output(self):
        while self.mining_running and self.mining_process:
            try:
                line = self.mining_process.stdout.readline()
                if line:
                    self.mining_queue.put(line)
                else:
                    break
            except Exception:
                break
        self.mining_queue.put(None)

    def stop_mining(self):
        if self.mining_process:
            self.mining_process.terminate()
            self.mining_process = None
        self.mining_running = False
        self.mining_start_btn.config(state='normal', bg=ACCENT)
        self.mining_stop_btn.config(state='disabled')
        self.mining_output.insert('end', "\n\u25fc Mining stopped.\n")
        self._status("Mining stopped", 'warn')

    def check_mining_queue(self):
        try:
            while True:
                line = self.mining_queue.get_nowait()
                if line is None:
                    if self.mining_running:
                        self.mining_output.insert('end', "\n\u25fc Mining process finished.\n")
                    break
                self.mining_output.insert('end', line)
                self.mining_output.see('end')
        except queue.Empty:
            pass
        finally:
            self.root.after(100, self.check_mining_queue)

# ============================================================
#  MAIN
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app  = PastellaWalletApp(root)
    root.mainloop()
