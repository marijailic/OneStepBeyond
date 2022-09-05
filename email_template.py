def get_template(data):
    return f"""<h1>{data["ime_izvodaca"]}</h1>
<p>{data["opis"]}</p>
<p>{data["mjesto"]}</p>
<p>{data["datum"]} | {data["vrijeme"]} h</p>
<p>{data["cijena"]} kn</p>"""
