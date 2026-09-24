from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    session
)

import mysql.connector
import json
import nltk
import re
import math
import os

from PIL import (
    Image,
    ImageEnhance,
    ImageFilter,
    ImageOps
)

import pytesseract

from collections import Counter

from nltk.corpus import stopwords

from nltk.stem import PorterStemmer

from PyPDF2 import PdfReader

from functools import wraps

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)# ============================================================
# OLLAMA / LOCAL AI
# ============================================================

try:
    from ollama import chat
    OLLAMA_AVAILABLE = True
except ImportError:
    chat = None
    OLLAMA_AVAILABLE = False


OLLAMA_MODEL = "gemma3:1b"


app = Flask(__name__)

app.config["SECRET_KEY"] = "health-copilot-secret-key-2026"

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# ============================================================
# DATABASE
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "port": 3307,
    "user": "root",
    "password": "amulya",
    "database": "health_copilot"
}


# ============================================================
# NLTK SETUP
# ============================================================

try:
    STOP_WORDS = set(stopwords.words("english"))
except LookupError:
    nltk.download("stopwords")
    STOP_WORDS = set(stopwords.words("english"))

stemmer = PorterStemmer()


# ============================================================
# MULTILINGUAL MEDICAL DATA
# ============================================================

SYMPTOMS = {
    "english": [
        "fever",
        "cough",
        "cold",
        "headache",
        "vomiting",
        "nausea",
        "pain",
        "fatigue",
        "weakness",
        "dizziness",
        "breathing difficulty",
        "shortness of breath",
        "chest pain",
        "stomach pain",
        "back pain",
        "sore throat",
        "diarrhea"
    ],

    "telugu": [
        "జ్వరం",
        "దగ్గు",
        "జలుబు",
        "తలనొప్పి",
        "వాంతులు",
        "వికారం",
        "నొప్పి",
        "అలసట",
        "బలహీనత",
        "తల తిరగడం",
        "ఛాతి నొప్పి",
        "కడుపు నొప్పి",
        "వెన్నునొప్పి"
    ],

    "hindi": [
        "बुखार",
        "खांसी",
        "जुकाम",
        "सिरदर्द",
        "उल्टी",
        "मतली",
        "दर्द",
        "थकान",
        "कमजोरी",
        "चक्कर",
        "सीने में दर्द",
        "पेट दर्द"
    ],

    "tamil": [
        "காய்ச்சல்",
        "இருமல்",
        "சளி",
        "தலைவலி",
        "வாந்தி",
        "குமட்டல்",
        "வலி",
        "சோர்வு",
        "பலவீனம்",
        "தலைச்சுற்றல்",
        "மார்பு வலி",
        "வயிற்று வலி"
    ],

    "kannada": [
        "ಜ್ವರ",
        "ಕೆಮ್ಮು",
        "ನೆಗಡಿ",
        "ತಲೆನೋವು",
        "ವಾಂತಿ",
        "ವಾಕರಿಕೆ",
        "ನೋವು",
        "ಆಯಾಸ",
        "ದೌರ್ಬಲ್ಯ",
        "ತಲೆಸುತ್ತು",
        "ಎದೆ ನೋವು",
        "ಹೊಟ್ಟೆ ನೋವು"
    ]
}


MEDICINES = [
    # ---------------- PAIN / FEVER ----------------
    "paracetamol",
    "acetaminophen",
    "dolo",
    "dolo 500",
    "dolo 650",
    "crocin",
    "calpol",
    "p 500",
    "p 650",
    "meftal",
    "meftal spas",
    "diclofenac",
    "aceclofenac",
    "naproxen",
    "nimesulide",
    "ketorolac",
    "tramadol",

    # ---------------- COLD / ALLERGY ----------------
    "cetirizine",
    "levocetirizine",
    "loratadine",
    "fexofenadine",
    "desloratadine",
    "chlorpheniramine",
    "montelukast",
    "montek",
    "allegra",
    "avil",
    "cpm",

    # ---------------- COUGH / COLD BRANDS ----------------
    "benadryl",
    "ascoril",
    "asthakind",
    "ambrolite",
    "mucinac",
    "ambroxol",
    "bromhexine",
    "guaifenesin",
    "dextromethorphan",

    # ---------------- ANTIBIOTICS ----------------
    "amoxicillin",
    "augmentin",
    "azithromycin",
    "azee",
    "amoxyclav",
    "cefixime",
    "cefpodoxime",
    "cephalexin",
    "cefuroxime",
    "ceftibuten",
    "doxycycline",
    "ciprofloxacin",
    "levofloxacin",
    "ofloxacin",
    "moxifloxacin",
    "metronidazole",
    "clindamycin",
    "clarithromycin",
    "erythromycin",

    # ---------------- ACIDITY / GAS ----------------
    "omeprazole",
    "pantoprazole",
    "pantocid",
    "rabeprazole",
    "esomeprazole",
    "lansoprazole",
    "dexlansoprazole",
    "famotidine",
    "ranitidine",
    "domperidone",
    "ondansetron",
    "gelusil",
    "digene",

    # ---------------- DIABETES ----------------
    "metformin",
    "glycomet",
    "glimepiride",
    "gliclazide",
    "glipizide",
    "sitagliptin",
    "linagliptin",
    "vildagliptin",
    "teneligliptin",
    "dapagliflozin",
    "empagliflozin",
    "canagliflozin",
    "pioglitazone",
    "insulin",

    # ---------------- BLOOD PRESSURE / HEART ----------------
    "amlodipine",
    "atenolol",
    "metoprolol",
    "bisoprolol",
    "carvedilol",
    "losartan",
    "telmisartan",
    "olmesartan",
    "valsartan",
    "ramipril",
    "enalapril",
    "lisinopril",
    "cilnidipine",
    "nifedipine",
    "hydrochlorothiazide",

    # ---------------- CHOLESTEROL ----------------
    "atorvastatin",
    "rosuvastatin",
    "simvastatin",
    "pravastatin",
    "fenofibrate",
    "ezetimibe",

    # ---------------- BLOOD THINNERS ----------------
    "aspirin",
    "ecosprin",
    "clopidogrel",
    "prasugrel",
    "ticagrelor",
    "warfarin",
    "apixaban",
    "rivaroxaban",

    # ---------------- VITAMINS / SUPPLEMENTS ----------------
    "becosules",
    "neurobion",
    "neurobion forte",
    "shelcal",
    "calcium",
    "vitamin d3",
    "cholecalciferol",
    "calcitriol",
    "vitamin b12",
    "methylcobalamin",
    "folic acid",
    "iron",
    "ferrous sulfate",
    "ferrous ascorbate",
    "zinc",
    "multivitamin",

    # ---------------- THYROID ----------------
    "levothyroxine",
    "thyroxine",
    "eltroxin",
    "thyronorm",

    # ---------------- STEROIDS / ANTI-INFLAMMATORY ----------------
    "prednisolone",
    "methylprednisolone",
    "dexamethasone",
    "hydrocortisone",

    # ---------------- SKIN / ANTIFUNGAL ----------------
    "fluconazole",
    "itraconazole",
    "terbinafine",
    "clotrimazole",
    "ketoconazole",
    "acyclovir",

    # ---------------- URINARY / KIDNEY RELATED ----------------
    "tamsulosin",
    "alfuzosin",
    "finasteride",
    "dutasteride",
    "potassium citrate",

    # ---------------- ANTI-NAUSEA / DIGESTION ----------------
    "ondansetron",
    "domperidone",
    "metoclopramide",
    "loperamide",
    "lactulose",
    "bisacodyl",

    # ---------------- ANXIETY / SLEEP ----------------
    "alprazolam",
    "clonazepam",
    "diazepam",

    # ---------------- COMMON BRAND NAMES ----------------
    "combiflam",
    "zerodol",
    "zerodol p",
    "zerodol sp",
    "okacet",
    "avil",
    "allegra",
    "montek lc",
    "pan",
    "pan 40",
    "pantop",
    "pantop 40",
    "rablet",
    "rabep",
    "glycomet gp",
    "amaryl",
    "telma",
    "telma 40",
    "telma h",
    "amlong",
    "norvasc",
    "ecosprin",
    "clopivas",
    "rosuvas",
    "crestor",
    "thyronorm",
    "eltroxin",
    "shelcal 500",
    "neurobion forte"

]


MEDICAL_ENTITIES = [
    "diabetes",
    "blood sugar",
    "glucose",
    "blood pressure",
    "hypertension",
    "cholesterol",
    "hemoglobin",
    "haemoglobin",
    "vitamin d",
    "vitamin b12",
    "anemia",
    "anaemia",
    "kidney",
    "liver",
    "heart",
    "thyroid",
    "creatinine",
    "platelets",
    "wbc",
    "rbc",
    "tsh",
    "t3",
    "t4"
]


# ============================================================
# NLP FUNCTIONS
# ============================================================

def tokenize(text):

    return re.findall(
        r"\b[\w'-]+\b",
        text.lower(),
        flags=re.UNICODE
    )


def remove_stopwords(tokens):

    return [
        word
        for word in tokens
        if word not in STOP_WORDS
    ]


def stemming(tokens):

    return [
        stemmer.stem(word)
        for word in tokens
        if word.isascii()
    ]


def create_ngrams(tokens, n):

    return [
        " ".join(tokens[i:i + n])
        for i in range(len(tokens) - n + 1)
    ]


def extract_keywords(text, limit=15):

    tokens = tokenize(text)

    cleaned = remove_stopwords(tokens)

    frequency = Counter(cleaned)

    return [
        word
        for word, count in frequency.most_common(limit)
        if len(word) > 2
    ]


def extract_symptoms(text):

    text_lower = text.lower()

    found = []

    for language, symptoms in SYMPTOMS.items():

        for symptom in symptoms:

            if symptom.lower() in text_lower:

                if symptom not in found:
                    found.append(symptom)

    return found


def extract_medicines(text):

    text_lower = text.lower()

    found = []

    for medicine in MEDICINES:

        if medicine.lower() in text_lower:

            if medicine not in found:
                found.append(medicine)

    return found


def extract_entities(text):

    text_lower = text.lower()

    found = []

    for entity in MEDICAL_ENTITIES:

        if entity.lower() in text_lower:

            if entity not in found:
                found.append(entity)

    return found


def classify_intent(question):

    q = question.lower()

    if any(word in q for word in [
        "summary",
        "summarize",
        "short summary",
        "సారాంశం",
        "सारांश",
        "சுருக்கம்",
        "ಸಾರಾಂಶ"
    ]):

        return "summary"


    if any(word in q for word in [
        "medicine",
        "tablet",
        "drug",
        "capsule",
        "మందు",
        "ఔషధం",
        "दवा",
        "மருந்து",
        "ಔಷಧ"
    ]):

        return "medicine"


    if any(word in q for word in [
        "report",
        "test",
        "result",
        "value",
        "lab",
        "రిపోర్ట్",
        "పరీక్ష",
        "रिपोर्ट",
        "जांच",
        "அறிக்கை",
        "ಪರೀಕ್ಷೆ"
    ]):

        return "report_question"


    if any(word in q for word in [
        "symptom",
        "symptoms",
        "problem",
        "pain",
        "fever",
        "లక్షణం",
        "లక్షణాలు",
        "समस्या",
        "लक्षण",
        "அறிகுறி",
        "ಲಕ್ಷಣ"
    ]):

        return "symptoms"


    return "general_health"


# ============================================================
# TEXT PROCESSING
# ============================================================

def split_sentences(text):

    return re.split(
        r"(?<=[.!?])\s+",
        text.strip()
    )


def tf(tokens):

    counts = Counter(tokens)

    total = len(tokens)

    if total == 0:
        return {}

    return {
        word: count / total
        for word, count in counts.items()
    }


def idf(documents):

    total_documents = len(documents)

    result = {}

    vocabulary = set()

    for doc in documents:

        vocabulary.update(doc)

    for word in vocabulary:

        document_count = sum(
            1
            for doc in documents
            if word in doc
        )

        result[word] = math.log(
            (total_documents + 1) /
            (document_count + 1)
        ) + 1

    return result


def cosine_similarity(vector_a, vector_b):

    common = set(vector_a) & set(vector_b)

    numerator = sum(
        vector_a[x] * vector_b[x]
        for x in common
    )

    denominator_a = math.sqrt(
        sum(
            value * value
            for value in vector_a.values()
        )
    )

    denominator_b = math.sqrt(
        sum(
            value * value
            for value in vector_b.values()
        )
    )

    if denominator_a == 0 or denominator_b == 0:

        return 0

    return numerator / (
        denominator_a * denominator_b
    )


def search_report(question, report, limit=4):

    if not report.strip():
        return []

    sentences = split_sentences(report)

    if not sentences:
        return []

    question_tokens = remove_stopwords(
        tokenize(question)
    )

    sentence_tokens = [
        remove_stopwords(
            tokenize(sentence)
        )
        for sentence in sentences
    ]

    documents = [
        question_tokens
    ] + sentence_tokens

    idf_values = idf(documents)

    def vector(tokens):

        term_frequency = tf(tokens)

        return {
            word:
                term_frequency[word] *
                idf_values.get(word, 1)
            for word in term_frequency
        }

    question_vector = vector(
        question_tokens
    )

    results = []

    for sentence, tokens in zip(
        sentences,
        sentence_tokens
    ):

        sentence_vector = vector(tokens)

        score = cosine_similarity(
            question_vector,
            sentence_vector
        )

        if score > 0:

            results.append(
                (score, sentence)
            )

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        sentence
        for score, sentence in results[:limit]
    ]


def summarize(text, max_sentences=5):

    sentences = split_sentences(text)

    if len(sentences) <= max_sentences:

        return text.strip()

    keywords = extract_keywords(
        text,
        20
    )

    scored = []

    for index, sentence in enumerate(sentences):

        words = tokenize(sentence)

        score = sum(
            1
            for word in words
            if word in keywords
        )

        scored.append(
            (
                score,
                index,
                sentence
            )
        )

    scored.sort(
        key=lambda x: x[0],
        reverse=True
    )

    selected = sorted(
        scored[:max_sentences],
        key=lambda x: x[1]
    )

    return " ".join(
        item[2]
        for item in selected
    )


# ============================================================
# GENERAL HEALTH KNOWLEDGE BASE PDF
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


KNOWLEDGE_PDF = os.path.join(
    BASE_DIR,
    "basic_health_qa_1000_questions.pdf"
)


HEALTH_KNOWLEDGE_BASE = []


def parse_health_qa_pdf():

    if not os.path.exists(KNOWLEDGE_PDF):

        print(
            "Knowledge base PDF not found:",
            KNOWLEDGE_PDF
        )

        return []

    try:

        reader = PdfReader(
            KNOWLEDGE_PDF
        )

        pages = []

        for page in reader.pages:

            try:

                page_text = (
                    page.extract_text() or ""
                )

                if page_text.strip():

                    pages.append(
                        page_text
                    )

            except Exception as error:

                print(
                    "Knowledge PDF page error:",
                    error
                )

        full_text = "\n".join(
            pages
        ).strip()

        if not full_text:

            print(
                "Knowledge base PDF contains no readable text."
            )

            return []

        full_text = full_text.replace(
            "\r\n",
            "\n"
        )

        full_text = re.sub(
            r"[ \t]+",
            " ",
            full_text
        )

        pattern = re.compile(
            r"(?:^|\n)\s*(\d+)\.\s*(.*?)"
            r"\n\s*Answer\s*:\s*(.*?)"
            r"(?=\n\s*\d+\.\s|\Z)",
            re.IGNORECASE | re.DOTALL
        )

        matches = pattern.findall(
            full_text
        )

        knowledge = []

        for number, question, answer in matches:

            question = re.sub(
                r"\s+",
                " ",
                question
            ).strip()

            answer = re.sub(
                r"\s+",
                " ",
                answer
            ).strip()

            if question and answer:

                knowledge.append({
                    "number": int(number),
                    "question": question,
                    "answer": answer
                })

        print(
            "Health knowledge base loaded:",
            len(knowledge),
            "Q&A pairs"
        )

        return knowledge

    except Exception as error:

        print(
            "Knowledge base PDF error:",
            error
        )

        return []


def search_health_knowledge(
    question,
    limit=3,
    min_score=0.08
):

    if not HEALTH_KNOWLEDGE_BASE:

        return []

    question_tokens = remove_stopwords(
        tokenize(question)
    )

    if not question_tokens:

        return []

    documents = [
        question_tokens
    ]

    knowledge_tokens = []

    for item in HEALTH_KNOWLEDGE_BASE:

        tokens = remove_stopwords(
            tokenize(
                item["question"]
                + " "
                + item["answer"]
            )
        )

        knowledge_tokens.append(
            tokens
        )

        documents.append(
            tokens
        )

    idf_values = idf(
        documents
    )

    def vector(tokens):

        term_frequency = tf(
            tokens
        )

        return {
            word:
                term_frequency[word]
                * idf_values.get(word, 1)
            for word in term_frequency
        }

    question_vector = vector(
        question_tokens
    )

    question_set = set(
        question_tokens
    )

    results = []

    for item, tokens in zip(
        HEALTH_KNOWLEDGE_BASE,
        knowledge_tokens
    ):

        if not tokens:

            continue

        item_vector = vector(
            tokens
        )

        similarity = cosine_similarity(
            question_vector,
            item_vector
        )

        token_set = set(
            tokens
        )

        overlap = len(
            question_set & token_set
        )

        overlap_ratio = (
            overlap /
            max(len(question_set), 1)
        )

        score = (
            similarity
            + (0.12 * overlap_ratio)
        )

        if score >= min_score:

            results.append({
                "score": score,
                "question": item["question"],
                "answer": item["answer"],
                "number": item["number"]
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:limit]


HEALTH_KNOWLEDGE_BASE = (
    parse_health_qa_pdf()
)


# ============================================================
# LOCAL HEALTH KNOWLEDGE
# ============================================================

GENERAL_HEALTH_INFO = {

    "fever": (
        "Fever can occur with infections and several "
        "other conditions. Keep hydrated and monitor "
        "the temperature. If fever is severe, persistent, "
        "or accompanied by serious symptoms, seek medical care."
    ),

    "cough": (
        "A cough can have many causes including infections, "
        "allergies, asthma, or irritation. Persistent or "
        "severe cough should be evaluated by a healthcare professional."
    ),

    "headache": (
        "Headaches can have many causes such as dehydration, "
        "stress, lack of sleep, migraine, or illness. "
        "Severe sudden headache or headache with neurological "
        "symptoms needs urgent medical attention."
    ),

    "blood pressure": (
        "Blood pressure is normally interpreted using the "
        "systolic and diastolic values together. A single "
        "reading does not always establish a diagnosis. "
        "Repeated abnormal readings should be discussed "
        "with a healthcare professional."
    ),

    "diabetes": (
        "Diabetes is a condition involving elevated blood "
        "glucose. Tests such as fasting glucose, post-meal "
        "glucose, and HbA1c may be used as part of medical evaluation."
    ),

    "cholesterol": (
        "A lipid profile commonly includes total cholesterol, "
        "LDL, HDL, and triglycerides. Interpretation depends "
        "on the person's overall health and risk factors."
    )
}


def local_health_answer(question):

    q = question.lower()

    for keyword, answer in GENERAL_HEALTH_INFO.items():

        if keyword in q:

            return answer

    return (
        "I can help explain general health information, "
        "medical terms, medicines, symptoms, and uploaded "
        "medical reports. For a specific medical concern, "
        "please provide the relevant details or upload the report."
    )


# ============================================================
# OLLAMA AI HEALTH ANSWER
# ============================================================

def generate_ai_health_answer(
    question,
    report_context="",
    knowledge_context=""
):

    if not OLLAMA_AVAILABLE:

        print(
            "Ollama Python package is not installed."
        )

        return None


    try:

        context_parts = []

        if knowledge_context.strip():

            context_parts.append(
                "RELEVANT KNOWLEDGE BASE INFORMATION:\n"
                + knowledge_context
            )


        if report_context.strip():

            context_parts.append(
                "RELEVANT UPLOADED REPORT INFORMATION:\n"
                + report_context
            )


        context = "\n\n".join(
            context_parts
        )


        if not context:

            context = (
                "No directly matching information "
                "was found in the application's local "
                "knowledge sources."
            )


        prompt = f"""
You are Health Copilot, a general health-information
assistant.

USER QUESTION:
{question}

{context}

Your task:

1. Answer the user's health-related question clearly.
2. You are allowed to answer questions even when the
   exact question is not present in the local knowledge base.
3. Use your general medical knowledge for questions that
   are not covered by the local knowledge base.
4. If local knowledge or uploaded report information is
   provided, use it as supporting context, but do not
   blindly copy it.
5. Do not invent laboratory values, diagnoses, symptoms,
   or medical history.
6. Do not claim that you have examined the patient.
7. Do not provide a definite diagnosis.
8. Do not prescribe prescription medicines.
9. For medicines, explain general purpose, common uses,
   important precautions, and advise following a clinician's
   or pharmacist's instructions.
10. For symptoms, explain common possible causes and
    when medical evaluation is appropriate.
11. If the question describes emergency warning signs such
    as severe chest pain, severe breathing difficulty,
    stroke-like symptoms, severe bleeding, loss of
    consciousness, or another potentially life-threatening
    situation, advise urgent/emergency medical care.
12. If the question is not health-related, politely say
    that Health Copilot is intended for health information.
13. Answer in the same language as the user's question
    whenever reasonably possible.
14. Keep the answer understandable and well structured.
15. Use bullet points when useful.
16. End with a short reminder that this is general
    health information and not a diagnosis.

IMPORTANT:
The user wants useful information, not only predefined
answers. Therefore, answer new health questions using
general medical knowledge when appropriate.
"""


        response = chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a careful, evidence-aware "
                        "general health-information assistant."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )


        if not response:

            return None


        message = response.get(
            "message",
            {}
        )


        answer = message.get(
            "content",
            ""
        )


        if not answer:

            return None


        return answer.strip()


    except Exception as error:

        print(
            "Ollama AI error:",
            error
        )

        return None


# ============================================================
# COPILOT
# ============================================================

def copilot(
    question,
    report=""
):

    question = question.strip()

    if not question:

        return {
            "answer": "Please enter a health question.",
            "intent": "unknown",
            "keywords": [],
            "entities": [],
            "symptoms": [],
            "medicines": [],
            "relevant_report": [],
            "knowledge_base": []
        }


    intent = classify_intent(
        question
    )


    keywords = extract_keywords(
        question
    )


    entities = extract_entities(
        question
    )


    symptoms = extract_symptoms(
        question
    )


    medicines = extract_medicines(
        question
    )


    relevant_report = []


    if report.strip():

        relevant_report = search_report(
            question,
            report
        )


    # --------------------------------------------------------
    # SUMMARY REQUEST
    # --------------------------------------------------------

    if (
        intent == "summary"
        and report.strip()
    ):

        answer = summarize(
            report
        )

        return {
            "answer": answer,
            "intent": intent,
            "keywords": keywords,
            "entities": entities,
            "symptoms": symptoms,
            "medicines": medicines,
            "relevant_report": [],
            "knowledge_base": []
        }


    # --------------------------------------------------------
    # SEARCH LOCAL KNOWLEDGE BASE
    # --------------------------------------------------------

    knowledge_results = search_health_knowledge(
        question,
        limit=3
    )


    knowledge_context = ""


    if knowledge_results:

        knowledge_context = "\n\n".join(
            [
                (
                    "Question: "
                    + item["question"]
                    + "\nAnswer: "
                    + item["answer"]
                )
                for item in knowledge_results
            ]
        )


    # --------------------------------------------------------
    # REPORT CONTEXT
    # --------------------------------------------------------

    report_context = ""


    if relevant_report:

        report_context = "\n".join(
            [
                "• " + item
                for item in relevant_report
            ]
        )

    elif report.strip() and intent == "report_question":

        # If the exact report question did not match,
        # still allow AI to answer the general health
        # part of the question.

        report_context = (
            "No directly matching passage was found "
            "in the uploaded report."
        )


    # --------------------------------------------------------
    # AI GENERATION
    # --------------------------------------------------------

    ai_answer = generate_ai_health_answer(
        question=question,
        report_context=report_context,
        knowledge_context=knowledge_context
    )


    if ai_answer:

        return {
            "answer": ai_answer,
            "intent": intent,
            "keywords": keywords,
            "entities": entities,
            "symptoms": symptoms,
            "medicines": medicines,
            "relevant_report": relevant_report,
            "knowledge_base": [
                {
                    "question": item["question"],
                    "answer": item["answer"],
                    "score": round(
                        item["score"],
                        4
                    )
                }
                for item in knowledge_results
            ]
        }


    # --------------------------------------------------------
    # FALLBACK IF OLLAMA IS TEMPORARILY UNAVAILABLE
    # --------------------------------------------------------

    if knowledge_results:

        best = knowledge_results[0]

        answer = (
            best["answer"]
            + "\n\n"
            "Source: Basic Health Q&A Knowledge Base."
            "\nThis is general health information and "
            "is not a diagnosis or a personal treatment recommendation."
        )

        return {
            "answer": answer,
            "intent": intent,
            "keywords": keywords,
            "entities": entities,
            "symptoms": symptoms,
            "medicines": medicines,
            "relevant_report": relevant_report,
            "knowledge_base": [
                {
                    "question": item["question"],
                    "answer": item["answer"],
                    "score": round(
                        item["score"],
                        4
                    )
                }
                for item in knowledge_results
            ]
        }


    answer = local_health_answer(
        question
    )

    return {
        "answer": answer,
        "intent": intent,
        "keywords": keywords,
        "entities": entities,
        "symptoms": symptoms,
        "medicines": medicines,
        "relevant_report": relevant_report,
        "knowledge_base": []
    }


# ============================================================
# DATABASE
# ============================================================

def get_connection():

    return mysql.connector.connect(
        **DB_CONFIG
    )


def save_record(
    text,
    symptoms,
    medicines,
    keywords,
    summary
):

    try:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO medical_records
            (text, symptoms, medicines, keywords, summary)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                text,
                ", ".join(symptoms),
                ", ".join(medicines),
                ", ".join(keywords),
                summary
            )
        )

        connection.commit()

        cursor.close()

        connection.close()

    except Exception as error:

        print(
            "Database error:",
            error
        )


# ============================================================
# FILE TEXT EXTRACTION
# ============================================================

def extract_pdf_text(file):

    reader = PdfReader(file)

    pages = []

    for page in reader.pages:

        try:

            page_text = (
                page.extract_text() or ""
            )

            pages.append(
                page_text
            )

        except Exception:

            continue

    return "\n".join(
        pages
    ).strip()

# ============================================================
# IMPROVED MEDICINE / IMAGE OCR
# ============================================================

def preprocess_ocr_image(image):
    """
    Improve medicine package images before OCR.
    """

    # Convert to RGB
    image = image.convert("RGB")

    # Make small medicine text larger
    width, height = image.size

    scale = 2

    image = image.resize(
        (
            width * scale,
            height * scale
        ),
        Image.Resampling.LANCZOS
    )

    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Improve contrast
    gray = ImageEnhance.Contrast(
        gray
    ).enhance(2.0)

    # Improve sharpness
    gray = ImageEnhance.Sharpness(
        gray
    ).enhance(2.0)

    # Slight smoothing
    gray = gray.filter(
        ImageFilter.SHARPEN
    )

    return gray


def extract_image_text(file):

    try:

        # ----------------------------------------------------
        # Open image
        # ----------------------------------------------------

        image = Image.open(file)

        image.load()


        # ----------------------------------------------------
        # Create improved OCR image
        # ----------------------------------------------------

        processed = preprocess_ocr_image(
            image
        )


        # ----------------------------------------------------
        # Try multiple Tesseract configurations
        # ----------------------------------------------------

        ocr_results = []


        configs = [
            "--psm 6",
            "--psm 11",
            "--psm 12",
            "--psm 3"
        ]


        for config in configs:

            try:

                text = pytesseract.image_to_string(
                    processed,
                    config=config
                )

                if text and text.strip():

                    ocr_results.append(
                        text.strip()
                    )

            except Exception as error:

                print(
                    "OCR configuration error:",
                    error
                )


        # ----------------------------------------------------
        # Also OCR original image
        # ----------------------------------------------------

        try:

            original_text = (
                pytesseract.image_to_string(
                    image,
                    config="--psm 6"
                )
            )

            if original_text and original_text.strip():

                ocr_results.append(
                    original_text.strip()
                )

        except Exception as error:

            print(
                "Original image OCR error:",
                error
            )


        # ----------------------------------------------------
        # Combine OCR results
        # ----------------------------------------------------

        if not ocr_results:

            return ""


        # Remove duplicate lines
        lines = []

        seen = set()

        for result in ocr_results:

            for line in result.splitlines():

                line = line.strip()

                if not line:
                    continue

                normalized = (
                    re.sub(
                        r"\s+",
                        " ",
                        line
                    )
                    .strip()
                    .lower()
                )

                if normalized not in seen:

                    seen.add(
                        normalized
                    )

                    lines.append(
                        line
                    )


        return "\n".join(
            lines
        ).strip()


    except Exception as error:

        print(
            "OCR error:",
            error
        )

        return ""
       

# ============================================================
# FILE-BASED LOGIN / AUTHENTICATION
# ============================================================

USERS_FILE = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)
    ),
    "users.json"
)

PROTECTED_API_ROUTES = {
    "/ask",
    "/upload",
    "/analyze_medicine",
    "/analyze_medicine_text",
    "/history"
}


def load_users():

    if not os.path.exists(
        USERS_FILE
    ):
        return {}

    try:

        with open(
            USERS_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(
                file
            )

        if isinstance(
            data,
            dict
        ):
            return data

        return {}

    except Exception as error:

        print(
            "Users file read error:",
            error
        )

        return {}


def save_users(
    users
):

    temp_file = (
        USERS_FILE
        + ".tmp"
    )

    with open(
        temp_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            users,
            file,
            indent=4,
            ensure_ascii=False
        )

    os.replace(
        temp_file,
        USERS_FILE
    )


def normalize_login_id(
    value
):

    value = value.strip()

    if "@" in value:

        return value.lower()

    return re.sub(
        r"[\s\-\(\)]",
        "",
        value
    )


def validate_login_id(
    value
):

    normalized = normalize_login_id(
        value
    )

    email_pattern = re.compile(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    )

    mobile_pattern = re.compile(
        r"^\+?[0-9]{10,15}$"
    )

    if email_pattern.fullmatch(
        normalized
    ):

        return (
            True,
            normalized,
            "email"
        )

    if mobile_pattern.fullmatch(
        normalized
    ):

        return (
            True,
            normalized,
            "mobile"
        )

    return (
        False,
        normalized,
        None
    )


def login_required(
    view_function
):

    @wraps(
        view_function
    )
    def wrapped(
        *args,
        **kwargs
    ):

        if "user_id" not in session:

            if request.path in PROTECTED_API_ROUTES:

                return jsonify({
                    "success": False,
                    "error": "Please login to continue.",
                    "login_required": True
                }), 401

            return redirect(
                url_for(
                    "login",
                    next=request.path
                )
            )

        return view_function(
            *args,
            **kwargs
        )

    return wrapped


# ============================================================
# LOGIN / REGISTER / LOGOUT
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "GET":

        if "user_id" in session:

            return redirect(
                url_for(
                    "home"
                )
            )

        return render_template(
            "login.html"
        )

    login_id = request.form.get(
        "login_id",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    next_url = request.form.get(
        "next",
        ""
    ).strip()

    valid, normalized_id, login_type = (
        validate_login_id(
            login_id
        )
    )

    if not valid:

        return render_template(
            "login.html",
            error=(
                "Please enter a valid email address "
                "or mobile number."
            ),
            next=next_url
        )

    if not password:

        return render_template(
            "login.html",
            error="Please enter your password.",
            next=next_url
        )

    users = load_users()

    user = users.get(
        normalized_id
    )

    if not user:

        return render_template(
            "login.html",
            error=(
                "Account not found. "
                "Please create an account first."
            ),
            next=next_url
        )

    password_hash = user.get(
        "password_hash",
        ""
    )

    if not password_hash:

        return render_template(
            "login.html",
            error="Account password is not configured. Please register again.",
            next=next_url
        )

    try:

        password_ok = check_password_hash(
            password_hash,
            password
        )

    except Exception:

        password_ok = False

    if not password_ok:

        return render_template(
            "login.html",
            error=(
                "Incorrect password. "
                "Please try again."
            ),
            next=next_url
        )

    session.clear()

    session["user_id"] = normalized_id
    session["login_id"] = normalized_id
    session["login_type"] = user.get(
        "login_type",
        login_type
    )

    if next_url.startswith(
        "/"
    ):

        return redirect(
            next_url
        )

    return redirect(
        url_for(
            "home"
        )
    )


@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "GET":

        if "user_id" in session:

            return redirect(
                url_for(
                    "home"
                )
            )

        return render_template(
            "register.html"
        )

    login_id = request.form.get(
        "login_id",
        ""
    ).strip()

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )

    valid, normalized_id, login_type = (
        validate_login_id(
            login_id
        )
    )

    if not valid:

        return render_template(
            "register.html",
            error=(
                "Please enter a valid email address "
                "or mobile number."
            )
        )

    if len(
        password
    ) < 6:

        return render_template(
            "register.html",
            error=(
                "Password must be at least 6 characters."
            )
        )

    if password != confirm_password:

        return render_template(
            "register.html",
            error="Passwords do not match."
        )

    users = load_users()

    if normalized_id in users:

        return render_template(
            "register.html",
            error=(
                "This email/mobile number is "
                "already registered."
            )
        )

    users[normalized_id] = {
        "login_id": normalized_id,
        "login_type": login_type,
        "password_hash": generate_password_hash(
            password
        )
    }

    save_users(
        users
    )

    return redirect(
        url_for(
            "login",
            registered="1"
        )
    )


@app.route(
    "/logout"
)
def logout():

    session.clear()

    return redirect(
        url_for(
            "login"
        )
    )


# ============================================================
# HOME + SEPARATE PAGES
# ============================================================

@app.route("/")
@login_required
def home():

    return render_template(
        "index.html"
    )


@app.route("/copilot")
@login_required
def copilot_page():

    return render_template(
        "copilot.html"
    )


@app.route("/report-analyzer")
@login_required
def report_analyzer_page():

    return render_template(
        "report_analyzer.html"
    )
@app.route("/medicine-analyzer")
@login_required
def medicine_analyzer_page():
    return render_template("medicine_analyzer.html")


@app.route("/analyze_medicine_text", methods=["POST"])
@login_required
def analyze_medicine_text():

    try:

        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({
                "error": "No medicine text received."
            }), 400


        text = data["text"].strip()


        if not text:
            return jsonify({
                "error": "Medicine text is empty."
            }), 400


        # Detect medicine names from OCR text
        medicines = extract_medicines(text)


        # ----------------------------------------------------
        # MEDICINE DETECTED
        # ----------------------------------------------------

        if medicines:

            medicine_name = medicines[0]


            # Ask local Gemma for general information
            ai_answer = generate_ai_health_answer(
                f"""
Give general educational information about the medicine
"{medicine_name}".

Please explain:

1. Common uses
2. Common side effects
3. Important precautions
4. When to contact a doctor

Do NOT give dosage instructions.
Do NOT prescribe the medicine.
Do NOT say that the medicine is definitely suitable
for the user.

Keep the answer simple and easy to understand.
""",
                report_context="",
                knowledge_context=""
            )


            if ai_answer:

                answer = (
                    f"💊 Medicine: {medicine_name}\n\n"
                    + ai_answer
                    + "\n\n"
                    "⚠️ Please verify the medicine name and "
                    "strength on the original package or "
                    "prescription before taking it."
                )

            else:

                answer = (
                    f"💊 Medicine detected: {medicine_name}\n\n"
                    "⚠️ I could not generate additional "
                    "medicine information right now.\n\n"
                    "Please verify the medicine name and "
                    "strength with the original package or "
                    "a pharmacist/doctor before use."
                )


        # ----------------------------------------------------
        # MEDICINE NOT DETECTED
        # ----------------------------------------------------

        else:

            answer = (
                "I could read text from the medicine image, "
                "but I could not confidently identify the "
                "medicine name.\n\n"
                "Please upload a clearer image showing the "
                "medicine name or label."
            )


        return jsonify({
            "success": True,
            "text": text,
            "medicines": medicines,
            "answer": answer
        })


    except Exception as error:

        print(
            "Medicine text analysis error:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500

       
          

@app.route("/medicine-reminder")
@login_required
def medicine_reminder():

    return render_template(
        "medicine_reminder.html"
    )


# ============================================================
# COPILOT API
# ============================================================

@app.route(
    "/ask",
    methods=["POST"]
)
@login_required
def ask():

    try:

        data = request.get_json() or {}

        question = data.get(
            "question",
            ""
        )

        report = data.get(
            "report",
            ""
        )

        result = copilot(
            question,
            report
        )

        return jsonify(
            result
        )

    except Exception as error:

        print(
            "Ask error:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# REPORT UPLOAD API
# ============================================================

@app.route(
    "/upload",
    methods=["POST"]
)
@login_required
def upload():

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "No file selected."
            }), 400


        file = request.files["file"]


        if not file.filename:

            return jsonify({
                "error": "No file selected."
            }), 400


        filename = file.filename.lower()


        if filename.endswith(".pdf"):

            text = extract_pdf_text(
                file
            )


        elif filename.endswith(".txt"):

            text = file.read().decode(
                "utf-8",
                errors="ignore"
            )


        elif filename.endswith(
            (
                ".png",
                ".jpg",
                ".jpeg",
                ".webp"
            )
        ):

            text = extract_image_text(
                file
            )

            if not text:

                return jsonify({
                    "error": (
                        "I could not reliably read text "
                        "from this image. Please use a "
                        "clearer image or install and "
                        "configure OCR support."
                    )
                }), 400


        else:

            return jsonify({
                "error": (
                    "Supported files: PDF, TXT, PNG, "
                    "JPG, JPEG and WEBP."
                )
            }), 400


        text = text.strip()


        if not text:

            return jsonify({
                "error": (
                    "No readable text was found in this file."
                )
            }), 400


        symptoms = extract_symptoms(
            text
        )


        medicines = extract_medicines(
            text
        )


        entities = extract_entities(
            text
        )


        keywords = extract_keywords(
            text
        )


        summary = summarize(
            text
        )


        save_record(
            text,
            symptoms,
            medicines,
            keywords,
            summary
        )


        return jsonify({
            "success": True,
            "filename": file.filename,
            "text": text,
            "summary": summary,
            "symptoms": symptoms,
            "medicines": medicines,
            "entities": entities,
            "keywords": keywords
        })


    except Exception as error:

        print(
            "Upload error:",
            error
        )

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# MEDICINE ANALYZER API
# ============================================================

@app.route(
    "/analyze_medicine",
    methods=["POST"]
)
@login_required
def analyze_medicine():

    try:

        if "file" not in request.files:

            return jsonify({
                "error": "Please upload a medicine image."
            }), 400


        file = request.files["file"]


        text = extract_image_text(
            file
        )


        if not text:

            return jsonify({
                "error": (
                    "I could not reliably read the medicine "
                    "name from this image. Please upload a "
                    "clear photo showing the medicine name "
                    "or label."
                )
            }), 400


        medicines = extract_medicines(
            text
        )


        if medicines:

            answer = (
                "The following medicine name(s) were "
                "detected from the image:\n\n"
                + "\n".join(
                    "• " + medicine
                    for medicine in medicines
                )
                + "\n\n"
                "The detected text should be verified "
                "against the original package or "
                "prescription before taking any medicine."
            )

        else:

            answer = (
                "I could read some text from the medicine "
                "image, but I could not confidently "
                "identify the medicine name.\n\n"
                "Detected text:\n"
                + text
            )


        return jsonify({
            "success": True,
            "text": text,
            "medicines": medicines,
            "answer": answer
        })


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "service": "Health Copilot"
    })


# ============================================================
# HISTORY
# ============================================================

@app.route("/history")
@login_required
def history():

    try:

        connection = get_connection()

        cursor = connection.cursor(
            dictionary=True
        )


        cursor.execute(
            """
            SELECT
                id,
                text,
                symptoms,
                medicines,
                keywords,
                summary
            FROM medical_records
            ORDER BY id DESC
            LIMIT 20
            """
        )


        records = cursor.fetchall()


        cursor.close()

        connection.close()


        return jsonify(
            records
        )


    except Exception as error:

        return jsonify({
            "error": str(error)
        }), 500


# ============================================================
# START SERVER
# ============================================================

if __name__ == "__main__":

    print("=" * 60)

    print(
        "Health Copilot starting..."
    )

    print(
        "Ollama Python package available:",
        OLLAMA_AVAILABLE
    )

    print(
        "AI Model:",
        OLLAMA_MODEL
    )

    print(
        "Knowledge Base Q&A:",
        len(HEALTH_KNOWLEDGE_BASE)
    )

    print("=" * 60)


    app.run(
        host="0.0.0.0",
        port=int(
            os.getenv(
                "PORT",
                "5000"
            )
        ),
        debug=False,
        use_reloader=False
    )
