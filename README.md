# Flask-applikation

En enkel Flask-applikation som demonstrerar grundläggande användarhantering:
- Registrering av användare  
- Inloggning och utloggning  
- Enkel återställning av lösenord  
- JWT-token genereras vid inloggning  

Applikationen är tänkt som ett utbildnings- och demonstrationsprojekt för att snabbt kunna spinna upp en lokal miljö med inloggningsflöde i Flask.

**Viktigt:**  
Denna applikation är inte avsedd för produktion och ska inte användas för verkliga användaruppgifter.  
Säkerhetshanteringen (lösenord, token, sessionsdata m.m.) är förenklad för tydlighetens skull.

---

## Funktioner

- Registrera nya användare  
- Logga in med användarnamn och lösenord  
- Logga ut och rensa session  
- Återställ lösenord via enkel formulärväg  
- JWT-token genereras och kan verifieras via `/verify`  

---

## Projektstruktur

```bash
applikation/
│
├── applikation.py
├── database.db     # Skapas vid uppstart av applikation
├── .env            # Skapas under steg 3
├── requirements.txt
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── register.html
│   ├── home.html
│   ├── reset_request.html
│   └── reset_password.html
│
└── static/
    ├── css/style.css
    └── img/background.jpg
```

---

## Installation & Körning

**1. Klona projektet**
```bash
git clone https://github.com/MathiasPersson84/flask-login-demo.git
cd flask-login-demo
```
**2. Installera beroenden**
```bash
pip install -r requirements.txt
```
**3. Skapa .env-fil med hemlighet**
```bash
python3 -c "import secrets; print(secrets.token_hex(16))" > .env   # Skapa en hemlig nyckel och spara den i en fil som heter ".env"
echo "FLASK_ENV=development" >> .env    # Lägg till att applikationen ska startas i DEBUG-läge
```
**4. Starta applikationen**
```bash
python3 applikation.py
```
**5. Öppna webbläsaren**  

Gå till ```http://127.0.0.1:5000```

---

## Testa JWT-token
När man skapat en användare och loggat in genereras en JWT-token.  
Testa JWT-token som utfärdas efter inloggning genom att antingen gå till ```/verify'``` eller till ex. ```https://jwt.io```.

---

## Krav

```bash
Python 3.8 eller senare
Flask 2.2 eller senare
PyJWT
python-dotenv
Werkzeug
```
Se ```requirements.txt``` för fullständig lista.

---

## Säkerhetsnotis

**Viktigt:**  
Denna applikation är inte säker och bör inte användas i produktion.
Lösenord lagras med hashing (via werkzeug.security), men inga extra skyddsåtgärder som:
- CSRF-skydd
- HTTPS
- E-postverifiering
- Rate limiting
- Avancerad JWT-hantering (refresh tokens etc.)

Den är tänkt som en grund för experiment, utbildning eller test av inloggningsflöden i Flask.

---
## Licens

Detta projekt är licensierat under MIT-licens. Se [LICENSE](LICENSE) för mer information.

