SYNONYMS = {
    # All the ways to say someone dropped/abandoned a subject
    "dropped": [
        "dropped", "quit", "left", "failed", "gave up", "gave in", "gave away", "stopped",
        "didn't take", "did not take", "didn't do", "did not do", "retook", "retake",
        "withdrawn", "withdrew", "withdrew from", "was withdrawn", "discontinued", "discontinued with",
        "stopped taking", "never took", "didn't finish", "did not finish", "wasn't entered for",
        "not entered for", "didn't sit", "did not sit", "removed", "removed from timetable",
        "excluded", "scrapped", "scrapped off", "resigned from", "didn't pass", "did not pass",
        "didn't complete", "did not complete", "unregistered", "opted out", "eliminated", "switched out",
        "was switched out", "cancelled", "dropped out", "let go", "lost", "missed", "abandoned",
        "didn't carry forward", "did not carry forward"
    ],

    # All the ways to say someone is interested in taking a subject
    "interest": [
        "interested in", "want to apply for", "want to apply to", "applying for", "applying to",
        "looking into", "looking at", "hoping to study", "hoping for", "considering", "planning to study",
        "thinking about", "thinking of", "wish to study", "aiming for", "want to pursue", "intend to study",
        "intent to study", "wish to apply for", "wish to apply to", "hope to do", "hoping for", "curious about",
        "planning on", "searching for", "looking for", "looking forward to", "would like to study",
        "studying", "study", "i want to study", "i hope to study", "i'm interested in", "keen on",
        "apply for", "apply to", "would love to study", "prefer to study", "desire to study"
    ],

    # All the ways to say someone did not drop anything, or none at all
    "none": [
        "nothing", "none", "n/a", "nil", "zero", "no subject", "no subjects",
        "not any", "not a single", "not one", "all", "didn't drop any", "did not drop any",
        "didn't drop anything", "did not drop anything",
        "haven't dropped any", "haven't dropped anything",
        "never dropped any", "never dropped anything",
        "didn't leave any", "did not leave any", "left none", "left nothing",
        "nope", "no course", "no courses", "no class", "no classes",
        "not applicable", "not relevant", "didn't quit any", "did not quit any",
        "didn't quit anything", "did not quit anything",
        "haven't quit any", "haven't quit anything",
        "never quit any", "never quit anything",
        "didn't fail any", "did not fail any", "didn't fail anything", "did not fail anything",
        "not dropped", "not left", "not failed", "not quit",
        "all kept", "kept all", "retained all", "none dropped"
    ],

    # Subject names and different ways these can be spelt
    "subjects": {
        # --- SCIENCE & MATHS ---
        "mathematics": [
            "math", "maths", "mathematics", "core maths", "pure maths",
            "stats", "statistics", "mechanics", "applied maths", "decision maths"
        ],
        "further mathematics": [
            "further mathematics", "further math", "further maths", "further-math", "f.maths", "f.math",
            "fmaths", "fmath", "furthermaths", "furthermath", "f maths", "f math", "fm"
        ],
        "biology": [
            "biology", "bio", "biological sciences"
        ],
        "chemistry": [
            "chemistry", "chem", "applied chemistry", "organic chemistry", "inorganic chemistry"
        ],
        "physics": [
            "physics", "phys", "applied physics", "astro physics", "astrophysics"
        ],
        "computer science": [
            "cs", "comp sci", "computing", "computer science", "information technology", "it", "ict", "informatics",
            "information systems", "ict", "information tech", "comp", "computers"
        ],

        # --- ENGLISH & HUMANITIES ---
        "english literature": [
            "english literature", "lit", "english lit", "literature", "literary studies", "eng lit"
        ],
        "english language": [
            "english language", "english lang", "eng lang", "lang", "language", "english studies"
        ],
        "history": [
            "history", "hist", "world history", "ancient history", "modern history"
        ],
        "geography": [
            "geography", "geo", "physical geography", "human geography", "geog"
        ],
        "philosophy": [
            "philosophy", "phil", "philosophy and ethics", "religious studies", "rs", "ethics"
        ],
        "classical civilisation": [
            "classical civilisation"
        ],

        # --- BUSINESS & ECON ---
        "business": [
            "business", "business studies", "biz", "bs", "business admin", "business administration", "commerce"
        ],
        "economics": [
            "economics", "econ", "microeconomics", "macroeconomics"
        ],
        "accounting": [
            "accounting", "accountancy", "finance", "financial studies"
        ],

        # --- SOCIAL SCIENCE / LAW ---
        "psychology": [
            "psychology", "psych", "applied psychology"
        ],
        "sociology": [
            "sociology", "socio", "social studies", "social science"
        ],
        "criminology": [
            "criminology", "crime", "crime science", "criminal justice", "criminal studies"
        ],
        "law": [
            "law", "legal studies", "criminal law", "public law", "constitutional law"
        ],
        "politics": [
            "politics", "government and politics", "govt and politics", "pol", "government",
            "international relations"
        ],
        "public services": [
            "public services", "public service", "uniformed services", "emergency services"
        ],

        # --- LANGUAGES ---
        "french": [
            "french", "francais", "fr"
        ],
        "spanish": [
            "spanish", "español", "espanol", "sp"
        ],
        "german": [
            "german", "deutsch", "de"
        ],
        "arabic": [
            "arabic", "ar"
        ],
        "urdu": [
            "urdu"
        ],
        "chinese": [
            "chinese", "mandarin", "zh"
        ],
        "italian": [
            "italian", "it"
        ],
        "latin": [
            "latin"
        ],
        "greek": [
            "greek"
        ],
        "russian": [
            "russian", "ru"
        ],
        "japanese": [
            "japanese", "jp"
        ],
        "portuguese": [
            "portuguese", "pt"
        ],
        "hindi": [
            "hindi"
        ],
        "persian": [
            "persian"
        ],
        "bengali": [
            "bengali", "bangla"
        ],
        "turkish": [
            "turkish", "turkce", "turkiye"
        ],
        "punjabi": [
            "punjabi"
        ],
        "polish": [
            "polish", "polski"
        ],
        "welsh": [
            "welsh", "cymraeg"
        ],
        "gaelic": [
            "gaelic", "scottish gaelic", "irish gaelic"
        ],

        # --- CREATIVE ARTS ---
        "art": [
            "art", "arts", "fine art", "visual art", "graphics", "graphic design", "photography", "art & design",
            "sculpture"
        ],
        "drama": [
            "drama", "theatre studies", "performing arts"
        ],
        "dance": [
            "dance", "dancing", "dance studies", "ballet", "contemporary dance"
        ],
        "music": [
            "music", "mus", "music technology", "music theory"
        ],
        "media studies": [
            "media studies", "media", "media science", "film studies", "film", "media production"
        ],
        "film studies": [
            "film studies", "film", "cinema studies", "filmmaking"
        ],
        "photography": [
            "photography", "photo studies"
        ],
        "graphics": [
            "graphics", "graphic design", "digital graphics", "graphic arts"
        ],

        # --- DESIGN / TECH ---
        "design and technology": [
            "design and technology", "d&t", "dt", "design tech", "product design", "food tech", "textiles",
            "fashion", "resistant materials"
        ],
        "engineering": [
            "engineering", "engineer", "mechanical engineering", "electrical engineering", "civil engineering",
            "chemical engineering"
        ],
        "automotive": [
            "automotive", "automotive studies", "automobile", "motor vehicle", "car technology"
        ],

        # --- HEALTH & SOCIAL CARE ---
        "pharmacy": [
            "pharmacy", "pharmacology"
        ],
        "health and social care": [
            "health and social care", "health studies", "social care", "healthcare", "health sciences", "health science"
        ],
        "public health": [
            "public health"
        ],
        "food science": [
            "food science", "food technology", "nutrition", "nutrition science", "food studies"
        ],
        "child development": [
            "child development", "childcare", "early childhood", "childhood studies"
        ],

        # --- HOSPITALITY / TOURISM ---
        "hospitality": [
            "hospitality", "hospitality studies", "hospitality management", "hotel management"
        ],
        "travel and tourism": [
            "travel and tourism", "tourism", "tourism studies", "travel", "tourism management"
        ],

        # --- AVIATION / TRANSPORT / LOGISTICS ---
        "aviation": [
            "aviation", "aviation studies", "airline operations", "pilot studies", "aeronautics", "flight operations"
        ],
        "logistics": [
            "logistics", "transport", "transport studies", "logistics management", "supply chain"
        ],

        # --- ANIMAL / AGRI / VET ---
        "animal management": [
            "animal management", "animal care", "animal studies", "animal science"
        ],
        "veterinary": [
            "veterinary", "vet", "veterinary studies", "veterinary medicine", "veterinary science"
        ],
        "agriculture": [
            "agriculture", "agricultural studies", "farming", "farm studies"
        ],
        "horticulture": [
            "horticulture", "gardening", "plant studies", "landscape studies"
        ],

        # --- SPORT, FITNESS, PE ---
        "pe": [
            "pe", "physical education", "sports science"
        ],
        "sports science": [
            "sports science", "sport science", "sports studies", "sport studies", "sports", "sport",
            "sports coaching", "fitness", "sports management"
        ],

        # --- BEAUTY, HAIR, FASHION ---
        "beauty therapy": [
            "beauty therapy", "beauty", "cosmetology", "beauty studies"
        ],
        "hairdressing": [
            "hairdressing", "hair styling", "hair studies"
        ],

    },
    # Courses for degree-level interests, not A-levels
    "courses": {

        # --- MEDICAL & HEALTH SCIENCES ---
        "medicine": [
            "medicine", "med", "med school", "medical degree", "doctor", "mbbs", "md", "medical studies",
            "clinical medicine", "medicine programme", "medic"
        ],
        "pharmacy": [
            "pharmacy", "pharmacology", "pharma", "pharmaceutical sciences", "pharmaceutical studies",
            "pharmacy school", "pharmacist"
        ],
        "dentistry": [
            "dentistry", "dentist", "bds", "dental surgery", "dental studies", "dental school", "dental science",
            "dental degree", "dental"
        ],
        "nursing": [
            "nursing", "nurse", "bsc nursing", "nursing degree", "nursing science", "nursing studies",
            "registered nurse", "adult nursing", "paediatric nursing", "mental health nursing", "midwifery"
        ],
        "physiotherapy": [
            "physiotherapy", "physio", "physical therapy", "physiotherapy degree", "physiotherapist"
        ],

        # --- BIOLOGICAL & PHYSICAL SCIENCES ---
        "biology": [
            "biology", "bio", "biological sciences", "life sciences", "biomedical sciences", "molecular biology",
            "cell biology", "biological science degree", "marine biology", "ecology", "biotechnology",
            "plant biology", "zoology"
        ],
        "biomedical engineering": [
            "biomedical engineering", "biomedical eng", "biomed engineering", "bioengineering",
            "medical engineering"
        ],
        "chemistry": [
            "chemistry", "chem", "chemistry degree", "chemical sciences", "applied chemistry",
            "medicinal chemistry", "pharmaceutical chemistry", "chemistry studies"
        ],
        "physics": [
            "physics", "phys", "physics degree", "applied physics", "theoretical physics",
            "physics with astronomy", "astrophysics", "physics studies"
        ],
        "environmental science": [
            "environmental science", "enviro science", "environmental studies", "environmental management",
            "environmental policy", "environmental engineering", "sustainability", "conservation science",
            "ecology", "environmental science degree"
        ],

        # --- MATHS, COMPUTER SCIENCE & ENGINEERING ---
        "mathematics": [
            "mathematics", "maths", "math", "core maths", "pure maths", "applied maths", "decision maths",
            "stats", "statistics", "mechanics", "math degree", "mathematics degree", "core mathematics",
            "f.maths", "f.math"
        ],
        "further mathematics": [
            "further mathematics", "further maths", "further math", "f.maths", "f.math", "further-math",
            "fmaths", "fmath", "furthermaths", "furthermath", "f maths", "f math", "further mathematics degree"
        ],
        "computer science": [
            "computer science", "cs", "comp sci", "software engineering", "computing", "informatics",
            "information systems", "ict", "information tech",
            "data science", "artificial intelligence", "ai", "cybersecurity", "computer engineering",
            "digital technology", "machine learning", "comp science", "comp", "computers"
        ],
        "engineering": [
            "engineering", "eng", "engineering degree", "mechanical engineering", "electrical engineering",
            "civil engineering",
            "chemical engineering", "mechatronics", "aerospace engineering",
            "structural engineering",
            "electronic engineering", "software engineering", "engineering science"
        ],

        # --- ARCHITECTURE, CONSTRUCTION & SURVEYING ---
        "architecture": [
            "architecture", "architect", "barch", "architectural studies", "architectural design",
            "architectural engineering", "architecture degree", "urban design", "landscape architecture",
            "architectural technology"
        ],
        "architecture technology": [
            "architectural technology", "architecture technology", "building technology"
        ],
        "construction management": [
            "construction", "construction management", "building studies", "construction engineering", "site management"
        ],
        "quantity surveying": [
            "quantity surveying", "surveyor", "building surveying", "construction surveying"
        ],

        # --- BUSINESS, ECONOMICS & MANAGEMENT ---
        "business": [
            "business", "business management", "bba", "business admin", "accounting", "accountancy",
            "business administration", "commerce",
            "business studies", "finance", "economics and finance", "mba", "management studies", "entrepreneurship",
            "marketing", "human resource management", "supply chain management"
        ],
        "economics": [
            "economics", "econ", "microeconomics", "macroeconomics", "economic studies", "economics degree",
            "finance and economics"
        ],
        "hospitality": [
            "hospitality", "international hospitality", "hospitality management", "hospitality and tourism",
            "hospitality with events", "events and hospitality", "culinary arts and hospitality",
            "hospitality business",
            "hospitality business management", "hospitality studies", "hospitality industry", "hospitality operations"
        ],
        "events management": [
            "events management", "event management", "events and hospitality", "events with hospitality",
            "event planning", "event studies"
        ],
        "tourism": [
            "tourism", "tourism management", "hospitality and tourism", "international tourism", "tourism studies"
        ],
        "culinary arts": [
            "culinary arts", "culinary management", "culinary studies", "culinary and hospitality"
        ],
        "logistics and supply chain": [
            "logistics", "logistics management", "supply chain", "supply chain management", "transport management"
        ],
        "sports management": [
            "sports management", "sport management", "sports administration"
        ],

        # --- SOCIAL SCIENCES & EDUCATION ---
        "psychology": [
            "psychology", "psych", "psyche", "clinical psychology", "forensic psychology", "applied psychology",
            "psychological sciences", "counselling psychology", "industrial psychology", "educational psychology",
            "psychology degree"
        ],
        "sociology": [
            "sociology", "socio", "social sciences", "social studies", "social research", "sociological studies",
            "sociology degree", "anthropology"
        ],
        "criminology": [
            "criminology", "crime science", "criminal justice", "criminal studies", "criminology degree"
        ],
        "social work": [
            "social work", "social worker", "social care", "social policy"
        ],
        "public services": [
            "public services", "public administration", "emergency management"
        ],
        "education": [
            "education", "teaching", "teacher training", "pgce", "b.ed", "educational studies", "education studies",
            "education degree", "school direct", "initial teacher training", "childhood studies",
            "educational psychology"
        ],
        "special education": [
            "special education", "special needs education", "sen", "inclusion studies"
        ],
        "early childhood education": [
            "early childhood education", "early years", "nursery studies", "childhood studies"
        ],
        "youth work": [
            "youth work", "youth studies", "youth and community work"
        ],
        "community development": [
            "community development", "community studies", "community management"
        ],

        # --- LAW, POLITICS & INTERNATIONAL STUDIES ---
        "law": [
            "law", "llb", "legal studies", "criminal law", "public law", "constitutional law", "barrister",
            "solicitor", "law school", "jurisprudence",
            "law degree", "legal practice", "commercial law", "international law", "family law"
        ],
        "politics": [
            "politics", "political science", "government and politics", "government studies", "public policy",
            "politics degree", "international politics"
        ],
        "international relations": [
            "international relations", "global studies", "international studies", "international affairs",
            "diplomacy", "international politics", "international development"
        ],
        "public relations": [
            "public relations", "pr", "corporate communications", "strategic communications",
            "communications management", "public affairs"
        ],

        # --- HUMANITIES & LANGUAGES ---
        "english": [
            "english", "english studies", "english degree", "creative writing", "linguistics", "comparative literature"
        ],
        "english literature": [
            "english literature", "lit", "english lit", "literature", "literary studies", "eng lit"
        ],
        "english language": [
            "english language", "english lang", "eng lang", "lang", "language", "english studies"
        ],
        "history": [
            "history", "historian", "historical studies", "history degree", "ancient history", "modern history",
            "history and politics", "history and economics"
        ],
        "philosophy": [
            "philosophy", "philosophy and ethics", "philosophy degree", "philosophical studies", "ethics",
            "theology", "philosophy and religion", "metaphysics"
        ],

        # --- CREATIVE ARTS, DESIGN, PERFORMANCE ---
        "art": [
            "art", "fine art", "visual art", "artist", "studio art", "art and design", "design", "applied arts",
            "sculpture", "painting", "graphic design", "illustration", "photography", "art history", "art degree"
        ],
        "drama": [
            "drama", "theatre", "theater", "theatre studies", "performing arts", "drama studies",
            "acting", "performance studies", "dramatic arts"
        ],
        "music": [
            "music", "music studies", "musician", "music performance", "music composition", "music production",
            "music technology", "conservatoire", "bmus", "musicology", "music degree"
        ],
        "animation": [
            "animation", "animation studies", "animated arts"
        ],
        "game design": [
            "game design", "game development", "games design", "video game design"
        ],
        "film production": [
            "film production", "film making", "film studies", "cinema production"
        ],
        "photography": [
            "photography", "photo studies", "photographic arts"
        ],
        "graphic design": [
            "graphic design", "graphics", "digital graphics", "visual communication"
        ],
        "interior design": [
            "interior design", "interior architecture", "interior decoration"
        ],
        "costume design": [
            "costume design", "costume production", "theatre costume", "stage costume"
        ],
        "sound engineering": [
            "sound engineering", "audio engineering", "music technology"
        ],
        "fashion management": [
            "fashion management", "fashion business", "fashion buying", "fashion marketing"
        ],
        "cosmetology": [
            "cosmetology", "beauty therapy", "beauty studies"
        ],
        "hair and makeup": [
            "hair and makeup", "hairdressing", "hair styling", "makeup artistry", "make-up"
        ],

        # --- SPORT, FITNESS & NUTRITION ---
        "sports science": [
            "sports science", "sport science", "sports studies", "sport studies", "sport and exercise science",
            "kinesiology", "sports therapy", "sports management", "sports coaching"
        ],
        "sports coaching": [
            "sports coaching", "sport coaching", "coaching science", "sports trainer"
        ],
        "physical education": [
            "physical education", "pe", "physical education studies", "sport education"
        ],
        "nutrition": [
            "nutrition", "nutrition science", "food science", "food technology", "dietetics"
        ],

        # --- ANIMAL, AGRICULTURE & ENVIRONMENT ---
        "animal science": [
            "animal science", "animal studies", "zoology", "animal management", "animal care"
        ],
        "veterinary": [
            "veterinary", "veterinary medicine", "vet science", "vet", "vet school", "veterinary surgeon",
            "veterinary studies", "bvetmed", "vet degree"
        ],
        "agriculture": [
            "agriculture", "agricultural science", "agricultural studies", "farm management", "farming"
        ],
        "horticulture": [
            "horticulture", "horticultural science", "gardening", "plant science"
        ],

        # --- AVIATION, TRANSPORT & MARITIME ---
        "aviation management": [
            "aviation", "aviation management", "air transport management", "pilot studies", "aeronautical science",
            "aeronautics", "flight operations"
        ],
        "maritime studies": [
            "maritime studies", "marine studies", "marine science", "shipping management"
        ],

        # --- FORENSIC SCIENCE ---
        "forensic science": [
            "forensic science", "forensics", "forensic studies"
        ],
    }
}