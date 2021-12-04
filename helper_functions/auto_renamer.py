import os  

dir = "/home/daniel/Documents/data/-/"
counter = 148
while(True):
  try:
    os.rename(dir + 'Untitled.jpg', dir + str(counter)+ ".jpg") 
    counter = counter + 1
    print("renamed ", str(counter))
  except:
    continue


