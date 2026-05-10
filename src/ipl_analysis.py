# %%
import pandas as pd

# %%
deliveries = pd.read_csv(r"C:\Users\Ujjawal\Desktop\Ujjawal\courses\Data Science\PROJECT\IPL ANALYSIS\Data\deliveries.csv")
matches = pd.read_csv(r"C:\Users\Ujjawal\Desktop\Ujjawal\courses\Data Science\PROJECT\IPL ANALYSIS\Data\matches.csv")


# %%
matches = matches.rename(columns={'id' : 'match_id'})

# %%
deliveries.head()

# %%
deliveries.shape

# %%
matches.shape

# %%
matches.columns

# %%
matches.isnull().sum()

# %%
deliveries['match_id'].nunique()

# %%
matches['match_id'].nunique()

# %%
matches.head()

# %%
deliveries.head()

# %%
df=pd.merge(matches , deliveries , on ='match_id')

# %%
df.shape

# %%
df.head()

# %% [markdown]
# *ADDING NEW COLUMN FOR ANALYSIS*

# %%
# checking if total runs present in data is correct or not
(df['total_runs'] == (df['batsman_runs']+df['extra_runs'])).all()

# %%
# adding boundary column
df['is_boundary'] = df['total_runs'].apply(lambda x: 1 if x in (4,6) else 0)

# %%
df['is_dot'] = df['total_runs'].apply(lambda x : 1 if x == 0 else 0)

# %%
def get_phase(over):
    if over <= 6:
        return "Powerplay" 
    elif over <= 15:
        return "Middle"
    else:
        return "Death"

df['phase'] = df['over'].apply(get_phase)


# %%
df[['match_id','batsman_runs' , 'extra_runs' ,'total_runs' , 'is_boundary' , 'is_dot' , 'phase' , 'over']].head()

# %% [markdown]
# *ANALYSIS 1 — Top Batsmen (Total Runs)*

# %%
df.groupby('batsman')['total_runs'].sum().sort_values(ascending = False).head(10)

# %%
temp = df.groupby(['batsman', 'Season'])['total_runs'].sum().reset_index()

# %%
idx = temp.groupby('Season')['total_runs'].idxmax()

temp.iloc[idx]

# %%
season_batsman_runs = df.groupby(['batsman', 'Season'])['total_runs'].sum().reset_index()

# %%
# top_per_season = season_batsman_runs.sort_values(['Season', 'total_runs'] , ascending=[True , False])
# top_per_season.groupby('Season').head(1)

# or 

top_per_season = season_batsman_runs.loc[season_batsman_runs.groupby('Season')['total_runs'].idxmax()]

top_per_season.head()

# %% [markdown]
# *NOW ADDING MORE MATRIX TO CALCULATE THE BEST BATSMAN*

# %% [markdown]
# *1ST ONE IS NO OF MATCHED PLAYED*

# %%
matches_played = df.groupby(['batsman' , 'Season'])['match_id'].nunique().reset_index(name='matches')
matches_played

# %%
runs = df.groupby(['batsman' , 'Season'])['total_runs'].sum().reset_index()
runs.head()

# %% [markdown]
# *BALLS FACED PER PLAYER PER SEASON*

# %%
balls = df[df['wide_runs'] ==0].groupby(['batsman' , 'Season'])['ball'].count().reset_index()
balls

# %%
stats = runs.merge(balls, on=('batsman' , 'Season')).merge(matches_played , on=('batsman' , 'Season'))
stats.head()

# %%
stats['strike_rate'] = ( stats['total_runs'] / stats['ball'] ) * 100

# %%
stats.sort_values('total_runs' , ascending=False).head(10)

# %% [markdown]
# *FILTER SERIOUS PLAYERS ON THE BASIS OF RUNS*

# %%
stats = stats[stats['matches']>=5]
stats['Season'] = stats['Season'].str.replace('IPL-' ,'')


# %%
top_players = stats.loc[stats.groupby('Season')['total_runs'].idxmax()]

top_players

# %% [markdown]
# *FILTER SERIOUS PLAYERS ON THE BASIS OF RUNS + STRIKE RATE*

# %%
# here we are using a formula 
# perf_Score = runs +(strike_rate*2) .... here 2 is just a assumption 
# “This is my scoring model based on assumptions”

# EXAMPLE 
 
# PLAYER A 
# Runs = 600 , SR = 120  , Score = 600 + (120 × 2) = 840
 
# PLAYER B
# Runs = 550 , SR = 160  , Score = 550 + (160 × 2) = 870

# Result:

# Player B ranks higher Because:
# Slightly fewer runs
# But much faster scoring

# %%
stats['performance_score'] = stats['total_runs'] + (stats['strike_rate'] * 2)

# %%
top_players = stats.loc[stats.groupby('Season')['performance_score'].idxmax()]

top_players

# %% [markdown]
# *to find most aggressive players who has faced atleast 100 balls*

# %%
stats[stats['ball'] >=100].sort_values('strike_rate' , ascending=False).head()

# %% [markdown]
# *Most consistent players*

# %%
stats.sort_values('matches', ascending=False).head(10)

# %% [markdown]
# *Performance by Phase*

# %%
df[df['phase'] == 'Powerplay']

# %%
df.groupby(['batsman' , 'Season' , 'phase'])['total_runs'].sum().reset_index()

# %%
phase_stats = df.groupby(['batsman', 'phase'])['total_runs'].sum().reset_index()

# %%
phase_stats.sort_values(['phase' , 'total_runs'] , ascending = [True , False]).head(10)

# %% [markdown]
# *Add strike rate by phase*

# %%
phase_runs = df[df['wide_runs'] == 0].groupby(['batsman' , 'phase'])['total_runs'].sum().reset_index()
phase_balls = df[df['wide_runs'] == 0].groupby(['batsman' , 'phase'])['ball'].count().reset_index()

# %%
phase_final = phase_runs.merge(phase_balls , on=['batsman' , 'phase'])

# %%
phase_final['strike_rate'] = (phase_final['total_runs'] / phase_final['ball']) * 100
phase_final.head()

# %%
phase_final = phase_final[phase_final['ball'] >= 30]
phase_final.head()

# %% [markdown]
# *Finding top players for each phase*

# %%
phase_final.sort_values(['phase' , 'strike_rate'] , ascending = [True , False]).groupby('phase').head(5)

# %% [markdown]
# *performance_Score*

# %%
phase_final['performance_score'] = ( phase_final['total_runs'] + phase_final['strike_rate'] * 2)

# %%
phase_final

# %%
phase_final.loc[phase_final.groupby('phase')['performance_score'].idxmax()]

# %% [markdown]
# *performance_Score using some other analysis method/formula*

# %%
phase_final['performance_score'] = ( phase_final['total_runs'] * .70) + (phase_final['strike_rate'] * .30)

# %%
phase_final.loc[phase_final.groupby('phase')['performance_score'].idxmax()]

# %% [markdown]
# *Match Winning Impact , to find MOM*

# %%
# df.groupby('batsman')['player_of_match'].count().sort_values(ascending = False)
matches['player_of_match'].value_counts().reset_index().head(15)


