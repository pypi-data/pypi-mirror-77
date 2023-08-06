This is a simple Python package that converts your beautiful photos to pencil art. The transformed photo just looks like a photo which is drawn using pencil.

For this package to run without any errors the following packages should be installed on your system 
1)opencv-python and 2)numpy

All you have to do is just download the package as

                   pip install img2sketch
You can use this package in your code as

##usage

                from Pencil.PencilArt import img2sketch
                img2sketch("/path/of/your/original/photo.jpg", "/path/where/your/newphoto/tobe/saved.jpg")
For example: I have pavan.jpg photo under /home/pavan/Desktop/pavan.jpg I want the new transfromed photo at the same folder (Desktop) as new.jpg Here my code looks like

                img2sketch("/home/pavan/Desktop/pavan.jpg", "/home/pavan/Desktop/new.jpg")
After the program executes the transformed photo is saved under the path you have provided.
