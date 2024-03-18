cluster_llm/load_dataset.py :
flowchart 따라서 작성됨. 공동 개발자 관련과 특허 관련 search는 아직 안했음.

dataset/kr_samename.csv:
한국인만 모아서, explode를 통해 공동 개발자들 다 찢어놓고, 이름이 한번만 등장하는 경우는 제거함.

graph_ex/graph_util.py:
plotly를 통해 grantt 그래프를 그림. x축은 시간, y축은 소속 명 으로 하였음.

preprocessing_data/.:
util들 모아놓은 폴더임. 딱히 사용은 안함.
