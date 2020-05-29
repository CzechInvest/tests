import requests
import sparql
import json

import urllib

def test_sparql():
    month = 3
    year = 2020
    data = (
            "PREFIX zdroj: <https://data.mpsv.cz/zdroj/>\n"
            "PREFIX pojem: <https://data.mpsv.cz/pojem/>\n"
            "PREFIX skos: <http://www.w3.org/2004/02/skos/core#>\n"
            "SELECT \n"
            "SUM(?uchazeciOZamestnani) AS ?uchazeciOZamestnani\n"
            "SUM(?dosazitelniUchazeci) AS ?dosazitelniUchazeci\n"
            "SUM(?podilNezamestnanychOsob) AS ?podilNezamestnanychOsob\n"
            "SUM(?volnaPracovnaMista) AS ?volnaPracovnaMista\n"
            "SUM(?obyvatelstvo15_64) AS ?obyvatelstvo15_64\n"
            "?nazevObce\n"
            "?nazevOkresu\n"
            "?rok\n"
            "?mesic\n"
            "FROM zdroj:NezamestnanostVObcich\n"
            "FROM NAMED zdroj:Okresy\n"
            "FROM NAMED zdroj:Kraje\n"
            "FROM NAMED zdroj:Obce\n"
            "WHERE \n"
            "{{\n"
            "?polozka pojem:mesic ?mesic .\n"
            "FILTER (MONTH(?mesic) = {month})\n"
            "?polozka pojem:rok ?rok .\n"
            "FILTER (YEAR(?rok) = {year})\n"
            "?polozka pojem:okres ?idOkresu .\n"
            "?polozka pojem:obec ?idObce .\n"
            "?polozka pojem:dosazitelniUchazeci ?dosazitelniUchazeci .\n"
            "?polozka pojem:podilNezamestnanychOsob ?podilNezamestnanychOsob .\n"
            "?polozka pojem:uchazeciOZamestnani ?uchazeciOZamestnani .\n"
            "?polozka pojem:volnaPracovnaMista ?volnaPracovnaMista .\n"
            "?polozka pojem:obyvatelstvo15_64 ?obyvatelstvo15_64\n"
            "GRAPH zdroj:Okresy\n"
            "{{\n"
            "?idOkresu skos:prefLabel ?nazevOkresu .\n"
            "?idOkresu pojem:kraj ?idKraje\n"
            "}}\n"
            "GRAPH zdroj:Kraje\n"
            "{{\n"
            "?idKraje skos:prefLabel ?nazevKraje\n"
            "}}\n"
            "GRAPH zdroj:Obce\n"
            "{{\n"
            "?idObce skos:prefLabel ?nazevObce\n"
            "}}\n"
            "}}\n"
            "GROUP BY ?rok ?mesic ?nazevObce ?nazevOkresu\n"
            "ORDER BY DESC(?rok), DESC(?mesic), ASC(?nazevObce), ASC(?nazevOkresu)"
            ).format(month=month, year=year)

    try:
        s = sparql.Service("https://www.mpsv.cz/sparql/", "utf-8", "POST",
            accept='application/json')
        result = s.query(data, raw=True)
        #response = requests.post("https://www.mpsv.cz/sparql/", data=data,
        #        headers={"Accept": "application/json"})
        data = json.load(result.decode("utf-8"))
        assert data
    except urllib.error.HTTPError as e:
        raise e
