"""
config.py — Central configuration for the Pew W152 Streamlit Dashboard.
Contains variable labels, value maps, thematic groupings, and design tokens.
"""

import pathlib, os

# ── Paths ────────────────────────────────────────────────────────────────────
DATA_DIR = pathlib.Path(__file__).parent
DATA_FILE = DATA_DIR / "ATP W152.csv"

# ── Survey Metadata ─────────────────────────────────────────────────────────
SURVEY_TITLE = "Pew Research Center — Wave 152 American Trends Panel"
SURVEY_DATES = "August 12 – 18, 2024"
SURVEY_N = 5_410
SURVEY_MODE = "Web + CATI (Computer-Assisted Telephone Interviewing)"
SURVEY_LANG = "English & Spanish"
WEIGHT_COL = "WEIGHT_W152"
REFUSED_CODE = 99  # coded as 99 or 99.0

# ── Color Palette (Nature Human Behaviour / Pew-inspired) ───────────────────
COLORS = {
    "primary":     "#0A6E78",   # deep teal
    "secondary":   "#E8574A",   # warm coral
    "accent1":     "#F5A623",   # amber
    "accent2":     "#6C5CE7",   # muted violet
    "accent3":     "#00B894",   # seafoam green
    "neutral":     "#636E72",   # cool grey
    "bg_dark":     "#0F1923",   # midnight
    "bg_card":     "#1A2634",   # card background (dark)
    "bg_light":    "#F8F9FA",   # light mode bg
    "text_dark":   "#DFE6E9",   # light text on dark bg
    "text_light":  "#2D3436",   # dark text on light bg
    "gradient_start": "#0A6E78",
    "gradient_end":   "#6C5CE7",
}

PLOTLY_PALETTE = [
    "#0A6E78", "#E8574A", "#F5A623", "#6C5CE7", "#00B894",
    "#FD79A8", "#74B9FF", "#FFEAA7", "#A29BFE", "#55EFC4",
    "#FF7675", "#81ECEC", "#DFE6E9", "#636E72",
]

DIVERGING_PALETTE = ["#E8574A", "#F5A623", "#DFE6E9", "#74B9FF", "#0A6E78"]

LIKERT_PALETTE_4 = ["#0A6E78", "#74B9FF", "#F5A623", "#E8574A"]
LIKERT_PALETTE_5 = ["#0A6E78", "#74B9FF", "#DFE6E9", "#F5A623", "#E8574A"]
LIKERT_PALETTE_6 = ["#0A6E78", "#00B894", "#74B9FF", "#F5A623", "#E8574A", "#636E72"]

# ── AI Block Variable Labels ────────────────────────────────────────────────
AI_HEARD_LABELS = {
    "AI_HEARD_W152": "How much have you heard about AI?"
}
AI_HEARD_VALUES = {1: "A lot", 2: "A little", 3: "Nothing at all", 99: "Refused"}

CNCEXC_LABELS = {"CNCEXC_W152": "More concerned or excited about AI in daily life?"}
CNCEXC_VALUES = {1: "More excited", 2: "Equally excited & concerned",
                 3: "More concerned", 99: "Refused"}

USEAI_LABELS = {"USEAI_W152": "Do you ever use AI-based tools?"}
USEAI_VALUES = {1: "Yes, regularly", 2: "Yes, occasionally", 3: "No", 99: "Refused"}

AICONTROL_LABELS = {
    "AICONTROL1_W152": "Want more or less control over how AI is used in life?",
    "AICONTROL2_W152": "How much control do you feel you currently have?",
}
AICONTROL_VALUES = {
    "AICONTROL1_W152": {1: "A lot more", 2: "A little more", 3: "About the same",
                        4: "A little less", 5: "A lot less", 99: "Refused"},
    "AICONTROL2_W152": {1: "A lot", 2: "Some", 3: "Not much", 4: "None at all", 99: "Refused"},
}

AICHANGE_LABELS = {"AICHANGE_W152": "AI impact on U.S. over next 20 years?"}
AICHANGE_VALUES = {1: "Very positive", 2: "Somewhat positive",
                   3: "Equally positive & negative", 4: "Somewhat negative",
                   5: "Very negative", 99: "Refused"}

# AI Future Impact sub-items
AIFUTRIMPCT_ITEMS = {
    "AIFUTRIMPCT_a_W152": "Economy",
    "AIFUTRIMPCT_b_W152": "How people do their jobs",
    "AIFUTRIMPCT_c_W152": "Medical care",
    "AIFUTRIMPCT_d_W152": "How people find things online",
    "AIFUTRIMPCT_e_W152": "Education of children",
    "AIFUTRIMPCT_f_W152": "Quality and originality of creative arts",
    "AIFUTRIMPCT_g_W152": "Quality of news",
    "AIFUTRIMPCT_h_W152": "U.S. elections",
    "AIFUTRIMPCT_i_W152": "Peoples privacy",
    "AIFUTRIMPCT_j_W152": "National security",
}
AIFUTRIMPCT_VALUES = {1: "Very positive", 2: "Somewhat positive",
                      3: "Somewhat negative", 4: "Very negative", 99: "Refused"}

# AI & Jobs
AIJOBS_LABELS = {"AIJOBS_W152": "AI will lead to more/fewer jobs in 20 yrs?"}
AIJOBS_VALUES = {1: "A lot more", 2: "A few more", 3: "About the same",
                 4: "A few fewer", 5: "A lot fewer", 99: "Refused"}

AIJOBIMPCT_ITEMS = {
    "AIJOBIMPCT_a_W152": "Factory workers",
    "AIJOBIMPCT_b_W152": "Truck drivers",
    "AIJOBIMPCT_c_W152": "Software engineers",
    "AIJOBIMPCT_d_W152": "Graphic designers",
    "AIJOBIMPCT_e_W152": "Cashiers",
    "AIJOBIMPCT_f_W152": "Teachers (K-12)",
    "AIJOBIMPCT_g_W152": "Journalists",
    "AIJOBIMPCT_h_W152": "Medical doctors",
    "AIJOBIMPCT_i_W152": "Musicians / performers",
    "AIJOBIMPCT_j_W152": "Lawyers",
}
AIJOBIMPCT_VALUES = {1: "A lot more", 2: "A few more", 3: "About the same",
                     4: "A few fewer", 99: "Refused"}

# Human vs AI
HUMANVAI_ITEMS = {
    "HUMANVAI_a_W152": "Making important medical decisions",
    "HUMANVAI_b_W152": "Driving a car or truck on roads",
    "HUMANVAI_c_W152": "Performing repetitive workplace tasks",
    "HUMANVAI_d_W152": "Making fair hiring decisions",
    "HUMANVAI_e_W152": "Identifying criminals in video footage",
    "HUMANVAI_f_W152": "Performing tasks safely in factories",
    "HUMANVAI_g_W152": "Providing financial advice",
    "HUMANVAI_h_W152": "Creating news articles",
}
HUMANVAI_VALUES = {1: "AI would do much better", 2: "AI would do somewhat better",
                   3: "Humans would do somewhat better", 4: "Humans would do much better",
                   99: "Refused"}

# Personal benefit / harm
PERSBENHRM_LABELS = {"PERSBENHRM_W152": "Will AI benefit or harm you personally?"}
PERSBENHRM_VALUES = {1: "Benefit me", 2: "Not sure", 3: "Harm me", 99: "Refused"}

# Trust AI providers
TRSTAIPRS_LABELS = {"TRSTAIPRS_W152": "Trust companies developing AI to act responsibly?"}
TRSTAIPRS_VALUES = {1: "A great deal / quite a bit", 2: "Some", 3: "Not too much / not at all",
                    99: "Refused"}

# AI Concerns
AICONCERN_ITEMS = {
    "AICONCERN_a_W152": "AI used to create realistic fake videos/images",
    "AICONCERN_b_W152": "Personal info used by AI without consent",
    "AICONCERN_c_W152": "AI used to monitor / track people",
    "AICONCERN_d_W152": "AI making decisions w/o human oversight",
    "AICONCERN_e_W152": "AI making unfair decisions based on race/gender",
    "AICONCERN_f_W152": "AI making mistakes in critical situations",
    "AICONCERN_g_W152": "Loss of human connection due to AI",
}
AICONCERN_VALUES = {1: "Extremely concerned", 2: "Very concerned",
                    3: "Somewhat concerned", 4: "Not too concerned",
                    5: "Not at all concerned", 99: "Refused"}

# Future AI (20-yr outlook on specific areas)
FUTRAI_ITEMS = {
    "FUTRAI_a_W152": "AI-powered self-driving cars widespread",
    "FUTRAI_b_W152": "AI diagnosing diseases as well as doctors",
    "FUTRAI_c_W152": "AI replacing most customer-service jobs",
    "FUTRAI_d_W152": "AI writing computer programs w/o engineers",
}
FUTRAI_VALUES = {1: "Definitely happen", 2: "Probably happen",
                 3: "Probably not happen", 4: "Definitely not happen",
                 5: "Already happening", 6: "Not sure", 99: "Refused"}

# Discrimination
DISCRIM1_ITEMS = {
    "DISCRIM1_a_W152": "AI treats people of different races fairly",
    "DISCRIM1_b_W152": "AI treats men and women fairly",
    "DISCRIM1_c_W152": "AI treats people of different ages fairly",
    "DISCRIM1_d_W152": "AI treats people of different income levels fairly",
    "DISCRIM1_e_W152": "AI treats people with different political views fairly",
    "DISCRIM1_f_W152": "AI treats people with disabilities fairly",
}
DISCRIM1_VALUES = {1: "Very confident", 2: "Somewhat confident",
                   3: "Not too confident", 4: "Not at all confident",
                   5: "Not sure", 99: "Refused"}

# Regulation
AIREG_LABELS = {"AIREG_W152": "Should government regulate AI more, less, or same?"}
AIREG_VALUES = {1: "Regulate more", 2: "About right", 3: "Regulate less", 99: "Refused"}

REGCONF_ITEMS = {
    "REGCONFG_W152": "Confidence in govt to manage AI responsibly",
    "REGCONFI_W152": "Confidence in industry to manage AI responsibly",
}
REGCONF_VALUES = {1: "A great deal", 2: "Quite a bit", 3: "Some",
                  4: "Not too much", 5: "Not at all", 6: "Not sure", 99: "Refused"}

# Chatbot
CHATAWARE_LABELS = {"CHATAWARE_W152": "Awareness of AI chatbots (ChatGPT, etc.)"}
CHATAWARE_VALUES = {1: "A lot", 2: "A little", 3: "Nothing at all", 99: "Refused"}

CHATUSE_LABELS = {"CHATUSE_W152": "Have you ever used a chatbot?"}
CHATUSE_VALUES = {1: "Yes", 2: "No", 99: "Refused"}

CHATHELPFUL_LABELS = {"CHATHELPFUL_W152": "How helpful was the chatbot?"}
CHATHELPFUL_VALUES = {1: "Extremely helpful", 2: "Very helpful",
                      3: "Somewhat helpful", 4: "Not too helpful",
                      5: "Not at all helpful", 99: "Refused"}

# ── Driving Block Variable Labels ────────────────────────────────────────────
DRIVE1_LABELS = {"DRIVE1_W152": "How often do you drive a car?"}
DRIVE1_VALUES = {1: "Every day", 2: "A few times a week", 3: "A few times a month",
                 4: "A few times a year", 5: "Rarely", 6: "Never", 99: "Refused"}

DRIVE2_ITEMS = {
    "DRIVE2_a_W152": "Distracted driving (e.g., cellphone use)",
    "DRIVE2_b_W152": "Speeding",
    "DRIVE2_c_W152": "Driving under the influence",
    "DRIVE2_d_W152": "Aggressive driving",
    "DRIVE2_e_W152": "Drivers running red lights / stop signs",
    "DRIVE2_f_W152": "Reckless driving (weaving, tailgating)",
}
DRIVE2_VALUES = {1: "Major problem", 2: "Minor problem",
                 3: "Not a problem", 99: "Refused"}

DRIVE3_LABELS = {"DRIVE3_W152": "How has driving safety changed in last 5 yrs?"}
DRIVE3_VALUES = {1: "A lot safer", 2: "Somewhat safer", 3: "About the same",
                 4: "Somewhat less safe", 5: "A lot less safe", 99: "Refused"}

DRIVER_LABELS = {"DRIVER_W152": "How often do you witness road rage?"}
DRIVER_VALUES = {1: "Often", 2: "Sometimes", 3: "Rarely", 4: "Never",
                 5: "Not applicable", 6: "Not sure", 99: "Refused"}

# ── Demographic Variable Labels ─────────────────────────────────────────────
DEMO_LABELS = {
    "F_AGECAT": "Age Group",
    "F_GENDER": "Gender",
    "F_EDUCCAT": "Education",
    "F_EDUCCAT2": "Education (detailed)",
    "F_RACETHNMOD": "Race / Ethnicity",
    "F_PARTY_FINAL": "Party Identification",
    "F_PARTYSUM_FINAL": "Party (summary)",
    "F_PARTYSUMIDEO_FINAL": "Party × Ideology",
    "F_IDEO": "Political Ideology",
    "F_INC_TIER2": "Income Tier",
    "F_INC_SDT1": "Household Income",
    "F_METRO": "Metro Status",
    "F_CREGION": "Census Region",
    "F_RELIG": "Religion",
    "F_RELIGCAT1": "Religion (summary)",
    "F_MARITAL": "Marital Status",
    "F_USR_SELFID": "Urban/Suburban/Rural",
    "F_INTFREQ": "Internet Frequency",
}

DEMO_VALUES = {
    "F_AGECAT": {1: "18-29", 2: "30-49", 3: "50-64", 4: "65+", 99: "Refused"},
    "F_GENDER": {1: "Male", 2: "Female", 3: "Other", 99: "Refused"},
    "F_EDUCCAT": {1: "College grad+", 2: "Some college", 3: "≤ High school",
                  99: "Refused"},
    "F_EDUCCAT2": {1: "Postgraduate", 2: "Bachelor's", 3: "Some college",
                   4: "Associate's", 5: "High school", 6: "< High school",
                   99: "Refused"},
    "F_RACETHNMOD": {1: "White non-Hispanic", 2: "Black non-Hispanic",
                     3: "Hispanic", 4: "Asian non-Hispanic",
                     5: "Other / multi-racial", 99: "Refused"},
    "F_PARTY_FINAL": {1: "Republican", 2: "Democrat", 3: "Independent",
                      4: "Something else", 99: "Refused"},
    "F_PARTYSUM_FINAL": {1: "Rep/Lean Rep", 2: "Dem/Lean Dem",
                         3: "No lean", 99: "Refused"},
    "F_PARTYSUMIDEO_FINAL": {1: "Cons. Rep", 2: "Mod/Lib Rep",
                             3: "Cons/Mod Dem", 4: "Liberal Dem",
                             99: "Refused"},
    "F_IDEO": {1: "Very conservative", 2: "Conservative", 3: "Moderate",
               4: "Liberal", 5: "Very liberal", 99: "Refused"},
    "F_INC_TIER2": {1: "Lower income", 2: "Middle income",
                    3: "Upper income", 99: "Refused"},
    "F_INC_SDT1": {1: "<$30K", 2: "$30-39K", 3: "$40-49K", 4: "$50-59K",
                   5: "$60-69K", 6: "$70-79K", 7: "$80-89K", 8: "$90-99K",
                   9: "$100K+", 99: "Refused"},
    "F_METRO": {1: "Metropolitan", 2: "Non-metropolitan"},
    "F_CREGION": {1: "Northeast", 2: "Midwest", 3: "South", 4: "West"},
    "F_RELIG": {1: "Protestant", 2: "Roman Catholic", 3: "Mormon",
                4: "Orthodox Christian", 5: "Jewish", 6: "Muslim",
                7: "Buddhist", 8: "Hindu", 9: "Atheist", 10: "Agnostic",
                11: "Nothing in particular", 12: "Something else", 99: "Refused"},
    "F_RELIGCAT1": {1: "Protestant", 2: "Catholic", 3: "Other Christian / non-Christian",
                    4: "Unaffiliated", 99: "Refused"},
    "F_MARITAL": {1: "Married", 2: "Widowed", 3: "Divorced",
                  4: "Separated", 5: "Never married", 6: "Living with partner",
                  99: "Refused"},
    "F_USR_SELFID": {1: "Urban", 2: "Suburban", 3: "Rural", 99: "Refused"},
    "F_INTFREQ": {1: "Almost constantly", 2: "Several times a day",
                  3: "About once a day", 4: "Several times a week",
                  5: "Less often", 6: "Never", 99: "Refused"},
}

# ── Convenience: all substantive question groups ─────────────────────────────
AI_SINGLE_QUESTIONS = {
    **AI_HEARD_LABELS, **CNCEXC_LABELS, **USEAI_LABELS,
    **AICHANGE_LABELS, **AIJOBS_LABELS, **PERSBENHRM_LABELS,
    **TRSTAIPRS_LABELS, **AIREG_LABELS,
    **CHATAWARE_LABELS, **CHATUSE_LABELS, **CHATHELPFUL_LABELS,
}

AI_SINGLE_VALUES = {
    "AI_HEARD_W152": AI_HEARD_VALUES,
    "CNCEXC_W152": CNCEXC_VALUES,
    "USEAI_W152": USEAI_VALUES,
    "AICHANGE_W152": AICHANGE_VALUES,
    "AIJOBS_W152": AIJOBS_VALUES,
    "PERSBENHRM_W152": PERSBENHRM_VALUES,
    "TRSTAIPRS_W152": TRSTAIPRS_VALUES,
    "AIREG_W152": AIREG_VALUES,
    "CHATAWARE_W152": CHATAWARE_VALUES,
    "CHATUSE_W152": CHATUSE_VALUES,
    "CHATHELPFUL_W152": CHATHELPFUL_VALUES,
}

DRIVING_SINGLE_QUESTIONS = {
    **DRIVE1_LABELS, **DRIVE3_LABELS, **DRIVER_LABELS,
}

DRIVING_SINGLE_VALUES = {
    "DRIVE1_W152": DRIVE1_VALUES,
    "DRIVE3_W152": DRIVE3_VALUES,
    "DRIVER_W152": DRIVER_VALUES,
}

# All battery items (multi-item question blocks) with shared value scales
AI_BATTERIES = {
    "AI Future Impact (20-yr)":      (AIFUTRIMPCT_ITEMS, AIFUTRIMPCT_VALUES),
    "AI & Job Impact by Sector":     (AIJOBIMPCT_ITEMS,  AIJOBIMPCT_VALUES),
    "Humans vs. AI — Who's Better?": (HUMANVAI_ITEMS,    HUMANVAI_VALUES),
    "AI Concerns":                   (AICONCERN_ITEMS,   AICONCERN_VALUES),
    "AI Predictions (20-yr)":        (FUTRAI_ITEMS,      FUTRAI_VALUES),
    "AI Fairness/Discrimination":    (DISCRIM1_ITEMS,    DISCRIM1_VALUES),
    "Confidence in Regulation":      (REGCONF_ITEMS,     REGCONF_VALUES),
}

DRIVING_BATTERIES = {
    "Driving Hazards (Major/Minor Problem)": (DRIVE2_ITEMS, DRIVE2_VALUES),
}
