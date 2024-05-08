from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
from settings import OPENAI_API_KEY
# import pandas as pd

# df = pd.read_csv('./corpus/employees.csv', sep=';', encoding='latin-1')
# print(df.head())

llm = ChatOpenAI(model="gpt-4", temperature=0)

agent = create_csv_agent(
    llm,
    'corpus/employees.csv',
    agent_type="openai-tools",
    pandas_kwargs={"encoding": "latin-1", "sep": ";"},
    verbose=True)

agent.run("What is the attrition rate for the last few years? The current date is 2024 May 06. You can assume that "
          "for any given date, if the date you are looking at is between the startDate and lastEmploymentDate, "
          "then that person is employed. If an employee does not have a lastEmploymentDate, the person is still "
          "employed")
