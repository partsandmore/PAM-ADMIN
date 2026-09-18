# -*- coding: utf-8 -*-
"""Demo people and companies, picked by hand from the extracted candidates.

Pattern matching on capitalisation could not separate "Anthony Lewis" from
"Add Invoice", so this list is curated rather than generated. Full names come
before bare first names in the apply order, which is handled by sorting on
length, so "George David" is never half-replaced by the "George" rule.
"""

PEOPLE = {
    "Aaron Zeen":       "Armin Ziegler",
    "Adrian Herman":    "Andreas Hartmann",
    "Andrew Jermia":    "Arno Jäger",
    "Anthony Lewis":    "Anton Lehmann",
    "Antony Lewis":     "Anton Lehner",
    "Brian Villalobos": "Bernd Vollmer",
    "Cameron Drake":    "Kai Drescher",
    "Connie Waters":    "Conny Wassermann",
    "Daniel Esbella":   "Daniel Eberle",
    "Doglas Martini":   "Dominik Martens",
    "Doris Crowley":    "Doris Kraus",
    "Elliot Murray":    "Elias Moser",
    "Emly Reachel":     "Emily Reichel",
    "George David":     "Georg David",
    "Harvey Smith":     "Hartmut Schmidt",
    "Hendry Daniel":    "Hendrik Daniel",
    "James Hong":       "Jakob Hoff",
    "Jay Ze":           "Jan Zerr",
    "Justin Lapointe":  "Julian Lang",
    "Kevin Alley":      "Kevin Albers",
    "Kevin Larry":      "Kevin Lorenz",
    "Linda Ray":        "Linda Reiter",
    "Linda Zimmer":     "Linda Zimmermann",
    "Lori Broaddus":    "Lora Breuer",
    "Mary Donald":      "Maria Donner",
    "Mary Zeen":        "Maria Zenner",
    "Matt Morgan":      "Mats Morgenstern",
    "Rebecca Smtih":    "Rebekka Schmitt",
    "Sean Hill":        "Sven Hügel",
    "Sophie Headrick":  "Sophie Heidrich",
    "Stephan Peralt":   "Stefan Perlat",
}

# bare first names used on their own in chat lists and labels
FIRST_NAMES = {
    "Adrian":   "Andreas",
    "Cameron":  "Kai",
    "Druman":   "Drumann",
    "George":   "Georg",
    "Gifford":  "Giffhorn",
    "Jackson":  "Jaksch",
    "Kathleen": "Kathrin",
    "Mercy":    "Merle",
    "Rufana":   "Rufina",
    "Shawn":    "Sven",
    "Sylvia":   "Silvia",
    "Teressa":  "Theresa",
    "Elisa":    "Elisa",
    "Michael":  "Michael",
    "Doris":    "Doris",
    "Sophie":   "Sophie",
}

COMPANIES = {
    "HCL Corp":   "HCL GmbH",
    "Ignis LLP":  "Ignis GbR",
    "Yip Corp":   "Yip AG",
}

# demo mailboxes, kept on example.com so nothing can be sent anywhere real
EMAILS = {
    "anthony@example.com":   "anton@example.com",
    "warren@example.com":    "werner@example.com",
    "Jnh343@example.com":    "jak343@example.com",
    "brian@example.com":     "bernd@example.com",
    "harvey@example.com":    "hartmut@example.com",
    "stephan@example.com":   "stefan@example.com",
    "doglas@example.com":    "dominik@example.com",
    "linda@example.com":     "linda@example.com",
    "elliot@example.com":    "elias@example.com",
    "sophie@example.com":    "sophie@example.com",
    "rebecca@example.com":   "rebekka@example.com",
    "connie@example.com":    "conny@example.com",
}

PERSON_MAP = {}
for part in (PEOPLE, FIRST_NAMES, COMPANIES, EMAILS):
    PERSON_MAP.update(part)
