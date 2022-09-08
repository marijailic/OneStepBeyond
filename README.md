# One Step Beyond
Projekt iz kolegija **Poslovni informacijski sustavi**

---

## Opis projekta
**One Step Beyond** je web aplikacija koja simulira prodaju/kupnju karata za koncerte i obavlja sve popratne funkcije (nabrojene u nastavku) kako bi omogućila i pojednostavila prodaju/kupnju.

---

## Funkcionalnosti web aplikacije

**Osnovne funkcionalnosti (CRUD):**
* Dodavanje koncerata pomoću web forme *(create)*
* Izlistavanje podataka o svim koncertima *(reed)*
* Dohvaćanje podataka o koncertu pojedinačno *(reed)*
* Promjena podataka o koncertima pomoću web forme *(update)*
* Brisanje koncerata *(delete)*

**Specifične funkcionalnosti:**
* Prikaz statistika o koncertima
* Pretraživanje koncerata pomoću naziva izvođača
* Slanje e-mail potvrde za svaku kupljenu kartu za koncert

*Napomena:*
*Kako bi web aplikacija omogućila slanje e-mail potvrde o kupljenoj karti za koncert potrebno je kreirati .env file sa sljedećim podacima:*
1. SENDGRID_API_KEY
- Upute o kreiranju API ključa možete pronaći [ovdje](https://www.youtube.com/watch?v=DA2ubUEV1uQ&ab_channel=StudyGyaan).
3. FROM_EMAIL
- E-mail adresa koju želite koristiti kao adresu pošiljatelja.
5. TO_EMAIL
- E-mail adresa koju želite koristiti kao adresu primatelja.

---

## Struktura web aplikacije

Web aplikacija se sastoji od dva povezana servisa (**admin** i **user**).

Pomoću **API admin** moguće je dodati koncert, pregledati sve koncerte, promjeniti podatke za odabrani koncert, izbrisati odabrani koncert i pregledati statistike o koncertima.

Pomoću **API user** moguće je pregledati sve koncerte, pretraživati koncerte, pregledati podatke za odabrani koncert i kupiti kartu za odabrani koncert.

---

## Lokalno pokretanje web aplikacije

**TO DO LISTA:**

- Preuzeti sve datoteke iz repozitorija i raspakirati ih u posebnu mapu.
- Dodati u mapu *.env* file prema ranijoj uputi.
- Putem terminala navigirati u kreiranu mapu.
- Izraditi docker image pomoću sljedeće naredbe:
`docker build --tag app-pis:1.0 .`
- Pokrenuti konteiner na temelju image-a pomoću sljedeće naredbe:
`docker run -p 8080:8080 -d app-pis:1.0`
- U preglediku pristupiti aplikaciji pomoću sljedeće adrese:
`localhost:8080`