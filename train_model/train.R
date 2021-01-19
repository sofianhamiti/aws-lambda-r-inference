library(randomForest)
library(MASS)

set.seed(42)

# Prepare dataset
cutoff = sample(1:nrow(Boston), nrow(Boston) * 0.7) # 70/30 split between test and train
train_set <- Boston[cutoff,]
test_set <- Boston[-cutoff,]

# Train model
rf_model = randomForest(medv ~ ., data = train_set, mtry = 6, importance = TRUE)

# Evaluate model (MSE)
boston.test = Boston[-cutoff, 'medv']
predictions = predict(rf_model, newdata = test_set)
round(mean((predictions - boston.test)^2), 2)

# Save model binary
saveRDS(rf_model, file = 'boston_model.rds')