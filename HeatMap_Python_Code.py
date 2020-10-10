#!/usr/bin/env python
# coding: utf-8

#Change the prameters
#(Required) S3 bucket that contains videos
bucketName = "<You_Bucket_name>" #Replace <You_Bucket_name> with the bucket name you created
imageName = "<You_Image_name>" #Replace <You_Image_name> with the Image name you uploaded, include the type such as .jpeg or .png

#(Optional)set the parameters for the HeatMap
matrixhight=20 #how many rectangle do you want vertically on the heatmap
matrixwidth=30 #how many rectangle do you want horizationally on the heatmap
DarkestColor = '#990000' #The darkest color you want on the heatmap
LabelType = "Person" #You can change this to any label type that Amazon Rekognition supports


#Install grapefruit library for more color choice on heatmap
import sys
get_ipython().system('{sys.executable} -m pip install grapefruit')


# Initialise Notebook
import boto3
from IPython.display import HTML, display
from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
from grapefruit import Color


# Init clients
rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')



get_ipython().system('mkdir m1tmp')
tempFolder = 'm1tmp/'


# Start person recognition job
recognizeLabelResponse = rekognition.detect_labels(
    Image={
        'S3Object': {
            'Bucket': bucketName,
            'Name': imageName,
        }
    },
    MinConfidence=80,
)

#display(recognizeLabelResponse)



#Define HeatMap function
c2 = Color.NewFromHtml(DarkestColor) 
def round_down(num, divisor):
    return num - (num%divisor)

def drawHeatMap (sourceImage,boxes):
    c1 = Color.NewFromHtml('#ffffff')
    
    # Download image locally
    imageLocation = tempFolder+os.path.basename(sourceImage)
    s3.download_file(bucketName, sourceImage, imageLocation)

    #Creat a matrix for heatmap
    matrix = np.full((matrixhight, matrixwidth), 0, dtype=np.uint)
            
    # Get Image Info
    bbImage = Image.open(imageLocation)
    draw = ImageDraw.Draw(bbImage,"RGBA")
    width, height = bbImage.size

    #Decide the "heat" for each rectangle
    maxnumber=0
    for box in boxes:
        x1 = int(round_down(box[1]['Left'], 1/matrixwidth) * matrixwidth)
        y1 = int(round_down(box[1]['Top'], 1/matrixhight) * matrixhight)
        x2 = int(round_down(box[1]['Left'] + box[1]['Width'], 1/matrixwidth) * matrixwidth)
        y2 = int(round_down(box[1]['Top'] + box[1]['Height'], 1/matrixhight) * matrixhight)
        
        for By in range(y1, y2+1):
            row=matrix[By]
            for Bx in range(x1,x2+1):
                row[Bx]=row[Bx]+1
                if maxnumber < row[Bx]:
                    maxnumber = row[Bx]
                
    #Draws the matrix on Image
    for y in range(matrixhight):
        for x in range(matrixwidth):
            bx1=x/matrixwidth*width
            by1=y/matrixhight*height
            bx2=(x+1)/matrixwidth*width
            by2=(y+2)/matrixhight*height
            if matrix[y][x] == 0:
                draw.rectangle((bx1,by1,bx2,by2),outline="White",fill=None)
            else:
                col = c2.Blend(c1, percent=int(matrix[y][x]) / int(maxnumber))
                transparency = str(col.html)+"BF" #75% transparency. To find more transparency code, go to https://gist.github.com/lopspower/03fb1cc0ac9f32ef38f4
                draw.rectangle((bx1,by1,bx2,by2),outline="White",fill=transparency)
            

    imageFormat = "PNG"
    ext = sourceImage.lower()
    if(ext.endswith('jpg') or ext.endswith('jpeg')):
       imageFormat = 'JPEG'

    bbImage.save(imageLocation,format=imageFormat)

    display(bbImage)



#Draw a heatmap on the image
boxes = []
Labels = recognizeLabelResponse['Labels']
for Label in Labels:
    if Label['Name'] == LabelType:
        for person in Label['Instances']:
            boxes.append ((Label['Name'], person['BoundingBox']))
drawHeatMap(imageName,boxes)
