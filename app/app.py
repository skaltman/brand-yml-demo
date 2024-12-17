from shiny.express import input, render, ui
import matplotlib.pyplot as plt
import pandas as pd
from mplstyle import mplstyle_from_brand

subscriptions = pd.read_csv("data/subscriptions.csv")
subscriptions["date"] = pd.to_datetime(subscriptions["date"])  

mplstyle_from_brand(__file__)

ui.page_opts(
    theme=ui.Theme.from_brand(__file__), 
    title="Explore total subscriptions", 
    fillable=True
)

with ui.sidebar():
    ui.input_selectize(
        "type", "Select Subscription Type",
        ["All"] + subscriptions["subscription_type"].unique().tolist(),  
    )

    ui.input_selectize(
        "start_month", 
        "Select Start Month", 
        [f"{i:02d}" for i in range(1, 13)],
        selected="01"
    )
    ui.input_selectize(
        "start_year", 
        "Select Start Year", 
        [str(year) for year in sorted(subscriptions.date.dt.year.unique())],
        selected="2020"
    )
    ui.input_selectize(
        "end_month", 
        "Select End Month", 
        [f"{i:02d}" for i in range(1, 13)],
        selected="11"
    )
    ui.input_selectize(
        "end_year", 
        "Select End Year", 
        [str(year) for year in sorted(subscriptions.date.dt.year.unique())],
        selected="2024"
    )


with ui.layout_column_wrap():
    with ui.card():
        ui.markdown("## Subscriptions by type")
        @render.plot
        def subscription_plot():
            subscription_type = input.type()
            filtered_data = (
                subscriptions if subscription_type == "All" 
                else subscriptions[subscriptions["subscription_type"] == subscription_type]
            )

            start_date = f"{input.start_year()}-{input.start_month()}-01"
            end_date = f"{input.end_year()}-{input.end_month()}-01"

            filtered_data = filtered_data[
                (filtered_data["date"] >= pd.to_datetime(start_date)) &
                (filtered_data["date"] <= pd.to_datetime(end_date))
            ]

            fig, ax = plt.subplots(figsize=(10, 6))
            for sub_type, group in filtered_data.groupby("subscription_type"):
                ax.plot(group["date"], group["active_subscriptions"], label=sub_type)
            
            ax.set_xlabel("Date")
            ax.set_ylabel("Subscription Count")
            ax.legend(title="Subscription Type")
            ax.grid(True, linestyle="--", alpha=0.6)

            return fig
    
    with ui.layout_column_wrap(width=1):
        with ui.layout_column_wrap():
            with ui.value_box(theme="primary"):
                "Current Subscriptions"
                f"{subscriptions[subscriptions['date'] == subscriptions['date'].max()]['active_subscriptions'].sum():,}"
                "Total current active subscriptions"


            with ui.value_box(theme="secondary"):
                "Most Popular Type"
                subscriptions.groupby("subscription_type")["active_subscriptions"].sum().idxmax()
                "By total subscriptions"

            with ui.value_box(theme="info"):
                "Months Tracked"
                f"{subscriptions['date'].nunique()}"
                "From January 2020 to November 2024"
        
        with ui.card():
            ui.markdown(
                """
                ## Dashboard styled with _brand.yml

                This is a sample Shiny app styled with a `_brand.yml` file. 

                Learn more:

                * `_brand.yml` documentation: https://posit-dev.github.io/brand-yml/
                * Shinylive example with `_brand.yml`: https://shinylive.io/py/examples/#branded-theming
                * Shiny for Python: https://shiny.posit.co/py/
                """
            )



