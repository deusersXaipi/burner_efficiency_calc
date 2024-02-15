#################################################################### IMPORTS ####################################################################


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras import regularizers
from tensorflow.keras.models import load_model


#################################################################### FUNCTIONS ####################################################################

def calculate_efficiency(df: pd.DataFrame, thermal_efficiency: float = 0.8) -> pd.DataFrame:
    """
    Calculate the efficiency of a burner.

    Parameters:
        - df (pandas DataFrame): DataFrame containing at least the columns 'temperature' and 'burner_power'.
        - thermal_efficiency (float, optional): The thermal efficiency of the burner. Defaults to 0.8.

    Returns:
        pandas DataFrame: DataFrame with an additional column 'efficiency' representing the calculated efficiency.
    """
    df['adjustment_factor'] = (df['temperature'] / df['burner_power']) * thermal_efficiency
    df['efficiency'] = (df['adjustment_factor'] * 100) / df['adjustment_factor'].max()
    return df



def plot_efficiency_evolution(df: pd.DataFrame, filename: str) -> None:
    """
    Plot the evolution of efficiency over time.

    Parameters:
        - df (pandas DataFrame): DataFrame containing the efficiency data.
        - filename (str): Name for the saved plot.

    Returns:
        None
    """
    fig = px.line(df, x=df.index, y='efficiency', title='Efficiency Evolution')
    fig.update_xaxes(title='Date')
    fig.update_yaxes(title='Efficiency')

    pio.write_html(fig, filename)



def plot_correlation_heatmap(df: pd.DataFrame, filename: str):
    """
    Plot a heatmap showing the correlation between variables in the DataFrame.

    Parameters:
        - df (pandas DataFrame): DataFrame containing the variables for correlation analysis.
        - filename (str): Name for the saved plot.

    Returns:
        None
    """
    # Calculate correlation matrix
    correlation_matrix = df.corr()

    # Create the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='Viridis'))

    # Customize layout
    fig.update_layout(
        title='Variables correlation',
        xaxis_title='Variables',
        yaxis_title='Variables')

    pio.write_html(fig, filename)



def plot_3d_scatter(df: pd.DataFrame, filename: str):
    """
    Plot a 3D scatter plot using temperature, burner power, and material.

    Parameters:
        - df (pandas DataFrame): DataFrame containing the data for the 3D scatter plot.
        - filename (str): Name for the saved plot.

    Returns:
        None
    """
    fig = go.Figure(data=[go.Scatter3d(
        x=df['temperature'],
        y=df['burner_power'],
        z=df['material'],
        mode='markers',
        marker=dict(
            size=5,
            color='blue',                # You can customize the color here
            opacity=0.8
        )
    )])

    # Customize layout
    fig.update_layout(scene=dict(
                        xaxis_title='Temperature',
                        yaxis_title='Burner power',
                        zaxis_title='Material'
                        ),
                        title='3D scatter plot',
                        margin=dict(l=0, r=0, b=0, t=30))

    pio.write_html(fig, filename)



def plot_density_heatmap(df: pd.DataFrame, filename: str):
    """
    Plot a 2D density heatmap of temperature and burner power.

    Parameters:
        - df (pandas DataFrame): DataFrame containing the data for the density heatmap.
        - filename (str): Name for the saved plot.

    Returns:
        None
    """
    fig = px.density_heatmap(df, x='temperature', y='burner_power', title='Temperature & Burner Power density plot')

    # Customize layout (optional)
    fig.update_layout(xaxis_title='Temperature',
                    yaxis_title='Burner power')

    pio.write_html(fig, filename)



def predict_burner_power(material:float, temperature:float, model_file:str) -> float:
    """
    Predicts the burner power using a pre-trained neural network model.

    Parameters:
    - material (float): The amount of material in kilograms.
    - temperature (float): The temperature in Celsius.
    - model_file (str): The file path to the pre-trained model.

    Returns:
    - float: The predicted burner power.
    """
    # Create and fit the StandardScaler
    scaler = StandardScaler()
    
    # Scaling the input data
    scaled_input = scaler.fit_transform([[material, temperature]])

    # Load the trained model from the file
    loaded_model = load_model(model_file)

    # Make predictions with the loaded model
    predicted_burner_power = loaded_model.predict(scaled_input)

    return round(predicted_burner_power[0][0], 2)