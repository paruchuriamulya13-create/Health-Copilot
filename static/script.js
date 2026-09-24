// ============================================================
// HEALTH COPILOT - SCRIPT.JS
// ============================================================

let uploadedReport = "";

let currentLanguage =
    localStorage.getItem("healthCopilotLanguage") || "en";


// ============================================================
// TRANSLATIONS
// ============================================================

const translations = {

    en: {

        title: "🩺 Health Copilot",

        description:
            "Your NLP-Based Healthcare Assistant",

        placeholder:
            "Type your health question here...",

        ask:
            "Ask Copilot",

        voice:
            "🎤 Voice",

        thinking:
            "Thinking...",

        uploading:
            "Uploading and analyzing...",

        analyzing:
            "Analyzing...",

        noQuestion:
            "Please enter a health question.",

        noFile:
            "Please select a file.",

        error:
            "Something went wrong. Please try again.",

        noSpeech:
            "Voice recognition is not supported in this browser.",

        listening:
            "Listening...",

        reportSummary:
            "Report Summary",

        symptoms:
            "Symptoms",

        medicines:
            "Medicines",

        entities:
            "Medical Entities",

        keywords:
            "Keywords",

        relevantReport:
            "Relevant Report Information",

        knowledgeBase:
            "Knowledge Base Information"

    },


    te: {

        title:
            "🩺 హెల్త్ కాపైలట్",

        description:
            "మీ NLP ఆధారిత ఆరోగ్య సహాయకుడు",

        placeholder:
            "మీ ఆరోగ్య ప్రశ్నను ఇక్కడ టైప్ చేయండి...",

        ask:
            "కాపైలట్‌ను అడగండి",

        voice:
            "🎤 వాయిస్",

        thinking:
            "ఆలోచిస్తోంది...",

        uploading:
            "అప్లోడ్ చేసి అనలైజ్ చేస్తోంది...",

        analyzing:
            "అనలైజ్ చేస్తోంది...",

        noQuestion:
            "దయచేసి ఆరోగ్య ప్రశ్నను నమోదు చేయండి.",

        noFile:
            "దయచేసి ఫైల్ ఎంచుకోండి.",

        error:
            "ఏదో సమస్య వచ్చింది. మళ్లీ ప్రయత్నించండి.",

        noSpeech:
            "ఈ బ్రౌజర్‌లో voice recognition అందుబాటులో లేదు.",

        listening:
            "వింటోంది...",

        reportSummary:
            "రిపోర్ట్ సారాంశం",

        symptoms:
            "లక్షణాలు",

        medicines:
            "మందులు",

        entities:
            "మెడికల్ అంశాలు",

        keywords:
            "ముఖ్య పదాలు",

        relevantReport:
            "రిపోర్ట్‌కు సంబంధించిన సమాచారం",

        knowledgeBase:
            "నాలెడ్జ్ బేస్ సమాచారం"

    },


    hi: {

        title:
            "🩺 हेल्थ कोपायलट",

        description:
            "आपका NLP आधारित स्वास्थ्य सहायक",

        placeholder:
            "अपना स्वास्थ्य प्रश्न यहाँ लिखें...",

        ask:
            "कोपायलट से पूछें",

        voice:
            "🎤 वॉइस",

        thinking:
            "सोच रहा है...",

        uploading:
            "अपलोड और एनालाइज़ हो रहा है...",

        analyzing:
            "एनालाइज़ हो रहा है...",

        noQuestion:
            "कृपया स्वास्थ्य प्रश्न दर्ज करें।",

        noFile:
            "कृपया फाइल चुनें।",

        error:
            "कुछ गलत हुआ। कृपया फिर से प्रयास करें।",

        noSpeech:
            "इस ब्राउज़र में वॉइस रिकग्निशन उपलब्ध नहीं है।",

        listening:
            "सुन रहा है...",

        reportSummary:
            "रिपोर्ट सारांश",

        symptoms:
            "लक्षण",

        medicines:
            "दवाइयाँ",

        entities:
            "मेडिकल जानकारी",

        keywords:
            "मुख्य शब्द",

        relevantReport:
            "रिपोर्ट से संबंधित जानकारी",

        knowledgeBase:
            "नॉलेज बेस जानकारी"

    },


    ta: {

        title:
            "🩺 ஹெல்த் கோபைலட்",

        description:
            "உங்கள் NLP அடிப்படையிலான சுகாதார உதவியாளர்",

        placeholder:
            "உங்கள் சுகாதார கேள்வியை இங்கே உள்ளிடவும்...",

        ask:
            "கோபைலட்டிடம் கேளுங்கள்",

        voice:
            "🎤 குரல்",

        thinking:
            "சிந்திக்கிறது...",

        uploading:
            "பதிவேற்றி பகுப்பாய்வு செய்கிறது...",

        analyzing:
            "பகுப்பாய்வு செய்கிறது...",

        noQuestion:
            "சுகாதார கேள்வியை உள்ளிடவும்.",

        noFile:
            "கோப்பை தேர்வு செய்யவும்.",

        error:
            "சிக்கல் ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.",

        noSpeech:
            "இந்த browser-ல் voice recognition இல்லை.",

        listening:
            "கேட்கிறது...",

        reportSummary:
            "அறிக்கை சுருக்கம்",

        symptoms:
            "அறிகுறிகள்",

        medicines:
            "மருந்துகள்",

        entities:
            "மருத்துவ தகவல்கள்",

        keywords:
            "முக்கிய சொற்கள்",

        relevantReport:
            "அறிக்கையுடன் தொடர்புடைய தகவல்",

        knowledgeBase:
            "அறிவு தள தகவல்"

    },


    kn: {

        title:
            "🩺 ಹೆಲ್ತ್ ಕೋಪೈಲಟ್",

        description:
            "ನಿಮ್ಮ NLP ಆಧಾರಿತ ಆರೋಗ್ಯ ಸಹಾಯಕ",

        placeholder:
            "ನಿಮ್ಮ ಆರೋಗ್ಯ ಪ್ರಶ್ನೆಯನ್ನು ಇಲ್ಲಿ ನಮೂದಿಸಿ...",

        ask:
            "ಕೋಪೈಲಟ್ ಅನ್ನು ಕೇಳಿ",

        voice:
            "🎤 ವಾಯ್ಸ್",

        thinking:
            "ಆಲೋಚಿಸುತ್ತಿದೆ...",

        uploading:
            "ಅಪ್ಲೋಡ್ ಮಾಡಿ ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",

        analyzing:
            "ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",

        noQuestion:
            "ದಯವಿಟ್ಟು ಆರೋಗ್ಯ ಪ್ರಶ್ನೆಯನ್ನು ನಮೂದಿಸಿ.",

        noFile:
            "ದಯವಿಟ್ಟು ಫೈಲ್ ಆಯ್ಕೆಮಾಡಿ.",

        error:
            "ಏನೋ ತಪ್ಪಾಗಿದೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",

        noSpeech:
            "ಈ browser ನಲ್ಲಿ voice recognition ಲಭ್ಯವಿಲ್ಲ.",

        listening:
            "ಕೇಳುತ್ತಿದೆ...",

        reportSummary:
            "ವರದಿ ಸಾರಾಂಶ",

        symptoms:
            "ಲಕ್ಷಣಗಳು",

        medicines:
            "ಔಷಧಿಗಳು",

        entities:
            "ವೈದ್ಯಕೀಯ ಮಾಹಿತಿಗಳು",

        keywords:
            "ಮುಖ್ಯ ಪದಗಳು",

        relevantReport:
            "ವರದಿಗೆ ಸಂಬಂಧಿಸಿದ ಮಾಹಿತಿ",

        knowledgeBase:
            "ಜ್ಞಾನ ಆಧಾರಿತ ಮಾಹಿತಿ"

    }

};


// ============================================================
// LANGUAGE
// ============================================================

function changeLanguage() {

    const languageElement =
        document.getElementById("language");

    if (!languageElement) {
        return;
    }

    currentLanguage =
        languageElement.value || "en";

    localStorage.setItem(
        "healthCopilotLanguage",
        currentLanguage
    );

    const t =
        translations[currentLanguage] ||
        translations.en;

    document.documentElement.lang =
        currentLanguage;

}


// ============================================================
// VOICE LANGUAGE
// ============================================================

function getVoiceLanguage() {

    const languages = {

        en: "en-IN",

        te: "te-IN",

        hi: "hi-IN",

        ta: "ta-IN",

        kn: "kn-IN"

    };

    return (
        languages[currentLanguage]
        || "en-IN"
    );
}


// ============================================================
// VOICE INPUT
// ============================================================

function startVoice() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;

    if (!SpeechRecognition) {

        const t =
            translations[currentLanguage]
            || translations.en;

        alert(t.noSpeech);

        return;
    }

    const recognition =
        new SpeechRecognition();

    recognition.lang =
        getVoiceLanguage();

    recognition.interimResults =
        false;

    recognition.continuous =
        false;


    const questionBox =
        document.getElementById("question");

    const voiceButton =
        document.getElementById("voiceButton");

    const t =
        translations[currentLanguage]
        || translations.en;


    if (voiceButton) {

        voiceButton.textContent =
            t.listening;

    }


    recognition.start();


    recognition.onresult =
        function(event) {

            const text =
                event.results[0][0]
                .transcript;

            if (questionBox) {

                questionBox.value =
                    text;

            }

        };


    recognition.onerror =
        function() {

            if (voiceButton) {

                voiceButton.textContent =
                    t.voice;

            }

        };


    recognition.onend =
        function() {

            if (voiceButton) {

                voiceButton.textContent =
                    t.voice;

            }

        };

}


// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent =
        value == null
            ? ""
            : String(value);

    return div.innerHTML;
}


// ============================================================
// ASK COPILOT
// ============================================================

async function askCopilot() {

    const questionElement =
        document.getElementById("question");

    const resultElement =
        document.getElementById(
            "copilotResult"
        );

    if (
        !questionElement ||
        !resultElement
    ) {
        return;
    }


    const question =
        questionElement.value.trim();


    const t =
        translations[currentLanguage]
        || translations.en;


    if (!question) {

        resultElement.innerHTML =
            `<div class="error">
                ${escapeHTML(t.noQuestion)}
            </div>`;

        return;
    }


    resultElement.innerHTML =
        `<div class="loading">
            ${escapeHTML(t.thinking)}
        </div>`;


    try {

        const response =
            await fetch(
                "/ask",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        question:
                            question,

                        report:
                            uploadedReport

                    })

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error
                || "Request failed"
            );

        }


        let html = "";


        if (data.answer) {

            html += `
                <div class="answer-box">

                    <h3>
                        💬 Answer
                    </h3>

                    <p>
                        ${escapeHTML(
                            data.answer
                        ).replace(
                            /\n/g,
                            "<br>"
                        )}
                    </p>

                </div>
            `;

        }


        if (data.intent) {

            html += `
                <div class="info-box">

                    <strong>
                        Intent:
                    </strong>

                    ${escapeHTML(
                        data.intent
                    )}

                </div>
            `;

        }


        if (
            data.keywords &&
            data.keywords.length
        ) {

            html += `
                <div class="info-box">

                    <strong>
                        ${escapeHTML(
                            t.keywords
                        )}:
                    </strong>

                    ${data.keywords
                        .map(
                            item =>
                                `<span class="tag">
                                    ${escapeHTML(item)}
                                </span>`
                        )
                        .join(" ")
                    }

                </div>
            `;

        }


        if (
            data.entities &&
            data.entities.length
        ) {

            html += `
                <div class="info-box">

                    <strong>
                        ${escapeHTML(
                            t.entities
                        )}:
                    </strong>

                    ${data.entities
                        .map(
                            item =>
                                `<span class="tag">
                                    ${escapeHTML(item)}
                                </span>`
                        )
                        .join(" ")
                    }

                </div>
            `;

        }


        if (
            data.relevant_report &&
            data.relevant_report.length
        ) {

            html += `
                <div class="report-info">

                    <h3>
                        📄
                        ${escapeHTML(
                            t.relevantReport
                        )}
                    </h3>

                    <ul>

                        ${data.relevant_report
                            .map(
                                item =>
                                    `<li>
                                        ${escapeHTML(item)}
                                    </li>`
                            )
                            .join("")
                        }

                    </ul>

                </div>
            `;

        }


        if (
            data.knowledge_base &&
            data.knowledge_base.length
        ) {

            html += `
                <div class="knowledge-info">

                    <h3>
                        📚
                        ${escapeHTML(
                            t.knowledgeBase
                        )}
                    </h3>
            `;


            data.knowledge_base.forEach(
                item => {

                    html += `
                        <div class="knowledge-item">

                            <strong>
                                ${escapeHTML(
                                    item.question
                                    || ""
                                )}
                            </strong>

                            <p>
                                ${escapeHTML(
                                    item.answer
                                    || ""
                                )}
                            </p>

                        </div>
                    `;

                }
            );


            html += `
                </div>
            `;

        }


        resultElement.innerHTML =
            html;

    }
    catch (error) {

        console.error(error);

        resultElement.innerHTML =
            `<div class="error">
                ${escapeHTML(t.error)}
            </div>`;

    }

}


// ============================================================
// REPORT UPLOAD
// ============================================================

async function uploadDocument() {

    const fileElement =
        document.getElementById("file");

    const resultElement =
        document.getElementById(
            "documentResult"
        );


    const t =
        translations[currentLanguage]
        || translations.en;


    if (
        !fileElement ||
        !fileElement.files ||
        !fileElement.files.length
    ) {

        if (resultElement) {

            resultElement.innerHTML =
                `<div class="error">
                    ${escapeHTML(t.noFile)}
                </div>`;

        }

        return;
    }


    const file =
        fileElement.files[0];


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    if (resultElement) {

        resultElement.innerHTML =
            `<div class="loading">
                ${escapeHTML(t.uploading)}
            </div>`;

    }


    try {

        const response =
            await fetch(
                "/upload",
                {

                    method: "POST",

                    body: formData

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error
                || "Upload failed"
            );

        }


        uploadedReport =
            data.text
            || "";


        let html = "";


        if (data.summary) {

            html += `
                <div class="answer-box">

                    <h3>
                        📋
                        ${escapeHTML(
                            t.reportSummary
                        )}
                    </h3>

                    <p>
                        ${escapeHTML(
                            data.summary
                        )}
                    </p>

                </div>
            `;

        }


        if (
            data.symptoms &&
            data.symptoms.length
        ) {

            html += `
                <div class="info-box">

                    <strong>
                        ${escapeHTML(
                            t.symptoms
                        )}:
                    </strong>

                    ${data.symptoms
                        .map(
                            item =>
                                `<span class="tag">
                                    ${escapeHTML(item)}
                                </span>`
                        )
                        .join(" ")
                    }

                </div>
            `;

        }


        if (
            data.medicines &&
            data.medicines.length
        ) {

            html += `
                <div class="info-box">

                    <strong>
                        ${escapeHTML(
                            t.medicines
                        )}:
                    </strong>

                    ${data.medicines
                        .map(
                            item =>
                                `<span class="tag">
                                    ${escapeHTML(item)}
                                </span>`
                        )
                        .join(" ")
                    }

                </div>
            `;

        }


        if (
            data.entities &&
            data.entities.length
        ) {

            html += `
                <div class="info-box">

                    <strong>
                        ${escapeHTML(
                            t.entities
                        )}:
                    </strong>

                    ${data.entities
                        .map(
                            item =>
                                `<span class="tag">
                                    ${escapeHTML(item)}
                                </span>`
                        )
                        .join(" ")
                    }

                </div>
            `;

        }


        if (
            data.keywords &&
            data.keywords.length
        ) {

            html += `
                <div class="info-box">

                    <strong>
                        ${escapeHTML(
                            t.keywords
                        )}:
                    </strong>

                    ${data.keywords
                        .map(
                            item =>
                                `<span class="tag">
                                    ${escapeHTML(item)}
                                </span>`
                        )
                        .join(" ")
                    }

                </div>
            `;

        }


        resultElement.innerHTML =
            html;

    }
    catch (error) {

        console.error(error);

        resultElement.innerHTML =
            `<div class="error">
                ${escapeHTML(
                    error.message
                    || t.error
                )}
            </div>`;

    }

}


// ============================================================
// MEDICINE ANALYZER
// ============================================================

async function analyzeMedicine() {

    const fileInput =
        document.getElementById(
            "medicineFile"
        );

    const result =
        document.getElementById(
            "medicineResult"
        );

    const button =
        document.getElementById(
            "medicineButton"
        );


    if (
        !fileInput ||
        !fileInput.files.length
    ) {

        result.innerHTML =
            `<div class="error">
                Please select a medicine image.
            </div>`;

        return;
    }


    const file =
        fileInput.files[0];


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    button.disabled =
        true;

    button.textContent =
        "🔍 Analyzing...";


    result.innerHTML =
        `<div class="loading">
            Reading medicine image...
        </div>`;


    try {

        const response =
            await fetch(
                "/analyze_medicine",
                {

                    method: "POST",

                    body: formData

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error
                || "Medicine analysis failed"
            );

        }


        let html = "";


        if (data.answer) {

            html += `
                <div class="answer-box">

                    <h3>
                        💊 Medicine Result
                    </h3>

                    <p>
                        ${escapeHTML(
                            data.answer
                        ).replace(
                            /\n/g,
                            "<br>"
                        )}
                    </p>

                </div>
            `;

        }


        if (data.text) {

            html += `
                <div class="info-box">

                    <strong>
                        Detected Text:
                    </strong>

                    <p>
                        ${escapeHTML(
                            data.text
                        )}
                    </p>

                </div>
            `;

        }


        result.innerHTML =
            html;

    }
    catch (error) {

        result.innerHTML =
            `<div class="error">
                ${escapeHTML(
                    error.message
                )}
            </div>`;

    }
    finally {

        button.disabled =
            false;

        button.textContent =
            "🔍 Read Medicine";

    }

}


// ============================================================
// X-RAY ANALYZER
// ============================================================

async function analyzeXray() {

    const fileInput =
        document.getElementById(
            "xrayFile"
        );

    const result =
        document.getElementById(
            "xrayResult"
        );

    const preview =
        document.getElementById(
            "xrayPreview"
        );

    const button =
        document.getElementById(
            "xrayButton"
        );


    if (
        !fileInput ||
        !fileInput.files.length
    ) {

        result.innerHTML =
            `<div class="error">
                Please select an X-Ray image.
            </div>`;

        return;
    }


    const file =
        fileInput.files[0];


    const imageURL =
        URL.createObjectURL(
            file
        );


    preview.innerHTML = `
        <img
            src="${imageURL}"
            alt="Uploaded X-Ray">
    `;


    const formData =
        new FormData();

    formData.append(
        "file",
        file
    );


    button.disabled =
        true;

    button.textContent =
        "🔍 Analyzing...";


    result.innerHTML =
        `<div class="loading">
            Uploading X-Ray...
        </div>`;


    try {

        const response =
            await fetch(
                "/analyze_xray",
                {

                    method: "POST",

                    body: formData

                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.error
                || "X-Ray analysis failed"
            );

        }


        result.innerHTML = `
            <div class="answer-box">

                <h3>
                    🩻 X-Ray Result
                </h3>

                <p>
                    ${escapeHTML(
                        data.answer
                    ).replace(
                        /\n/g,
                        "<br>"
                    )}
                </p>

            </div>
        `;

    }
    catch (error) {

        result.innerHTML =
            `<div class="error">
                ${escapeHTML(
                    error.message
                )}
            </div>`;

    }
    finally {

        button.disabled =
            false;

        button.textContent =
            "🔍 Analyze X-Ray";

    }

}


// ============================================================
// PAGE LOAD
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        const languageElement =
            document.getElementById(
                "language"
            );

        if (languageElement) {

            languageElement.value =
                currentLanguage;

        }

    }
);

/* =========================================================
   MEDICINE REMINDER
   ========================================================= */

let medicineReminders =
    JSON.parse(localStorage.getItem("medicineReminders")) || [];


/* ---------------------------------------------------------
   GO HOME
   --------------------------------------------------------- */

function goHome() {
    window.location.href = "/";
}


/* ---------------------------------------------------------
   REQUEST NOTIFICATION PERMISSION
   --------------------------------------------------------- */

function requestNotificationPermission() {

    if (!("Notification" in window)) {
        alert("This browser does not support notifications.");
        return;
    }

    Notification.requestPermission().then(function(permission) {

        if (permission === "granted") {
            alert("Medicine notifications enabled.");
        } else {
            alert("Please allow notifications in your browser settings.");
        }

    });
}


/* ---------------------------------------------------------
   ADD MEDICINE REMINDER
   --------------------------------------------------------- */

function addMedicineReminder() {

    const name =
        document.getElementById("medicineName").value.trim();

    const time =
        document.getElementById("medicineTime").value;

    const frequency =
        document.getElementById("medicineFrequency").value;

    const dose =
        document.getElementById("medicineDose").value.trim();


    if (!name) {
        alert("Please enter the medicine name.");
        return;
    }

    if (!time) {
        alert("Please select a reminder time.");
        return;
    }


    const reminder = {

        id: Date.now(),

        name: name,

        time: time,

        frequency: frequency,

        dose: dose,

        lastNotified: ""

    };


    medicineReminders.push(reminder);

    saveMedicineReminders();

    displayReminderMessage(
        "Medicine reminder added successfully."
    );


    document.getElementById("medicineName").value = "";

    document.getElementById("medicineTime").value = "";

    document.getElementById("medicineDose").value = "";

    document.getElementById("medicineFrequency").value = "daily";


    loadMedicineReminders();
}


/* ---------------------------------------------------------
   SAVE REMINDERS
   --------------------------------------------------------- */

function saveMedicineReminders() {

    localStorage.setItem(
        "medicineReminders",
        JSON.stringify(medicineReminders)
    );
}


/* ---------------------------------------------------------
   LOAD REMINDERS
   --------------------------------------------------------- */

function loadMedicineReminders() {

    const list =
        document.getElementById("reminderList");

    if (!list) {
        return;
    }


    medicineReminders =
        JSON.parse(
            localStorage.getItem("medicineReminders")
        ) || [];


    if (medicineReminders.length === 0) {

        list.innerHTML = `
            <div class="empty-reminders">
                No medicine reminders added yet.
            </div>
        `;

        return;
    }


    list.innerHTML = "";


    medicineReminders.forEach(function(reminder) {

        const item =
            document.createElement("div");

        item.className = "medicine-reminder-item";


        let frequencyText = "Every Day";


        if (reminder.frequency === "weekdays") {
            frequencyText = "Monday - Friday";
        }

        if (reminder.frequency === "weekends") {
            frequencyText = "Saturday - Sunday";
        }

        if (reminder.frequency === "once") {
            frequencyText = "Once";
        }


        item.innerHTML = `

            <div class="medicine-reminder-icon">
                💊
            </div>

            <div class="medicine-reminder-details">

                <h3>
                    ${escapeHTML(reminder.name)}
                </h3>

                <p>
                    ⏰ <strong>${escapeHTML(reminder.time)}</strong>
                </p>

                <p>
                    📅 ${frequencyText}
                </p>

                ${
                    reminder.dose
                    ? `<p>💊 Dose: ${escapeHTML(reminder.dose)}</p>`
                    : ""
                }

            </div>

            <div class="medicine-reminder-actions">

                <button
                    onclick="testMedicineReminder(${reminder.id})"
                >
                    🔔 Test
                </button>

                <button
                    class="delete-button"
                    onclick="deleteMedicineReminder(${reminder.id})"
                >
                    🗑️ Delete
                </button>

            </div>
        `;


        list.appendChild(item);

    });
}


/* ---------------------------------------------------------
   DELETE REMINDER
   --------------------------------------------------------- */

function deleteMedicineReminder(id) {

    const confirmed =
        confirm("Delete this medicine reminder?");

    if (!confirmed) {
        return;
    }


    medicineReminders =
        medicineReminders.filter(function(reminder) {

            return reminder.id !== id;

        });


    saveMedicineReminders();

    loadMedicineReminders();
}


/* ---------------------------------------------------------
   TEST REMINDER
   --------------------------------------------------------- */

function testMedicineReminder(id) {

    const reminder =
        medicineReminders.find(function(item) {

            return item.id === id;

        });


    if (!reminder) {
        return;
    }


    showMedicineNotification(reminder);
}


/* ---------------------------------------------------------
   SHOW NOTIFICATION
   --------------------------------------------------------- */

function showMedicineNotification(reminder) {

    const title =
        "💊 Medicine Reminder";


    const message =
        "Time to take " +
        reminder.name +
        (reminder.dose
            ? " - " + reminder.dose
            : "");


    if (
        "Notification" in window &&
        Notification.permission === "granted"
    ) {

        new Notification(title, {

            body: message,

            icon: "/static/medicine-icon.png"

        });

    } else {

        alert(
            title +
            "\n\n" +
            message
        );

    }
}


/* ---------------------------------------------------------
   CHECK REMINDERS
   --------------------------------------------------------- */

function checkMedicineReminders() {

    if (medicineReminders.length === 0) {
        return;
    }


    const now =
        new Date();


    const currentTime =
        String(now.getHours()).padStart(2, "0") +
        ":" +
        String(now.getMinutes()).padStart(2, "0");


    const today =
        now.toISOString().split("T")[0];


    const day =
        now.getDay();


    medicineReminders.forEach(function(reminder) {

        if (reminder.time !== currentTime) {
            return;
        }


        if (reminder.lastNotified === today) {
            return;
        }


        let shouldNotify = true;


        if (reminder.frequency === "weekdays") {

            shouldNotify =
                day >= 1 && day <= 5;

        }


        if (reminder.frequency === "weekends") {

            shouldNotify =
                day === 0 || day === 6;

        }


        if (!shouldNotify) {
            return;
        }


        showMedicineNotification(reminder);


        reminder.lastNotified = today;


        if (reminder.frequency === "once") {

            medicineReminders =
                medicineReminders.filter(
                    function(item) {
                        return item.id !== reminder.id;
                    }
                );

        }

    });


    saveMedicineReminders();

    loadMedicineReminders();
}


/* ---------------------------------------------------------
   ESCAPE HTML
   --------------------------------------------------------- */

function escapeHTML(value) {

    return String(value)

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");
}


/* ---------------------------------------------------------
   MESSAGE
   --------------------------------------------------------- */

function displayReminderMessage(message) {

    const box =
        document.getElementById("reminderMessage");


    if (!box) {
        return;
    }


    box.style.display = "block";

    box.innerHTML =
        "✅ " + escapeHTML(message);


    setTimeout(function() {

        box.style.display = "none";

    }, 3000);
}


/* ---------------------------------------------------------
   START REMINDER CHECKER
   --------------------------------------------------------- */

setInterval(
    checkMedicineReminders,
    30000
);
