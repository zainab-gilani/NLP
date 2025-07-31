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

    # Subject names and different ways these can be spelt
    "subjects": {
        "mathematics": [
            "math", "maths", "mathematics", "further maths", "further mathematics", "core maths", "pure maths",
            "stats", "statistics", "mechanics", "applied maths", "decision maths"
        ],
        "computer science": [
            "cs", "comp sci", "computing", "computer science", "information technology", "it", "ict", "informatics",
            "information systems", "ict", "information tech"
        ],
        "biology": [
            "biology", "bio", "biological sciences"
        ],
        "physics": [
            "physics", "phys", "applied physics", "astro physics", "astrophysics"
        ],
        "chemistry": [
            "chemistry", "chem", "applied chemistry", "organic chemistry", "inorganic chemistry"
        ],
        "psychology": [
            "psychology", "psych", "applied psychology"
        ],
        "english literature": [
            "english literature", "lit", "english lit", "literature", "literary studies"
        ],
        "english language": [
            "english language", "english lang", "eng lang", "lang", "language", "english studies"
        ],
        "history": [
            "history", "hist", "world history", "ancient history", "modern history"
        ],
        "geography": [
            "geography", "geo", "physical geography", "human geography"
        ],
        "business": [
            "business", "business studies", "biz", "bs", "business admin", "business administration", "commerce"
        ],
        "economics": [
            "economics", "econ", "microeconomics", "macroeconomics"
        ],
        "music": [
            "music", "mus", "music technology", "music theory"
        ],
        "philosophy": [
            "philosophy", "phil", "philosophy and ethics", "religious studies", "rs", "ethics"
        ],
        "law": [
            "law", "legal studies", "criminal law", "public law", "constitutional law"
        ],
        "sociology": [
            "sociology", "socio", "social studies"
        ],
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
        "art": [
            "art", "fine art", "visual art", "graphics", "graphic design", "photography", "art & design",
            "sculpture"
        ],
        "media studies": [
            "media studies", "media", "media science", "film studies", "film", "media production"
        ],
        "design and technology": [
            "design and technology", "d&t", "dt", "design tech", "product design", "food tech", "textiles",
            "fashion", "resistant materials"
        ],
        "politics": [
            "politics", "government and politics", "govt and politics", "pol", "government",
            "international relations"
        ],
        "pharmacy": [
            "pharmacy", "pharmacology"
        ],
        "accounting": [
            "accounting", "accountancy", "finance", "financial studies"
        ],
        "drama": [
            "drama", "theatre studies", "performing arts"
        ],
        "pe": [
            "pe", "physical education", "sports science"
        ],
        "travel and tourism": [
            "travel and tourism"
        ],
        "health and social care": [
            "health and social care"
        ],
        "child development": [
            "child development"
        ],
        "classical civilisation": [
            "classical civilisation"
        ],
    },

    # Courses for degree-level interests, not A-levels
    "courses": {
        "medicine": [
            "medicine", "med", "med school", "medical degree", "doctor", "mbbs", "md", "medical studies",
            "clinical medicine", "medicine programme", "medic"
        ],

        "computer science": [
            "computer science", "cs", "comp sci", "software engineering", "computing", "informatics",
            "information systems", "ict", "information tech",
            "data science", "artificial intelligence", "ai", "cybersecurity", "computer engineering",
            "digital technology", "machine learning"
        ],

        "law": [
            "law", "llb", "legal studies", "criminal law", "public law", "constitutional law", "barrister",
            "solicitor", "law school", "jurisprudence",
            "law degree", "legal practice", "commercial law", "international law", "family law"
        ],

        "pharmacy": [
            "pharmacy", "pharmacology", "pharma", "pharmaceutical sciences", "pharmaceutical studies",
            "pharmacy school", "pharmacist"
        ],

        "engineering": [
            "engineering", "eng", "engineering degree", "mechanical engineering", "electrical engineering",
            "civil engineering",
            "chemical engineering", "biomedical engineering", "mechatronics", "aerospace engineering",
            "structural engineering",
            "electronic engineering", "software engineering", "engineering science"
        ],

        "business": [
            "business", "business management", "bba", "business admin", "accounting", "accountancy",
            "business administration", "commerce",
            "business studies", "finance", "economics and finance", "mba", "management studies", "entrepreneurship",
            "marketing", "human resource management", "supply chain management"
        ],

        "psychology": [
            "psychology", "psych", "psyche", "clinical psychology", "forensic psychology", "applied psychology",
            "psychological sciences", "counselling psychology", "industrial psychology", "educational psychology",
            "psychology degree"
        ],

        "music": [
            "music", "music studies", "musician", "music performance", "music composition", "music production",
            "music technology", "conservatoire", "bmus", "musicology", "music degree"
        ],

        "history": [
            "history", "historian", "historical studies", "history degree", "ancient history", "modern history",
            "history and politics", "history and economics"
        ],

        "english": [
            "english", "english literature", "english language", "english studies", "english degree", "literature",
            "creative writing", "english lit", "english lang", "literary studies", "linguistics",
            "comparative literature"
        ],

        "architecture": [
            "architecture", "architect", "barch", "architectural studies", "architectural design",
            "architectural engineering", "architecture degree", "urban design", "landscape architecture",
            "architectural technology"
        ],

        "biology": [
            "biology", "bio", "biological sciences", "life sciences", "biomedical sciences", "molecular biology",
            "cell biology", "biological science degree", "marine biology", "ecology", "biotechnology",
            "plant biology", "zoology"
        ],

        "sociology": [
            "sociology", "socio", "social sciences", "social studies", "social research", "sociological studies",
            "sociology degree", "anthropology"
        ],

        "art": [
            "art", "fine art", "visual art", "artist", "studio art", "art and design", "design", "applied arts",
            "sculpture", "painting", "graphic design", "illustration", "photography", "art history", "art degree"
        ],

        "dentistry": [
            "dentistry", "dentist", "bds", "dental surgery", "dental studies", "dental school", "dental science",
            "dental degree", "dental"
        ],

        "veterinary": [
            "veterinary", "veterinary medicine", "vet science", "vet", "vet school", "veterinary surgeon",
            "veterinary studies", "bvetmed", "vet degree"
        ],

        "nursing": [
            "nursing", "nurse", "bsc nursing", "nursing degree", "nursing science", "nursing studies",
            "registered nurse", "adult nursing", "paediatric nursing", "mental health nursing", "midwifery"
        ],

        "education": [
            "education", "teaching", "teacher training", "pgce", "b.ed", "educational studies", "education studies",
            "education degree", "school direct", "initial teacher training", "childhood studies",
            "educational psychology"
        ],

        "criminology": [
            "criminology", "crime science", "criminal justice", "criminal studies", "criminology degree"
        ],

        "journalism": [
            "journalism", "media journalism", "news reporting", "broadcast journalism", "sports journalism",
            "journalist", "news media", "magazine journalism"
        ],

        "public relations": [
            "public relations", "pr", "corporate communications", "strategic communications",
            "communications management", "public affairs"
        ],

        "international relations": [
            "international relations", "global studies", "international studies", "international affairs",
            "diplomacy", "international politics", "international development"
        ],

        "politics": [
            "politics", "political science", "government and politics", "government studies", "public policy",
            "politics degree", "international politics"
        ],

        "economics": [
            "economics", "econ", "microeconomics", "macroeconomics", "economic studies", "economics degree",
            "finance and economics"
        ],

        "philosophy": [
            "philosophy", "philosophy and ethics", "philosophy degree", "philosophical studies", "ethics",
            "theology", "philosophy and religion", "metaphysics"
        ],

        "environmental science": [
            "environmental science", "enviro science", "environmental studies", "environmental management",
            "environmental policy", "environmental engineering", "sustainability", "conservation science",
            "ecology", "environmental science degree"
        ],

        "media": [
            "media", "media studies", "communications", "communication studies", "digital media",
            "media production", "film studies", "film and media", "broadcast media", "mass communication",
            "media degree"
        ],
    }
}