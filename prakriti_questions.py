"""
59-Question Prakriti Assessment Questionnaire
English + Gujarati (ગુજરાતી)
"""

PRAKRITI_QUESTIONS = {
    "personal_info": [
        {
            "id": 1,
            "type": "text",
            "question_en": "First Name",
            "question_gu": "પ્રથમ નામ",
            "field": "first_name"
        },
        {
            "id": 2,
            "type": "text",
            "question_en": "Middle Name",
            "question_gu": "મધ્ય નામ",
            "field": "middle_name"
        },
        {
            "id": 3,
            "type": "text",
            "question_en": "Last Name",
            "question_gu": "છેલ્લું નામ",
            "field": "last_name"
        },
        {
            "id": 4,
            "type": "radio",
            "question_en": "Gender",
            "question_gu": "લિંગ",
            "field": "gender",
            "options": [
                {"value": "male", "label_en": "Male", "label_gu": "પુરુષ", "vata": 0, "pitta": 0, "kapha": 0},
                {"value": "female", "label_en": "Female", "label_gu": "સ્ત્રી", "vata": 0, "pitta": 0, "kapha": 0}
            ]
        },
        {
            "id": 5,
            "type": "textarea",
            "question_en": "Permanent Address",
            "question_gu": "કાયમી સરનામું",
            "field": "address"
        },
        {
            "id": 6,
            "type": "tel",
            "question_en": "Phone Number",
            "question_gu": "ફોન નંબર",
            "field": "phone"
        },
        {
            "id": 7,
            "type": "email",
            "question_en": "Email Address",
            "question_gu": "ઈમેલ સરનામું",
            "field": "email"
        },
        {
            "id": 8,
            "type": "number",
            "question_en": "Age",
            "question_gu": "ઉંમર",
            "field": "age"
        },
        {
            "id": 9,
            "type": "date",
            "question_en": "Date",
            "question_gu": "તારીખ",
            "field": "date"
        },
        {
            "id": 10,
            "type": "radio",
            "question_en": "Are you willing to participate in genetic analysis in Ayurgenomics project?",
            "question_gu": "શું તમે આયુર્જેનોમિક્સ પ્રોજેક્ટમાં આનુવંશિક વિશ્લેષણમાં ભાગ લેવા તૈયાર છો?",
            "field": "genetic_consent",
            "options": [
                {"value": "yes", "label_en": "Yes", "label_gu": "હા", "vata": 0, "pitta": 0, "kapha": 0},
                {"value": "no", "label_en": "No", "label_gu": "ના", "vata": 0, "pitta": 0, "kapha": 0}
            ]
        }
    ],
    "body_measurements": [
        {
            "id": 11,
            "type": "number",
            "question_en": "Weight (kg)",
            "question_gu": "વજન (કિલો)",
            "field": "weight"
        },
        {
            "id": 12,
            "type": "number",
            "question_en": "Height (cm)",
            "question_gu": "ઊંચાઈ (સેમી)",
            "field": "height"
        }
    ],
    "body_structure": [
        {
            "id": 13,
            "type": "radio",
            "question_en": "Body Frame",
            "question_gu": "શરીર રચના",
            "field": "body_frame",
            "options": [
                {"value": "narrow", "label_en": "Narrow", "label_gu": "સાંકડું", "vata": 3, "pitta": 0, "kapha": 0},
                {"value": "medium", "label_en": "Medium", "label_gu": "મધ્યમ", "vata": 0, "pitta": 3, "kapha": 0},
                {"value": "wide", "label_en": "Wide", "label_gu": "પહોળું", "vata": 0, "pitta": 0, "kapha": 3}
            ]
        },
        {
            "id": 14,
            "type": "radio",
            "question_en": "Body Build (Bulk)",
            "question_gu": "શરીર બાંધકામ",
            "field": "body_build",
            "options": [
                {"value": "weak", "label_en": "Weakly developed", "label_gu": "ઓછું વિકસિત", "vata": 3, "pitta": 0, "kapha": 0},
                {"value": "moderate", "label_en": "Moderately developed", "label_gu": "મધ્યમ વિકસિત", "vata": 0, "pitta": 3, "kapha": 0},
                {"value": "well", "label_en": "Well developed", "label_gu": "સારી રીતે વિકસિત", "vata": 0, "pitta": 0, "kapha": 3}
            ]
        },
        {
            "id": 15,
            "type": "radio",
            "question_en": "Body Build (Musculature)",
            "question_gu": "પેશી રચના",
            "field": "musculature",
            "options": [
                {"value": "thin", "label_en": "Thin musculature", "label_gu": "પાતળી પેશીઓ", "vata": 3, "pitta": 0, "kapha": 0},
                {"value": "soft", "label_en": "Soft and loosely knitted musculature", "label_gu": "નરમ પેશીઓ", "vata": 0, "pitta": 2, "kapha": 1},
                {"value": "firm", "label_en": "Smooth and firmly knitted musculature", "label_gu": "મજબૂત પેશીઓ", "vata": 0, "pitta": 1, "kapha": 2}
            ]
        }
    ]
}
