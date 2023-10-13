import streamlit as st
import pandas as pd
import numpy as np
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)
import altair as alt


html_code = """
<div class="loader">
  <div class="loader__bar"></div>
  <div class="loader__bar"></div>
  <div class="loader__bar"></div>
  <div class="loader__bar"></div>
  <div class="loader__bar"></div>
  <div class="loader__ball"></div>
</div>
"""

css_code = """
<style>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  height: 100vh;
  padding-top: 100px;
}

.loader {
  margin-top: -125px;
  margin-left: 0px;
  position: relative;
  width: 75px;
  height: 100px;
}

.loader__bar {
  position: absolute;
  bottom: 0;
  width: 10px;
  height: 50%;
  background: #EA4961;
  transform-origin: center bottom;
  box-shadow: 1px 1px 0 rgba(0, 0, 0, 0.2);
}

.loader__bar:nth-child(1) {
  left: 0;
  transform: scale(1, 0.2);
  animation: barUp1 4s infinite;
}

.loader__bar:nth-child(2) {
  left: 15px;
  transform: scale(1, 0.4);
  animation: barUp2 4s infinite;
}

.loader__bar:nth-child(3) {
  left: 30px;
  transform: scale(1, 0.6);
  animation: barUp3 4s infinite;
}

.loader__bar:nth-child(4) {
  left: 45px;
  transform: scale(1, 0.8);
  animation: barUp4 4s infinite;
}

.loader__bar:nth-child(5) {
  left: 60px;
  transform: scale(1, 1);
  animation: barUp5 4s infinite;
}

.loader__ball {
  position: absolute;
  bottom: 10px;
  left: 0;
  width: 10px;
  height: 10px;
  background: #EA4961;
  border-radius: 50%;
  animation: ball 4s infinite;
}

@keyframes ball {
  0% {
    transform: translate(0, 0);
  }
  5% {
    transform: translate(8px, -14px);
  }
  10% {
    transform: translate(15px, -10px);
  }
  17% {
    transform: translate(23px, -24px);
  }
  20% {
    transform: translate(30px, -20px);
  }
  27% {
    transform: translate(38px, -34px);
  }
  30% {
    transform: translate(45px, -30px);
  }
  37% {
    transform: translate(53px, -44px);
  }
  40% {
    transform: translate(60px, -40px);
  }
  50% {
    transform: translate(60px, 0);
  }
  57% {
    transform: translate(53px, -14px);
  }
  60% {
    transform: translate(45px, -10px);
  }
  67% {
    transform: translate(37px, -24px);
  }
  70% {
    transform: translate(30px, -20px);
  }
  77% {
    transform: translate(22px, -34px);
  }
  80% {
    transform: translate(15px, -30px);
  }
  87% {
    transform: translate(7px, -44px);
  }
  90% {
    transform: translate(0, -40px);
  }
  100% {
    transform: translate(0, 0);
  }
}

@keyframes barUp1 {
  0% {
    transform: scaleY(0.2);
  }
  40% {
    transform: scaleY(0.2);
  }
  50% {
    transform: scaleY(1);
  }
  90% {
    transform: scaleY(1);
  }
  100% {
    transform: scaleY(0.2);
  }
}

@keyframes barUp2 {
  0% {
    transform: scaleY(0.4);
  }
  40% {
    transform: scaleY(0.4);
  }
  50% {
    transform: scaleY(0.8);
  }
  90% {
    transform: scaleY(0.8);
  }
  100% {
    transform: scaleY(0.4);
  }
}

@keyframes barUp3 {
  0% {
    transform: scaleY(0.6);
  }
  100% {
    transform: scaleY(0.6);
  }
}

@keyframes barUp4 {
  0% {
    transform: scaleY(0.8);
  }
  40% {
    transform: scaleY(0.8);
  }
  50% {
    transform: scaleY(0.4);
  }
  90% {
    transform: scaleY(0.4);
  }
  100% {
    transform: scaleY(0.8);
  }
}

@keyframes barUp5 {
  0% {
    transform: scaleY(1);
  }
  40% {
    transform: scaleY(1);
  }
  50% {
    transform: scaleY(0.2);
  }
  90% {
    transform: scaleY(0.2);
  }
  100% {
    transform: scaleY(1);
  }
}

.title {
  margin-top: 20px;
  margin-left: 86px;
  font-size: 50px;
  color: white;
}
</style>
"""

st.markdown("<div class='title-container'><h1 class='title'>Scorecard Prototype</h1></div>", unsafe_allow_html=True)

st.markdown(html_code, unsafe_allow_html=True)
st.markdown(css_code, unsafe_allow_html=True)

st.subheader("Sample Chart")


# chart_data = pd.DataFrame(np.random.randn(10, 1), columns=["Productivity"])
#
# st.line_chart(chart_data)
#
# chart_data2 = pd.DataFrame(np.random.randn(10, 3), columns=["a", "b", "c"])
#
# st.bar_chart(chart_data2)
#
# st.button("Download Excel")

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a UI on top of a dataframe to let viewers filter columns

    Args:
        df (pd.DataFrame): Original dataframe

    Returns:
        pd.DataFrame: Filtered dataframe
    """
    modify = st.checkbox("Add filters")

    if not modify:
        return df

    df = df.copy()

    # Specify the date format when reading the CSV file
    date_format = "%d/%m/%Y"
    df['Date'] = pd.to_datetime(df['Date'], format=date_format)

    modification_container = st.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filter dataframe on", df.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Values for {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Values for {column}",
                    _min,
                    _max,
                    (_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Values for {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                    format="DD/MM/YYYY",  # Specify the date format here
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
                # Convert datetime values to date without time
                df[column] = df[column].dt.date
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    df = df[df[column].str.contains(user_text_input)]

    return df

#df = pd.read_csv("TestData.csv", parse_dates=['Date'], dayfirst=True)  # Specify date parsing options

df = pd.read_csv("TestData.csv", parse_dates=['Date'], dayfirst=True)  # Specify date parsing options

# Convert the datetime values in the 'Date' column to date without time
df['Date'] = df['Date'].dt.date

# Create a categorical x-axis using Altair
chart = alt.Chart(filter_dataframe(df)).mark_bar().encode(
    x=alt.X('Date:O', title="Date"),  # Use 'O' for ordinal (categorical) field
    y=alt.Y('Productivity:Q', title="Productivity"),
).properties(
    width=800,  # Set the chart width as needed
    height=400,  # Set the chart height as needed
    title="Productivity by Date",
)

# Convert the Altair chart to JSON and display it using st.altair_chart
st.altair_chart(chart, use_container_width=True)