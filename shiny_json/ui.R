#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Flood Warning System"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(cellWidths = c("25%", "75%"),
      textInput('Postcode', 'Enter the postcode', ''),
      sliderInput("bins",
                  "Number of days:",
                  min = 1,
                  max = 50,
                  value = 30),
      actionButton("goButton", "Analyse!")),
    
    # Show a plot of the generated distribution
    mainPanel(
        #tabPanel("Plot",
        tabsetPanel(
          tabPanel('Plot',plotOutput("distPlot"),textOutput('text1')),
          tabPanel("Map",plotOutput("map_plot")))))
  ))
