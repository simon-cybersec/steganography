# Steganography
Embedding data into PNG images.

It is possible to embed:
- message string
- a whole file

Easy testing:  

    test.py <image file> (-e | -d) [-m MESSAGE | -f FILE] [-o OUTPUT] [-h] 

  -h, --help            show help message  
  -e, --encode          encode  
  -d, --decode          decode  
  -o, --output <OUTPUT> output file name  
  -m, --message <MESSAGE>   string message to be embedded  
  -f, --file <FILE>     file to be embedded.  


[Project working, but still in development]  