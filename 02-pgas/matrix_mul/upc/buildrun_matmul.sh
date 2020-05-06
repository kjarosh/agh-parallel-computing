#!/bin/bash
# alias upcxx="/usr/local/upcxx/bin/upcxx"
# alias upcxx-run="/usr/local/upcxx/bin/upcxx-run"

/usr/local/upcxx/bin/upcxx -O matrixmul.cpp -o matrixmul
/usr/local/upcxx/bin/upcxx-run -n 2 -N 1 matrixmul asd 1000 1