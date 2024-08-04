import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os

def plot_tokens_per_second(csv_path: str, title: str, ylimit: int = None):
    # Read the data into a DataFrame
    df = pd.read_csv(csv_path)

    # Sort the dataframe by Request Number to ensure the X-axis is in order
    df = df.sort_values(by='Request Number')

    # Set the style
    sns.set(style="whitegrid")

    # Create the figure and axis
    fig, ax = plt.subplots(figsize=(20, 10))

    # Plot the bar chart with color gradient
    bars = ax.bar(df['Request Number'], df['Tokens per Second'], color=sns.color_palette("viridis", len(df)))

    # Add labels on top of the bars with better positioning and formatting
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.0f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5),  # 5 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=11, color='black')

    # Set the labels and title with increased font size
    ax.set_xlabel('Request Number', fontsize=14)
    ax.set_ylabel('Tokens per Second', fontsize=14)
    ax.set_title(title, fontsize=18, fontweight='bold')

    # Set Y-axis limit if provided
    if ylimit is not None:
        ax.set_ylim(0, ylimit)

    # Improve the x-axis labels by rotating and adjusting them
    plt.xticks(df['Request Number'], rotation=60, ha='center', fontsize=12)

    # Add grid lines for better readability
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Convert title to filename
    filename = re.sub(r'\s+', '-', title) + '.png'

    # Define the folder path and ensure it exists
    folder_path = 'images'
    os.makedirs(folder_path, exist_ok=True)

    # Save the improved plot as a PNG file with increased width
    plt.savefig(os.path.join(folder_path, filename), bbox_inches='tight')

    # Show the improved plot with increased width
    plt.show()

if __name__ == "__main__":
    # Example usage
    y_axis_limit = 50
    plot_tokens_per_second("results.csv", "Llama-3-70B-Instruct-FP8-(Sequential)-(H100-PCie-2-GPUs)")
    # plot_tokens_per_second("results.csv", "Llama-3-70B-Instruct-FP8-(Concurent)-(H100-PCie-2-GPUs)")
    # plot_tokens_per_second("results.csv", "Llama-3.1-70b-versatile-(Concurent)-(Groq)", 250)
    # plot_tokens_per_second("results.csv", "Llama-3.1-70b-versatile-(Sequential)-(Groq)", 250)