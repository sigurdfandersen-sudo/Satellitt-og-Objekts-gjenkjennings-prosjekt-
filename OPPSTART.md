# Oppsummering og oppstart

> Gjeldende arbeidsmåte: Sigurd skriver all prosjektkode selv og velger egen struktur. Vi forklarer og arbeider ett lite steg om gangen. Se [AGENTS.md](AGENTS.md); disse reglene gjelder foran eldre forslag om automatisk implementering.

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

Et eget miljø er opprettet i .venv med eksisterende Python 3.13.13. Det isolerer prosjektets installerte pakker fra andre prosjekter. Miljøet inneholder nå PyTorch med CUDA 12.8, torchvision, Ultralytics og bildebibliotekene. Se den kontrollerte installasjonsstatusen nedenfor.

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

Bibliotekene er installert. requirements.txt viser direkte biblioteker; requirements-lock.txt er et øyeblikksbilde av alle installerte pakker i dette Windows/Python 3.13-miljøet. Ingen ferdigtrente modellvekter eller datasett er lastet ned av oppstarten.

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
2. Biblioteker og GPU-støtte er installert og kontrollert. Velg .venv i VS Code.
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

## Installert og kontrollert miljø

Dato: 21. oktober 2026. Python 3.13.13, torch 2.11.0+cu128, torchvision 0.26.0+cu128 og ultralytics 8.4.183. Øvrige direkte pakker står i requirements.txt. Modellfamilien YOLO26 og versjonsnummeret på Python-pakken Ultralytics er forskjellige navn/numre.

Kontroller som er gjennomført:

- Import av torch, torchvision, ultralytics, NumPy, Pillow, Matplotlib og OpenCV.
- CUDA tilgjengelig og GPU identifisert som Quadro RTX 4000 Max-Q, 8 GB.
- Liten matriseberegning på GPU med riktig resultat.
- YOLO26n bygget fra inkludert YAML og kjørt med et syntetisk bilde på GPU. Den brukte tilfeldige vekter; kontrollen er ikke et resultat for skipsdeteksjon.
- pip check fant ingen ødelagte avhengigheter.

Kontrollen sier at miljøet kjører. HRSID-trening og praktisk treningshastighet er ikke prøvd.

### Gjenskape miljøet på en tilsvarende Windows-PC

Etter å ha opprettet og valgt .venv installeres GPU-utgaven først:

```powershell
.\.venv\Scripts\python.exe -m pip install torch==2.11.0 torchvision==0.26.0 --index-url https://download.pytorch.org/whl/cu128
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
```

Dette oppsettet er kontrollert med NVIDIA-driver 573.91 og CUDA 12.8-støtte. Andre operativsystemer, GPU-er eller Python-versjoner kan kreve andre installasjonsvalg. CUDA-runtime følger PyTorch-pakken; denne installasjonen krevde ikke separat CUDA Toolkit.

### YOLO26n og TorchScript

Vi skal bruke yolo26n.pt som ferdigtrent startmodell. Det er en PyTorch-modellfil som støtter videre trening gjennom Ultralytics. Den skal senere lagres under models/.

TorchScript er et eksportformat, ikke en egen detektor eller et nødvendig treningsbibliotek. Ultralytics dokumenterer at PyTorch har avviklet videre satsing på TorchScript (deprecated), og beholder eksport for eldre integrasjoner. Vi trenger ikke TorchScript-eksport for å trene eller bruke modellen fra Python. Eventuell eksport velges etter at vi har en modell og vet hvor den skal kjøres.

At modellen brukes til bilder tatt ovenfra endrer datasett og treningsbehov, men krever ikke et eget bibliotek kalt «aerial imagery».

Ultralytics-innstillingene fra miljøkontrollen ligger under runs/ultralytics-settings, med sync slått av. Dette ble satt for kontrollprosessen. Framtidige programmer skal bruke en uttrykkelig prosjektkonfigurasjon for modell-, data- og resultatmapper.

Kilder:

- [YOLO26 og yolo26n.pt](https://docs.ultralytics.com/models/yolo26/)
- [TorchScript-eksport og status](https://docs.ultralytics.com/integrations/torchscript/)
- [PyTorch lokalt](https://pytorch.org/get-started/locally/)

