import csv
import numpy
import math
import random
from numpy import matrix
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
from math import pi,exp
import time

def compare(x,y):
	if x<y: return -1
	elif x>y: return 1
	else: return 0
	
def minimum(x,comp):
	m = x[0]
	pos = 0
	for i in range(1,len(x)):
		if comp(x[i],m)<0: 
			m=x[i]
			pos = i
	return (m,pos)
	

def sort(x,comp):
	l=len(x)
	ind = numpy.array(range(0,len(x)))
	for i in range(0,l):
		(m,j) = minimum(x[i:l],comp)
		x[j+i] = x[i]
		x[i] = m
		temp=ind[i]
		ind[i]=ind[j+i]
		ind[j+i] = temp
	return (x,ind)


def sort_buble(x,comp):
	index = numpy.array(range(0,len(x)))
	for i in range(1,len(x)):
		j = i-1
		while j>=0:
			if comp(x[j],x[j+1])>0:
				temp = x[j]
				x[j]=x[j+1]
				x[j+1]=temp
				temp = index[j]
				index[j] = index[j+1]
				index[j+1] = temp
			j=j-1
	return (x,index)

def sort_shell(x,comp):
	l = len(x)
	index = numpy.array(range(0,len(x)))
	ind = [1]
	k=1
	while True:
		k = 3*k+1
		if k<l: 
			ind.append(k)
		else:
			break
			
	while len(ind)>0:
		k = ind.pop()
		for i in range(0,k):
			ind_temp = index[i::k]
			(x[i::k],i_p) = sort_buble(x[i::k],comp)
			index[i::k] = ind_temp[i_p]
	return (x,index)	

	
def left(a,b):
	res = a[0]*b[1]-a[1]*b[0]
	if res <0:
		return -1
	elif res >0:
		return 1
	else:
		return o
	


def merge((x1,i1),(x2,i2),comp):
	x = numpy.array(numpy.concatenate((x1,x2)))
	ind = numpy.array(numpy.concatenate((i1,i2)))
	l1 = len(x1)
	l2 = len(x2)
	i = 0
	j = 0
	while i+j < l1+l2:
		if i < l1 and j < l2:
			if comp(x1[i],x2[j])<=0:
				x[i+j] = x1[i]
				ind[i+j] = i1[i]
				i=i+1
			else:
				x[i+j] = x2[j]
				ind[i+j] = i2[j]
				j=j+1
		elif i < l1: 
			x[i+j] = x1[i]
			ind[i+j] = i1[i]
			i=i+1
		else:
			x[i+j] = x2[j]
			ind[i+j] = i2[j]
			j=j+1
	
	return (x,ind)

def sort_merge(x, comp, ind = False):
	l = len(x)
	if ind is False:
		ind = numpy.array(range(0,l))
	if l<= 3:
		(x_s,x_ind) = sort_shell(x,comp)
		return (x_s,ind[x_ind])
	else:
		return merge(sort_merge(x[0:(l/2)],comp,ind[0:(l/2)]),sort_merge(x[(l/2):(l)],comp,ind[(l/2):(l)]),comp)
		
	
def sort_merge_nr(x,comp):
	l = len(x)
	ind = numpy.array(range(0,l))
	k = 1 
	while k < l:
		i=0
		while i < l:
			i1 = i
			i2 = i+2*k
			(x[i1:i2],ind[i1:i2]) = merge((x[i1:i1+k],ind[i1:i1+k]),(x[i1+k:i2],ind[i1+k:i2]),comp)
			i = i + 2*k	
		k = k*2	
	return (x,ind)


def sort_quick(x,comp):
	l=len(x)
	ind = numpy.array(random.sample(numpy.array(range(0,l)),l))
	#print ind
	x = x[ind]
	#print "Inside after shuffle: ", x
	i=1
	j=l-1
	flag = 0
	while j>=i:
		while i<l and comp(x[i],x[0])<=0 :
			i = i+1
		while comp(x[0],x[j])<0:
			j = j-1
		if i<j:
			temp = x[i]
			x[i] = x[j]
			x[j] = temp
			temp = ind[i]
			ind[i] = ind[j]
			ind[j] = temp
			i = i+1
			j = j-1
			
	temp = x[0]
	x[0] = x[j]
	x[j] = temp
	temp = ind[0]
	ind[0] = ind[j]
	ind[j] = temp	
	#print "After partition: ", x
	
	if j > 2:
		(x[0:j],ind_temp) = sort_quick(x[0:j],comp)
		ind[0:j] = ind[ind_temp]
	else:
		if j==2 and compare(x[0],x[1])>0:
			temp = x[0]
			x[0] = x[1]
			x[1] = temp
			temp = ind[0]
			ind[0] = ind[1]
			ind[1] = temp	
		
	if l-j > 3:		
		(x[(j+1):l],ind_temp) = sort_quick(x[(j+1):l],comp)
		ind[(j+1):l] = ind[ind_temp + j+1]
	else:
		if j == l-3 and compare(x[l-2],x[l-1])>0:
			temp = x[l-1]
			x[l-1] = x[l-2]
			x[l-2] = temp
			temp = ind[l-1]
			ind[l-1] = ind[l-2]
			ind[l-2] = temp	
	
	return (x,ind)
  


