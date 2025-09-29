# Comprehensive legal database with international coverage
COUNTRIES = [
    "USA", "United Kingdom", "Canada", "Australia", "Germany", "France", 
    "Japan", "China", "India", "Brazil", "South Africa", "European Union",
    "International", "Singapore", "United Arab Emirates"
]

LEGAL_SYSTEMS = [
    "Common Law", "Civil Law", "Islamic Law", "Customary Law", "Mixed System",
    "International Law", "EU Law", "Federal System", "Unitary System"
]

CONSTITUTIONAL_ARTICLES = {
    "USA": [
        {
            "article": "First Amendment",
            "text": "Congress shall make no law respecting an establishment of religion, or prohibiting the free exercise thereof; or abridging the freedom of speech, or of the press; or the right of the people peaceably to assemble, and to petition the Government for a redress of grievances.",
            "topics": ["freedom of speech", "religion", "press", "assembly", "petition"],
            "impact": "high"
        },
        {
            "article": "Fourth Amendment", 
            "text": "The right of the people to be secure in their persons, houses, papers, and effects, against unreasonable searches and seizures, shall not be violated, and no Warrants shall issue, but upon probable cause, supported by Oath or affirmation, and particularly describing the place to be searched, and the persons or things to be seized.",
            "topics": ["privacy", "search and seizure", "criminal procedure", "warrants"],
            "impact": "high"
        }
    ],
    "United Kingdom": [
        {
            "article": "Magna Carta (1215) - Clause 39",
            "text": "No free man shall be seized or imprisoned, or stripped of his rights or possessions, or outlawed or exiled, or deprived of his standing in any other way, nor will we proceed with force against him, or send others to do so, except by the lawful judgement of his equals or by the law of the land.",
            "topics": ["due process", "rule of law", "legal rights", "fair trial"],
            "impact": "foundational"
        }
    ]
}

LEGAL_DATABASE = {
    "precedents": {
        "USA": [
            "Marbury v. Madison (1803) - Judicial review established",
            "Brown v. Board of Education (1954) - Equal protection", 
            "Roe v. Wade (1973) - Privacy rights (overturned 2022)",
            "Citizens United v. FEC (2010) - Campaign finance"
        ]
    },
    "legal_principles": [
        "Stare decisis - adherence to precedent",
        "Ratio decidendi - the reasoning behind a decision", 
        "Obiter dictum - incidental remarks",
        "Res judicata - matter already judged",
        "Actus reus - guilty act",
        "Mens rea - guilty mind"
    ]
}