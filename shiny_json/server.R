#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(RCurl)
library(RJSONIO)
library(plyr)
library(maps) 
library(mapdata)
library(RgoogleMaps)
url <- function(address, return.call = "json", sensor = "false") {
  root <- "http://maps.google.com/maps/api/geocode/"
  u <- paste(root, return.call, "?address=", address, "&sensor=", sensor, sep = "")
  return(URLencode(u))
}

geoCode <- function(address,verbose=FALSE) {
  if(verbose) cat(address,"\n")
  u <- url(address)
  doc <- getURL(u)
  x <- fromJSON(doc,simplify = FALSE)
  if(x$status=="OK") {
    lat <- x$results[[1]]$geometry$location$lat
    lng <- x$results[[1]]$geometry$location$lng
    location_type <- x$results[[1]]$geometry$location_type
    formatted_address <- x$results[[1]]$formatted_address
    return(c(lat, lng, location_type, formatted_address))
  } else {
    return(c(NA,NA,NA, NA))
  }
}

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  output$distPlot<-renderPlot({
    if (input$goButton == 0)
      return()
    x    <- faithful[, 2] 
    bins <- seq(min(x), max(x), length.out = input$bins + 1)
    #draw the histogram with the specified number of bins
    hist(x, breaks = bins, col = 'darkgray', border = 'white',main=paste("Flood Analysis"),xlab="Days Range",ylab="Rainfall Intensity")
    #var_location <- geoCode(input$Postcode)
    #var_location
  })
  #   output$distPlot <- renderPlot({
  #   
  #   # generate bins based on input$bins from ui.R
  #   x    <- faithful[, 2] 
  #   bins <- seq(min(x), max(x), length.out = input$bins + 1)
  #   # draw the histogram with the specified number of bins
  #   hist(x, breaks = bins, col = 'darkgray', border = 'white',main=paste("Flood Analysis"),xlab="Days Range",ylab="Rainfall Intensity")
  # })
    output$text1 <- renderText({
      if (input$goButton == 0)
        return()
      var_location <- geoCode(input$Postcode)
      var_location
    })
    output$map_plot <- renderPlot({ 
      if (input$goButton == 0)
        return()
      display_map <- geoCode(input$Postcode)
      lat <- display_map[1]
      lng <- display_map[2]
      
      print(lat)
      print(lng)
      #map.where(database='world',lat,lng)
      #map.where(database='county','newcastle',lat,lng)
      #map('worldHires','Canada', xlim=c(-141,-53), ylim=c(40,85), col='gray90', fill=TRUE)
      wm <- map("worldHires",fill=TRUE,col='gray90',xlim=c(-141,-53),ylim=c(40,85)) 
      
      # center = c(mean(lat), mean(lng))  #tell what point to center on 
      # zoom <- 5  #zoom: 1 = furthest out (entire globe), larger numbers = closer in 
      # terrmap <- GetMap(center=center, zoom=zoom, maptype= "satellite", destfile = "terrain.png") #lots of visual options, just like google maps: maptype = c("roadmap", "mobile", "satellite", "terrain", "hybrid", "mapmaker-roadmap", "mapmaker-hybrid") 
 
      #map.where(wm,lat,lng)
      # take out islands, but you loose e.g. UK, New Zealand, small island states
      
    })
})
