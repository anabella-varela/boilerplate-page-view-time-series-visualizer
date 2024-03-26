import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', index_col= 0, parse_dates=True)
# Clean data
df = df[
    (df['value'] <= df['value'].quantile(0.975)) &
    (df['value'] >= df['value'].quantile(0.025))
]


def draw_line_plot():
    # Draw line plot
    # Draw line plot with matplotlib function
    fig= plt.figure(figsize=(10, 5)) #set the size
    plt.plot(df.index, df['value'], color='red') #plot inside the figure
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019', fontsize=11)
    plt.xlabel('Date', fontsize=10)
    plt.ylabel('Page Views', fontsize=10)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar["Years"] = df_bar.index.year
    df_bar["Months"] = df_bar.index.month_name()
    df_bar = pd.DataFrame(df_bar.groupby(["Years", "Months"],sort=False)["value"].mean().round().astype(int))
    # the above df has a miltiindexing that makes me the plotting very complicated. If I unstacke the df I no longer have a multiindexing and can plot easily
    df_bar = df_bar.unstack()

    # Draw bar plot
    fig = df_bar.plot.bar(
    legend=True,
    figsize = (13,10),
    ylabel="Average Page Views",
    xlabel = "Years",
    fontsize = 10).figure

    plt.legend(["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = pd.Categorical([d.year for d in df_box.date])
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
        
    fig, _ = plt.subplots(1, 2, figsize=(25,8))

    # Drawing first plot
    plt.subplot(1,2,1)
    sns.boxplot(x=df_box['year'], y=df_box['value'], data=df_box, orient='v')

    plt.title('Year-wise Box Plot (Trend)')
    plt.xlabel('Year')
    plt.ylabel('Page Views')

    # Drawing second plot
    plt.subplot(1,2,2)
    sns.boxplot(x=df_box['month'], y=df_box['value'], data=df_box,
                         order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
                        'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], orient='v')

    plt.title('Month-wise Box Plot (Seasonality)')
    plt.xlabel('Month')
    plt.ylabel('Page Views')
    
     # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
