async function translate() {
    const text = document.getElementById("textInput").value;
    const sourceLanguage = document.getElementById("sourceLanguage").value;
    const targetLanguage = document.getElementById("targetLanguage").value;

    const message = document.getElementById("message");
    const translatedOutput = document.getElementById("translatedOutput");

    message.innerText = "";
    translatedOutput.innerText = "Translating...";

    try{
        const response = await fetch("/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text,
                source_language: sourceLanguage,
                target_language: targetLanguage
            })
        }),

        const data = await response.json();

        if (data.success){
            translatedOutput.innerText = data.translated_text;
        } else {
            translatedOutput.innerText = "Your translation will appear here.";
            message.innerText = data.message;
        }
    } catch (error){
        translatedOutput.innerText = "Your translation will appear here.";
        message.innerText = "Something went wrong. Please try again.";
    }
}

function copyText(){
    const translatedText = document.getElementById("translatedOutput").innerText;

    if (
        translatedText == "Your translation will appear here." ||
        translatedText == "Translating"
    ){
        alert("There is no translated text to copy.");
        return;
    }

    navigator.clipboard.writeText(translatedText);
    alert("Translation copied to clipboard.")
}

function speakText(){
    const translatedText = document.getElementById("translatedOutput").innerText;

    if (
        translatedText == "Your translation will appear here." ||
        translatedText == "Translating"
    ){
        alert("There is no translated text to read.");
        return;
    }

    const speech = new SpeechSynthesisUtterance(translatedText);
    window.speechSynthesis.speak(speech);
}