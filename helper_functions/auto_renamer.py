import os  

dir = "/home/daniel/Desktop/data/tmp/"
counter = 1
while(True):
  try:
    os.rename(dir + 'Untitled.jpg', dir + str(counter)+ "n.jpg") 
    counter = counter + 1
    print("renamed ", str(counter))
  except:
    continue


