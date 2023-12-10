# Base class for chart styling and saving
import base64
from io import BytesIO

import numpy as np
from matplotlib import pyplot as plt


class ChartStyler:
    @staticmethod
    def style_chart(x_label, y_label, title, y_ticks, grid, grid_alpha):
        plt.xlabel(x_label, fontsize=12, color='#696A8F')
        plt.ylabel(y_label, fontsize=12, color='#696A8F')
        plt.title(title, fontsize=14, color='#696A8F')

        if grid:
            plt.grid(axis='y', linestyle='--', alpha=grid_alpha)

        if y_ticks is not None:
            plt.yticks(y_ticks)

    @staticmethod
    def save_and_encode_plot():
        # Save the plot to a BytesIO object
        image_stream = BytesIO()
        plt.savefig(image_stream, format='png')
        image_stream.seek(0)
        img_data = base64.b64encode(image_stream.read()).decode('utf-8')
        plt.close()  # Close the plot to free up resources
        return img_data if img_data else None


# Service class for generating charts
class GraphGeneratorService(ChartStyler):
    @staticmethod
    def make_line_graph(x_values, y_values, x_label, y_label, title, y_ticks=None, grid=None, grid_alpha=None):
        if grid is None:
            grid = plt.get_current_fig_manager()
        elif grid_alpha is None:
            grid_alpha = 0.3
        plt.plot(x_values, y_values, color="blue")
        ChartStyler.style_chart(x_label, y_label, title, y_ticks, grid, grid_alpha)
        return ChartStyler.save_and_encode_plot()

    @staticmethod
    def generate_bar_chart(categories, values, special_bars=None, x_label=None, y_label=None, title=None,
                           y_ticks=None, grid=True, grid_alpha=0.5):
        # Set the background color
        plt.figure(facecolor='#F8F8F8')

        # Use a colormap to generate colors dynamically
        colors = plt.cm.viridis(np.linspace(0, 1, len(categories)))

        # Plotting the bar chart with styling options
        bars = plt.bar(categories, values, color=colors, edgecolor='#B0B1C3', linewidth=1.2, alpha=0.7)

        # Set individual colors for specific bars if special_bars is provided
        if special_bars:
            for i, bar in enumerate(bars):
                if i in special_bars:
                    bar.set_color('#FF5733')  # Highlight color for special bars

        # Style the plot using the ChartStyler
        ChartStyler.style_chart(x_label, y_label, title, y_ticks, grid, grid_alpha)

        # Save the plot to a BytesIO object and encode it in base64
        return ChartStyler.save_and_encode_plot()

    @staticmethod
    def generate_pie_chart(categories, values, title):
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=categories, autopct='%1.1f%%', startangle=140)
        plt.title(title)
        plt.axis('equal')  # Ensure pie chart is a circle
        return GraphGeneratorService.save_and_encode_plot()
