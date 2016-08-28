#-*-coding:utf-8-*-

from pyspark import SparkConf,SparkContext


#file = sc.textFile("/tmp/access.log")
#println(words.collect().mkstring(" "))
    


    
# Configure Spark
conf = SparkConf().setMaster("local[*]")
conf = conf.setAppName("split file")
sc   = SparkContext(conf=conf)
 
file = sc.textFile("/tmp/access.log")
print(type(file))
file_read = str(file.collect())
print(file_read.collect())
#print(file)    
# Execute Main functionality
#    main(sc)
    
