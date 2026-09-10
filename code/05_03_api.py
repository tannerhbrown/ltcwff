import requests
from pandas import DataFrame
import pandas as pd

fc_url = 'https://fantasyfootballcalculator.com/api/v1/adp/ppr?teams=12&year=2020'

resp = requests.get(fc_url)

df = DataFrame(resp.json()['players'])
df.head()

def fc_adp(scoring='ppr', teams=12, year=2020):
    ffc_com = 'https://fantasyfootballcalculator.com'
    resp = requests.get(
        f'{ffc_com}/api/v1/adp/{scoring}?teams={teams}&year={year}'
    )
    df = DataFrame(resp.json()['players'])

    # data doesn't come with teams, year columns, let's add them
    df['year'] = year
    df['teams'] = teams
    return df

df_10_std = fc_adp('standard', 10, 2019)
df_10_std.head()

df_history = pd.concat(
    [fc_adp('standard', 12, year=y) for y in range(2009, 2020)],
    ignore_index=True)

df_history.head()


# Exercises #

import requests
from pandas import DataFrame
import pandas as pd

# given urls
url_adp = 'https://api.myfantasyleague.com/2019/export?TYPE=adp&JSON=1'
url_player = 'https://api.myfantasyleague.com/2019/export?TYPE=players&JSON=1'

# call w/ requests
resp_adp = requests.get(url_adp)
resp_player = requests.get(url_player)

# need to inspect the .json() results in the REPL to see what we want/can turn
# into a DataFrame -- usually list of dicts
df_adp = DataFrame(resp_adp.json()['adp']['player'])
df_player = DataFrame(resp_player.json()['players']['player'])

# now combine
df = pd.merge(df_adp, df_player)

# get rid of IDP players, take top 200
df = df.query("position in ('WR', 'RB', 'TE', 'QB', 'Def', 'PK')")
df = df.head(200)
