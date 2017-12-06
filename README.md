# FakeReviewerDetection

This project was done as a part of Data Visual and Analytics course - CSE6242 at Georgia Institute of Technology.

# Desctiption

A fake reviewer detection system using Belief propagation

Dependencies:
numpy
sumproduct

features.py -> function kde():
  #input : grouped_df -> reviewer wise grouped data :

  #output: grouped_pr -> product wise grouped data including burst periods in ordinal form:
  
  product_id, ratings, date, bursts                    
  5555991584, [5.0, 5.0, 4.0, 5.0, 5.0, 5.0], [[730243], [730261], [730267], [730411]], [[[730243], [735079]]] 



To convert dates from ordinal to date format, use fromordinal() 
  
