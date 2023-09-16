import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df["date"] = pd.to_datetime(df["date"]) #convert to date
df = df.set_index('date') #set index to date

# Clean data
df = df.loc[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig = sns.lineplot(data=df, legend=False)
    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
  
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Year'] = df_bar.index.year
    df_bar['Month'] = df_bar.index.month_name()
    df_bar = pd.DataFrame(df_bar.groupby(['Years', 'Months'], sort=False)['value'].mean().round().astype(int))
    df_bar = df_bar.rename(columns={"value": "Average Page Views"})
    df_bar = df_bar.reset_index() #reset index
    #create df for start of 2016
    missing = {
       "Years": [2016, 2016, 2016, 2016],
       "Months": ['January', 'February', 'March', 'April'],
       "Average Page Views": [0, 0, 0, 0]}
    missing = pd.DataFrame(missing)
    df_bar = pd.concat([missing, df_bar], ignore_index=False, sort=False, axis=0)

    # Draw bar plot
    fig = sns.catplot(data=df_bar, kind='bar', x='Years', y='Average Page Views', hue='Months', palette='flare')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(15, 10))
    #Yearly boxplots
    fig = sns.boxplot(data=df_box, x='year', y='value', ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Years")
    axes[0].set_ylabel("Page Views")
    #monthly boxplots
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
    sns.boxplot(data=df_box, x = "month", y="value", order=months, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Months")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
