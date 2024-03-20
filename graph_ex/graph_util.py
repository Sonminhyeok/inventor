import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import ast
def draw_bars_by_csv(df, num_rows, x_name="keyphrarse", y_name="similarity"): #when convert csv df to graph
    fig = go.Figure()
    for i in range(num_rows):
        fig.add_trace(
            go.Bar(
                x=eval(df[x_name][i]),
                y=eval(df[y_name][i]),
                name=f"{i}번째 행"
            )
        )
    fig.update_yaxes(range=[0.0, 0.8])
    fig.show()
    fig.write_html('draws_bars_by_csv.html', auto_open=True)

def draw_bars_by_list(num_rows, x, y): #when convert 2-dimlist to graph
    fig = go.Figure()
    for i in range(num_rows):       
        fig.add_trace(
            go.Bar(
                x=x[i],
                y=y[i],
                name=f"{i}번째 행"
            )
        )
    fig.update_yaxes(range=[0.0, 0.8])
    fig.show()
    # fig.write_html('draws_bars_by_list.html', auto_open=True)
def draw_gantt_by_csv(df, name):
    list1 =[]
    df = df[df["name"].str.contains(name)]
    for i in df["record"]:
        for m in eval(i):
            list1.append(m)
        
    # print(list1[0])
    
    
    
    fig = px.timeline(list1, x_start="start", x_end="end", y="applicant",color="applicant")
    fig.update_yaxes(autorange="reversed")  # Y축 역방향으로 설정
    fig.show()
    fig.write_html(f'draws_gantt_by_csv_{name}.html', auto_open=True)

def main():
    name="소원욱"
    df= pd.read_csv("./../dataset/result.csv")
    
    draw_gantt_by_csv(df,name)
    
if __name__ == "__main__":
    main()
