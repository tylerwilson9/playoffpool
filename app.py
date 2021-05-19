import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path

module_path = Path(__file__)
dir_path = module_path.resolve().parent

skater_url = 'https://www.hockey-reference.com/playoffs/NHL_2021_skaters.html'
goalie_url = 'https://www.hockey-reference.com/playoffs/NHL_2021_goalies.html'
goali_pnts = np.array([1,3])

def load_picks():
    picks = pd.read_csv(dir_path / 'picks.csv').iloc[:-2,[0,2,4,6,8,10,12,14]]
    return picks

def get_stats():
    goalies = pd.read_html(goalie_url,header=1,
                           index_col='Player')[0][['W','SO']].astype('int')
    skaters = pd.read_html(skater_url,header=1,index_col='Player')[0][[
        'PTS']]
    skaters.drop(index='Player',inplace=True)
    skaters = skaters.astype('int')

    return goalies,skaters

def get_scores():
    g,s = get_stats()
    picks = load_picks()
    scores = {p:[s[s.index.isin(picks[p])].sum().values[0],
                 sum(g[g.index.isin(picks[p])].values@goali_pnts)]
              for p in picks.columns
              }
    score_df = pd.DataFrame.from_dict(scores,orient='index',
                                      columns=['skaters','goalies'])
    score_df['total'] = score_df.sum(axis=1)
    return score_df

def get_team_score(player):
    g,s = get_stats()
    picks = load_picks()
    df1 = s[s.index.isin(picks[player])].rename(columns={'PTS':'pts'})
    df2 = pd.DataFrame(g[g.index.isin(picks[player])]@goali_pnts).rename(
        columns={0:'pts'})
    total = pd.DataFrame.from_dict({'TOTAL':df1.sum() + df2.sum()},
                                   orient='index')
    df = pd.concat([df1,df2,total])
    return df

teams = load_picks().columns
scores = get_scores().sort_values(by='total',ascending=False)
dean_winning = scores.loc['Dean']['total'] == scores['total'].max()
if dean_winning:
    st.markdown('# Unfortunatley yes. Dean **is** winning.')
else:
    st.markdown('# Praise to McJesus. Dean **is not** winning.')
st.markdown('## Standings')
st.write(scores)
st.markdown('## Player Scores')
col1, col2 = st.beta_columns(2)
with col1:
    display_team = st.radio("Display Team Score",options = teams)

with col2:
    st.write(get_team_score(display_team))





