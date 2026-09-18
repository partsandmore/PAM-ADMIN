# -*- coding: utf-8 -*-
"""Third pass: strings that only appear on the chat page.

The conversation uses typographic apostrophes (U+2019), so those keys are
written with ’ rather than a straight quote - the straight-quote
spelling would never match.
"""

CHAT = {
    # image alt text
    "Icon": "Symbol",
    "image": "Bild",
    "Image": "Bild",
    "Img": "Bild",
    "img": "Bild",
    "Logo": "Logo",
    "Photo": "Foto",
    "Camera": "Kamera",
    "Audio": "Audio",
    "Contact": "Kontakt",

    # chat actions
    "Mark as Favourite": "Als Favorit markieren",
    "Mark as Unread": "Als ungelesen markieren",
    "Archive Chat": "Chat archivieren",
    "Archeive Chat": "Chat archivieren",      # template's own typo
    "Pin Chat": "Chat anheften",
    "Pin Chats": "Chats anheften",
    "Mute Notification": "Benachrichtigung stummschalten",
    "Disappearing Message": "Verschwindende Nachricht",
    "Clear Message": "Nachrichten löschen",
    "Delete Chat": "Chat löschen",
    "Block": "Blockieren",
    "Copy": "Kopieren",
    "All Chats": "Alle Chats",
    "Online": "Online",
    "You": "Sie",
    "is typing": "schreibt gerade",

    # calls
    "Missed Video Call": "Verpasster Videoanruf",
    "Incoming Video Call": "Eingehender Videoanruf",

    # inputs
    "Search For Contacts or Messages": "Kontakte oder Nachrichten suchen",
    "Search Contacts": "Kontakte suchen",
    "Type Your Message": "Nachricht eingeben",

    # days / dates in the thread
    "Sunday": "Sonntag",
    "Monday": "Montag",
    "Tuesday": "Dienstag",
    "Wednesday": "Mittwoch",
    "Thursday": "Donnerstag",
    "Friday": "Freitag",
    "Saturday": "Samstag",
    "Today, July 24": "Heute, 24. Juli",

    # demo person on this page
    "Edward Lietz": "Eduard Leitz",

    # the demo conversation
    "Hi How are you \U0001F525": "Hallo, wie geht es dir \U0001F525",
    "Haha oh man \U0001F525": "Haha, oh Mann \U0001F525",
    "Do you know which...": "Weißt du, welche …",
    "Do you have a moment?": "Hast du einen Moment?",
    "Hi John, I wanted to update you on a new company policy regarding remote work.":
        "Hallo Jan, ich wollte dich über eine neue Regelung zum mobilen Arbeiten "
        "informieren.",
    "Sure, Sarah. What’s the new policy?":
        "Klar, Sabine. Wie lautet die neue Regelung?",
    "Starting next month, we’ll be implementing a hybrid work model. Employees "
    "can work from home up to three days a week.":
        "Ab dem nächsten Monat führen wir ein hybrides Arbeitsmodell ein. "
        "Mitarbeiter können bis zu drei Tage pro Woche von zu Hause arbeiten.",
    "That sounds great! Are there any specific requirements for tracking our hours "
    "when working remotely?":
        "Das klingt gut! Gibt es besondere Vorgaben für die Zeiterfassung im "
        "mobilen Arbeiten?",
    "Yes, we’ll be using a time-tracking tool to log hours. You’ll need to "
    "ensure you’re logged in during your scheduled work hours.":
        "Ja, wir nutzen ein Zeiterfassungswerkzeug. Du musst während deiner "
        "geplanten Arbeitszeit angemeldet sein.",
    "Got it. Do we need to fill out any forms to start working remotely?":
        "Verstanden. Müssen wir Formulare ausfüllen, um mobil arbeiten zu dürfen?",
}
