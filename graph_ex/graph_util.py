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
    
    df = pd.DataFrame([ast.literal_eval(row) for row in df["record"]])
    
    # 특정 이름을 포함하는 행만 필터링
    df = df[df["name"].str.contains(name)]
    # "start"와 "end" 열의 데이터 타입을 날짜로 변환
    df["start"] = pd.to_datetime(df["start"])
    df=df.sort_values(by=["start"])
    df["end"] = pd.to_datetime(df["end"])
    fig = px.timeline(df, x_start="start", x_end="end", y="applicant",color="applicant")
    fig.update_yaxes(autorange="reversed")  # Y축 역방향으로 설정
    fig.show()
    fig.write_html(f'draws_gantt_by_csv_{name}.html', auto_open=True)

def main():
    name="김민수"
    df= pd.read_csv("./../dataset/result.csv")
    
    draw_gantt_by_csv(df,name)
    
if __name__ == "__main__":
    main()
