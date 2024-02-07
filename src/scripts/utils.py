""" 
CENTERS_ID 
+--------+--------------------------------------+----+
| codigo | nome do núcleo                       | id |
+--------+--------------------------------------+----+
| SPA    | Núcleo de Aquarius                   |  1 |
| CCPA   | Centro de Conferências Pedra Angular |  2 |
| JAR    | Núcleo de Jarinu                     |  3 |
| CPS    | Núcleo de Campinas                   |  4 |
| SOR    | Núcleo de Sorocaba                   |  5 |
| LOR    | Núcleo de Lorena                     |  6 |
| BAU    | Núcleo de Bauru                      |  7 |
| MAR    | Centro de Conferências Aurora        |  8 |
| RIB    | Núcleo de Ribeirão Preto             |  9 |
| CUR    | Núcleo de Curitiba                   | 10 |
| RIO    | Centro de Conferências Novo Sol      | 11 |
| LST    | Centro de Conferências Fênix         | 12 |
| VIT    | Núcleo de Vitória                    | 13 |
| PMN    | Centro de Conferências Graal         | 14 |
| BSB    | Centro de Conferências Água Viva     | 15 |
| POA    | Núcleo de Porto Alegre               | 16 |
| CBA    | Núcleo de Cuiabá                     | 17 |
| FOR    | Centro de Conferências Nova Luz      | 18 |
| BEL    | Núcleo de Belém                      | 19 |
| MAN    | Núcleo de Manaus                     | 20 |
| SANTOS | Núcleo de Santos                     | 21 |
| SJC    | Sala de São José dos Campos          | 22 |
| FLR    | Núcleo de Florianópolis              | 23 |
| GYN    | Núcleo de Goiânia                    | 24 |
| SAL    | Núcleo de Salvador                   | 25 |
+--------+--------------------------------------+----+
"""

CENTERS_ID = {
    "SPA": 1,
    "CCPA": 2,
    "JAR": 3,
    "CPS": 4,
    "SOR": 5,
    "LOR": 6,
    "BAU": 7,
    "MAR": 8,
    "RIB": 9,
    "CUR": 10,
    "RIO": 11,
    "LST": 12,
    "VIT": 13,
    "PMN": 14,
    "BSB": 15,
    "POA": 16,
    "CBA": 17,
    "FOR": 18,
    "BEL": 19,
    "MAN": 20,
    "SANTOS": 21,
    "SJC": 22,
    "FLR": 23,
    "GYN": 24,
    "SAL": 25,
}

COLUMNS_INDEXES = [0, 2, 4, 5, 9, 10, 13, 14, 15, 20, 21, 24, 25, 26, 35, 40]

COLUMNS = {
    0: "center_ref",
    1: "name",
    2: "gender",
    3: "birth",
    4: "city",
    5: "state",
    6: "rg",
    7: "ssp",
    8: "cpf",
    9: "phone",
    10: "email",
    11: "sos_contact",
    12: "sos_type",
    13: "sos_phone",
    14: "aspect",
    15: "p21",
}

ASPECTS = {
    "P": "21",
    "1o. Aspecto": "A1",
    "2o. Aspecto": "A2",
    "E.C.S.": "A3",
    "Ekklesia": "A4",
    "Graal": "GR",
    "Quinto": "A5",
    "Sexto": "A6",
}
