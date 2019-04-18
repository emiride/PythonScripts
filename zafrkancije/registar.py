import requests
import json
import csv


csv_file = open("registar.csv", "w", encoding='utf-8', newline='')
registar_writer = csv.writer(csv_file, dialect=csv.excel)
registar_writer.writerow(["Id","ime","prezime","email", 'telefon', 'institucija', 'ministarstvo', 'strucna sprema', 'naziv radnog mjesta',
                          'naziv organa uprave', 'osnovna plata', 'datumZasnivanjaRadnogOdnosaNaNeodredjenoVrijeme', 'datumPrestankaRadnogOdnosaNaNeodredjenoVrijeme',
                          'trajanjeUgovoraNaOdredjenoVrijemeOD', 'trajanjeUgovoraNaOdredjenoVrijemeDO', 'resornoMinistarstvoOrgana', 'sjedisteOrgana', 'napomena'])
for i in range(616):
    while True:
        r = requests.get("https://www.anticorrupiks.com/api/ZaposleneOsobeJavniSektors/created/desc/"+str(i+1)+"/undefined/undefined/undefined/undefined")
        try:
            json_object = json.loads(r.text, );
            break
        except:
            continue
    results = json_object['results']
    for result in results:
        id = result['id']
        ime = result['ime']
        prezime = result['prezime']
        email = result['email']
        telefon = result['telefon']
        institucija= result['institucija']
        ministarstvo= result['ministarstvo']
        strucnaSprema= result['strucnaSprema']
        nazivRadnogMjesta= result['nazivRadnogMjesta']
        nazivOrganaUprave= result['nazivOrganaUprave']
        osnovnaPlata= result['osnovnaPlata']
        datumZasnivanjaRadnogOdnosaNaNeodredjenoVrijeme= result['datumZasnivanjaRadnogOdnosaNaNeodredjenoVrijeme']
        datumPrestankaRadnogOdnosaNaNeodredjenoVrijeme= result['datumPrestankaRadnogOdnosaNaNeodredjenoVrijeme']
        trajanjeUgovoraNaOdredjenoVrijemeOD= result['trajanjeUgovoraNaOdredjenoVrijemeOD']
        trajanjeUgovoraNaOdredjenoVrijemeDO= result['trajanjeUgovoraNaOdredjenoVrijemeDO']
        resornoMinistarstvoOrgana= result['resornoMinistarstvoOrgana']
        sjedisteOrgana = result['sjedisteOrgana']
        napomena = result['napomena']
        registar_writer.writerow([id, ime, prezime, email, telefon, institucija, ministarstvo, strucnaSprema, nazivRadnogMjesta,nazivOrganaUprave,
                                 osnovnaPlata, datumZasnivanjaRadnogOdnosaNaNeodredjenoVrijeme, datumPrestankaRadnogOdnosaNaNeodredjenoVrijeme,
                                 trajanjeUgovoraNaOdredjenoVrijemeOD, trajanjeUgovoraNaOdredjenoVrijemeDO, resornoMinistarstvoOrgana,
                                 sjedisteOrgana, napomena])
        csv_file.flush()
        print(id, ime)
csv_file.close()