import uuid
from datetime import datetime

from app.customers.dental_office import DentalOffice
from app.database.store import PromptStore
from app.proxy.providers.gateway import provider_for
from app.proxy.providers.swap_note import SwapNote
from app.scrub.catalog import RedactionCatalog
from app.scrub.sensitive_span import SensitiveSpan
from app.security import checkGatewayKey

_sessions = {}
_store = PromptStore()
_catalog = RedactionCatalog()


class Prompt:
    def __init__(self):
        self.id = uuid.uuid4().hex
        self.text = ""
        self.sentAt = None
        self.spans = []
        self.confirmed = False
        self.choice = None
        self.outgoing = None
        self.warning = None
        self.swapNote = None
        self.model = None
        self.office = None

    def accept(self, text: str) -> str:
        self.text = text
        return "accepted"

    def scan(self):
        return _catalog.findSpans(self.text)

    def flagSensitive(self, foundSpans) -> str:
        self.spans = [
            SensitiveSpan(item["start"], item["end"], item["text"], item["fakeWord"])
            for item in foundSpans
        ]
        return "flagged"

    def countSecrets(self) -> int:
        return sum(1 for span in self.spans if span.flagged)

    def confirmRedaction(self) -> str:
        self.confirmed = True
        return "permitted"

    def applyRedaction(self) -> str:
        self.choice = "apply"
        text = self.text
        # Later spans keep their indexes only if earlier text has not moved yet.
        for span in sorted(self.spans, key=lambda item: item.start, reverse=True):
            mapping = span.replace()
            text = text[: span.start] + mapping.pseudo + text[span.end :]
            span.flagged = False
        self.outgoing = text
        self.warning = None
        return text

    def keepOriginal(self) -> str:
        self.choice = "keep"
        for span in self.spans:
            span.removeFlag()
        self.outgoing = self.text
        self.warning = (
            "You chose to keep flagged information. "
            "It will be sent to the AI company at your own risk."
        )
        return self.text

    def send(self, text: str):
        if not self.confirmed:
            return {
                "ok": False,
                "message": "This prompt is held until you confirm. It was not sent.",
            }
        provider = provider_for(self.model)
        if provider is None:
            return {
                "ok": False,
                "message": f"Unknown model '{self.model}'. Nothing was sent.",
            }
        reply = provider.complete(text)
        self.sentAt = datetime.now()
        fake_words = []
        if self.choice == "apply":
            fake_words = [span.mapping.pseudo for span in self.spans if span.mapping]
        self.swapNote = SwapNote(self.model, fake_words)
        _store.save_confirmation(
            prompt_text=self.text,
            text_sent=text,
            secret_count=len(self.spans),
            choice=self.choice,
            model=self.model,
        )
        return {"ok": True, "reply": reply}


def begin_prompt(request):
    if not checkGatewayKey():
        return {"ok": False, "message": "Gateway key check failed."}
    text = (request.text or "").strip()
    if not text:
        return {"ok": False, "message": "Enter a prompt before submitting."}
    office = DentalOffice("Cedar Dental", "D-104", allowed=request.officeActive)
    if not office.canSend():
        return {
            "ok": False,
            "message": (
                "Cedar Dental is not allowed to send prompts. "
                "Nothing was sent to the AI company."
            ),
        }
    prompt = Prompt()
    prompt.model = request.model
    prompt.office = office
    prompt.accept(text)
    found = prompt.scan()
    prompt.flagSensitive(found)
    _sessions[prompt.id] = prompt
    return {
        "ok": True,
        "promptId": prompt.id,
        "secretCount": prompt.countSecrets(),
        "subscriptionLength": office.subscription.length(),
        "office": office.name,
        "flagged": [
            {
                "start": span.start,
                "end": span.end,
                "text": span.original,
                "placeholder": span.fakeWord.fakeWord,
            }
            for span in prompt.spans
        ],
    }


def confirm_prompt(prompt_id: str, choice: str, model=None):
    prompt = _sessions.get(prompt_id)
    if prompt is None:
        return {"ok": False, "message": "That prompt expired. Submit it again."}
    if model:
        prompt.model = model
    prompt.confirmRedaction()
    if choice == "apply":
        outgoing = prompt.applyRedaction()
    elif choice == "keep":
        outgoing = prompt.keepOriginal()
    else:
        prompt.confirmed = False
        return {"ok": False, "message": "Choose apply redaction or keep original."}
    sent = prompt.send(outgoing)
    if not sent["ok"]:
        return sent
    return {
        "ok": True,
        "choice": prompt.choice,
        "warning": prompt.warning,
        "textSent": outgoing,
        "reply": sent["reply"],
        "secretCount": len(prompt.spans),
        "model": prompt.swapNote.model,
        "fakeWords": prompt.swapNote.fakeWordUsed(),
        "sentAt": prompt.sentAt.isoformat(timespec="seconds"),
    }


def flagged_report():
    return _store.flagged_report()
