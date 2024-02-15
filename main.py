import argparse
import pandas as pd
from efficiency_calculator import calculate_efficiency, plot_efficiency_evolution, plot_correlation_heatmap, plot_3d_scatter, plot_density_heatmap

def main():
    # Load DataFrame from CSV file
    df = pd.read_csv("data.csv", index_col='day')
    df.index = pd.to_datetime(df.index)
    result = calculate_efficiency(df)
    print(result)
    parser = argparse.ArgumentParser(description="Run different functions on data.")
    parser.add_argument("function", choices=["calculate_efficiency", "plot_efficiency_evolution", "plot_correlation_heatmap", "plot_3d_scatter", "plot_density_heatmap", "predict_burner_power"], help="Choose a function to run")
    
    # Add arguments for function parameters
    parser.add_argument("--material", type=float, help="Material in kilograms")
    parser.add_argument("--temperature", type=float, help="Temperature in Celsius")
    parser.add_argument("--model_file", help="Path to the model file")

    args = parser.parse_args()

    if args.function == "plot_efficiency_evolution":
        #df = pd.read_csv("data.csv")
        plot_efficiency_evolution(result, "results/efficiency_evolution_plot.html")
    elif args.function == "plot_correlation_heatmap":
        #df = pd.read_csv("data.csv")
        plot_correlation_heatmap(result, "results/correlation_heatmap.html")
    elif args.function == "plot_3d_scatter":
        #df = pd.read_csv("data.csv")
        plot_3d_scatter(result, "results/scatter_plot_3D.html")
    elif args.function == "plot_density_heatmap":
        #df = pd.read_csv("data.csv")
        plot_density_heatmap(result, "results/density_heatmap.html")
    elif args.function == "predict_burner_power":
        from efficiency_calculator import predict_burner_power
        if args.material is None or args.temperature is None or args.model_file is None:
            parser.error("You must provide --material, --temperature, and --model_file arguments for predict_burner_power function")
        result = predict_burner_power(args.material, args.temperature, args.model_file)
        print("Predicted burner power:", result, "\n")
    else:
        parser.error("Invalid function")

if __name__ == "__main__":
    main()
