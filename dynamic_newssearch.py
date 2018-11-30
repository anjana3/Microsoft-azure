#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
.libPaths("rlibs")
install.packages(c("tensorflow","rpart.plot","shiny","shinydashboard","shinythemes","DT","dplyr","data.table","rsample","corrplot"), dependencies=TRUE, repos='http://cran.us.r-project.org')
library(e1071)
library(tensorflow)
library(keras)
library(caret)
library(rpart.plot)
library(ggplot2)
library(shiny)
library(shinydashboard)
library(shinythemes)
library(ggplot2)
library(shinyjs)
library(DT)
library(dplyr)
library(data.table)
library(rsample)
library(corrplot)


# Define UI for application that draws a histogram
ui <- fluidPage(shinyUI(dashboardPage(skin = "blue",
                                      dashboardHeader(title = span(tagList(icon("cog", lib = "glyphicon"), "Prediction Analysis"))),
                                      dashboardSidebar(
                                        sidebarMenu(
                                          menuItem("Details of the Applicaiton",tabName = "details",icon = icon("blackboard",lib = "glyphicon")),
                                          menuItem("Data Preparation", tabName = "preparation", icon = icon("wrench")),
                                          menuItem('Train the Model',tabName = "model",icon = icon("cogs")),
                                          menuItem("prediction",tabName = "pred",icon = icon("tasks",lib = "glyphicon")))
                                      ),
                                      dashboardBody(
                                        tabItems(
                                          tabItem(tabName = "preparation",
                                                  
                                                  fluidPage(
                                                    sidebarLayout(
                                                      sidebarPanel(
                                                        p(h4("Please upload a CSV formatted file with your data.")),
                                                        fileInput("uploaded_file", "Choose CSV File",
                                                                  multiple = TRUE,
                                                                  accept = c("text/csv",
                                                                             "text/comma-separated-values,text/plain",
                                                                             ".csv")),
                                                        
                                                        # Horizontal line ----
                                                        tags$hr(),
                                                        
                                                        # Input: Checkbox if file has header ----
                                                        checkboxInput("header", "Header", TRUE),
                                                        
                                                        # Input: Select separator ----
                                                        radioButtons("sep", "Separator",
                                                                     choices = c(Semicolon = ";",
                                                                                 Comma = ",",
                                                                                 Tab = "\t"),
                                                                     selected = ","),
                                                        
                                                        
                                                        # Horizontal line ----
                                                        tags$hr(),
                                                        
                                                        # Input: Select number of rows to display ----
                                                        radioButtons("disp", "Display",
                                                                     choices = c(All = "all",
                                                                                 Head = "head"),
                                                                     selected = "head"),
                                                        
                                                        # Select variables to display ----
                                                        uiOutput("selectbox"),
                                                        tags$hr(),
                                                        uiOutput("checkbox")
                                                      ),
                                                      
                                                      # Main panel for displaying outputs ----
                                                      mainPanel(
                                                        
                                                        tabsetPanel(
                                                          id = "dataset",
                                                          tabPanel(h4("Features"), DT::dataTableOutput("rendered_file"),
                                                                   tags$hr(),
                                                                   mainPanel(h4("Structure of  Feaures"),verbatimTextOutput("summary")),
                                                                   mainPanel(h4("summary of Features",verbatimTextOutput("summary1")))
                                                          ),
                                                          tabPanel(h4("Target variable"),DT::dataTableOutput("rendered_file1"),
                                                                   tags$hr(),
                                                                   mainPanel(h4("Target variable summary"),verbatimTextOutput("summary_target")),
                                                                   mainPanel(h4("Target variable structure"),verbatimTextOutput("summary_target1"))
                                                                   
                                                                   
                                                                   
                                                          )
                                                          
                                                        )
                                                      )
                                                    )
                                                  )
                                          ),
                                          tabItem(tabName = "model",
                                                  fluidRow(
                                                    box(title = "Tensor flow regression ",status = "primary", solidHeader = TRUE, collapsible = TRUE, width = 11,
                                                        h4("Linear Regression with TensorFlow Canned Estimators. Linear Regression is an algorithm that is frequently taught to first time practitioners of Machine Learning. The first principles of gradient descent and loss are taught using Linear Regression. This model is about implementing Linear Regression using TensorFlow."),
                                                        h5("In regression problem, we aim to predict the output of a continuous value."),
                                                        
                                                        actionButton('rpart',label = 'Tensor flow regression',icon("hand-right",lib = "glyphicon"),
                                                                     
                                                                     style="color: #fff; background-color: green;border-color: #2e6da4",width = 200),
                                                        
                                                        conditionalPanel(
                                                          condition = "input.rpart % 2 == 0",
                                                          "Data is under training with tensor flow regression model"
                                                        ))    
                                                  ),
                                                  
                                                  tags$hr(),
                                                  box(title = "RandomForest classification",status = "primary",solidHeader = TRUE,collapsible = TRUE,width = 11,
                                                      h4("Random Forest classification"),
                                                      actionButton('rf',label = 'RandomForest Classifer',icon("tree-conifer", lib="glyphicon"),
                                                                   style="color: #fff; background-color: green;border-color: #2e6da4",width = 200))
                                                      
                                                  
                                                  
                                          ),
                                          tabItem(tabName = "details",
                                                  fluidPage(
                                                    box(
                                                      title = "Details of the application",status = "primary",solidHeader = TRUE,collapsible = TRUE,width = 8,
                                                      h4("This application is designed to build a model to predict the target value (or) target class. By taking the user input csv and algorithm to build a model."),
                                                      p(h4("it works only for numerical data "))
                                                    ),
                                                    box(title = "How To Use", status = "primary", solidHeader = TRUE,
                                                        collapsible = TRUE, width = 8,
                                                        p(h3("DATA PREPARATION")),
                                                        tags$hr(),
                                                        h4("Step 1: Upload Dataset"),
                                                        h5("Ideally any csv file is useable.  It is recommended to perform cleaning and munging methods prior to the upload though. We intend to apply data munging/cleaning methods in this app in the near future."),
                                                        h4("Step 2: Select  Feature variables in the select feature variables"),
                                                        h5("you can see those selected variables summary in the file tab under summary of the features."),
                                                        h4("Step 3: Select  one target variable which has to predict from select target variable tab"),
                                                        h5("The target variable tab contains the values of the variable with complete summary of the target variable. "),
                                                        h4("Step 4: Train the  Model"),
                                                        h5("Choose algorithm to train the model after selecting the features and target variables .")
                                                    ),
                                                    tags$hr(),
                                                    box(title = "Train the model",status = "primary", solidHeader = TRUE,
                                                        collapsible = TRUE, width = 8,
                                                        tags$hr(),
                                                        h4("Step 1: Train the model to predict the target value."),
                                                        h4("Step 2: Click on the model which is in the colour green."),
                                                        tags$hr(),
                                                        h4(" Choose algorithm based on your targets "),
                                                        h4("Example:Regression : Target variable"), 
                                                        h4("Classification : Target Classes")
                                                    ),
                                                    tags$hr(),
                                                    box(title="Prediction",status = "primary", solidHeader = TRUE,
                                                        collapsible = TRUE, width = 8,
                                                        tags$hr(),
                                                        h4("step 1: Click on MSE  if the model run for regression probelm."),
                                                        h4("Stpe 2: Click on Prediction values to the prediction values for new data.")
                                                    ))),
                                          tabItem(tabName = "pred",
                                                  fluidPage(
                                                    tabsetPanel(
                                                      tabPanel(h4("Mean Absolute Error "),verbatimTextOutput("mae")),
                                                      tabPanel(h4("Prediction values"),tableOutput("pred_values")),
                                                      tabPanel(h4("Correlation"),plotOutput("corre")),
                                                      tabPanel(h4("randomtab"),tableOutput("rand"))
                                                      )
                                                  ))
                                          
                                        )
                                      ))
))

# Define server logic required to draw a histogram
server <- function(input, output) {
  
  # Read file ----
  df <- reactive({
    req(input$uploaded_file)
    read.csv(input$uploaded_file$datapath,
             header = input$header,
             sep = input$sep)  
    
  })
  
  
  # Dynamically generate UI input when data is uploaded ----
  output$checkbox <- renderUI({
           checkboxGroupInput(inputId = "select_var", 
                       label = "Select Feature variables", 
                       choices = names(df()),
                       selected = names(df()))
    
                       
  })
  output$selectbox<-renderUI({
    selectInput(inputId = "select_var_tar",
                label = "Select Target Variable",
                choices = names(df()))
 
     })
  
  
 
 
  # Select columns to print ----
  df_sel <- reactive({
    req(input$select_var)
    df_sel <- df() %>% select(input$select_var)
 
     })
  

  
  df_sel_tar <- reactive({
    req(input$select_var_tar)
    
    df_sel_tar <- df() %>% select(input$select_var_tar)
    
     })
  
  output$summary1<-renderPrint({
    if(input$disp=="head"){
      summary(df_sel())
    }
    else{
      df_sel()
    }
  }) 
  
  output$summary<-renderPrint({
    if(input$disp=="head"){
      str(df_sel())
    }
    else{
      df_sel()
    }
  })    
  
  output$summary_target<-renderPrint({
    if(input$disp=="head"){
      summary(df_sel_tar())
    }
    else{
      df_sel_tar()
    }
  })
  output$summary_target1<-renderPrint({
    if(input$disp=="head"){
      str(df_sel_tar())
    }
    else{
      df_sel_tar()
    }
  })
  # Print data table ----  
  output$rendered_file <- DT::renderDataTable({
    if(input$disp == "head") {
      head(df_sel())
    }
    else {
      df_sel()
    }
  })
  
  output$rendered_file1 <- DT::renderDataTable({
    if(input$disp == "head") {
      head(df_sel_tar())
    }
    else {
      df_sel_tar()
    }
  })
  
  set.seed(1000)
  observe({
    features=as.data.frame(df_sel())
    labels=df_sel_tar()
    df=data.frame(features,labels)  
    
    train_test_split <- initial_split(features, prop = 0.8)
    train_data_bos <- data.matrix(training(train_test_split))
    test_data_bos  <- data.matrix(testing(train_test_split))
    
    label_split<-initial_split(labels,prop = 0.8)
    train_lab_bos<- data.matrix(training(label_split))
    test_lab_bos <- data.matrix(testing(label_split))
    
    train_data_bos <- scale(train_data_bos) 
    
    
    build_model <- function() {
      
      model <- keras_model_sequential() %>%
        layer_dense(units = 64, activation = "relu",
                    input_shape = dim(train_data_bos)[2]) %>%
        layer_dense(units = 64, activation = "relu") %>%
        layer_dense(units = 1)
      
      model %>% compile(
        loss = "mse",
        optimizer = optimizer_rmsprop(),
        metrics = list("mean_absolute_error")
      )
      model
    }
    
    model <- build_model()
    # model %>% summary()
    #train the model
    # Display training progress by printing a single dot for each completed epoch.
    print_dot_callback <- callback_lambda(
      on_epoch_end = function(epoch, logs) {
        if (epoch %% 80 == 0) cat("\n")
        cat(".")
      }
    )  
    
    epochs <- 500
    
    # The patience parameter is the amount of epochs to check for improvement.
    early_stop <- callback_early_stopping(monitor = "val_loss", patience = 20)
    
    model <- build_model()
    history <- model %>% fit(
      train_data_bos,
      train_lab_bos,
      epochs = epochs,
      validation_split = 0.2,
      verbose = 0,
      callbacks = list(early_stop, print_dot_callback)
    )
    
    pp1 = plot(history, metrics = "mean_absolute_error", smooth = FALSE) +
      coord_cartesian(xlim = c(0, 150), ylim = c(0, 10)) 
    
    c(loss, mae) %<-% (model %>% evaluate(test_data_bos, test_lab_bos, verbose = 0))
    
    pp= paste0("Mean absolute error on test set: $", sprintf("%.2f", mae * 1000))
    test_predictions <- model %>% predict(test_data_bos)
    test_predictions[ , 1]
    
    observeEvent(input$rpart,{
      output$mae<-renderPrint(pp)
      output$pred_values<-renderTable(
        if(input$disp == "head") {
          table(head(test_predictions))
        }
        else {
          table(test_predictions) 
        })
      output$corre<-renderPlot(
        
        corrplot(cor(df),method = "number"))
      
    })   
    
  })
  
observe({
  features=as.data.frame(df_sel())
  labels=df_sel_tar()
  df=data.frame(features,labels)  

  
  train_test_split_ran <- initial_split(features, prop = 0.8)
  train_data_ran <- as.data.frame(training(train_test_split_ran))
  test_data_ran  <- as.data.frame(testing(train_test_split_ran))
  
  label_split_ran<-initial_split(labels,prop = 0.8)
  train_lab_ran<- as.data.frame(training(label_split_ran))
  test_lab_ran <- as.data.frame(testing(label_split_ran))
  
  
  
  observeEvent(input$rf,{
    output$rand<-renderTable(
      if(input$disp == "head") {
        table(head(train_lab_ran))
      }
      else {
        table(train_lab_ran) 
      })
  })
  
})
  
}

# Run the application 
shinyApp(ui = ui, server = server)

