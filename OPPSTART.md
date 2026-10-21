# Oppsummering og oppstart

Oppdatert 21. oktober 2026.

## Hva vi skal gjøre

Sigurd arbeider videre med skipsdeteksjon som et selvstendig spor. Mattias arbeider med antenne/mottak. Sigurds minimumsmål er et eget lite CNN for skip/bakgrunn og en finjustert YOLO-modell for flere skip med bokser. Egen prediksjon av én boks er et tilleggsmål. Arbeidet gjøres trinnvis med forklaring før nye modelldeler.

Dette dokumentet supplerer PLAN.md. Den tidligere ideen om å knytte KI direkte til antennebildene er ikke et krav for Sigurds spor. Nå er oppstart og struktur godkjent; dataklargjøring og modellarbeid kommer i senere steg.

## Begrepene og dataflyten

- Ultralytics er Python-pakken vi bruker til YOLO-trening og prediksjon.
- YOLO er modellfamilien som finner objekter og deres bokser.
- COCO er både et separat bildedatasett og et format for markeringer. Her bruker vi COCO-formatet for HRSID. Vi trenger ikke laste ned COCO-bildedatasettet.
- HRSID er våre SAR-bilder med skipsmarkeringer. SAR-bilder viser radarrefleksjoner.
- JSON er et tekstformat som lagrer strukturerte data, som bilder, kategorier og bokser.
- YAML er et lesbart tekstformat for innstillinger, som plassering av datasett og klassenavn.

Flyt: HRSID-bilder + COCO-JSON → kontroll og datadeling → YOLO-bilder og tekstmarkeringer → finjustering → bokser og skårer.

Startmodell er foreløpig yolo26n.pt, den lille nano-detektoren fra den gjeldende Ultralytics-dokumentasjonen. Den er ferdigtrent på COCO og skal trenes videre på HRSID. Vi begynner med én klasse: ship. Bakgrunn er ikke en ekstra objektklasse.

COCO lagrer vanlige bokser som [x, y, bredde, høyde], der x og y er øvre venstre hjørne. YOLO bruker klasse-ID og normalisert midtpunkt, bredde og høyde. Normalisert betyr delt på bildets bredde/høyde. Klassen ship skal mappes eksplisitt til 0; COCO sine standardklasser skal ikke automatisk brukes på HRSID. Ultralytics har convert_coco, men standardmappingen til COCO-klasser må slås av for et slikt egendefinert datasett. Alle konverterte bokser kontrolleres på bilder før trening.

## Python-miljø

Et eget miljø er opprettet i .venv med eksisterende Python 3.13.13. Det isolerer prosjektets installerte pakker fra andre prosjekter. Det inneholder foreløpig Python og pip; PyTorch og Ultralytics er ikke installert i dette steget.

Fra prosjektmappen i PowerShell kan miljøet aktiveres med:

```powershell
.\.venv\Scripts\Activate.ps1
```

Man kan også bruke Python direkte uten aktivering:

```powershell
.\.venv\Scripts\python.exe --version
.\.venv\Scripts\python.exe -m pip --version
```

I VS Code velges .venv\Scripts\python.exe som Python-tolk. En tolk er programmet som kjører Python-koden.

Neste installasjonssteg er å velge en stabil PyTorch/torchvision-kombinasjon med GPU-støtte, og deretter Ultralytics. Pillow, NumPy og Matplotlib trengs til bilder og visning. Nøyaktige versjoner registreres etter vellykket installasjon i en requirements-fil. Vi lager ikke en fiktiv liste over installerte versjoner nå. Ingen modeller eller datasett er lastet ned av oppstarten.

## Hvordan filene håndteres

| Plassering | Innhold | Til GitHub? |
|---|---|---|
| README.md | Kort introduksjon og lenker | Ja |
| PLAN.md | Prosjektplan | Ja |
| OPPSTART.md | Dette dokumentet | Ja |
| .venv/ | Python og installerte pakker | Nei |
| data/raw/ | Originale HRSID-bilder, annotasjoner og medfølgende vilkår | Nei |
| data/processed/ | Konverterte YOLO-data og CNN-utsnitt | Nei |
| data/splits/ | Tekstlister over hvilken del hvert bilde tilhører | Ja, med originale filnavn/bilde-ID-er |
| configs/ | Innstillinger, for eksempel senere hrsid.yaml | Ja |
| src/ | Egen Python-kode, lagt til stegvis | Ja |
| models/ | Nedlastede og egne modellvekter | Nei |
| runs/ | Genererte treningsresultater og mellomfiler | Nei |
| reports/ | Kort forsøkslogg, tabeller og utvalgte resultater | Ja, vurder bilder og datavilkår før publisering |

.gitkeep er en tom plassholder som gjør at tomme mapper kan følge Git. .gitignore bestemmer hva Git ikke skal ta med. Filen sletter ingenting og skjuler ikke filer som allerede er sporet.

Originaldata endres ikke. Vi deler data i trening, validering og test før vi lager nye utsnitt. Trening lærer vekter, validering brukes til modellvalg, og test gir sluttvurderingen. Kildescener holdes samlet når tilgjengelig informasjon tillater det. Egen CNN og YOLO bruker samme underliggende deling.

## Lisens: trenger vi å betale eller registrere noe?

For et lokalt læringsprosjekt finnes en gratis vei: Ultralytics under AGPL-3.0. Ultralytics oppgir akademisk arbeid, personlige prosjekter og læring som aktuelle bruksområder. Det er ikke nødvendig å kjøpe Enterprise eller registrere en skykonto for denne lokale arbeidsmåten. Gratis betyr at lisensvilkårene fortsatt gjelder.

AGPL-3.0 er en åpen kildekodelisens. Ved deling av et omfattet program må blant annet tilhørende kildekode og lisensinformasjon følge vilkårene. Modifiserte programmer med nettverksbruk har også et særskilt krav om tilbud om kildekode til brukerne. Privat lokal kjøring betyr ikke i seg selv at all privat kode må publiseres. Ultralytics markedsfører Enterprise som alternativet for proprietær bruk; lukket produkt eller tjeneste må vurderes særskilt før en eventuell videreføring. Kommersiell bruk alene er ikke generelt forbudt av AGPL.

Forslag for dette prosjektet er åpen kildekode under AGPL-3.0 for koden som bruker Ultralytics. Vi har ikke lagt til en LICENSE-fil på vegne av begge repo-eierne. Avklar lisensvalget med Mattias før den legges til. Ikke sett bare MIT på en samlet Ultralytics-basert løsning uten å kontrollere forpliktelsene.

HRSID-repoet inneholder GPL-3.0 og ber om sitering av HRSID-artikkelen. Dette alene avklarer ikke nødvendigvis alle rettigheter til bildene i eksterne nedlastinger. Behold medfølgende vilkår, oppgi datakilde og artikkel, og ikke legg hele datasettet på GitHub. Kontroller vilkårene i den faktiske nedlastingen før viderepublisering av bilder eller vekter. Lisens for programvare, startvekter og treningsdata er separate spørsmål. Å bruke COCO-formatet betyr ikke at COCO-bildedatasettets lisens automatisk gjelder HRSID.

Dette er praktisk lisensinformasjon for planlegging, ikke en vurdering av et framtidig kommersielt produkt.

## Neste små steg

1. Avklare lisensforslaget og åpne prosjektmappen i VS Code.
2. Installere PyTorch med riktig GPU-støtte og deretter Ultralytics i .venv.
3. Legge HRSID i data/raw og se på noen bilder og fasitbokser.
4. Dokumentere datadelingen og lage YOLO-konvertering.
5. Starte liten CNN-øvelse og et kort YOLO-forsøk. Ingen lang trening før dataene er kontrollert.

## Kilder kontrollert 21. oktober 2026

- [Ultralytics: installasjon og lokal bruk](https://docs.ultralytics.com/quickstart/)
- [Ultralytics: COCO-konvertering](https://docs.ultralytics.com/reference/data/converter/)
- [Ultralytics: lisensvalg](https://www.ultralytics.com/license)
- [AGPL-3.0: lisensvilkår](https://www.gnu.org/licenses/agpl-3.0.html)
- [HRSID: prosjekt, sitering og nedlastinger](https://github.com/chaozhong2010/HRSID)
- [HRSID: repoets LICENSE](https://github.com/chaozhong2010/HRSID/blob/master/LICENSE)
