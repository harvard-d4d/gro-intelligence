#!/bin/bash
qpdf --password=$1 --decrypt $2 $3
rm $2
