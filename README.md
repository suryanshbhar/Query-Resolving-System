# QUERY RESOLVING SYSYTEM
This webpage illustrates the application of natural language processing.
The user has to input a corpus with a query to the application and the apllication return the most semantically and contextually similar answers.<br>
The web application has been deployed using heroku and is available at https://query-resolving-system.herokuapp.com/ 
## Description
The project basically aims to provide a context limited query answering system.<br>
Text preprocessing has been done using nltk library.<br>
Further nltk-word tagger has been used to answer one word queries.<br>
And 'multi-qa-MiniLM-L6-cos-v1' sentence transformer model has been used to return contextually similar answers<br>
## Usage
<ul>
<li>After visiting the home page user has press the the link to visit the convert page</li>
<li>At the convert page user can then either select a sample corpus or provide his custom corpus in the textarea</li>
<li>User is then required to input a query which would be resolved by the application</li>
</ul>

#### I/O 
![](images/code.PNG)
#### Usage Contsraints
The  first attribute is a string containg the name of the input csv file.It should contain the input model and should be present in the working directory.
###### * It should have more than 3 columns.
###### * First column is the object/variable name.
###### * From 2nd to last columns contain numeric values only.

The second attribute is a string containing comma seperated weights.
Example: "1,1,1,1" 
###### * Weights should be numerical and should be separated by commas.

The third attribute is a string containing comma seperated impacts.
Example: "+,-,-,+"
###### * Impacts could either be '+' or '-'. Impacts should be comma separated.

###### * Number of WEIGHTS and IMPACTS must be equal to the number of COLUMNS(excluding the first object column) in the input file

## Authors
Suryansh Bhadwaj

## License
[MIT](https://choosealicense.com/licenses/mit/)


