Steps for running the FlowNet 2.0 : 

1. To run the FlowNet we have to store the Images in text files (.txt) to get the output (.flo) files. For this **run the text_file_conversion.ipynb** notebook
2. To run the FLowNet model we need data in the output file as '.flo' extension. To execute this :
   
   $python Change-Output-File.py
   
3. To run the FLowNet Model on docker run : 
   $ ./run-network.sh -n FlowNet2-s -g 1 -vv data/flow-first-images.txt data/flow-second-images.txt data/flow-outputs.txt
   (Here, flow-first-images.txt is first input file, flow-second-images.txt is second input file and flow-outputs.txt is the output file created in above step)
   
4. To copy the generated .flo files in a specific folder run :
   
   $python copy-Flo-Files-Both.py (for Both Cars) 
   
   $python copy-Flo-Files-Red.py (for Red Car)
   
   $python copy-Flo-Files-Yellow.py (for Yellow Car)
   
5. To convert .flo files into .png run :
   $python -m flowiz demo/flo/*.flo 
   
6. To copy the generated .png files in a specific folder run :
   
   $python Copy-Both-Car-Images.py
   
   $python Copy-Red-Car-Images.py
   
   $python Copy-Yellow-Car-Images.py
   
7. To get the Position and Direction of the cars **run the car-coordinates.ipynb notebook**.
   (All the data will get stored in the CSV files after running this notebook)
