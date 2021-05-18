import pandas as pd
import numpy as np
import streamlit as st

skater_url = 'https://www.hockey-reference.com/playoffs/NHL_2021_skaters.html'
goalie_url = 'https://www.hockey-reference.com/playoffs/NHL_2021_goalies.html'
goali_pnts = np.array([1,3])

def load_picks():
    picks = pd.read_csv('picks.csv').iloc[:,[0,2,4,6,8,10,12,14]]
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
                 np.dot(g[g.index.isin(picks[p])].values[0],goali_pnts)]
              for p in picks.columns
              }
    score_df = pd.DataFrame.from_dict(scores,orient='index',
                                      columns=['skaters','goalies'])
    score_df['total'] = score_df.sum(axis=1)
    return score_df

st.write(get_scores().sort_values(by='total',ascending=False))





