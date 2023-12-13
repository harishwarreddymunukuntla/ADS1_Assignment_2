import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def read_data(filename):
    """
    Reads data from the given CSV file and performs data preprocessing.

    Parameters:
    filename (str): Path to the CSV file.

    Returns:
    pd.DataFrame: Original DataFrame read from the CSV file.
    pd.DataFrame: Cleaned and transposed DataFrame.
    """
    # Read data from CSV file
    df = pd.read_csv(filename)
    # Transpose the DataFrame
    df_transpose = df.T.reset_index()
    # Set the first row as column names
    df_transpose.columns = df_transpose.iloc[0]
    # Remove unnecessary rows
    df_transpose = df_transpose.drop(index=[0, 1, 2, 3])
    # Rename the 'Country Name' column to 'Year' and reset the index
    df_transpose = df_transpose.rename(
        columns={'Country Name': 'Year'}).reset_index(drop=True)
    # Display summary statistics of the transposed DataFrame
    print(df_transpose.describe())
    # Clean the DataFrame by dropping columns with NaN values
    df_clean = df_transpose.dropna(axis=1)
    # Return both the original and cleaned DataFrames
    return df, df_clean


def Statistics(df, country_list, indicator_list, index):
    """
    Generate a bar plot for a specific indicator over the years for selected
    countries.

    Parameters:
    df (pd.DataFrame): Original DataFrame.
    country_list (list): List of countries to include.
    indicator_list (list): List of indicators to include.
    index (int): Index of the indicator to be plotted from the indicator_list.

    Returns: None
    """
    # Filter DataFrame for selected countries and indicator
    df_sub = df[df["Country Name"].isin(
        country_list) & df["Indicator Name"].isin(indicator_list)]
    df_pop = df_sub[df_sub["Indicator Name"] == indicator_list[index]]

    # Display summary statistics
    print(df_pop.describe())
    # Drop columns with NaN values
    df_pop1 = df_pop.dropna(axis=1)

    # Create a new DataFrame for plotting
    if(index==1):
        df_new = pd.concat([df_pop1.iloc[:, 0], df_pop1.iloc[:, -6:]], axis=1)
    else:
        df_new = pd.concat([df_pop1.iloc[:, 0], df_pop1.iloc[:, -8:-2]], axis=1)
    df_new.set_index(["Country Name"], inplace=True)
    # Generate bar plot
    ax = df_new.plot(kind="bar", edgecolor='black')
    plt.xticks(rotation=45)
    # Adjust legend position
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    # Set plot title
    ax.set_title(
        f"{indicator_list[index]} ({df_new.columns[0]}-{df_new.columns[-1]})")
    # Show the plot
    plt.show()


def correlations(df, country_list, indicator_list, index, cmapstyle):
    """
    Generate a heatmap for correlation between indicators for a specific 
    country.

    Parameters:
    df (pd.DataFrame): Original DataFrame.
    country_list (list): List of countries to include.
    indicator_list (list): List of indicators to include.
    index (int): Index of the country for which correlation is calculated.
    cmapstyle (str): Colormap style for the heatmap.

    Returns:
    None
    """
    # Filter DataFrame for selected countries and indicators
    df_sub = df[df["Country Name"].isin(
        country_list) & df["Indicator Name"].isin(indicator_list)]
    # Display summary statistics
    print(df_sub.describe())
    # Filter data for the specific country and drop columns with NaN values
    df_temp = df_sub[df_sub["Country Name"] ==
                     country_list[index]].dropna(axis=1)
    # Set the indicator names as the index
    df_temp.set_index(["Indicator Name"], inplace=True)
    # Drop unnecessary columns
    df_temp.drop(["Country Name", "Country Code",
                 "Indicator Code"], axis=1, inplace=True)
    # Calculate the correlation matrix
    corr_matrix = df_temp.T.corr()
    # Set seaborn style
    sns.set(style="white")
    # Create a figure and axis
    plt.figure(figsize=(8, 6))
    # Generate heatmap with annotations
    sns.heatmap(corr_matrix, annot=True, cmap=cmapstyle,
                fmt=".2f", linewidths=.5)
    # Adjust the font size on heatmap
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)
    # Set the title of the heatmap
    plt.title(f"{country_list[index]}", fontsize=25)
    # Show the plot
    plt.show()


def Statistics_line(df, country_list, indicator_list, index):
    """
    Generate a line plot for a specific indicator over the years for selected 
    countries.

    Parameters:
    df (pd.DataFrame): Original DataFrame.
    country_list (list): List of countries to include.
    indicator_list (list): List of indicators to include.
    index (int): Index of the indicator to be plotted from the indicator_list.

    Returns:
    None
    """
    # Filter DataFrame for selected countries and indicator
    df_sub = df[df["Country Name"].isin(
        country_list) & df["Indicator Name"].isin(indicator_list)]
    df_pop = df_sub[df_sub["Indicator Name"] == indicator_list[index]]
    # Drop columns with NaN values
    df_pop1 = df_pop.dropna(axis=1)
    df_new = pd.concat([df_pop1.iloc[:, 0], df_pop1.iloc[:, -8:-2]], axis=1)
    # Create a new DataFrame for plotting
    df_new.set_index(["Country Name"], inplace=True)
    # Create a new figure with specified size
    plt.figure(figsize=(10, 6))
    # Plot a line for each country
    for country in df_new.index:
        plt.plot(df_new.columns,
                 df_new.loc[country], label=country, marker='o')
    # Set labels and legend
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    # Add grid to the plot
    plt.grid(True)
    # Add the title to plot
    plt.title(f"{indicator_list[index]}", fontsize=25)
    # Show the plot
    plt.show()


def main():
    """
    Main function to analyze and visualize climate data.

    Returns:
    None
    """
    # path to CSV file
    filename = "climate.csv"

    # Read the data from the CSV file
    df, df_clean = read_data(filename)
    # List of countries and indicators for analysis
    country_list = ["India", "South Africa", "Zimbabwe", "United States",
                    "United Kingdom", "Nigeria"]
    indicator_list = [
        "Population growth (annual %)",
        "CO2 emissions (kt)",
        "Renewable electricity output (% of total electricity output)",
        "Agricultural land (sq. km)",
        "Urban population growth (annual %)",
        "Foreign direct investment, net inflows (% of GDP)"]

    # Call functions to generate plots and visualizations
    Statistics(df, country_list, indicator_list, 0)
    Statistics(df, country_list, indicator_list, 1)
    Statistics_line(df, country_list, indicator_list, 5)
    Statistics_line(df, country_list, indicator_list, 4)
    correlations(df, country_list, indicator_list, 0, "coolwarm")
    correlations(df, country_list, indicator_list, 3, "viridis")


# Execute the main function if the script is run
if __name__ == "__main__":
    main()
