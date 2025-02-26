from langchain_experimental.agents import create_pandas_dataframe_agent
import pandas as pd
import os
from dotenv import load_dotenv
from .tools import create_visualization, df

load_dotenv()

def analyze_data(question: str) -> str:
    """
    Direct data analysis without using LLM for common questions
    """
    question = question.lower()
    print(f"Analyzing question: {question}")
    
    print("Received question for analysis.")
    
    if "ratio" in question and ("children" in question or "child" in question) and ("adult" in question or "adults" in question):
        print("Calculating ratio of children to adults...")
        children_count = df[df['Age'] < 18].shape[0]
        adults_count = df[df['Age'] >= 18].shape[0]
        if adults_count == 0:
            return "There are no adults in the dataset."
        ratio = children_count / adults_count
        return f"The ratio of children to adults is {children_count}:{adults_count} or approximately {ratio:.2f}:1."
    
    elif "percentage" in question and ("male" in question or "man" in question):
        male_count = df[df['Sex'] == 'male'].shape[0]
        total_count = df.shape[0]
        if total_count == 0:
            return "There are no passengers in the dataset."
        male_percentage = (male_count / total_count) * 100
        return f"{male_percentage:.2f}% of passengers were male on the Titanic."
    
    if "percentage" in question and "survived" in question:
        survival_rate = (df['Survived'].mean() * 100)
        return f"{survival_rate:.2f}% of passengers survived the Titanic disaster."
    
    elif "average" in question and "fare" in question:
        avg_fare = df['Fare'].mean()
        return f"The average fare price was £{avg_fare:.2f}"
    
    elif "histogram" in question and "age" in question:
        return create_visualization._run("histogram", "Age")
    
    elif ("bar" in question or "chart" in question) and "class" in question and "survival" in question:
        return create_visualization._run("bar", "Pclass", "Survived")
    
    elif "how many" in question and "passengers" in question:
        total = len(df)
        return f"There were {total} passengers in the dataset."
    
    else:
        return "I can help you with:\n- Survival statistics\n- Average fare price\n- Age distribution\n- Survival by passenger class\n- Passenger counts\nPlease ask about one of these topics."

def get_agent_response(question: str) -> str:
    """
    Get response from the agent for a given question
    """
    try:
        return analyze_data(question)
    except Exception as e:
        return f"Error processing your question: {str(e)}" 