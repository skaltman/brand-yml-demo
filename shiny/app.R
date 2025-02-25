library(shiny)
library(dplyr)
library(ggplot2)
library(lubridate)
library(bslib)
library(bsicons)
library(thematic)

# Read the data
subscriptions <- 
  readr::read_csv("../data/subscriptions.csv") |>
  mutate(date = as.Date(date))

thematic::thematic_shiny()

options(bslib.color_contrast_warnings = FALSE)

ui <- page_fluid(

  layout_sidebar(
    sidebar = sidebar(
      selectInput(
        "type", "Select Subscription Type",
        choices = c("All", unique(subscriptions$subscription_type))
      ),
      
      selectInput(
        "start_month", "Select Start Month",
        choices = sprintf("%02d", 1:12),
        selected = "01"
      ),
      
      selectInput(
        "start_year", "Select Start Year",
        choices = sort(unique(year(subscriptions$date))),
        selected = "2020"
      ),
      
      selectInput(
        "end_month", "Select End Month",
        choices = sprintf("%02d", 1:12),
        selected = "11"
      ),
      
      selectInput(
        "end_year", "Select End Year",
        choices = sort(unique(year(subscriptions$date))),
        selected = "2024"
      )
    ),
    
    layout_column_wrap(
      card(
        card_header("Subscriptions by type"),
        plotOutput("subscription_plot")
      ),
      
      layout_column_wrap(
        width = 1,
        layout_column_wrap(
          value_box(
            title = "Current Subscriptions",
            value = 
              format(
                sum(subscriptions$active_subscriptions[
                  subscriptions$date == max(subscriptions$date)
                ]),
                big.mark = ","
              ),
            showcase = bs_icon("graph-up"),
            theme = "primary"
          ),
          
          value_box(
            title = "Most Popular Type",
            value = 
              subscriptions |>
                group_by(subscription_type) |>
                summarize(total = sum(active_subscriptions)) |>
                arrange(desc(total)) |>
                slice(1) |>
                pull(subscription_type),
            showcase = bs_icon("star"),
            theme = "secondary"
          ),
          
          value_box(
            title = "Months Tracked",
            value = length(unique(subscriptions$date)),
            showcase = bs_icon("calendar"),
            subtitle = "From January 2020 to November 2024",
            theme = "info"
          )
        ),
        card(
          card_header("Dashboard Information"),
          card_body(
            markdown("
              ## Dashboard styled with _brand.yml

              This is a sample Shiny app styled with a `_brand.yml` file. 

              Learn more:

              * `_brand.yml` documentation: https://posit-dev.github.io/brand-yml/
              * Shinylive example with `_brand.yml`: https://shinylive.io/py/examples/#branded-theming
              * bslib: https://rstudio.github.io/bslib/
              * Shiny: https://shiny.posit.co/
            ")
          )
        )
      )
    )
  ),
  title = "Explore total subscriptions"
)

server <- function(input, output) {
  output$subscription_plot <- renderPlot({
    filtered_data <- if (input$type == "All") {
      subscriptions
    } else {
      subscriptions |> filter(subscription_type == input$type)
    }
    
    start_date <- glue::glue("{input$start_year}-{input$start_month}-01") |> lubridate::as_date()
    end_date <- glue::glue("{input$end_year}-{input$end_month}-01") |> lubridate::as_date()
    
    filtered_data <- 
      filtered_data |>
      filter(date >= start_date, date <= end_date)
    
    filtered_data |>
    ggplot(aes(x = date, y = active_subscriptions, color = subscription_type)) +
      geom_line() +
      labs(
        x = "Date",
        y = "Subscription Count",
        color = "Subscription Type"
      ) +
      scale_color_manual(values = c("#4D6CFA", "#BA274A")) +
      theme_minimal() 
  })
}

shinyApp(ui = ui, server = server)