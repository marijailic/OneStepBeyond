def get_template(data):
    return f"""<h1>Poštovani, ovaj e-mail je zamjena za fizičke ulaznice.</h1>
<h2>Pri ulasku u koncertnu dvoranu dovoljno je prikazati ovaj e-mail.</h2>
<h1>Podaci o koncertu:</h1>
<h3>Naziv izvođača: {data["ime_izvodaca"]}</h3>
<p><b>Mjesto:</b> {data["mjesto"]}</p>
<p><b>Datum:</b> {data["datum"]} | <b>Vrijeme:</b> {data["vrijeme"]} h</p>
<p><b>Cijena:</b> {data["cijena"]} kn</p>
<p>One Step Beyond nije organizator ponuđenih događaja. Događaj vodi organizator, koji također izdaje ulaznice. One Step Beyond djeluje samo kao distributer za prodaju ulaznica u ime organizatora i stoga ne snosi nikakvu odgovornost u vezi organizacije događaja i / ili njegovog održavanja.</p>
<p><b>Hvala što se posjetili One Step Beyond!</b></p>"""
