import matplotlib.pyplot as plt
import seaborn as sns

#### Visualisation functions #######

def bar_chart(x_axis: str, y_axis: str, title: str, x_lable: str, y_lable:str, data):
    """
    Bar chart
    """
    # Bar chart: late rate by service
    sns.barplot(x = x_axis, y = y_axis, data=data)
    plt.title(title)
    plt.ylabel(y_lable)
    plt.xlabel(x_lable)
    plt.savefig("bar_chart.png", dpi=300, bbox_inches='tight')
    plt.show()

def line_chart(x_axis, y_axis, title, x_lable, y_lable, data, marker):
    # Line chart: late rate over months
    sns.lineplot(x = x_axis, y = y_axis, data=data, marker=marker)
    plt.title(title)
    plt.ylabel(y_lable)
    plt.xlabel(x_lable)
    plt.savefig("line_chart.png", dpi=300, bbox_inches='tight')
    plt.show()

def heatmap_chart(df, title):
    # Heatmap: region vs service late rate
    pivot = df.pivot_table(index="region", columns="service_type", values="is_late", aggfunc="mean")
    sns.heatmap(pivot, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title(title)
    plt.savefig("heatmap_chart.png", dpi=300, bbox_inches='tight')
    plt.show()

def scatter_graph(x_axis, y_axis, title, hue, data):
# Scatter: delivery time vs rating
    sns.scatterplot(x = x_axis, y = y_axis, hue=hue, data=data)
    plt.title(title)
    plt.savefig("scatter_graph.png", dpi=300, bbox_inches='tight')
    plt.show()
