library(randomForest)
library(jsonlite)

# download model file from S3 into /tmp folder
system("aws s3 cp ${S3_MODEL_URI} /tmp/model.rds")

handler <- function(data) {
  model <- readRDS("/tmp/model.rds")
  # predict with loaded model
  predictions <- predict(model, newdata=data)
  # prepare response payload
  payload <- toJSON(list(predictions=predictions))
  return(payload)
}