import pandas as pd
import matplotlib.pyplot as plt
import requests
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns
import pygwalker as pg
from sklearn.preprocessing import StandardScaler
import folium
from geopy.geocoders import Nominatim

import ssl
import certifi
import geopy.geocoders
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

def get_vicpop_data(port):
    fission_url = f"http://localhost:{port}/search-vic-population"
    response = requests.get(fission_url,verify=False)
    return response.json()

def get_subcrimecount_data(port):
    fission_url = f"http://localhost:{port}/search-vic-crime-by-offence-count"
    response = requests.get(fission_url,verify=False)
    return response.json()

def get_southaus_data(port):
    fission_url = f"http://localhost:{port}/search-south-crimegov"
    response = requests.get(fission_url,verify=False)
    return response.json()

def get_viccrimegov_data(port):
    fission_url = f"http://localhost:{port}/search-vic-crimegov"
    response = requests.get(fission_url,verify=False)
    return response.json()

def process_vic_pop(port):
    population_data = pd.DataFrame(get_vicpop_data(port))
    population_cols = [col for col in population_data.columns if 'tpop_' in col and int(col.split('_')[1]) in range(2019, 2024)]
    population_sums = []
    for col in population_cols:
        year = int(col.split('_')[1])
        pop_sum = population_data[col].sum()
        population_sums.append((year, pop_sum))
    population_sums.sort(key=lambda x: x[0])
    return population_sums

def process_vic_subcrime(port):
    crime_count = pd.DataFrame(get_subcrimecount_data(port))
    crime_count['Sum of Offence Count' ] = crime_count['Sum of Offence Count' ].astype(str)
    crime_count['Sum of Offence Count' ] = crime_count['Sum of Offence Count' ].str.replace(',', '')
    crime_count['Sum of Offence Count' ] = crime_count['Sum of Offence Count' ].astype(int)
    return crime_count

def combine_vic_pop_crime(port):
    population_sums = process_vic_pop(port)   
    crime_count = process_vic_subcrime(port)
    population_df = pd.DataFrame(population_sums, columns=['year', 'population'])
    merged_df = pd.merge(crime_count, population_df, left_on='filters', right_on='year', how='left')
    merged_df = merged_df.drop(['filters'], axis=1)
    return merged_df

def get_user_input_cdivision():
    while True:
        input_division = input("Enter Crime Subdivision (A, B, C, D, or E) or type 'Esc' to cancel: ")
        input_division = input_division.upper()  # Convert to uppercase to standardize the input

        if input_division == "ESC":
            print("Operation cancelled by the user.")
            return None  # Return None to indicate cancellation

        # Dictionary of valid subdivisions
        offence_divisions = {
            "A": "A Crimes against the person",
            "B": "B Property and deception offences",
            "C": "C Drug offences",
            "D": "D Public order and security offences",
            "E": "E Justice procedures offences"
        }

        if input_division in offence_divisions:
            return offence_divisions[input_division]  # Return the corresponding division description
        else:
            print("Invalid input. Please enter A, B, C, D, or E, or type 'Esc' to cancel.")


def plot_offence_vs_population(port):
    merged_df = combine_vic_pop_crime(port)
    RANDOM_STATE = 42
    FIG_SIZE = (12, 8)
    N_ESTIMATORS = 100
    
    offence_division = get_user_input_cdivision()
        
    
    # Filter the DataFrame for the specific 'Offence Division: Descending'
    filtered_df = merged_df[merged_df['Offence Division: Descending'] == offence_division]

    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print(f"No data found for offence division: {offence_division}")
        return

    # Extract the data for the regression models
    X = filtered_df[['population']]
    y = filtered_df['Sum of Offence Count']

    # Linear Regression model
    linear_model = LinearRegression()
    linear_model.fit(X, y)

    # Polynomial Regression model (degree 2)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    poly_model = LinearRegression()
    poly_model.fit(X_poly, y)

    # Random Forest Regression model
    rf_model = RandomForestRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
    rf_model.fit(X, y)

    # Generate predictions
    X_pred = np.linspace(X.min(), X.max(), 100).reshape(-1, 1)
    X_pred_df = pd.DataFrame(X_pred, columns=['population'])
    y_pred_linear = linear_model.predict(X_pred_df)
    y_pred_poly = poly_model.predict(poly.fit_transform(X_pred_df))
    y_pred_rf = rf_model.predict(X_pred_df)

    # Use seaborn style for better aesthetics
    sns.set(style='whitegrid')

    # Plotting the line graph
    plt.figure(figsize=FIG_SIZE)
    
    # Scatter plot for actual data
    plt.scatter(filtered_df['population'], filtered_df['Sum of Offence Count'], color='blue', label='Actual Data', s=50)
    
    # Line plots for predictions
    plt.plot(X_pred, y_pred_linear, color='red', linestyle='-', linewidth=2, label='Linear Regression')
    plt.plot(X_pred, y_pred_poly, color='green', linestyle='--', linewidth=2, label='Polynomial Regression (degree 2)')
    plt.plot(X_pred, y_pred_rf, color='purple', linestyle='-.', linewidth=2, label='Random Forest Regression')
    
    # Adding titles and labels
    plt.title(f'Sum of Offence Count vs Population\n({offence_division})', fontsize=16, weight='bold')
    plt.xlabel('Population', fontsize=14)
    plt.ylabel('Sum of Offence Count', fontsize=14)
    
    # Customizing legend
    plt.legend(fontsize=12, loc='upper left', frameon=True, shadow=True, borderpad=1)
    
    # Enhancing the grid and layout
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Display the plot
    plt.show()


def process_pop_map(port):
    population_data = pd.DataFrame(get_vicpop_data(port))
    population_data.columns = population_data.columns.str.strip()

    # Remove the suffixes from 'lga_name'
    population_data['lga_name'] = population_data['lga_name'].str.split(' \(').str[0]

    # Group by 'lga_name' and sum up the population for each location
    population_data = population_data.groupby('lga_name').sum().reset_index()
    return population_data


def process_crime_lga(port):
    crime_lga = pd.DataFrame(get_viccrimegov_data(port))
    crime_lga['Sum of Offence Count' ] = crime_lga['Sum of Offence Count' ].astype(str)
    crime_lga['Sum of Offence Count' ] = crime_lga['Sum of Offence Count' ].str.replace(',', '')
    crime_lga['Sum of Offence Count' ] = crime_lga['Sum of Offence Count' ].astype(int)
    pivot_df = crime_lga.pivot(index='Local Government Area: Descending', columns='filters', values='Sum of Offence Count')
    # Rename columns
    pivot_df.columns = ['scrime_' + str(col) for col in pivot_df.columns]
    # Reset index
    pivot_df.reset_index(inplace=True)
    return pivot_df


def combine_pop_crime_map(port):
    population_data = process_pop_map(port)
    pivot_df = process_crime_lga(port)
    merged_df = pd.merge(pivot_df, population_data, left_on='Local Government Area: Descending', right_on='lga_name', how='inner')

    # Drop the redundant 'Local Government Area' column
    merged_df.drop('lga_name', axis=1, inplace=True)
    merged_df.rename(columns={'Local Government Area: Descending': 'lga'}, inplace=True)
    return merged_df


def get_user_input_location():
    while True:
        user_lga_names = input("Enter the LGA name(s) separated by comma: ").strip().split(',')
        user_lga_names = [name.strip() for name in user_lga_names]  # Clean up input
        user_year = input("Enter the year (2019-2031): ").strip()
        if not user_year.isdigit():
            print("Invalid input. Please enter a valid year between 2019 and 2031. Please re-run the function")
            return
        user_year = int(user_year)
        if 2019 <= user_year <= 2031:
            if user_year > 2023:
                print(f'The input year {user_year} is in the future. The crime count is predicted based on the estimated population.')
            return user_lga_names, user_year
        else:
            print("Invalid input. Please enter a valid year between 2019 and 2031. Please re-run the function")
            return

def predict_crime_count(lga_name, user_year, merged_df, lga_data):
    population_columns = [f'tpop_{year}' for year in range(2019, 2024)]
    crime_columns = [f'scrime_{year}' for year in range(2019, 2024)]

    X_train = merged_df[merged_df['lga'] == lga_name][population_columns].values.flatten()  # Population data flattened to 1D array
    y_train = merged_df[merged_df['lga'] == lga_name][crime_columns].values.flatten()
    poly = PolynomialFeatures(degree=2)
    X_poly_train = poly.fit_transform(X_train.reshape(-1, 1))
    model = LinearRegression()
    model.fit(X_poly_train, y_train)

    new_population = lga_data.iloc[0][f'tpop_{user_year}']  # Adjust this value as needed
    new_population_poly = poly.transform([[new_population]])
    crime_predict = model.predict(new_population_poly)
    crime_predict = int(crime_predict[0])
    return crime_predict

def print_pop_crime_map(port):
    user_lga_names, user_year = get_user_input_location()
    merged_df = combine_pop_crime_map(port)
    # Filter data for the specified LGAs and year
    filtered_data = merged_df[merged_df['lga'].isin(user_lga_names)]
    # Initialize the geocoder
    geolocator = Nominatim(user_agent="city_locator")
    # Get the coordinates for each LGA
    locations = {}
    population = {}
    crime_count = {}
    for lga_name in user_lga_names:
        # Find the location coordinates for each LGA
        location = geolocator.geocode(lga_name + ', Australia')
        if location:
            locations[lga_name] = (location.latitude, location.longitude)

            # Extract population for the specified year and LGA
            lga_data = filtered_data[(filtered_data['lga'] == lga_name) & (filtered_data[f'tpop_{user_year}'].notnull())]
            if not lga_data.empty:
                population[lga_name] = lga_data.iloc[0][f'tpop_{user_year}']
                if 2019 <= int(user_year) <= 2023:
                    crime_count[lga_name] = lga_data.iloc[0][f'scrime_{user_year}']
                elif int(user_year) > 2023:
                    crime_count[lga_name] = predict_crime_count(lga_name, user_year, merged_df, lga_data)
        else:
            print(f"No location found for {lga_name}.")
            return

    # Create a map centered at the specified location
    map_center = [-36, 145]  # Center of Australia
    if locations:
        m = folium.Map(location=map_center, zoom_start=6)
        # Add markers for each location with population information
        for lga_name, location in locations.items():
            if lga_name in population:
                popup_text = f"{lga_name}<br>Population in {user_year}: {population[lga_name]}<br>Crime in {user_year}: {crime_count[lga_name]}"
            else:
                popup_text = f"No population data available for {user_year}"

            folium.Marker(
                location=location,
                popup=popup_text,
                tooltip=lga_name
            ).add_to(m)

        # Display the map
        display(m)
    else:
        print("No valid locations found.")


def process_southaus(port):
    south_aus = pd.DataFrame(get_southaus_data(port))
    south_aus = south_aus.drop('@timestamp', axis=1)
    south_aus['Sum of Offence count' ] = south_aus['Sum of Offence count' ].astype(str)
    south_aus['Sum of Offence count' ] = south_aus['Sum of Offence count' ].str.replace(',', '')
    south_aus['Sum of Offence count' ] = south_aus['Sum of Offence count' ].astype(int)
    south_aus['Reported Date per month'] = pd.to_datetime(south_aus['Reported Date per month'])
    # Extract month and year
    south_aus['Month'] = south_aus['Reported Date per month'].dt.month
    south_aus['Year'] = south_aus['Reported Date per month'].dt.year
    # Create the new DataFrame with the desired columns
    new_df = south_aus[['Month', 'Sum of Offence count', 'Year']]
    # Rename columns
    new_df.columns = ['Month', 'Count', 'Year']
    return new_df


def pgwalk_southaus(port):
    new_df = process_southaus(port)
    vis_spec = r"""{"config":[{"config":{"defaultAggregated":false,"geoms":["area"],"coordSystem":"generic","limit":-1,"timezoneDisplayOffset":0,"folds":["Count"]},"encodings":{"dimensions":[{"fid":"Count","name":"Count","basename":"Count","analyticType":"dimension","semanticType":"quantitative","aggName":"sum","offset":0},{"fid":"gw_mea_key_fid","name":"Measure names","analyticType":"dimension","semanticType":"nominal"}],"measures":[{"fid":"Month","name":"Month","basename":"Month","semanticType":"quantitative","analyticType":"measure","offset":0},{"fid":"Year","name":"Year","basename":"Year","semanticType":"nominal","analyticType":"measure","offset":0},{"fid":"gw_count_fid","name":"Row count","analyticType":"measure","semanticType":"quantitative","aggName":"sum","computed":true,"expression":{"op":"one","params":[],"as":"gw_count_fid"}},{"fid":"gw_mea_val_fid","name":"Measure values","analyticType":"measure","semanticType":"quantitative","aggName":"sum"}],"rows":[{"fid":"Count","name":"Count","basename":"Count","analyticType":"dimension","semanticType":"quantitative","aggName":"sum","offset":0}],"columns":[{"fid":"Month","name":"Month","basename":"Month","semanticType":"quantitative","analyticType":"dimension","offset":0}],"color":[{"fid":"Year","name":"Year","basename":"Year","semanticType":"nominal","analyticType":"measure","offset":0}],"opacity":[{"fid":"Year","name":"Year","basename":"Year","semanticType":"nominal","analyticType":"measure","offset":0}],"size":[],"shape":[],"radius":[],"theta":[],"longitude":[],"latitude":[],"geoId":[],"details":[],"filters":[{"fid":"Year","name":"Year","basename":"Year","semanticType":"nominal","analyticType":"measure","offset":0,"rule":{"type":"not in","value":[2021,2023]}}],"text":[]},"layout":{"showActions":true,"showTableSummary":false,"stack":"none","interactiveScale":false,"zeroScale":true,"size":{"mode":"fixed","width":462,"height":440},"format":{},"geoKey":"name","resolve":{"x":false,"y":false,"color":true,"opacity":true,"shape":false,"size":false},"scaleIncludeUnmatchedChoropleth":false,"showAllGeoshapeInChoropleth":false,"colorPalette":"spectral","useSvg":false,"scale":{"opacity":{},"size":{}}},"visId":"gw_2u97","name":"Chart 1"}],"chart_map":{},"workflow_list":[{"workflow":[{"type":"filter","filters":[{"fid":"Year","rule":{"type":"not in","value":[2021,2023]}}]},{"type":"view","query":[{"op":"raw","fields":["Month","Count","Year","Year"]}]}]}],"version":"0.4.8.4"}"""
    pg.walk(new_df, spec=vis_spec)


def build_train_pop_crime(port):
    merged_df = combine_vic_pop_crime(port)
    merged_df = merged_df.drop(columns=['Offence Division: Descending'])
    result = merged_df.groupby(['year', 'population']).sum().reset_index()
    result = result.drop(columns=['year'])
    X = result[['Sum of Offence Count']]
    y = result['population']
    return X, y

def data_pred(port):
    X, y = build_train_pop_crime(port)
    new_df = process_southaus(port)
    degree = 2
    model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
    model.fit(X, y)
    
    yearly_crime_counts = new_df.groupby('Year').agg({'Count': 'sum'}).reset_index()
    yearly_crime_counts.rename(columns={'Count': 'Sum of Offence Count'}, inplace=True)
    
    X_yearly = yearly_crime_counts[['Sum of Offence Count']]
    yearly_crime_counts['Predicted Population'] = model.predict(X_yearly).astype(int)
    
    model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
    model_rf.fit(X, y)
    
    predicted_population_rf = model_rf.predict(X_yearly)
    predicted_population_rf = np.maximum(0, predicted_population_rf)  # Clip negative values to 0 using np.maximum
    yearly_crime_counts['Predicted Population (Random Forest)'] = predicted_population_rf.astype(int)
    
    model_lr = LinearRegression()
    model_lr.fit(X, y)
    
    predicted_population_lr = model_lr.predict(X_yearly)
    predicted_population_lr = np.maximum(0, predicted_population_lr)  # Clip negative values to 0 using np.maximum
    yearly_crime_counts['Predicted Population (Linear Regression)'] = predicted_population_lr.astype(int)
    
    return yearly_crime_counts

def predict_pop_by_crime(port):
    yearly_crime_counts = data_pred(port)
    print(yearly_crime_counts)
    
    plt.figure(figsize=(10, 6))
    plt.plot(yearly_crime_counts['Year'], yearly_crime_counts['Predicted Population (Linear Regression)'], marker='o', linestyle='-', color='b')
    plt.plot(yearly_crime_counts['Year'], yearly_crime_counts['Predicted Population (Random Forest)'], marker='x', linestyle='--', color='r')

    # Adding labels and title
    plt.xlabel('Year')
    plt.ylabel('Predicted Population')
    plt.title('Year vs Predicted Population')
    plt.grid(True)
    plt.xticks(yearly_crime_counts['Year'])  # Ensure x-ticks are the years

    # Display the plot
    plt.legend(['Linear Regression', 'Random Forest'])
    plt.show()
