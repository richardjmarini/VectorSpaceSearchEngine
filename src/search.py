#!/usr/bin/env python
"""
   Author: Richard J. Marini (richardjmarini@gmail.com)
   Date: 02/05/2014
   Description:  Vector space search engine 
   Development Resources:
      http://en.wikipedia.org/wiki/Vector_space_model
      http://en.wikipedia.org/wiki/Tf-idf
      http://en.wikipedia.org/wiki/Cosine_similarity
      http://en.wikipedia.org/wiki/Norm_%28mathematics%29
"""

from glob import glob
from optparse import OptionParser, make_option
from sys import exit, argv, stdin
from os import pardir, path
from re import sub

from document import Document
from vector import Vector
from termdocumentmatrix import TermDocumentMatrix

def parse_args(argv):

   optParser= OptionParser()

   [optParser.add_option(opt) for opt in [
      make_option("-d", "--documents", default= path.join(pardir, "documents", "*.txt"), help= "documents directory"),
      make_option("-q", "--query", default= stdin, help= "query to use for search")
   ]]

   optParser.set_usage("%prog --query")

   opts, args= optParser.parse_args()
   if opts.query == stdin:
      setattr(opts, "query", stdin.read().lower())

   return opts


if __name__ == '__main__':

   opts= parse_args(argv)

   tdm= TermDocumentMatrix()

   [tdm.add(sub("\n", "", open(filename).read().lower()), id= filename) for filename in glob(opts.documents)]

   tdm.index()
   tdm.display()

   print "========================================"
   #print "Query: ", opts.query
   print "Results:"
   results= []
   for (cosine, (document_id, text)) in tdm.find(opts.query):
      results.append((cosine, document_id))

   # sort the results by cosine similularity
   for (cosine, document_id) in sorted(results, key= lambda r: r[0], reverse= True):
      print cosine, document_id
  
