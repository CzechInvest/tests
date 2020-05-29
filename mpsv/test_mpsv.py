import requests
import sparql
import json

import urllib

def test_sparql():
    month = 3
    year = 2020
    data = """
PREFIX zdroj: <https://data.mpsv.cz/zdroj/>
PREFIX pojem: <https://data.mpsv.cz/pojem/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
SELECT
SUM(?uchazeciOZamestnani) AS ?uchazeciOZamestnani
SUM(?dosazitelniUchazeci) AS ?dosazitelniUchazeci
SUM(?podilNezamestnanychOsob) AS ?podilNezamestnanychOsob
SUM(?volnaPracovnaMista) AS ?volnaPracovnaMista
SUM(?obyvatelstvo15_64) AS ?obyvatelstvo15_64
?nazevObce
?nazevOkresu
?rok
?mesic
FROM zdroj:NezamestnanostVObcich
FROM NAMED zdroj:Okresy
FROM NAMED zdroj:Kraje
FROM NAMED zdroj:Obce
WHERE
{
?polozka pojem:mesic ?mesic .
FILTER (MONTH(?mesic) = 3)
?polozka pojem:rok ?rok .
FILTER (YEAR(?rok) = 2020)
?polozka pojem:okres ?idOkresu .
?polozka pojem:obec ?idObce .
?polozka pojem:dosazitelniUchazeci ?dosazitelniUchazeci .
?polozka pojem:podilNezamestnanychOsob ?podilNezamestnanychOsob .
?polozka pojem:uchazeciOZamestnani ?uchazeciOZamestnani .
?polozka pojem:volnaPracovnaMista ?volnaPracovnaMista .
?polozka pojem:obyvatelstvo15_64 ?obyvatelstvo15_64
GRAPH zdroj:Okresy
{
?idOkresu skos:prefLabel ?nazevOkresu .
?idOkresu pojem:kraj ?idKraje

}
GRAPH zdroj:Kraje
{
?idKraje skos:prefLabel ?nazevKraje
}
GRAPH zdroj:Obce
{
?idObce skos:prefLabel ?nazevObce
}
}
GROUP BY ?rok ?mesic ?nazevObce ?nazevOkresu
ORDER BY DESC(?rok), DESC(?mesic), ASC(?nazevObce), ASC(?nazevOkresu)
"""

    #data = (
    #        "PREFIX zdroj: <https://data.mpsv.cz/zdroj/>\n"
    #        "PREFIX pojem: <https://data.mpsv.cz/pojem/>\n"
    #        "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n"
    #        "SELECT \n"
    #        "SUM(?uchazeciOZamestnani) AS ?uchazeciOZamestnani\n"
    #        "SUM(?dosazitelniUchazeci) AS ?dosazitelniUchazeci\n"
    #        "SUM(?podilNezamestnanychOsob) AS ?podilNezamestnanychOsob\n"
    #        "SUM(?volnaPracovnaMista) AS ?volnaPracovnaMista\n"
    #        "SUM(?obyvatelstvo15_64) AS ?obyvatelstvo15_64\n"
    #        "?nazevObce\n"
    #        "?nazevOkresu\n"
    #        "?rok\n"
    #        "?mesic\n"
    #        "FROM zdroj:NezamestnanostVObcich\n"
    #        "FROM NAMED zdroj:Okresy\n"
    #        "FROM NAMED zdroj:Kraje\n"
    #        "FROM NAMED zdroj:Obce\n"
    #        "WHERE \n"
    #        "{{\n"
    #        "?polozka pojem:mesic ?mesic .\n"
    #        "FILTER (MONTH(?mesic) = {month})\n"
    #        "?polozka pojem:rok ?rok .\n"
    #        "FILTER (YEAR(?rok) = {year})\n"
    #        "?polozka pojem:okres ?idOkresu .\n"
    #        "?polozka pojem:obec ?idObce .\n"
    #        "?polozka pojem:dosazitelniUchazeci ?dosazitelniUchazeci .\n"
    #        "?polozka pojem:podilNezamestnanychOsob ?podilNezamestnanychOsob .\n"
    #        "?polozka pojem:uchazeciOZamestnani ?uchazeciOZamestnani .\n"
    #        "?polozka pojem:volnaPracovnaMista ?volnaPracovnaMista .\n"
    #        "?polozka pojem:obyvatelstvo15_64 ?obyvatelstvo15_64\n"
    #        "GRAPH zdroj:Okresy\n"
    #        "{{\n"
    #        "?idOkresu skos:prefLabel ?nazevOkresu .\n"
    #        "?idOkresu pojem:kraj ?idKraje\n"
    #        "}}\n"
    #        "GRAPH zdroj:Kraje\n"
    #        "{{\n"
    #        "?idKraje skos:prefLabel ?nazevKraje\n"
    #        "}}\n"
    #        "GRAPH zdroj:Obce\n"
    #        "{{\n"
    #        "?idObce skos:prefLabel ?nazevObce\n"
    #        "}}\n"
    #        "}}\n"
    #        "GROUP BY ?rok ?mesic ?nazevObce ?nazevOkresu\n"
    #        "ORDER BY DESC(?rok), DESC(?mesic), ASC(?nazevObce), ASC(?nazevOkresu)"
    #        ).format(month=month, year=year)
    
    try:
        s = sparql.Service("https://www.mpsv.cz/sparql/", "utf-8", "POST",
            accept='application/json')
        result = s.query(data, raw=True)
        data = json.loads(result.read().decode("utf-8"))
        assert len(data["results"]) > 0
    except urllib.error.HTTPError as e:
        raise e
