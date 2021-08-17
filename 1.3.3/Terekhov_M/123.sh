#!/bin/bash
a=$(ls | grep .py$ | grep -v change_name.py)
echo $a
