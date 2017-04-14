#setup
#==============================================================================
#import graphlab module
import graphlab as gl
 
#read training data CSV to variable 'data'
data = gl.SFrame.read_csv('train.csv', verbose=False)
 
#read validation data CSV to variable 'testdata'
testdata = gl.SFrame.read_csv('validation.csv', verbose=False)

#read validation with average ctr to variable 'averagectrdata'
averagectrdata = gl.SFrame.read_csv('ValidationACTR.csv', verbose=False)
#==============================================================================

#create model
#==============================================================================
#  #create logisic regression classifier from chosen features
#  #data = train.csv
#  #click is target
#  model = gl.random_forest_classifier.create(data, target='click', features=['advertiser', 'useragent', 'slotheight', 'slotwidth'])
#  
#  #predict the PCTR values against the validation dataset,
#  #testdata = validation.csv
#  #values = predicted values
#  values = model.predict(testdata, output_type='probability')
#  
#  #test model prediction, prints first 5 rows
#  print values.head(5)
#  
#  #add values as a column
#  #values = values from the prediction
#  #newdata is the new variable for this new Sframe
#  #testdata is our validation dataset
#  newdata = testdata.add_column(values, name='PCTR')
#  
#  #SAVING
#  newdata.save('validationprediction.csv', format='csv')
#==============================================================================

#model = gl.boosted_trees_classifier.create(data, target='click', features=['advertiser', 'slotheight', 'slotwidth', 'hour', 'weekday'] , max_iterations=20)
  
#predictions = model.predict(testdata, output_type='probability')

#print predictions

newdata = averagectrdata.add_column(predictions, 'PCTR')

newdata.save('boostedtreePCTR.csv', format='csv')