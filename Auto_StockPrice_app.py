import pandas as pd
import yfinance as yf
import altair as alt
import streamlit as st

st.title('自動車業界　株価可視化アプリ')

st.sidebar.write("""
# 自動車業界株価
こちらは株価可視化ツールです。以下のオプションから表示日数を指定できます。
""")

st.sidebar.write("""
## 表示日数選択
""")

days = st.sidebar.slider('日数', 1, 60, 30)

st.write(f"""
### 過去　**{days}日間** の自動車業界株価
""")

@st.cache
def get_data(days, tickers):
    df = pd.DataFrame()
    for company in tickers.keys():
        tkr = yf.Ticker(tickers[company])
        hist = tkr.history(period=f'{days}d')
        hist.index = hist.index.strftime('%d %B %Y')
        hist = hist[['Close']]
        hist.columns = [company]
        hist = hist.T
        hist.index.name = 'Name'
        df = pd.concat([df, hist])
    return df
try:
    st.sidebar.write("""
    ## 株価の範囲指定
    """)
    ymin, ymax = st.sidebar.slider(
        '範囲を指定して下さい。',
        0.0, 10000.0, (0.0, 10000.0)
    )

    tickers = {
        'toyota': '7203.T',
        'nissan': '7201.T',
        'honda': '7267.T',
        'subaru': '7270.T',
        'mazda': '7261.T',
        'suzuki': '7269.T',
        'yamaha': '7272.T',
        'kawasaki': '7012.T'
    }

    df = get_data(days, tickers)
    companies = st.multiselect(
        '会社名を選択して下さい。',
        list(df.index),
        ['toyota', 'nissan', 'honda', 'subaru', 'mazda', 'suzuki', 'yamaha', 'kawasaki']
    )

    if not companies:
        st.error('少なくとも一社は選んでください。')
    else:
        data = df.loc[companies]
        st.write("### 株価 (JPY)", data.sort_index())
        data = data.T.reset_index()
        data = pd.melt(data, id_vars=['Date']).rename(
            columns={'value': 'Stock Prices (JPY)'}
        )

        chart = (
            alt.Chart(data)
                .mark_line(opacity=0.8, clip=True)
                .encode(
                x="Date:T",
                y=alt.Y("Stock Prices (JPY):Q", stack=None,
                        scale=alt.Scale(domain=[ymin, ymax])),
                color='Name:N'
            )
        )
        st.altair_chart(chart, use_container_width=True)
except:
    st.error(
        "エラー!! サイドバーの値などを調整して下さい。"
    )
