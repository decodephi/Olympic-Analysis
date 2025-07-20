import numpy as np


def fetch_medal_tally(df, year, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    if year != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == year) & (medal_df['region'] == country)]

    if flag == 1:
        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']

    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    return x


def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country

# def data_over_time(df,col):

#     nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index().sort_values('index')
#     nations_over_time.rename(columns={'index': 'Edition', 'Year': col}, inplace=True)
#     return nations_over_time

# def data_over_time(df, col):
#     tmp_df = df.drop_duplicates(['Year', col])
#     nations_over_time = tmp_df['Year'].value_counts().reset_index(name='Count')
#     nations_over_time.rename(columns={'index': 'Edition'}, inplace=True)
#     nations_over_time = nations_over_time.sort_values('Edition')
#     nations_over_time.rename(columns={'Count': col}, inplace=True)
#     return nations_over_time

def data_over_time(df, col):
    # Drop duplicates to count unique entities (like nations) per year
    tmp_df = df.drop_duplicates(['Year', col])

    # Group by year and count unique entries for `col`
    nations_over_time = tmp_df.groupby('Year')[col].nunique().reset_index()

    # Rename columns
    nations_over_time.rename(columns={'Year': 'Edition', col: col}, inplace=True)

    # Sort by year (Edition)
    nations_over_time = nations_over_time.sort_values('Edition')

    return nations_over_time




def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(df, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals'}, inplace=True)
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful(df, sport):
    temp_df = df if sport == 'Overall' else df[df['Sport'] == sport]
    temp_df = temp_df.dropna(subset=['Name', 'Sport', 'region'])  # Optional safety check
    

    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name', 'Medal Count']

    x = x.head(15).merge(df[['Name', 'Sport', 'region']], on='Name', how='left').drop_duplicates('Name')

    return x[['Name', 'Medal Count', 'Sport', 'region']]


# /////////////////////////////////////////////////////////////////

def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    # Get top 10 athletes by medal count
    top_athletes = temp_df['Name'].value_counts().reset_index().head(10)
    top_athletes.columns = ['Name', 'Medals']  # Rename for clarity

    # Merge with temp_df to get sport information (and avoid merging with full df)
    merged = top_athletes.merge(temp_df[['Name', 'Sport']], on='Name', how='left')

    # Drop duplicate names (some athletes may have multiple sports listed)
    result = merged.drop_duplicates('Name')

    return result[['Name', 'Medals', 'Sport']]


def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

    final = men.merge(women, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

    final.fillna(0, inplace=True)

    return final