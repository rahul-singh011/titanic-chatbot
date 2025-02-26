import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import pandas as pd
from langchain.tools import BaseTool

df = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')

def plot_to_base64():
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    plt.close()
    return image_base64

class CreateVisualizationTool(BaseTool):
    name: str = "create_visualization"
    description: str = "Creates visualizations for the Titanic dataset. Useful for creating charts and graphs of passenger data."
    
    def _run(self, plot_type: str, x: str, y: str = None):
        plt.figure(figsize=(10, 6))
        
        if plot_type == "histogram":
            sns.histplot(data=df, x=x)
            plt.title(f"Distribution of {x}")
            
        elif plot_type == "bar":
            if y:
                sns.barplot(data=df, x=x, y=y)
                plt.title(f"{y} by {x}")
            else:
                df[x].value_counts().plot(kind='bar')
                plt.title(f"Count of {x}")
                
        elif plot_type == "scatter":
            if y:
                sns.scatterplot(data=df, x=x, y=y)
                plt.title(f"{y} vs {x}")
            else:
                raise ValueError("Scatter plot requires both x and y values")
        
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        return {
            "image": plot_to_base64(),
            "type": "image"
        }

    def _arun(self, plot_type: str, x: str, y: str = None):
        raise NotImplementedError("Async not implemented")

create_visualization = CreateVisualizationTool() 