# Forslag til prosjektplan

Dato: 21. oktober 2026. Status: Oppstart av miljø og struktur er godkjent. Modellarbeid skjer stegvis. Se OPPSTART.md for gjeldende oppstart og avgrensning.

## Kort oppsummering

Sigurd og Mattias undersøker satellittmottak og gjenkjenning av skip i satellittbilder. Mattias har hovedansvar for antenne og mottak. Sigurd har hovedansvar for data, nevrale nettverk og evaluering. Arbeidet med nevrale nettverk deles i en egen liten PyTorch-modell for læring og en ferdigtrent YOLO-modell som finjusteres til skipsdeteksjon.

HRSID er valgt som datasett. Målet etter omtrent én måned er å vise skipsfunn med bokser i bilder modellen ikke har trent på, og forklare hvordan egenmodellen virker. Antennens bilder og HRSID behandles som to ulike datakilder. Direkte båtdeteksjon i egne mottatte bilder er ikke et krav: det avhenger av sensor, oppløsning og mottaksmuligheter.

## 1. Mål og avgrensning

Minimumsleveransen er:

- En egen CNN som klassifiserer små utsnitt som skip eller bakgrunn.
- En finjustert YOLO-detektor som finner flere skip og tegner bokser rundt dem.
- Resultatbilder, en kort forsøkslogg og en vurdering av feil.
- En forklaring av dataklargjøring, trening og evaluering.

Hvis minimumsleveransen er stabil, kan egenmodellen utvides til å forutsi én boks i utsnitt med høyst ett skip. Dette er et tilleggsmål. Oljesøl, skipstype, sporing, kartkoordinater, kontinuerlig drift og eget brukergrensesnitt utsettes.

Boksene gir plassering i bildets piksler. Geografisk plassering krever ytterligere informasjon om hvordan bildet ligger på jordoverflaten.

## 2. Datasett: HRSID

HRSID inneholder 5 604 SAR-bilder og 16 951 markerte skip. SAR betyr Synthetic Aperture Radar: satellitten måler refleksjoner fra utsendte radarsignaler. Bildene viser radarrespons og ser annerledes ut enn vanlige fotografier.

Vi foreslår JPG-utgaven. Den er mindre plasskrevende enn PNG-utgaven. Markeringene følger COCO-opplegget, et vanlig format for bilder, objektklasser og bokser. En annotasjon er en fasitmarkering av et objekt.

Datasettet er et praktisk valg fordi det er rettet mot skip og inneholder ferdige markeringer. Det er likevel nødvendig å kontrollere at bilder og markeringer stemmer, og å konvertere markeringene til YOLO-format. HRSID er ikke direkte ferdig konfigurert for Ultralytics.

Radar har også utfordringer: kornete mønstre, sterke refleksjoner fra land og havneanlegg, små skip og skip tett sammen. Gode resultater på HRSID dokumenterer ikke automatisk at modellen virker på andre satellitter eller vanlige fotografier.

### Databruk i de to delene

- Egen CNN: små utsnitt med ett helt skip, og utsnitt uten skip. Delvise skip og utsnitt med flere skip håndteres etter en uttrykkelig regel, og utelates i første forsøk.
- YOLO: datasettbilder med alle skip markert med vanlige rektangulære bokser. Bakgrunn regnes ikke som en egen objektklasse.
- Behold rådata urørt og lag bearbeidede data separat.
- Undersøk den eksisterende trenings-/testdelingen. Lag validering fra treningsdelen og hold testdata av til slutt.
- Lag delingen før nye utsnitt. Hold utsnitt fra samme kildescene samlet når informasjonen tillater det. Hvis eksisterende deling har overlappende kildescener, dokumenteres begrensningen.
- HRSID tilbyr 400 ekstra bakgrunnsbilder for robusthetstesting. Bruken bestemmes før forsøkene; de samme bildene skal ikke brukes både til trening og som uavhengig test.

## 3. Modeller

### A. Egen modell i PyTorch

Bygg et lite CNN av importerte byggesteiner som nn.Conv2d, aktiveringsfunksjoner og nn.Linear. CNN betyr konvolusjonsnettverk: små lærte filtre søker etter lokale mønstre i bildet. Sigurd skriver modellens oppbygning, datalasting og treningsløkke og forklarer ett steg om gangen.

Første mål er skip/bakgrunn. Deretter kan samme nettverk få en ekstra utgang som beregner fire bokstall. Dette kalles regresjon, altså å beregne tallverdier. Bokstap beregnes bare der fasiten inneholder et skip. En modell med én boks løser ikke generell deteksjon av flere skip.

### B. Ultralytics YOLO

Foreslått startmodell: YOLO26n Detect, med vektene yolo26n.pt. Bokstaven n står for nano, den minste varianten i denne modellfamilien. Den er et rimelig første forsøk for PC-en og tidsrammen. Valget kontrolleres mot tilgjengelig stabil pakke ved oppstart.

Finjustering betyr å trene videre på ferdig lærte vekter. Startvektene er trent på COCO, ikke på HRSID-radarbilder. Modellen må derfor trenes og evalueres på vårt datasett før vi kan si noe om ytelsen.

YOLO26s er bare et mulig senere forsøk dersom målinger viser behov og kapasitet. Vi planlegger én hovedmodell, vanlig boksgjenkjenning og én klasse: ship. Segmentering og roterte bokser er ikke nødvendig i første versjon.

Sammenligningen mellom egen CNN og YOLO blir pedagogisk. Klassifisering av utvalgte utsnitt og deteksjon i hele bilder er ulike oppgaver; resultatprosentene kan ikke sammenlignes direkte. Ferdigtrening, modellstørrelse og databruk må oppgis.

## 4. Utstyr og programvare

| Behov | Forslag og begrunnelse |
|---|---|
| Datamaskin | Bruk eksisterende PC først. Tidligere kontroll i denne chatten viste Quadro RTX 4000 Max-Q med 8 GB grafikkminne. Treningskapasitet må måles. |
| Diskplass | Sett av omtrent 20–30 GB som foreløpig arbeidsmargin, ikke som en bekreftet nedlastingsstørrelse. |
| Internett | Nedlasting av data, pakker og modellvekter. |
| Python og VS Code | Utvikling og kjøring av egne programmer. |
| PyTorch | Egen CNN, automatisk beregning av gradienter og bruk av GPU. |
| Ultralytics | Trening, prediksjon og evaluering av YOLO. |
| Pillow, NumPy og Matplotlib | Bilder, tallbehandling, bokser og grafer. |
| Git/GitHub | Kode, plan, forsøkslogg og samarbeid. Store datasett og vekter lagres separat. |

GPU er grafikkprosessoren. VRAM er dens arbeidsminne. CUDA lar PyTorch utføre beregninger på NVIDIA-GPU. Et eget virtuelt Python-miljø holder prosjektets pakker adskilt fra MNIST-oppsettet. Eksakte pakkeversjoner og installasjon bestemmes ved implementeringsstart.

Ingen nye maskinvarekjøp er foreslått for Sigurds del. Antenne, radiomottaker, kabel og annet mottaksutstyr avklares i Mattias sin delplan.

## 5. Forslag til fire uker

Tidsanslag: 8–12 timer per uke for Sigurds del. Dette er en antakelse som må avklares. Ved mindre tid prioriteres minimumsleveransen og én-boks-utvidelsen tas bort.

| Uke | Arbeid | Ferdigkriterium |
|---|---|---|
| 1 | Forstå SAR og markeringer. Kontrollere et lite datautvalg. Vise fasitbokser. Lage utsnitt og forstå CNN-lag. Kjøre et kort teknisk YOLO-forsøk tidlig. | Bokser stemmer visuelt, datadelingen er dokumentert, og treningsoppsettet kan kjøre. |
| 2 | Trene egen klassifikator og første YOLO-modell. Logge innstillinger, tid og minnebruk. | Begge deler gir svar på valideringsbilder. Treffer og feil er lagret. |
| 3 | Undersøke feil og endre én ting om gangen. Eventuelt legge til én boks i egenmodellen. | En hovedmodell er valgt ut fra validering. Egenmodellen kan forklares. |
| 4 | Evaluere på holdt av testdata. Lage enkel bildedemonstrasjon og rapport. Samordne framføring med Mattias. | Reproduserbare resultater, kjente begrensninger og en demonstrasjon som kan kjøres uten nett. |

En batch er en gruppe bilder behandlet før en vektoppdatering. En epoke er en gjennomgang av treningsdataene. Batchstørrelse og bildestørrelse velges etter en kort måling, ikke et løfte om treningshastighet.

## 6. Hvordan vi vurderer resultatet

- Egen klassifikator: riktige og feilaktige skip/bakgrunn-avgjørelser, med fordeling mellom klassene.
- YOLO: precision (andel funn som er riktige), recall (andel virkelige skip som finnes), og mAP50 samt mAP50–95 (mål som også vurderer boksplassering).
- IoU er arealet der fasitboks og modellboks overlapper, delt på arealet de dekker til sammen.
- Undersøk også små skip, havner, åpent hav og bakgrunn uten skip.
- Modellens skår er ikke automatisk en nøyaktig sannsynlighet. En valgt terskel bestemmer hvilke funn som vises.
- Sett ingen lovet resultatprosent før første modell er målt.

For hvert forsøk lagres datadeling, innstillinger, programversjoner, treningslengde og resultater. Terskler og modellvalg bestemmes med valideringsdata. Testdata brukes til avsluttende vurdering.

## 7. Kompleksitet og reserveplan

| Risiko | Tiltak |
|---|---|
| Feil ved konvertering av bokser | Tegn konverterte bokser på bilder før trening. |
| For lite GPU-minne eller treg trening | Start med nano-modell og lite datautvalg; juster batch og bildeoppløsning. |
| Egen detektor blir for omfattende | Behold egen klassifikator som læringsleveranse; YOLO leverer flere bokser. |
| Nedlasting eller programvare tar tid | Verifiser en liten komplett kjede tidlig. |
| Antennemottaket gir andre bilder | Vis delene separat og forklar sensor- og oppløsningsforskjellen. |

## 8. Avklaringer før utvikling

1. Hvor mange timer per uke har Sigurd og Mattias tilgjengelig, og hva er endelig frist?
2. Hvilke krav stiller eventuell skoleoppgave til egen kode og ferdigtrente modeller?
3. Skal planen godkjennes med egen klassifikator + YOLO som minimum og én boks som tilleggsmål?
4. Hva skal Mattias demonstrere, og hvordan presenteres delene sammen?

Neste steg i planleggingen er å avklare disse punktene og oppdatere planen. Dette dokumentet starter ingen trening eller installasjon.

## Kilder

- [HRSID: offisiell beskrivelse, markeringer og nedlastinger](https://github.com/chaozhong2010/HRSID)
- [Ultralytics: deteksjonsmodeller og trening](https://docs.ultralytics.com/tasks/detect/)
- [Ultralytics: dataformat](https://docs.ultralytics.com/datasets/detect/)
- [Ultralytics: evalueringsmål](https://docs.ultralytics.com/guides/yolo-performance-metrics/)
- [PyTorch: installasjonsvalg](https://pytorch.org/get-started/locally/)

Kildene for HRSID og modellvalget ble kontrollert 21. oktober 2026. Lisensvilkår for datasett, programvare og vekter kontrolleres før eventuell deling eller publisering av disse.

